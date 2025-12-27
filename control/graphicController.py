import model.graphicalUtilities as gUTIL

def loadStyleSheet():
    try:
        styleSheet = gUTIL.loadStyleSheet()
        return styleSheet
    except:
        return None