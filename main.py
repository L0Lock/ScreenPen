import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QShortcut, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint

# source: https://www.youtube.com/watch?v=qEgyGyVA1ZQ


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        top = 400
        left = 400
        width = 800
        height = 600

        icon = "icons/icon.png"

        self.setWindowTitle("ScreenPen drawing board")
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon(icon))
        # Window style
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setStyleSheet("background:transparent")
        # self.setAttribute(Qt.WA_NoSystemBackground)
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

# ---------- sets image ----------
        self.image = QImage(self.size(), QImage.Format_RGBA64)
        self.image.fill(Qt.transparent)
        # self.image.setStyleSheet("background:transparent;")

# ---------- init drawing state ----------
        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.red
        self.lastPoint = QPoint()

    def paintEvent(self, event): # event de type QPaintEvent
        self.drawing = True
        self.lastPoint = 0
        painter = QPainter(self) # recupere le QPainter du widget
        painter.drawRect(5,5,120,40) # dessiner un rectangle noir
        self.drawing = False
        return

# ---------- Define Menus ----------
    # mainmenu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        toolMenu = mainMenu.addMenu("Tool")
        toolColor = mainMenu.addMenu("Color")
    # smenu save
        saveAction = QAction(QIcon("icons/save.png"), "Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.saveFrame)
    # smenu clear frame
        clearFrameAction = QAction(QIcon("icons/clear.png"), "Clear Frame", self)
        clearFrameAction.setShortcut("Ctrl+Del")
        fileMenu.addAction(clearFrameAction)
        clearFrameAction.triggered.connect(self.clearFrame)
    # smenu Tool Pen
        toolPenAction = QAction(QIcon("icons/toolPen.png"), "Pen", self)
        # clearAction.setShortcut("Ctrl+Del")
        toolMenu.addAction(toolPenAction)

# ---------- Catch Mouse Down --------

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

# ---------- Catch Mouse Move --------
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

# ---------- Catch Mouse Up --------
    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

# ---------- Paint --------
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

# ---------- Save Action ----------
    def saveFrame(self):
        filePath,  _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPEG(*.jpg *.jpeg);; ALL Files(*.*)")
        if filePath == "":
            return
        self.image.save(filePath)

# ---------- Clear Frame Action ----------
    def clearFrame(self):
        self.image.fill(Qt.white)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = Window()
    # Window style
    # Window.setStyleSheet("background:transparent;")
    # Window.setAttribute(Qt.WA_TranslucentBackground)
    # Window.setAttribute(Qt.WA_NoSystemBackground, True)
    # Window.setWindowFlags(Qt.FramelessWindowHint)
    # Window.setWindowFlags(Window.windowFlags() | Qt.WindowStaysOnTopHint)
    Window.show()
    app.exec()
