
class BEM:

    # inicializace tridy
    def __init__(self, cssName):
        self.cssName = cssName

    # jedna se o BEM selektor?
    def isBEM(self):
        if (("__" in self.cssName) or ("--" in self.cssName)):
            return True
        else:
            return False

    # Block
    def getBlock(self):
        if self.isBEM():
            bemBlock = self.cssName.split("--")[0].split("__")[:1]
            return "".join(bemBlock).encode("UTF-8")
        else:
            return False

    # Element
    def getElement(self):
        if self.isBEM():
            bemElement = self.cssName.split("--")[0].split("__")[1:]
            return "__".join(bemElement).encode("UTF-8")
        else:
            return False

    # Modifier
    def getModifier(self):
        if self.isBEM():
            bemModifier = self.cssName.split("--")[1:]
            return "".join(bemModifier).encode("UTF-8")
        else:
            return False


    # Rozklad na jednotlive casti BEM syntaxe
    def getBEM(self):
        bem = {};

        bem["selector"] = self.cssName.encode("UTF-8")
        bem["block"] = getBlock(self.cssName)

        if( getElement(self.cssName) ):
            bem["element"] = getElement()
        if( getModifier(self.cssName) ):
            bem["modifier"] = getModifier()

        return bem