# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction():
    # get the number of cards in the current collection, which is stored in
    # the main window
    addonPath = os.getcwd()
    pathToFind='Anki2'
    foundAnkiAt = addonPath.find(pathToFind)
    addonPath = addonPath[:foundAnkiAt + len(pathToFind)]

    if addonPath.find('/')==-1:
        addonPath+='\\addons21'
    else:
        addonPath+='/addons21'
    
    
    try:
        addonList=[folder for folder in os.listdir(addonPath) if os.path.isdir(addonPath+"/"+folder)]
        addonListString = '\n'.join(addonList)
        
        # Setting up message boxes
        msgBox =QMessageBox()
        msgBox.setWindowTitle("Anki Addons' Exporter")
        msgBox.setWindowIcon(QIcon("anki_exporter_logo.png")) #Set icon for msgbox
        msgBox.setText("Exported! \n-Click \"Show Details\" to see the codes.\n-Click \"Save all\" to copy to the clipboard")
        msgBox.setDetailedText(addonListString)
        msgBox.setStandardButtons(QMessageBox.Ok|QMessageBox.SaveAll)
        msgBox.setDefaultButton(QMessageBox.SaveAll)
        res = msgBox.exec_()
        

        # Handling message box click message
        if res== QMessageBox.SaveAll:
            clipboard = QApplication.clipboard() #QtWidgets.
            clipboard.setText(addonListString)
    except Exception as e:
        e2 = sys.exc_info()[0]
        errorBox = QMessageBox()
        errorBox.setWindowTitle("Error from Anki Addons' Exporter")
        errorBox.setIcon(QMessageBox.Critical)
        errorBox.setText("Error:%s\n%s"%e2,e)
        errorBox.exec()
  

# create a new menu item, "test"
action = QAction("Addons' Code Exporter", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)