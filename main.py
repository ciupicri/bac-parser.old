#!/usr/bin/env python
import logging
import logging.config
import os.path
import sys
from gzip import GzipFile
from bz2 import BZ2File
from lzma import LZMAFile

from utils import get_data_from_file

COMPRESSED_FILE_CLASSES = {'.gz': GzipFile,
                           '.bz2': BZ2File,
                           '.xz': LZMAFile}

def open_compressed_file(filename):
    ext = os.path.splitext(filename)[1]
    f = COMPRESSED_FILE_CLASSES.get(ext, file)(filename)
    dir(f) # workaround for https://bugzilla.redhat.com/show_bug.cgi?id=720111
    return f

def main():
    for filename in sys.argv[1:]:
        logging.info("Extracting from %s" % (filename,))
        with open_compressed_file(filename) as f:
            for i in get_data_from_file(f):
                print i
                print '#'*72

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
