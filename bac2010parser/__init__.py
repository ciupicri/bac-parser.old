import logging
import lxml.etree
import re

import MainTimeline
import maintable

js_ged_regex = re.compile(r'''function\s+ged\(\)\s*{\s*return\s+"([^"]*)"\s*;\s*}''')

def get_data_from_file(f):
    global js_ged_regex

    logger = logging.getLogger('get_data_from_file')
    for line in f:
        ged = js_ged_regex.search(line)
        if not ged:
            continue
        html = MainTimeline.s3(ged.group(1)).decode('base64')
        main_table = maintable.get_mainTable(html)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('main_table:\n' + \
                lxml.etree.tostring(main_table, pretty_print=True))
        for i in maintable.get_data_from_mainTable(main_table):
            yield i
