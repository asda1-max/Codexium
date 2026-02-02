def loadStyleSheet():
    #Load Stylesheet untuk aplikasi
    with open("view/stylesheet/Darkeum.qss", "r", encoding="utf-8") as styleFile:
        styleSheet = styleFile.read()
        return styleSheet