import logging

import sys
from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed()

from .elev import Elev
from ..utils import grouper
from ..maintable import get_data_from_tr

TR1_COLS = (
    None, # Nr. crt.
    'nume',
    None, # Pozitia in ierarhie...
    None, # Pozitia in ierarhie...
    'scoala',
    'judet',
    'promotie_anterioara',
    'forma_invatamant',
    'specializare',
    'd_romana_oral_nota',
    'd_romana_scris_nota', 'd_romana_scris_nota_contestatie', 'd_romana_scris_nota_finala',
    None, # col span...
    'd_limba_moderna_nume', 'd_limba_moderna_nota',
    'd_profil_scris_nume',
    'd_alegere_aria_curiculara_nume',
    'd_alegere_alte_arii_curiculare_nume',
    None, # media
    'rezultat_final',
    )

TR2_COLS = (
    'd_limba_materna_oral_nota',
    'd_limba_materna_scris_nota', 'd_limba_materna_scris_nota_contestatie', 'd_limba_materna_scris_nota_finala',
    'd_profil_scris_nota', 'd_profil_scris_nota_contestatie', 'd_profil_scris_nota_finala',
    'd_alegere_aria_curiculara_nota', 'd_alegere_aria_curiculara_nota_contestatie', 'd_alegere_aria_curiculara_nota_finala',
    'd_alegere_alte_arii_curiculare_nota', 'd_alegere_alte_arii_curiculare_nota_contestatie', 'd_alegere_alte_arii_curiculare_nota_finala',
    )

def get_elev_from_mainTable(main_table):
    logger = logging.getLogger('bac2010parser.rezultate.get_elev_from_mainTable')
    for trs in grouper(2, main_table.xpath(r'''tr[@hint]''')):
        ipshell() # this call anywhere in your program will start IPython
        sys.exit(1)
        d = get_data_from_tr(trs[0], TR1_COLS)
        d.update(get_data_from_tr(trs[1], TR2_COLS))

        elev = Elev(**d)
        if logger.isEnabledFor(logging.INFO):
            logger.info("extracted %s" % (elev,))
        yield elev
