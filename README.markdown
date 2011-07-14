This is a scraping script for extracting the results of the
[Romanian Baccalaureate][1] from http://bacalaureat.edu.ro. It works for the
years 2010 and 2011. It can read from standard input or files. The files can
be compressed with gzip, bzip2 or xz.

I wrote it to help a friend who wanted to analyze the results the of the exam. You can read her analysis at the following addresses:

 - http://www.dianacoman.com/blog/2011/07/08/avem-date-de-la-bac-ce-facem-cu-ele/
 - http://www.dianacoman.com/blog/2011/07/09/topul-hotiei-dovedite-la-bacalaureat-2011/
 - http://www.dianacoman.com/blog/2011/07/10/topul-liceelor-la-bacalaureat-2011/

[1]: http://en.wikipedia.org/wiki/Romanian_Baccalaureate


Usage
=====

    ./main.py --help
    usage: main.py [-h] [-o OUTPUT] [--format FORMAT] [--dbtable DBTABLE]
                   FILE [FILE ...]

    Extrage informații despre elevi din fișiere HTML

    positional arguments:
      FILE                  O pagină de pe site-ul edu.ro. Folosiți - pentru
                            stdin.

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            Fișierul de ieșire. Implicit e stdout.
      --format FORMAT       Formatul de ieșire. Formate suportate: python, pickle,
                            sqlite. Format implicit: python.
      --dbtable DBTABLE     Numele tabelului din baza de date. Nume implicit:
                            rezultate.


Usage examples
==============

    ./main.py data/page_21.html
    ./main.py data/page_21.html{,.gz,.bz2,.xz}
    ./main.py data/page_18.html data/page_18.html
    tar xJfO bac2010_alfabetic_page.tar.xz | ./main.py --format sqlite --output bac.sqlite --dbtable results2010 -


Installation and Requirements
=============================

 - python 2.7
 - [python-lxml](http://lxml.de/)
 - [pyliblzma](https://launchpad.net/pyliblzma)

Fedora 15
---------

yum install python-lxml pyliblzma


Copyright and License
=====================

The code is too simple and too ugly to require legal paperwork, so I declare
it public domain. Though if you find this useful in any way, I would like you
to tell me about it or give me some credit. Thank you!


Credits
=======

This wouldn't have been possible without the [Sothink SWF Decompiler][2]. Shame
on Siveco for using Flash even if it wasn't really needed.

[2]: http://www.sothink.com/product/flashdecompiler/
