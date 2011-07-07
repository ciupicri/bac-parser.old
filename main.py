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
print lxml.etree.tostring(main_table, pretty_print=True)
