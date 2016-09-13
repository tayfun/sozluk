# -*- coding: utf8 -*-
import scrapers


def test_saksafon(mocker):
    mock_get_webpage = mocker.patch('scrapers.get_webpage')
    with open('./tests/responses/saksafon.html', 'r') as response_file:
        content = response_file.read()
    mock_get_webpage.return_value = content
    entry = scrapers.scrape_meaning('saksafon')
    assert entry['sources'] == [{
        'tags': ['isim', u'Frans\u0131zca saxophone', u'm\xfczik'],
        'definitions': [{
            'meaning': u'Genellikle pirin\xe7ten yap\u0131lm\u0131\u015f, metal tu\u015flara bas\u0131larak \xe7al\u0131nan, \xe7o\u011funlukla bandolarda ve caz topluluklar\u0131nda kullan\u0131lan bir t\xfcr \xfcflemeli \xe7alg\u0131',  # NOQA
            'example': {
                'sentence': u'Saksafoncu, saksafonun borusunu havalara kald\u0131rarak sololar yap\u0131yordu.',  # NOQA
                'author': u'\xc7. Altan'
            },
            'tags': ['isim', u'm\xfczik']
        }]
    }]
    assert entry['entry'] == 'saksafon'
    assert entry['norm'] == 'saksafon'


def test_hercai_menekse(mocker):
    mock_get_webpage = mocker.patch('scrapers.get_webpage')
    with open(u'./tests/responses/hercai menekşe.html', 'r') as response_file:
        content = response_file.read()
    mock_get_webpage.return_value = content
    entry = scrapers.scrape_meaning(u'hercai menekşe')
    assert entry['entry'] == u'hercai menekşe'
    assert entry['sources'] == [{
        'tags': ['isim', 'bitki bilimi'],
        'definitions': [{
            'meaning': u'Menek\u015fegillerden, mor, sar\u0131, beyaz renkte, menek\u015feye benzer \xe7i\xe7ekleri olan y\u0131ll\u0131k bir bitki (Viola tricolor)',  # NOQA
            'example': {},
            'tags': ['isim', 'bitki bilimi'],
        }, {
            'meaning': u'Bu bitkinin \xe7i\xe7e\u011fi',
            'example': {
                'sentence': u'Kanatl\u0131 hercai menek\u015feler gibi kelebekler ekinlerin s\xfck\xfbnunda u\xe7u\u015furken bu kitap\xe7\u0131ktan birka\xe7 sayfa okunsun.',  # NOQA
                'author': u'A. H. M\xfcft\xfco\u011flu'
            },
            'tags': []
        }]
    }]
    assert entry['norm'] == 'hercai menekse'


def test_her(mocker):
    mock_get_webpage = mocker.patch('scrapers.get_webpage')
    with open(u'./tests/responses/her.html', 'r') as response_file:
        content = response_file.read()
    mock_get_webpage.return_value = content
    entry = scrapers.scrape_meaning('her')
    assert entry['entry'] == 'her'
    assert entry['sources'] == [{
        'tags': [u'sıfat', u'Farsça her'],
        'definitions': [{
            'meaning': u'Önüne geldiği ismin benzerlerini "teker teker hepsi, birer birer hepsi, birer birer tamamı" anlamıyla kapsayacak biçimde genelleştiren söz',
            'example': {
                'sentence': u'Bir hafta, her gece çalışmak suretiyle hikâyesini bitirdi.',  # NOQA
                'author': u'H. E. Adıvar',
            },
            'tags': [u'sıfat']
        }]
    }]
    assert entry['related_entries'] == {
        'compound_entries': [
            'her bir',
            'her biri',
            'hercai',
            'her daim',
            'her dem',
            u'her gün',
            u'herhâlde',
            u'her hâlde',
            u'her hâlükârda',
            'herhangi',
            'herkes',
            'her yerdelik',
            'her zaman',
        ],
        'idioms': [
            u"her ağacın meyvesi olmaz",
            u"her ağaçtan kaşık olmaz",
            u"her aşın kaşığı olmak",
            u"her boyaya girip çıkmak",
            u"her boyayı boyadı, bir fıstıki yeşil (mi) kaldı?",
            u"her çiçek koklanmaz",
            u"her çok azdan olur",
            u"her dağın derdi kendine göre",
            u"her deliğe elini sokma, ya yılan çıkar ya çıyan",
            "her derde deva olmak",
            u"her düşüş bir öğreniş",
            u"her firavunun bir Musa'sı çıkar",
            u"her gördüğü sakallıyı babası sanmak",
            u"her gün baklava börek yense bıkılır",
            u"her horoz kendi çöplüğünde öter",
            u"her ihtimale karşı",
            u"her işin (veya şeyin) başı sağlık",
            u"her işte bir hayır vardır",
            u"her kafadan bir ses çıkmak",
            u"her kaşığın kısmeti bir olmaz",
            u"her koyun kendi bacağından asılır",
            u"her kuşun eti yenmez",
            u"her lafın altından kalkmak",
            u"her sakaldan bir tel çekseler köseye sakal olur",
            u"her şeyin vakti var, horoz bile vaktinde öter",
            u"her ne pahasına olursa olsun",
            u"her şeyin yenisi, dostun eskisi",
            u"her şeyin yokluğu yokluktur",
            u"her tarakta bezi olmak",
            u"her taş baş yarmaz",
            u"her telden çalmak",
            u"her yiğidin bir yoğurt yiyişi vardır",
            u"her yiğidin gönlünde bir aslan yatar",
            u"her yokuşun bir inişi, her inişin bir yokuşu vardır",
            u"her zaman eşek ölmez, on köfte on paraya olmaz",
            u"her zaman gemicinin istediği rüzgâr esmez",
            u"her ziyan bir öğüttür",
        ]
    }
    assert entry['norm'] == 'her'


