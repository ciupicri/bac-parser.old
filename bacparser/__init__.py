import logging
import lxml.etree

from . import ged
from . import maintable

def get_data_from_file(f, get_data_from_mainTable):
    logger = logging.getLogger('bacparser.get_data_from_file')
    for line in f:
        html = ged.get_inner_html(line)
        if not html:
            continue
        main_table = maintable.get_mainTable(html)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('main_table:\n' + \
                lxml.etree.tostring(main_table, pretty_print=True))
        for i in get_data_from_mainTable(main_table):
            yield i
