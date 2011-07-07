import itertools
import lxml.html

from elev import Elev

def get_mainTable(html):
    html = html[html.index('<HTML>'):]
    html = unicode(html, 'utf-8')
    doc = lxml.html.fromstring(html)
    main_table = doc.xpath(r'''//table[@id="mainTable"]''')[0]
    return main_table

def get_data_from_mainTable(main_table):
    L = []
    get_hint = lambda tr: tr.attrib['hint'].strip().upper()
    for hint, trs in itertools.groupby(main_table.xpath(r'''tr[@hint]'''), get_hint):
        d = {'nume': hint}
        for tr in trs:
            if tr.find('script') is not None:
                d.update(get_data_from_tr_with_script(tr))
            else:
                d.update(get_data_from_tr_without_script(tr))
        L.append(Elev(**d))
    return L

def get_data_from_tr_with_script(tr):
    cols = (None, # Nr. crt.
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
    d = {c: td.xpath('.//text()')[0].strip()
            for c, td in zip(cols, tr.xpath('td')) if c}
    return d

def get_data_from_tr_without_script(tr):
    d = {}
    cols = ('d_limba_materna_competente', 'd_limba_materna_scris_nota', 'd_limba_materna_scris_nota_contestatie', 'd_limba_materna_scris_nota_finala',
            'd_profil_scris_nota', 'd_profil_scris_nota_contestatie', 'd_profil_scris_nota_finala',
            'd_alegere_scris_nota', 'd_alegere_nota_scris_contestatie', 'd_alegere_nota_scris_finala'
            )
    d = {c: td.xpath('.//text()')[0].strip()
            for c, td in zip(cols, tr.xpath('td')) if c}
    return d
