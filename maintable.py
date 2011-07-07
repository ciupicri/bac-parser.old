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
        if tr.attrib['class'] == 'tr1':
            L.append(get_data_from_tr1(tr))
        elif tr.attrib['class'] == 'tr2':
            L.append(get_data_from_tr2(tr))
        else:
            raise Exception("cucu bau")
    return L

def get_data_from_tr1(tr):
    return tr

def get_data_from_tr2(tr):
    return tr
