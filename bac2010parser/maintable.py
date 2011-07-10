import logging
import lxml.html

def get_mainTable(html):
    html = html[html.index('<HTML>'):]
    html = unicode(html, 'utf-8')
    doc = lxml.html.fromstring(html)
    main_table = doc.xpath(r'''//table[@id="mainTable"]''')[0]
    return main_table

def get_data_from_tr(tr, cols):
    return {c: td.xpath('.//text()')[0].replace('&nbsp', '').strip()
                for c, td in zip(cols, tr.xpath('td')) if c}
