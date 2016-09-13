from datetime import datetime
import re
from time import sleep

import requests
from requests.exceptions import RequestException
from lxml import html

from encoding import normalize


DICTIONARY_URL = \
    u'http://www.tdk.org.tr/index.php?option=com_gts&arama=gts&kelime={}'
# Tag delimiters could be a comma or a double space characters.
TAG_DEL = re.compile(r'\s\s+|,\s+')
MEANING_START = re.compile("^\s*(\d*\.)?\s*")
MEANING_END = re.compile(r"[-\"'\s]*$")


def get_tags(elements):
    tags = set()
    for tag_text in elements:
        for tag in TAG_DEL.split(tag_text):
            tags.add(tag.strip())
    # Remove empty tags (both None and empty strings).
    tags = filter(None, tags)
    return tags


def get_webpage(entry):
    """Cached for testing only."""
    """
This works:
'http://www.tdk.org.tr/index.php?option=com_gts&arama=gts&kelime=hercai%20menek%C5%9Fe'

But encoding Turkish characters normally does not:
ipdb> response  = requests.get(DICTIONARY_URL + '&kelime=hercai+meneks%CC%A7e')

    """
    if not getattr(get_webpage, '__cache__', None):
        get_webpage.__cache__ = {}
    page_from_cache = get_webpage.__cache__.get(entry)
    if page_from_cache is None:
        # urlencoding automatically done by requests is not 'liked' by the
        # incompetent server of TDK.
        # page_from_cache = requests.post(DICTIONARY_URL, data={
        #     'kelime': entry
        # }).content
        for i in range(5):
            try:
                page_from_cache = requests.get(DICTIONARY_URL.format(entry)).content
                break
            except RequestException:
                # Try again.
                sleep(10)
        get_webpage.__cache__[entry] = page_from_cache
    return page_from_cache


def scrape_meaning(entry_string):
    """
    Scrapes meaning of the entry from TDK website.

    See 'sak' as a complicated keyword with multiple meanings:
        http://www.tdk.org.tr/index.php?option=com_gts&arama=gts&kelime=sak

    It has two different meanings, and also it is referenced in the idioms
    dictionary.
    """
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
    page = get_webpage(entry_string)
    tree = html.fromstring(page)
    definition_tables = tree.xpath('//*[@id="hor-minimalist-a"]')
    for definition_el in definition_tables:
        source = {
            'tags': [],
            'definitions': []
        }
        tag_elements = definition_el.xpath("thead/tr/th/i//text()")
        source['tags'] = get_tags(tag_elements)
        for meaning_tr in definition_el.xpath('tr'):
            definition = {
                'meaning': '',
                'tags': set(),
                'example': {},
            }
            meaning = "".join(meaning_tr.xpath('td/text()'))
            meaning = MEANING_START.sub('', meaning)
            meaning = MEANING_END.sub('', meaning)
            definition['meaning'] = meaning
            for index, i_element in enumerate(meaning_tr.xpath('td/i')):
                # The first <i> element is the type (sifat, isim etc.) and it
                # exists even if it is empty.
                # The second is the example sentence. And bold is the author.
                if index == 0:
                    tags = get_tags(i_element.xpath('text()'))
                    definition['tags'] = tags
                    continue
                example_text = ''.join(i_element.xpath('text()')).strip()
                if example_text:
                    try:
                        author = ''.join(
                            meaning_tr.xpath('td/b')[-1].xpath('text()'))
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
        title = ''.join(other_dictionary.xpath('thead//text()'))
        if 'deyim' in title:
            other_topic = 'idioms'
        else:
            other_topic = 'compound_entries'
        related_entry_list = other_dictionary.xpath('tbody/tr/td/a/text()')
        for related_entry in related_entry_list:
            entry['related_entries'][other_topic].append(
                related_entry.strip())
    from pprint import pprint
    pprint(entry)
    return entry


def print_meaning(entry_string):
    entry = scrape_meaning(entry_string)
    from pprint import pprint
    pprint(entry)

