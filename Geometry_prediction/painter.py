import sys
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import urllib.request
from PyQt5.QtCore import Qt,QLine,QPoint


from_class = uic.loadUiType("/home/addinedu/amr_ws/MachineLearning/src/Geometry_prediction/paint.ui")[0]
class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pixmap = QPixmap(self.label.width(),self.label.height())
        self.pixmap.fill(Qt.white)

        self.label.setPixmap(self.pixmap)
        self.x,self.y = None,None
        self.draw_picture = None

        self.input.clicked.connect(self.pic)
        self.clear.clicked.connect(self.clearing)


    def clearing(self):
        self.pixmap.fill(Qt.white)
        self.label.setPixmap(self.pixmap)
        self.draw_picture = None
        self.text.setText("") 

    def pic(self):
        self.draw_picture = self.label.pixmap().copy()
        self.text.setText("circle")
        file_path = "/home/addinedu/amr_ws/MachineLearning/src/Geometry_prediction/drawn_picture.png"
        self.label.pixmap().save(file_path)
        self.text.setText(f"Saved: {file_path}")

        QApplication.quit()

    def mouseMoveEvent(self, event):
        if self.x is None:
            self.x = event.x()
            self.y = event.y()
            return
        
        painter = QPainter(self.label.pixmap())
        painter.setPen(QPen(Qt.black,10,Qt.SolidLine))
        painter.drawLine(self.x,self.y,event.x(),event.y())
        painter.end()
        self.update()

        self.x = event.x()
        self.y = event.y()

    def mouseReleaseEvent(self, event):
        self.x = None
        self.y = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    myWindows.show()
    
    sys.exit(app.exec_())