def test_mey(mocker):
    mock_get_webpage = mocker.patch('scrapers.get_webpage')
    with open(u'./tests/responses/mey.html', 'r') as response_file:
        content = response_file.read()
    mock_get_webpage.return_value = content
    entry = scrapers.scrape_meaning(u'mey')
    assert entry['entry'] == u'mey'
    assert entry['sources'] == [{
        'tags': ['isim', u'Farsça mey', u'eskimiş'],
        'definitions': [{
            'meaning': u'Şarap',
            'example': {},
            'tags': ['isim'],
        }]}, {
        'tags': ['isim', u'müzik'],
        'definitions': [{
            'meaning': u'Türk halk müziğinde kullanılan, ağzı yassı bir zurna türü',
            'example': {},
            'tags': ['isim', u'müzik'],
        }]
    }]
    assert entry['norm'] == 'mey'
    assert entry['related_entries'] == {
        'idioms': [],
        'compound_entries': ['meyhane']
    }


def test_ufuk(mocker):
    mock_get_webpage = mocker.patch('scrapers.get_webpage')
    with open(u'./tests/responses/ufuk.html', 'r') as response_file:
        content = response_file.read()
    mock_get_webpage.return_value = content
    entry = scrapers.scrape_meaning(u'ufuk')
    assert entry['entry'] == u'ufuk'
    assert entry['sources'] == [{
        'tags': ['isim', u'Arapça ufḳ',],
        'definitions': [{
            'tags': ['isim',],
            'meaning': u'Düz arazide veya açık denizde gökle yerin birleşir gibi göründüğü yer, çevren',
            'example': {
                'sentence': u'Geniş çöl ufukları arasında çadırlarımızı kurduk.',
                'author': 'F. R. Atay'
            }
        }, {
            'tags': [u'coğrafya'],
            'meaning': u'Çekülün gösterdiği dikey çizgi ile gözlemci üzerinden geçen düzlem, göz erimi',
            'example': {}
        }, {
            'tags': [],
            'meaning': u'Anlayış, kavrayış, görüş, düşünce gücü, ihata',
            'example': {
                'sentence': u'Bu dar zihinlerde, ufku genişlememiş dimağlarda, zaruri olarak faziletler de dardı.',
                'author': u'Ö. Seyfettin'
            }
        }, {
            'tags': [],
            'meaning': u'Çevre, dolay',
            'example': {}
        }]
    }]
    assert entry['norm'] == 'ufuk'
    assert entry['related_entries'] == {
        'idioms': ['ufku daralmak', u'ufkunu genişletmek'],
        'compound_entries': [u'ufuk çizgisi', 'ufku dar', u'ufku geniş']
    }
