#!/usr/bin/env python
import cPickle
import os.path
import sys
import urlparse

from bac2010parser.rezultate.elev import Elev
from bac2010parser import get_data_from_file
from bac2010parser.centre import get_centru_from_mainTable

def main():
    centre = []
    for filename in sys.argv[1:]:
        with open(filename) as f:
            for centru in get_data_from_file(f, get_centru_from_mainTable):
                centre.append(centru)
                url = 'http://' + filename[filename.index('bacalaureat.edu.ro'):]
                url = urlparse.urljoin(url, centru.link_licee_arondate)
                print url
    with open('/tmp/centre.pickle', 'wb') as fout:
        cPickle.dump(centre, fout)

main()
