#!/usr/bin/env python
import lxml.etree
import re
import sys
import MainTimeline
import maintable

ged_regex = re.compile(r'''function\s+ged\(\)\s*{\s*return\s+"([^"]*)"\s*;\s*}''')

f = open(sys.argv[1], 'rt')
html = f.read()
f.close()


ged = ged_regex.search(html).group(1)
html = MainTimeline.s3(ged).decode('base64')
main_table = maintable.get_mainTable(html)
data = maintable.get_data_from_mainTable(main_table)
for i in data:
    print lxml.etree.tostring(i, pretty_print=True)
    print '='*72
