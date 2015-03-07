#!/usr/bin/python
import os
import sys
import glob
import codecs
from HTMLParser import HTMLParser
import bem

# ======================================== #
# parser
# ======================================== #

structure = {}

class ClassParser(HTMLParser):
    def handle_starttag(self, tag, attrs):

        # prochazeni vsech atributu pocatecniho tagu
        for attr in attrs:

            # parsuj jen class atribut
            if attr[0] == "class":

                # prochazeni vicenasobnych trid
                allClasses = attr[1].split(" ")

                for className in allClasses:

                    # pokud je css trida platny BEM selektor tak...
                    if( bem.isBEM( className ) ):

                        # zjisti nazev blocku a uloz si ho do definice struktury
                        thisBemBlock = bem.getBlock( className )
                        if( thisBemBlock not in structure.keys() ):
                            structure[thisBemBlock] = []

                        # zjisti selektor a uloz si ho do definice struktury
                        thisBemSelector = className.encode("UTF-8")
                        if( thisBemSelector not in structure[thisBemBlock] ):
                            structure[thisBemBlock].append( thisBemSelector )

# ======================================== #
# parsovani souboru po radcich
# ======================================== #

parser = ClassParser()
with codecs.open("testdata/index.php", "r", "UTF-8") as f:
    for line in f:
        if ((line != "") and (line != "\n")):
            line = line.strip().replace('\n','');
            parser.feed(line)

# ======================================== #
# parsovani ulozeneho pole
# ======================================== #

for block in structure.keys():
    print "===================="
    print "Module: %s " % block
    print "===================="
    print ""
    for selector in structure[block]:
        print ".%s{\n\t\n}\n" % selector



