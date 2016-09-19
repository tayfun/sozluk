# -*- coding: utf8 -*-
from datetime import datetime
import re
from time import sleep

import requests
from requests.exceptions import RequestException
from lxml import html

from encoding import normalize


DICTIONARY_URL = \
    u'http://www.tdk.org.tr/index.php?option=com_gts&arama=gts&kelime={}'
DOMAIN = 'http://tdk.org.tr'
# Tag delimiters could be a comma or a double space characters.
TAG_DEL = re.compile(r'\s\s+|,\s+')
MEANING_START = re.compile("^\s*(\d*\.)?\s*")
MEANING_END = re.compile(r"[-\"'\s]*$")


def get_tags(tag_list):
    tags = set()
    for tag_text in tag_list:
        for tag in TAG_DEL.split(tag_text):
            tags.add(tag.strip())
    # Remove empty tags (both None and empty strings are removed).
    tags = filter(None, tags)
    return tags


def get_url(url):
    """Return page from cache, retry on error."""
    page_content = None
    for i in range(5):
        try:
            page_content = requests.get(url).content
            break
        except RequestException:
            if (i == 4):
                raise
            # Try again after waiting for a bit.
            sleep(10)
    return page_content


def get_meaning_page(entry):
    """
    Return the meaning page for an entry.

    This works:
    http://www.tdk.org.tr/index.php?option=com_gts&arama=gts&
    kelime=hercai%20menek%C5%9Fe

    But encoding Turkish characters normally does not:
    response  = requests.get(DICTIONARY_URL + '&kelime=hercai+meneks%CC%A7e')

    ie.

    Url encoding automatically done by requests is not 'liked' by the
    incompetent server of TDK.

    page_from_cache = requests.post(DICTIONARY_URL, data={
        'kelime': entry
    }).content

    Above returns a 404 page for entries having Turkish characters.
    """
    if not getattr(get_meaning_page, '__cache__', None):
        get_meaning_page.__cache__ = {}
    page_from_cache = get_meaning_page.__cache__.get(entry)
    if page_from_cache is None:
        page_from_cache = get_url(DICTIONARY_URL.format(entry))
        get_meaning_page.__cache__[entry] = page_from_cache
    return page_from_cache


def scrape_meaning(entry_string):
    """
    Scrapes meaning of the entry from TDK website.

    See 'sak' as a complicated keyword with multiple meanings:
        http://www.tdk.org.tr/index.php?option=com_gts&arama=gts&kelime=sak

    It has two different meanings, and also it is referenced in the idioms
    dictionary.

    Also check out the tests to understand the structure of the returned
    dictionary.
    """
    # If starting with a paranthesis, remove it. Example entry: (bir yeri)
    # ırgat pazarına döndürmek & URL:
    # http://tdk.org.tr/index.php?option=com_gts&arama=gts&kelime=%C4%B1rgat%20pazar%C4%B1na%20d%C3%B6nd%C3%BCrmek
    if entry_string[0] == '(' and ')' in entry_string:
        entry_string = entry_string.split(')')[1].strip()
    now = datetime.now().isoformat()
    entry = {
        'entry': entry_string,
        'norm': normalize(unicode(entry_string)),
        'created': now,
        'updated': now,
        'related_entries': {
            'compound_entries': [],
            'idioms': []
        },
        'sources': [],
    }
    page = get_meaning_page(entry_string)
    tree = html.fromstring(page)
    definition_tables = tree.xpath('//*[@id="hor-minimalist-a"]')
    for definition_table in definition_tables:
        source = {
            'tags': [],
            'definitions': []
        }
        tag_list = definition_table.xpath("./thead/tr/th/i//text()")
        source['tags'] = get_tags(tag_list)
        for meaning_tr in definition_table.xpath('./tr'):
            definition = {
                'meaning': '',
                'tags': set(),
                'example': {},
            }
            meaning = "".join(meaning_tr.xpath('./td/text()'))
            meaning = MEANING_START.sub('', meaning)
            meaning = MEANING_END.sub('', meaning)
            if not meaning:
                # Yeah, some definitions are in a link inside td and we get
                # nothing for this reason. ex. Ir
                meaning = meaning_tr.text_content()
                meaning = MEANING_START.sub('', meaning)
                meaning = MEANING_END.sub('', meaning)
            definition['meaning'] = meaning
            for index, i_element in enumerate(meaning_tr.xpath('./td/i')):
                # The first <i> element is the type (sifat, isim etc.) and it
                # exists even if it is empty.
                # The second is the example sentence. And bold is the author.
                if index == 0:
                    tags = get_tags(i_element.xpath('./text()'))
                    definition['tags'] = tags
                    continue
                example_text = ''.join(i_element.xpath('text()')).strip()
                if example_text:
                    try:
                        author = ''.join(
                            meaning_tr.xpath('./td/b')[-1].xpath('text()'))
                        author = author.strip()
                    except IndexError:
                        author = None
                    definition['example'] = {
                        'sentence': example_text,
                        'author': author
                    }
            source['definitions'].append(definition)
        entry['sources'].append(source)
    other_dictionary_tables = tree.xpath('//*[@id="hor-minimalist-b"]')
    for other_dictionary in other_dictionary_tables:
        title = ''.join(other_dictionary.xpath('./thead//text()'))
        if 'deyim' in title:
            other_topic = 'idioms'
        else:
            other_topic = 'compound_entries'
        related_entry_list = other_dictionary.xpath('./tbody/tr/td/a/text()')
        for related_entry in related_entry_list:
            entry['related_entries'][other_topic].append(
                related_entry.strip())
    return entry


def get_entries_and_next_page(url):
    """
    Returns the entries found on the page and the links for more.

    The URLs are of pattern:
        http://tdk.org.tr/index.php?option=com_yazimkilavuzu&arama=kelime&kelime=a&kategori=yazim_listeli&ayn=bas
    """
    entry_list_page = get_url(url)
    tree = html.fromstring(entry_list_page)
    next_page = None
    entry_set = set()
    rows = tree.xpath('//td')
    # The first 5 tds are the search boxes and next page buttons.
    # The last two td's are an empty one and the menu.
    keyword_tds = rows[6:-2]
    for td in keyword_tds:
        keyword = td.text_content()
        keyword = keyword.split(",")[0].split("/")[0].split("(")[0]
        # Don't lowercase here, because it introduces a bug where I becomes i
        # (dotless i becomes i) ex. Irak (the country)
        keyword = keyword.strip()
        entry_set.add(keyword)

    if keyword_tds:
        try:
            next_page = rows[5].findall('.//a')[1].get('href')
            next_page = DOMAIN + next_page
        except IndexError:
            next_page = None
        # Last page also has a link to current page as "next page".
        if url == next_page:
            next_page = None

    return (entry_set, next_page)
