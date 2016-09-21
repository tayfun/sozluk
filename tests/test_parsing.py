# -*- coding: utf8 -*-
import scrapers


def test_saksafon(mocker):
    mock_get_url = mocker.patch('scrapers.get_url')
    with open('./tests/responses/saksafon.html', 'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
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
    mock_get_url = mocker.patch('scrapers.get_url')
    with open(u'./tests/responses/hercai menekşe.html', 'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
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
    mock_get_url = mocker.patch('scrapers.get_url')
    with open(u'./tests/responses/her.html', 'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
    entry = scrapers.scrape_meaning('her')
    assert entry['entry'] == 'her'
    assert entry['sources'] == [{
        'tags': [u'sıfat', u'Farsça her'],
        'definitions': [{
            'meaning': (
                u'Önüne geldiği ismin benzerlerini "teker teker hepsi, '
                u'birer birer hepsi, birer birer tamamı" anlamıyla '
                u'kapsayacak biçimde genelleştiren söz'
            ),
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
    mock_get_url = mocker.patch('scrapers.get_url')
    with open(u'./tests/responses/mey.html', 'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
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
            'meaning':
                u'Türk halk müziğinde kullanılan, ağzı yassı bir zurna türü',
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
    mock_get_url = mocker.patch('scrapers.get_url')
    with open(u'./tests/responses/ufuk.html', 'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
    entry = scrapers.scrape_meaning(u'ufuk')
    assert entry['entry'] == u'ufuk'
    assert entry['sources'] == [{
        'tags': ['isim', u'Arapça ufḳ'],
        'definitions': [{
            'tags': ['isim'],
            'meaning': (
                u'Düz arazide veya açık denizde gökle yerin '
                u'birleşir gibi göründüğü yer, çevren'
            ),
            'example': {
                'sentence':
                    u'Geniş çöl ufukları arasında çadırlarımızı kurduk.',
                'author': 'F. R. Atay'
            }
        }, {
            'tags': [u'coğrafya'],
            'meaning': (
                u'Çekülün gösterdiği dikey çizgi ile gözlemci '
                u'üzerinden geçen düzlem, göz erimi'
            ),
            'example': {}
        }, {
            'tags': [],
            'meaning': u'Anlayış, kavrayış, görüş, düşünce gücü, ihata',
            'example': {
                'sentence': (
                    u'Bu dar zihinlerde, ufku genişlememiş dimağlarda, '
                    u'zaruri olarak faziletler de dardı.'
                ),
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


def test_Ir(mocker):
    mock_get_url = mocker.patch('scrapers.get_url')
    with open(u'./tests/responses/Ir.html', 'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
    entry = scrapers.scrape_meaning(u'Ir')
    assert entry['entry'] == u'Ir'
    assert entry['norm'] == u'ir'
    assert entry['sources'] == [{
        'tags': ['kimya'],
        'definitions': [{
            'tags': ['kimya'],
            'meaning': u'İridyum elementinin simgesi',
            'example': {}
        }]}, {
        'tags': ['isim'],
        'definitions': [{
            'tags': [u'bakınız'],
            'meaning': u'bakınız yır',
            'example': {}
        }]
    }]
    assert entry['related_entries'] == {
        'idioms': [],
        'compound_entries': []
    }


def test_first_page_letter_f(mocker):
    mock_get_url = mocker.patch('scrapers.get_url')
    with open(u'./tests/responses/f_first.html', 'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
    words, next_page = scrapers.get_entries_and_next_page(
        'http://tdk.org.tr/index.php?option=com_yazimkilavuzu&arama=kelime'
        '&kelime=f&kategori=yazim_listeli&ayn=bas')
    assert words == set(
        entry.strip() for entry in
        u"""F
        f
        fa
        faal
        faaliyet
        faallik
        fa anahtarı
        fabl
        fabrika
        fabrikacı
        fabrikacılık
        fabrikasyon
        fabrikatör
        fabrikatörlük
        facia
        facialaşma
        facialaşmak
        facialaştırma
        facialaştırmak
        facialı
        faça
        façalı
        façeta
        façetalı
        façetasız
        façuna
        façunalık
        fagosit
        fagositoz
        fagot
        fağfur
        fağfuri
        fahiş
        fahişe
        fahişelik
        fahişlik
        fahrenhayt
        fahri
        fahri konsolos
        fahrilik
        fahriye
        fahte
        fahur
        faik
        faikiyet
        faiklik
        fail
        faili meçhul
        failimuhtar
        faillik
        faiz
        faizci
        faizcilik
        faiz fiyatı
        faiz haddi
        faizlendirme
        faizlendirmek
        faizli
        faiz oranı
        faizsiz""".split('\n')
    )
    assert next_page == (
        'http://tdk.org.tr/index.php?option=com_yazimkilavuzu'
        '&view=yazimkilavuzu&kategori1=yazim_listeli&ayn1=bas'
        '&kelime1=f&sayfa1=60'
    )


def test_last_page_letter_f(mocker):
    mock_get_url = mocker.patch('scrapers.get_url')
    with open(u'./tests/responses/f_last.html', 'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
    words, next_page = scrapers.get_entries_and_next_page(
        'http://tdk.org.tr/index.php?option=com_yazimkilavuzu&'
        'view=yazimkilavuzu&kategori1=yazim_listeli&ayn1=bas'
        '&kelime1=f&sayfa1=1560')
    assert words == set(
        entry.strip() for entry in
        u"""fümerol
        füniküler
        fünye
        Fürs
        füru
        fürumaye
        füsun
        füsunkâr
        füsunlu
        fütuhat
        fütuhatçı
        fütuhatçılık
        fütur
        fütursuz
        fütursuzca
        fütursuzcasına
        fütursuzluk
        fütürist
        fütüristlik
        fütürizm
        fütürolog
        fütüroloji
        fütürolojik
        fütüvvet
        füze
        füzeatar
        füzeci
        füzen
        füzesavar
        füzyometre
        füzyon""".split('\n')
    )
    assert next_page is None


def test_birinin_sapkasini_with_paranthesis(mocker):
    """Test an entry that starts with paranthesis."""
    mock_get_url = mocker.patch('scrapers.get_url')
    with open('./tests/responses/şapkasını giymek (veya taşımak).html',
              'r') as response_file:
        content = response_file.read()
    mock_get_url.return_value = content
    entry = scrapers.scrape_meaning(u'(birinin) şapkasını giymek (veya taşımak)')
    assert entry['sources'] == [{
        'tags': [],
        'definitions': [{
            'meaning': u'kendi kimliğinin veya düşüncelerinin dışında başka birinin kimliğini geçici olarak taşımak veya onun düşünceleriyle ortaya çıkmak',  # NOQA
            'example': {
                'author': None,
                'sentence': u"T\xfcrkler ba\u015fl\u0131k olarak 1925'te \u015fapkay\u0131 kabul ettiler."  # NOQA
            },
            'tags': []
        }]
    }]
    assert entry['entry'] == u'şapkasını giymek (veya taşımak)'
    assert entry['norm'] == 'sapkasini giymek (veya tasimak)'
