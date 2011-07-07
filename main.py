#!/usr/bin/env python
import re
import sys
import MainTimeline

ged_regex = re.compile(r'''function\s+ged\(\)\s*{\s*return\s+"([^"]*)"\s*;\s*}''')

f = open(sys.argv[1], 'rt')
html = f.read()
f.close()

ged = ged_regex.search(html).group(1)
data = MainTimeline.s3(ged).decode('base64')
print data
