#!/usr/bin/env python
# vim: set fileencoding=utf-8
import argparse
import cPickle
import functools
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
                        help=u'Fișierul de ieșire. Implicit e stdout.')
    parser.add_argument('--format', metavar='FORMAT',
                        type=str, choices=('python', 'pickle'),
                        default='python',
                        help=u'''Formatul de ieșire. Formate suportate: %(choices)s. Format implicit: %(default)s.''')
    args = parser.parse_args()
    return args

def get_data(filenames):
    for filename in filenames:
        logging.info("Extracting from %s" % (filename,))
        with open_compressed_file(filename) as f:
            for i in get_data_from_file(f):
                yield i

def output_python(f, record):
    f.write(repr(record))
    f.write('\n#######################################################################\n')

def output_pickle(f, record):
    cPickle.dump(record, f)

def main():
    args = parse_args()
    if args.format == 'python':
        output = functools.partial(output_python, args.output)
    elif args.format == 'pickle':
        output = functools.partial(output_pickle, args.output)
    for i in get_data(args.filenames):
        output(i)

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
