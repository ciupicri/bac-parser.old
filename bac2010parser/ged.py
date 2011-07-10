import re

import MainTimeline

js_ged_regex = re.compile(r'''function\s+ged\(\)\s*{\s*return\s+"([^"]*)"\s*;\s*}''')

def get_inner_html(line):
    global js_ged_regex
    ged = js_ged_regex.search(line)
    if not ged:
        return None
    return MainTimeline.s3(ged.group(1)).decode('base64')
