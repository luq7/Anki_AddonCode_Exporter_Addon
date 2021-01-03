# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from .anki_addon_exporter import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
class MyApp(QtWidgets.QMainWindow, anki_addon_exporter.Ui_Dialog):
    def __init__(self, parent=None): 
        super(MyApp, self).__init__(parent)
        self.setupUi(self)
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(self.scriptDir+ os.path.sep + "anki_exporter_logo.png"))# Set icon for main scene
        self.textEdit.setText("""ヾ(^  ^ゞ)""")
        self.textEdit.setEnabled(True)
        # Varaible declaration
        self.directory=None
        self.addonList=None
        self.foundAnkiAt=None
        self.pathToFind='Anki2'
        self.copyAll=""

        # Creating a messagebox
        self.msgBox=QtWidgets.QMessageBox()
        self.msgBox.setWindowIcon(QtGui.QIcon(self.scriptDir+ os.path.sep + "anki_exporter_logo.png")) #Set icon for msgbox
        # Set a clipboard
        self.clipboard = QtWidgets.QApplication.clipboard()
        
        # Event handling 
        self.bt_copy.clicked.connect(self.bt_Copy_handle)     # Copy All button handle
        self.bt_Export.clicked.connect(self.bt_Export_handle) # Export button hanlde
        self.textEdit.cursorPositionChanged.connect(self.textClear)
        
    def textClear(self):
        self.textEdit.clear()
        self.textEdit.cursorPositionChanged.disconnect(self.textClear)

    def bt_Sync_handle(self):
        deck_id = mw.col.decks.id('ANKI_ADDON_CODES')
        deck = mw.col.decks.get(deck_id)
        mw.col.decks.save(deck)
        mw.col.reset()
        mw.reset()

    def bt_Copy_handle(self):
        """
        Copy the extracted addon's code to the clipboard. If it is empty then show error
        """
        if self.textEdit.isEnabled():
            self.clipboard.setText(self.copyAll)
            self.msgBox.setText("Got'em! (Copied to your clipboard.)")
            self.msgBox.exec()
        else:
            self.msgBox.setText("Nothing to copy!")
            self.msgBox.exec()
    
    def bt_Export_handle(self):
        """
        Handle bt_Export by extracting the addon's code and show it on textEdit
        """
        self.textEdit.clear()
        self.directory = os.getcwd()
        self.foundAnkiAt=self.directory.find(self.pathToFind)
        self.directory=self.directory[:self.foundAnkiAt + len(self.pathToFind)]

        if self.directory.find('/')==-1:
            self.directory+='\\addons21'
        else:
            self.directory+='/addons21'
        
        self.addonList=[folder for folder in os.listdir(self.directory) if os.path.isdir(self.directory+os.path.sep+folder)]
        self.copyAll= '\n'.join(self.addonList)
        self.textEdit.setText(self.copyAll)

def testFunction():
    try:
        mw.myWidget= form = MyApp()
        form.show()        
    except Exception as e:
        print(e)

# create a new menu item, "test"
action = QAction("Test", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)