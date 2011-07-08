import logging
import lxml.etree
import re

import MainTimeline
import maintable

ged_regex = re.compile(r'''function\s+ged\(\)\s*{\s*return\s+"([^"]*)"\s*;\s*}''')

def get_data_from_file(f):
    logger = logging.getLogger('get_data_from_file')
    html = f.read()
    ged = ged_regex.search(html).group(1)
    html = MainTimeline.s3(ged).decode('base64')
    main_table = maintable.get_mainTable(html)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug('main_table:\n' + \
            lxml.etree.tostring(main_table, pretty_print=True))
    return maintable.get_data_from_mainTable(main_table)


