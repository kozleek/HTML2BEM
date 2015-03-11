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

fileStructure = {}

def mergeStructure(x, y):
    z = x.copy()
    z.update(y)
    return z

class ClassParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global fileStructure
        structure = bem.parseBEM( attrs )
        fileStructure = mergeStructure( fileStructure, structure )

# ======================================== #
# parsovani souboru po radcich
# ======================================== #

filename = sys.argv[1]

parser = ClassParser()
with codecs.open(filename, "r", "UTF-8") as f:
    for line in f:
        if ((line != "") and (line != "\n")):
            line = line.strip().replace('\n','');
            parser.feed(line)

# ======================================== #
# parsovani ulozeneho pole
# ======================================== #

print "....."
print fileStructure
print "....."

for block in fileStructure.keys():
    with codecs.open("output/" + block + ".scss" , "w", "UTF-8") as f:
        f.write("/* ==================== */\n")
        f.write("/* === %s */ \n" % block)
        f.write("/* ==================== */\n\n")
        for selector in fileStructure[block]:
            f.write(".%s{\n\t\n}\n\n" % selector)
        f.close()

