#!/usr/bin/python
import os
import sys
import codecs
from bs4 import BeautifulSoup
import bem

def main(argv):

    # textovy banner pro hlavicku .scss souboru
    def banner( blockName ):
        fw.write("/*\n")
        fw.write("=======================\n")
        fw.write("%s\n" % blockName)
        fw.write("=======================\n")
        fw.write("*/\n\n")

    # parametry prikazove radky
    # pokud bude nejaky parametr tak ho pouzij jako nazev vstupniho souboru
    if len(argv) > 1:
        fileName = argv[1]
    else:
        # pokud neni zadan zadny vstupni soubor tak ukonci beh skriptu
        sys.exit("No input file")

    # parser html dokumentu
    soup = BeautifulSoup(open(fileName), 'html.parser')
    # pole vsech nalezenych uzlu html dokumentu
    allTags = soup.findAll()
    # pole pro vsechny nalezene tridy
    allClassesNames = []
    # pole pro vsechny zname bloky
    allBlockNames = []

    # prochazeni vsech nalezenych tagu ze souboru
    for tag in allTags:
        tagClass = tag.get('class')
        # pridej jmeno tridy jen pokud nejake je a neni uz v ulozene v poli
        if (tagClass != None) and (tagClass not in allClassesNames):
            allClassesNames = allClassesNames + tagClass

    # unikatni pole vsech trid serazene podle abecedy a bez duplicit
    allClassesNames = sorted(list(set( allClassesNames )))

    # prochazeni jednotlivych nazvu trid
    for className in allClassesNames:
        if( bem.isBEM( className ) ):

            # zjisteni nazvu bloku
            thisBlock = bem.getBlock( className )
            # zjisteni aktualniho selektoru
            thisSelector = className

            # seznam vsech blocks, pridej jen pokud jiz v poli neni
            if( thisBlock not in allBlockNames ):
                allBlockNames.append(thisBlock)

    # zapis do souboru -> tvorba vystupnich .scss souboru

    # vytvoreni pozadovane adresarove struktury
    outputPath = "output/modules"

    if not os.path.exists(outputPath):
        os.makedirs(outputPath)

    # prochazeni vsech nazvu blocks
    for blockName in allBlockNames:

        # soubor do ktereho se bude zapisovat
        fo = "output/modules/" + blockName + ".scss"
        # vytvoreni noveho souboru
        with codecs.open( fo , "wa", "UTF-8") as fw:

            # vytvoreni banneru pro dokument
            banner(blockName)

            # vyhledani vsech trid ktere patri do daneho blocku
            blockNameSelectors = [s for s in allClassesNames if blockName in s]
            for blockNameSelector in blockNameSelectors:
                fw.write(".%s{}\n\n" % blockNameSelector)

            # ukonceni zapisu do souboru
            fw.close()

if __name__ == "__main__":
    main(sys.argv)