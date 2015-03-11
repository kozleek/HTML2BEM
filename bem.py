
# ======================================== #
# jedna se o BEM selektor?
# ======================================== #

def isBEM( cssClassName ):
    if (("__" in cssClassName) or ("--" in cssClassName)):
        return True
    else:
        return False

# ======================================== #
# Block
# ======================================== #

def getBlock ( cssClassName ):
    if isBEM(cssClassName):
        bemBlock = cssClassName.split("--")[0].split("__")[:1]
        return "".join(bemBlock).encode("UTF-8")
    else:
        return False

# ======================================== #
# Element
# ======================================== #

def getElement ( cssClassName ):
    if isBEM(cssClassName):
        bemElement = cssClassName.split("--")[0].split("__")[1:]
        return "__".join(bemElement).encode("UTF-8")
    else:
        return False

# ======================================== #
# Modifier
# ======================================== #

def getModifier ( cssClassName ):
    if isBEM(cssClassName):
        bemModifier = cssClassName.split("--")[1:]
        return "".join(bemModifier).encode("UTF-8")
    else:
        return False


# ======================================== #
# Rozklad na jednotlive casti BEM syntaxe
# ======================================== #

def getBEM ( cssClassName ):
    bem = {};

    bem["selector"] = cssClassName.encode("UTF-8")
    bem["block"] = getBlock(cssClassName)

    if( getElement(cssClassName) ):
        bem["element"] = getElement(cssClassName)
    if( getModifier(cssClassName) ):
        bem["modifier"] = getModifier(cssClassName)

    return bem

def parseCss( cssClassNames ):
    structure = {}

    # prochazeni vsech atributu pocatecniho tagu
    for attr in cssClassNames:

        # parsuj jen class atribut
        if attr[0] == "class":

            # prochazeni vicenasobnych trid
            allClasses = attr[1].split(" ")

            for className in allClasses:

                # pokud je css trida platny BEM selektor tak...
                if( isBEM( className ) ):

                    # zjisti nazev blocku a uloz si ho do definice struktury
                    thisBemBlock = getBlock( className )
                    if( thisBemBlock not in structure.keys() ):
                        structure[thisBemBlock] = []

                    # zjisti selektor a uloz si ho do definice struktury
                    thisBemSelector = className.encode("UTF-8")
                    if( thisBemSelector not in structure[thisBemBlock] ):
                        structure[thisBemBlock].append( thisBemSelector )

    return structure