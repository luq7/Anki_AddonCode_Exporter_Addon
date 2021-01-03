from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from .anki_addon_exporter import *



class MyApp(QtWidgets.QMainWindow, anki_addon_exporter.Ui_Dialog):
    """
    GUI class: Creates an instance of anki_addon_exporter scene
    
    Parameters:
    QtWidgets.QMainWindow: Main windows.
    anki_addon_exporter.Ui_Dialog: The instance to be crated
    """
    def __init__(self, parent=None): 
        """
        Attributes
        -------------------
        scriptDir: str 
            used to get the absolute path for the logo: "anki_exporter_logo.png"
        textEdit:  QTextEdit
            the text edit field from GUI
        directory: str
            directory where the addons are at, e.g. for windows: C:/Users/{username}/AppData/Roaming/Anki2/addons21
            for mac and linux refenrece: https://docs.ankiweb.net/#/files?id=file-locations
        addonList: list of str
            each cell of the list is an addon's code
        foundAnkiAt: int
            used to find the "Anki2" from the OS directory. 
            e.g. C:/Users/{username}/AppData/Roaming/"---->Anki2<------"/addons21 
        pathToFind : str 
            the substring to look for in the OS directory
        copyAll : str
            all the elements in addonList in line separated format
        clipboad : QtClipboard
            used to copy all the addons code to the clipboard
        bt_copy : QtPushButton
        bt_Export: QtPushButton
        ...
        Methods 
        ----------------------
        bt_Copy_handle() : return void
        bt_Export_handle():return void
        
        """
        super(MyApp, self).__init__(parent)
        self.setupUi(self)
        
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(self.scriptDir+ os.path.sep + "anki_exporter_logo.png"))# Set icon for main scene
        self.textEdit.setEnabled(True)
        # Varaible declaration
        self.directory=None
        self.addonList=None
        self.foundAnkiAt=None
        self.pathToFind='Anki2'
        self.copyAll=""
        self.firstRunFlag=True
        # Creating a messagebox
        self.msgBox=QtWidgets.QMessageBox()
        self.msgBox.setWindowIcon(QtGui.QIcon(self.scriptDir+ os.path.sep + "anki_exporter_logo.png")) #Set icon for msgbox
        # Set a clipboard
        self.clipboard = QtWidgets.QApplication.clipboard()
        
        # Event handling 
        self.bt_copy.clicked.connect(self.bt_Copy_handle)     # Copy All button handle
        self.bt_Export.clicked.connect(self.bt_Export_handle) # Export button hanlde
        

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

action = QAction("Anki_Addon_Code_Export", mw)
action.triggered.connect(testFunction)
mw.form.menuTools.addAction(action)