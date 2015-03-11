#!/usr/bin/python
import os
import sys
import codecs
from HTMLParser import HTMLParser
import bem

# ======================================== #
# parser html dokumentu
# ======================================== #

class HTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # prochazeni vsech atributu pocatecniho tagu
        for attr in attrs:

            # parsuj jen class atribut
            if attr[0] == "class":

                # prochazeni vicenasobnych trid
                cssClasses = attr[1].split(" ")
                for cssClass in cssClasses:

                    # pokud trida neni v globalnim poli nazvu trid tak ji tam pridej
                    global structureClasses
                    if( cssClass not in structureClasses ):
                        structureClasses.append( cssClass )

# ======================================== #
# hlavni program
# ======================================== #

structureClasses = []
structure = {}

# ======================================== #
# parsovani dokumentu
# naplneni globalniho pole nazvu trid
# ======================================== #

parser = HTMLParser()

fi = "testdata/index.php"
with codecs.open(fi, "r", "UTF-8") as f:
    for line in f:
        if ((line != "") and (line != "\n")):
            line = line.strip().replace('\n','');
            parser.feed( line.encode("UTF-8") )

# ======================================== #
# parsovani globalniho pole nazvu trid
# ======================================== #

for cssClass in structureClasses:

    if( bem.isBEM( cssClass ) ):
        # zjisteni nazvu bloku
        thisBlock = bem.getBlock( cssClass )
        # zjisteni aktualniho selektoru
        thisSelector = cssClass

        # vytvoreni struktury dokumentu (pojmenovane pole)
        if( thisBlock not in structure.keys() ):
            structure[thisBlock] = []
            structure[thisBlock].append( thisSelector )
        else:
            structure[thisBlock].append( thisSelector )

# ======================================== #
# tvorba souboru a obsahu
# ======================================== #

for block in structure.keys():

    fo = "output/" + block + ".scss"

    # vystupni soubor neexistuje
    if not os.path.isfile( fo ):

        # vytvoreni noveho souboru
        with open( fo , "w") as fw:

            fw.write("/*\n")
            fw.write("=======================\n")
            fw.write("%s\n" % block)
            fw.write("=======================\n")
            fw.write("*/\n\n")

            # zapsani selektoru do souboru
            for selector in structure[block]:
                fw.write(".%s{\n\t\n}\n\n" % selector)
            fw.close()
