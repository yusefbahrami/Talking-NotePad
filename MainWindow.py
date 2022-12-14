from PyQt5.QtWidgets import QMainWindow, QAction, QStatusBar, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QFont, QKeySequence
from CentralWidget import CentralWidget


class MainWindow(QMainWindow):
    def __init__(self, speakObject: QThread) -> None:
        super().__init__()
        self.setWindowTitle("Notepad")
        self.font = QFont("vazir", 8)
        self.setFont(self.font)
        self.setMinimumSize(300, 300)
        self.resize(600, 400)
        self.speakObject = speakObject
        self.toolStripMenu()

        # using in file dialogs
        self.fileTypes = "Text File (*.txt);; All File (*.*)"
        self.fileName = None
        self.isSaved = True

        # self.fileToolStripMenu.triggered.connect(self.onMyToolBarButtonClick)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.widget = CentralWidget()
        self.setCentralWidget(self.widget)

        self.widget.txtDisplay.textChanged.connect(self.textChanged)

    def toolStripMenu(self):
        self.menu = self.menuBar()

        # File menu
        self.newToolStripMenuItem = QAction("New", self)
        self.newToolStripMenuItem.setShortcut(QKeySequence("ctrl+n"))
        self.newToolStripMenuItem.triggered.connect(self.newDocument)

        self.openToolStripMenuItem = QAction("Open", self)
        self.openToolStripMenuItem.setShortcut(QKeySequence("ctrl+o"))
        self.openToolStripMenuItem.triggered.connect(
            self.openMenu)
        self.saveToolStripMenuItem = QAction("Save", self)
        self.saveToolStripMenuItem.setShortcut(QKeySequence("ctrl+s"))
        self.saveToolStripMenuItem.triggered.connect(
            self.isFirstSave)

        self.saveAsToolStripMenuItem = QAction("SaveAs", self)
        self.saveAsToolStripMenuItem.setShortcut(QKeySequence("ctrl+shift+s"))
        self.saveAsToolStripMenuItem.triggered.connect(self.saveMenu)

        self.exitToolStripMenuItem = QAction("Exit", self)
        self.exitToolStripMenuItem.setShortcut(QKeySequence("alt+x"))
        self.exitToolStripMenuItem.triggered.connect(self.exitFunction)

        self.fileToolStripMenu = self.menu.addMenu("&File")
        self.fileToolStripMenu.addAction(self.newToolStripMenuItem)
        self.fileToolStripMenu.addAction(self.openToolStripMenuItem)
        self.fileToolStripMenu.addAction(self.saveToolStripMenuItem)
        self.fileToolStripMenu.addAction(self.saveAsToolStripMenuItem)
        self.fileToolStripMenu.addSeparator()
        self.fileToolStripMenu.addAction(self.exitToolStripMenuItem)

        # View menu
        self.wordWrapToolStripMenuItem = QAction("Word Wrap", self)
        self.wordWrapToolStripMenuItem.setShortcut(QKeySequence("alt+z"))
        self.wordWrapToolStripMenuItem.setCheckable(True)
        self.wordWrapToolStripMenuItem.setChecked(False)
        self.wordWrapToolStripMenuItem.triggered.connect(self.setWordWrap)

        self.viewToolStripMenu = self.menu.addMenu("&View")
        self.viewToolStripMenu.addAction(self.wordWrapToolStripMenuItem)

        # Run menu
        self.speakToolStripMenuItem = QAction("Speak", self)
        self.speakToolStripMenuItem.setShortcut(QKeySequence("ctrl+alt+s"))
        self.speakToolStripMenuItem.triggered.connect(self.speakMethod)

        self.runToolStripMenu = self.menu.addMenu("&Run")
        self.runToolStripMenu.addAction(self.speakToolStripMenuItem)

    def textChanged(self):
        self.isSaved = False

    def resetDocuemnt(self):
        self.widget.txtDisplay.setText("")
        self.fileName = None
        self.isSaved = True

    def newDocument(self):
        if self.isSaved == False:
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Save?")
            msgBox.setIcon(QMessageBox.Question)
            msgBox.setText("Do You Want to Save?")
            msgBox.setStandardButtons(
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            msgBoxValue = msgBox.exec()
            if msgBoxValue == QMessageBox.Yes:
                self.isFirstSave()
                self.resetDocuemnt()
            elif msgBoxValue == QMessageBox.No:
                self.resetDocuemnt()

        elif self.isSaved == True:
            self.resetDocuemnt()

    # save region

    def handleSaveFile(self):
        try:
            with open(self.fileName[0], 'w') as file:
                file.write(self.widget.txtDisplay.toPlainText())
            self.isSaved = True
        except FileNotFoundError:
            pass

    def isFirstSave(self):
        if self.fileName and self.fileName[0] != '':
            self.handleSaveFile()
        else:
            self.saveMenu()

    def saveMenu(self):
        # self.fileName will be a tuple
        self.fileName = QFileDialog.getSaveFileName(
            self, "Save File", filter=self.fileTypes)
        self.handleSaveFile()
    # end save region

    def openMenu(self):
        self.newDocument()
        self.fileName = QFileDialog.getOpenFileName(
            self, "Open File", filter=self.fileTypes)
        try:
            with open(self.fileName[0], 'r') as file:
                text = tuple(file.readlines())
                for line in text:
                    self.widget.txtDisplay.setText(
                        f"{self.widget.txtDisplay.toPlainText()}{line.strip()}\n")
            self.isSaved = True
        except FileNotFoundError:
            pass

    def exitFunction(self):
        self.newDocument()
        exit()

    def setWordWrap(self):
        print("in word wrap")

    def speakMethod(self):
        self.speakObject.setText(self.widget.txtDisplay.toPlainText())
        self.speakObject.start()
