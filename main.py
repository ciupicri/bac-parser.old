#!/usr/bin/env python
# vim: set fileencoding=utf-8
import argparse
import cPickle
import functools
import logging
import logging.config
import os.path
import sys
import sqlite3
from gzip import GzipFile
from bz2 import BZ2File
from lzma import LZMAFile

from bacparser.rezultate.elev import Elev
from bacparser import get_data_from_file
from bacparser.rezultate import get_elev_from_mainTable

COMPRESSED_FILE_CLASSES = {'.gz': GzipFile,
                           '.bz2': BZ2File,
                           '.xz': LZMAFile}

def open_compressed_file(filename):
    global COMPRESSED_FILE_CLASSES

    if filename == '-':
        return sys.stdin
    ext = os.path.splitext(filename)[1]
    f = COMPRESSED_FILE_CLASSES.get(ext, file)(filename)
    dir(f) # workaround for https://bugzilla.redhat.com/show_bug.cgi?id=720111
    return f

def get_data(filenames):
    for filename in filenames:
        logging.info("Extracting from %s" % (filename,))
        with open_compressed_file(filename) as f:
            for i in get_data_from_file(f, get_elev_from_mainTable):
                yield i


def output_python(f, record):
    f.write(repr(record))
    f.write('\n#######################################################################\n')

def output_pickle(f, record):
    cPickle.dump(record, f, -1)


def db_create_table(conn, tbl_name):
    f = ('%s varchar(100)' % (i,) for i in Elev._fields)
    conn.execute('CREATE TABLE %s (%s)' % (tbl_name, ",".join(f)))


def parse_args():
    parser = argparse.ArgumentParser(
            description=u'Extrage informații despre elevi din fișiere HTML')
    parser.add_argument('filenames', metavar='FILE', type=str, nargs='+',
                        help=u'O pagină de pe site-ul edu.ro. Folosiți - pentru stdin.')
    parser.add_argument('-o', '--output', metavar='OUTPUT',
                        type=str, default=sys.stdout,
                        help=u'Fișierul de ieșire. Implicit e stdout.')
    parser.add_argument('--format', metavar='FORMAT',
                        type=str, choices=('python', 'pickle', 'sqlite'),
                        default='python',
                        help=u'''Formatul de ieșire. Formate suportate: %(choices)s. Format implicit: %(default)s.''')
    parser.add_argument('--dbtable', metavar='DBTABLE',
                        type=str, default='rezultate',
                        help=u'Numele tabelului din baza de date. Nume implicit: %(default)s.')
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.format == 'python' or args.format == 'pickle':
        if args.format == 'python':
            fout = open(args.output, 'wt') if isinstance(args.output,basestring) else args.output
            output = functools.partial(output_python, fout)
        elif args.format == 'pickle':
            fout = open(args.output, 'wb') if isinstance(args.output,basestring) else args.output
            output = functools.partial(output_pickle, fout)
        with fout:
            for i in get_data(args.filenames):
                output(i)
    elif args.format == 'sqlite':
        con = sqlite3.connect(args.output)
        db_create_table(con, args.dbtable)
        insert_query = 'INSERT INTO %s VALUES(%s)' % \
            (args.dbtable, ','.join('?'*len(Elev._fields)))
        with con:
            con.executemany(insert_query, get_data(args.filenames))

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
