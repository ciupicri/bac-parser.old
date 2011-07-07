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
        if tr.find('script') is not None:
            d = get_data_from_tr_with_script(tr)
            L.append(d)
        else:
            d = get_data_from_tr_without_script(tr)
            L.append(d)
    return L

def get_data_from_tr_with_script(tr):
    d = {}
    return d

def get_data_from_tr_without_script(tr):
    d = {}
    return d
