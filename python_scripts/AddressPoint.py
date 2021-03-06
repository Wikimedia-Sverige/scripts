#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# Short script for formatting AddressPoint datafile
# run using python AddressPoint.py -i <filnamn>
#
import codecs
import getopt
import os
import sys


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:")
    except getopt.GetoptError:
        print u'python AddressPoint.py -i <filnamn>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print u'python AddressPoint.py -i <filnamn>'
            sys.exit()
        elif opt == "-i":
            inputfile = arg
    if len(inputfile) > 0:
        outputfile = u'%s-mod.txt' % os.path.splitext(inputfile)[0]
        try:
            fIn = codecs.open(inputfile, 'r', 'Latin-1')
        except IOError:
            print u'Skrev du verkligen rätt filnamn?'
            sys.exit(2)
        lines = fIn.read().split(u'\n')
        fIn.close()

        fOut = codecs.open(outputfile, 'w', 'utf8')
        for line in lines:
            if len(line) == 0:
                continue
            p = line.split(u';')
            p[2] = p[2].title()  # first name
            p[3] = p[3].title()  # last name
            p[4] = u'%s %s'.strip() % (p[4].title(), p[5])  # To address
            p[5] = ''  # street number
            p[12] = u'%s %s'.strip() % (p[12].title(), p[13])  # To address
            p[13] = ''  # street number
            line_out = ';'.join(p)
            fOut.write(u'%s\n' % line_out)
        fOut.close()
        print u'Filen "%s" finns nu formaterad på "%s"' % (inputfile, outputfile)
        sys.exit()
    else:
        print u'Angav du inget filnamn? Programmet används med "python AddressPoint.py -i <filnamn>"'
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
