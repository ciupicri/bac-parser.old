import logging

from ..maintable import get_data_from_tr

###

from .centru import Centru

CENTRU_TR_COLS = (
    None, # Nr. crt.
    'nume',
    'cod_sirues',
    'localitate',
    None, # Licee arondate'
    None,
    )

def get_centru_from_mainTable(main_table):
    logger = logging.getLogger('bac2010parser.centre.get_centru_from_mainTable')
    for tr in main_table.xpath('tr')[1:]:
        d = get_centru_extra_data_from_tr(tr)
        d.update(get_data_from_tr(tr, CENTRU_TR_COLS))
        centru = Centru(**d)
        if logger.isEnabledFor(logging.INFO):
            logger.info("extracted %s" % (centru,))
        yield centru

def get_centru_extra_data_from_tr(tr):
    anchor = tr.xpath('td[5]/a')[0]
    if anchor.text.strip() != 'Licee arondate':
        raise Exception("Licee arondate aiurea")
    return {'link_licee_arondate': anchor.attrib['href']}

###

from .liceu import Liceu

LICEU_TR_COLS = (
    None, # Nr. crt.
    'nume',
    'cod_sirues',
    'localitate',
    )

def get_liceu_from_mainTable(main_table):
    logger = logging.getLogger('bac2010parser.centre.get_liceu_from_mainTable')
    for tr in main_table.xpath('tr')[1:]:
        d = get_data_from_tr(tr, LICEU_TR_COLS)
        liceu = Liceu(**d)
        if logger.isEnabledFor(logging.INFO):
            logger.info("extracted %s" % (liceu,))
        yield liceu
