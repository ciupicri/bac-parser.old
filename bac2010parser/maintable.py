import logging
import lxml.etree
import lxml.html
import sys

def get_mainTable(html):
    html = html[html.index('<HTML>'):]
    html = unicode(html, 'utf-8')
    doc = lxml.html.fromstring(html)
    main_table = doc.xpath(r'''//table[@id="mainTable"]''')[0]
    return main_table

def get_data_from_tr(tr, cols):
    return {c: td.xpath('.//text()')[0].replace('&nbsp', '').strip()
                for c, td in zip(cols, tr.xpath('td')) if c}

def main(f):
    with f:
        html = f.read()
        main_table = get_mainTable(html)
        print lxml.etree.tostring(main_table, pretty_print=True)

if __name__ == '__main__':
    main(sys.stdin)
