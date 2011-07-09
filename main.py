#!/usr/bin/env python
# vim: set fileencoding=utf-8
import argparse
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
    if filename == '-':
        return sys.stdin
    ext = os.path.splitext(filename)[1]
    f = COMPRESSED_FILE_CLASSES.get(ext, file)(filename)
    dir(f) # workaround for https://bugzilla.redhat.com/show_bug.cgi?id=720111
    return f

def parse_args():
    parser = argparse.ArgumentParser(
            description=u'Extrage informații despre elevi din fișiere HTML')
    parser.add_argument('filenames', metavar='FILE', type=str, nargs='+',
                        help=u'O pagină de pe site-ul edu.ro. Folosiți - pentru stdin.')
    parser.add_argument('-o', '--output', metavar='OUTPUT',
                        type=argparse.FileType('w'), default=sys.stdout,
                        help=u'Fișierul de ieșire.')
    args = parser.parse_args()
    return args

def get_data(filenames):
    for filename in filenames:
        logging.info("Extracting from %s" % (filename,))
        with open_compressed_file(filename) as f:
            for i in get_data_from_file(f):
                yield i

def main():
    args = parse_args()
    for i in get_data(args.filenames):
        args.output.write(repr(i))
        args.output.write('\n#######################################################################\n')

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
