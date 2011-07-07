import itertools
import lxml.html

def get_mainTable(html):
    html = html[html.index('<HTML>'):]
    html = unicode(html, 'utf-8')
    doc = lxml.html.fromstring(html)
    main_table = doc.xpath(r'''//table[@id="mainTable"]''')[0]
    return main_table

def get_data_from_mainTable(main_table):
    L = []
    get_hint = lambda tr: tr.attrib['hint'].strip().upper()
    for hint, trs in itertools.groupby(main_table.xpath(r'''tr[@hint]'''), get_hint):
        d = {}
        for tr in trs:
            if tr.find('script') is not None:
                d.update(get_data_from_tr_with_script(tr))
            else:
                d.update(get_data_from_tr_without_script(tr))
        L.append(d)
    return L

def get_data_from_tr_with_script(tr):
    d = {}
    d['scoala'] = tr.xpath('td[5]/a/text()')[0].strip()
    d['judet'] = tr.xpath('td[6]/a/text()')[0].strip()
    d['specializare'] = tr.xpath('td[9]/text()')[0].strip()
    d['d1_nume'] = "limba si literatura romana"
    d['d1_oral'] = tr.xpath('td[10]/text()')[0].strip()
    d['d1_scris_final']= tr.xpath('td[13]/text()')[0].strip()
    d['d0_nume'] = tr.xpath('td[14]/text()')[0].strip()
    d['d2_nume'] = tr.xpath('td[15]/text()')[0].strip()
    d['d2_oral'] = tr.xpath('td[16]/text()')[0].strip()
    d['d3_nume'] = tr.xpath('td[17]/text()')[0].strip()
    d['d4_nume'] = tr.xpath('td[18]/text()')[0].strip()
    d['d5_nume'] = tr.xpath('td[19]/text()')[0].strip()
    return d

def get_data_from_tr_without_script(tr):
    d = {}
    d['d0_oral'] = tr.xpath('td[1]/text()')[0].strip()
    d['d0_scris_final'] = tr.xpath('td[4]/text()')[0].strip()
    d['d3_scris_final'] = tr.xpath('td[7]/text()')[0].strip()
    d['d4_scris_final'] = tr.xpath('td[10]/text()')[0].strip()
    d['d5_scris_final'] = tr.xpath('td[13]/text()')[0].strip()
    return d
