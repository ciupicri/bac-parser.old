import lxml.html

def get_mainTable(html):
    html = html[html.index('<HTML>'):]
    html = unicode(html, 'utf-8')
    doc = lxml.html.fromstring(html)
    main_table = doc.xpath(r'''//table[@id="mainTable"]''')[0]
    return main_table

def get_data_from_mainTable(main_table):
    L = []
    for tr in main_table.xpath(r'''tr[@hint]'''):
        L.append(get_data_from_tr(tr))
    return L

def get_data_from_tr(tr):
    return tr
