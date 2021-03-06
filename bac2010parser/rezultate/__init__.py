import logging
import re

from .elev import Elev
from ..utils import grouper
from ..maintable import get_data_from_tr

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
    'd_alegere_scris_nota', 'd_alegere_scris_nota_contestatie', 'd_alegere_scris_nota_finala'
    )

js_luat_regex = re.compile(r'''Luat_?De_?Pe_?BacalaureatEduRo\["([^"]*)"]="([^"]*)";''')

def get_elev_from_mainTable(main_table):
    logger = logging.getLogger('bac2010parser.rezultate.get_elev_from_mainTable')
    for trs in grouper(2, main_table.xpath(r'''tr[@hint]''')):
        d = get_extra_data_from_tr(trs[0])
        d.update(get_data_from_tr(trs[0], TR_SCRIPT_COLS))

        if trs[1].find('script') is not None:
            raise Exception('Am gasit script in al doilea tr')
        d.update(get_data_from_tr(trs[1], TR_WITHOUT_SCRIPT_COLS))

        elev = Elev(**d)
        if logger.isEnabledFor(logging.INFO):
            logger.info("extracted %s" % (elev,))
        yield elev

def get_extra_data_from_tr(tr):
    global js_luat_regex

    script = tr.xpath('script/text()')[0]
    items = js_luat_regex.findall(script)
    if len(items) != 3:
        raise Exception("script paranormal: n-am gasit 3 chei")
    if not (items[0][0] == items[1][0] == items[2][0]):
        raise Exception("script paranormal: cheie inegale")
    return {'nume': items[0][0].replace('<br>', '').strip(),
            'rezultat_final': items[2][1].strip()}
