#!/usr/bin/env python
import logging
import logging.config
import sys

from utils import get_data_from_file

def main():
    with open(sys.argv[1], 'rt') as f:
        for i in get_data_from_file(f):
            print i
            print '='*72

if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    main()
