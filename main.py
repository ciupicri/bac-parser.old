#!/usr/bin/env python
import lxml.etree
import re
import sys
import MainTimeline
import maintable

ged_regex = re.compile(r'''function\s+ged\(\)\s*{\s*return\s+"([^"]*)"\s*;\s*}''')

def main():
    f = open(sys.argv[1], 'rt')
    html = f.read()
    f.close()

    ged = ged_regex.search(html).group(1)
    html = MainTimeline.s3(ged).decode('base64')
    main_table = maintable.get_mainTable(html)
    with open('/tmp/main_table.xml', 'wt') as f:
        f.write(lxml.etree.tostring(main_table, pretty_print=True))
    data = maintable.get_data_from_mainTable(main_table)
    for i in data:
        print i
        print '='*72

if __name__ == '__main__':
    main()
