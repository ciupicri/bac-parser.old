#!/usr/bin/env python
import cPickle
from glob import glob
import logging
import logging.config
import os.path
import sys
import urlparse

from bac2010parser import get_data_from_file
from bac2010parser.centre import (get_centru_from_mainTable,
                                  get_liceu_from_mainTable)

DATA_DIR = r'/home/ciupicri/work/bac/spider/data'

def get_judete():
    with open('/home/ciupicri/work/bac/spider/lista_judete') as f:
        judete = [line.strip() for line in f]
    return judete

def get_centre_for_judet(year, judet):
    global DATA_DIR
    c_pages_glob = os.path.join(DATA_DIR, 'bacalaureat.edu.ro', str(year),
        'rapoarte', judet, 'unitati_arondate', 'page_*.html')
    for c_page in glob(c_pages_glob):
        with open(c_page) as c_f:
            for centru in get_data_from_file(c_f, get_centru_from_mainTable):
                l_page = urlparse.urljoin(c_page, centru.link_licee_arondate)
                with open(l_page) as l_f:
                    licee = list(get_data_from_file(l_f, get_liceu_from_mainTable))
                yield (centru, licee)

def main():
    centre = {}
    for judet in get_judete():
        centre[judet] = list(get_centre_for_judet(2011, judet))
    with open('/tmp/centre2.pickle', 'wb') as f:
        cPickle.dump(centre, f)

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
