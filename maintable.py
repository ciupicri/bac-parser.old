import itertools
import logging
import lxml.html
import re

from elev import Elev

TR_SCRIPT_COLS = (
    None, # Nr. crt.
    None, # Nume... <script>
    None, # Pozitia in ierarhie...
    None, # Pozitia in ierarhie...
    'scoala',
    'judet',
    'promotie_anterioara',
    'forma_invatamant',
    'specializare',
    'd_romana_competente', 'd_romana_scris_nota', 'd_romana_scris_nota_contestatie', 'd_romana_scris_nota_finala',
    'd_limba_materna_nume',
    'd_limba_moderna_nume', 'd_limba_moderna_nota',
    'd_profil_scris_nume',
    'd_alegere_scris_nume',
    'd_competente_digitale',
    None, # LuatDePe_Bac...
    None, # Luat_DePe_Bac...
    )

TR_WITHOUT_SCRIPT_COLS = (
    'd_limba_materna_competente', 'd_limba_materna_scris_nota', 'd_limba_materna_scris_nota_contestatie', 'd_limba_materna_scris_nota_finala',
    'd_profil_scris_nota', 'd_profil_scris_nota_contestatie', 'd_profil_scris_nota_finala',
    'd_alegere_scris_nota', 'd_alegere_nota_scris_contestatie', 'd_alegere_nota_scris_finala'
    )

LUAT_REGEX = re.compile(r'''Luat_?De_?Pe_?BacalaureatEduRo\["([^"]*)"]="([^"]*)";''')

def get_mainTable(html):
    html = html[html.index('<HTML>'):]
    html = unicode(html, 'utf-8')
    doc = lxml.html.fromstring(html)
    main_table = doc.xpath(r'''//table[@id="mainTable"]''')[0]
    return main_table

def get_data_from_mainTable(main_table):
    logger = logging.getLogger('maintable.get_data_from_mainTable')
    L = []
    get_hint = lambda tr: tr.attrib['hint'].strip().upper()
    for hint, trs in itertools.groupby(main_table.xpath(r'''tr[@hint]'''), get_hint):
        tr = trs.next()
        d = get_extra_data_from_tr(tr)
        d.update(get_data_from_tr(tr, TR_SCRIPT_COLS))

        tr = trs.next()
        if tr.find('script') is not None:
            raise Exception('Am gasit script in al doilea tr')
        d.update(get_data_from_tr(tr, TR_WITHOUT_SCRIPT_COLS))

        try:
            trs.next()
            raise Exception("Mai mult de 2 tr-uri")
        except StopIteration:
            pass

        elev = Elev(**d)
        if logger.isEnabledFor(logging.INFO):
            logger.info("extracted %s" % (elev,))
        L.append(elev)
    return L

def get_data_from_tr(tr, cols):
    return {c: td.xpath('.//text()')[0].replace('&nbsp', '').strip()
                for c, td in zip(cols, tr.xpath('td')) if c}

def get_extra_data_from_tr(tr):
    script = tr.xpath('script/text()')[0]
    items = LUAT_REGEX.findall(script)
    if len(items) != 3:
        raise Exception("script paranormal: n-am gasit 3 chei")
    if not (items[0][0] == items[1][0] == items[2][0]):
        raise Exception("script paranormal: cheie inegale")
    return {'nume': items[0][0].replace('<br>', '').strip(),
            'rezultat_final': items[2][1].strip()}
