import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QLine,QPoint
from PyQt5 import uic
import cv2
import numpy as np
import time,datetime
class NewWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle('HSV')
        uic.loadUi('cameraWiget.ui', self)  

        # self.slider_H.setRange(0, 180)
        # self.slider_S.setRange(0, 255)
        self.slider_V.setRange(0, 255)
        self.slider_R.setRange(0, 255)
        self.slider_G.setRange(0, 255)
        self.slider_B.setRange(0, 255)

        image = self.main_window.label.pixmap().toImage()
        h, w = image.height(), image.width()
        qimage_format = image.format()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        arr = np.array(ptr).reshape(h, w, 4)  

        # Convert RGBA to RGB
        self.image = cv2.cvtColor(arr, cv2.COLOR_RGBA2RGB)

        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        self.h_value, self.s_value, self.v_value = self.hsv_image[h // 2, w // 2]
        self.r_value, self.g_value, self.b_value = self.image[h // 2, w // 2]

        print('---------', self.h_value, self.s_value, self.v_value, self.r_value, self.g_value, self.b_value)

        # self.slider_H.setValue(self.h_value)
        # self.slider_S.setValue(self.s_value)
        self.slider_V.setValue(self.v_value)
        self.slider_R.setValue(self.r_value)
        self.slider_G.setValue(self.g_value)
        self.slider_B.setValue(self.b_value)

        # self.label_H.setText(f'H: {self.h_value}')
        # self.label_S.setText(f'S: {self.s_value}')
        self.label_V.setText(f'V: {self.v_value}')
        self.label_R.setText(f'R: {self.r_value}')
        self.label_G.setText(f'G: {self.g_value}')
        self.label_B.setText(f'B: {self.b_value}')

        # self.slider_H.valueChanged.connect(self.adjustCameraHSV)
        # self.slider_S.valueChanged.connect(self.adjustCameraHSV)
        self.slider_V.valueChanged.connect(self.adjustCameraHSV)
        self.slider_R.valueChanged.connect(self.adjustCameraRGB)
        self.slider_G.valueChanged.connect(self.adjustCameraRGB)
        self.slider_B.valueChanged.connect(self.adjustCameraRGB)

    def adjustCameraHSV(self):
        
        # h_value = self.slider_H.value()
        # s_value = self.slider_S.value()
        v_value = self.slider_V.value()

        
        # self.label_H.setText(f'H: {h_value}')
        # self.label_S.setText(f'S: {s_value}')
        self.label_V.setText(f'V: {v_value}')

        self.main_window.update_image_hsv(self.h_value, self.s_value, v_value - self.v_value)

    def adjustCameraRGB(self):
        r_value = self.slider_R.value()
        g_value = self.slider_G.value()
        b_value = self.slider_B.value()

        self.label_R.setText(f'R: {r_value}')
        self.label_G.setText(f'G: {g_value}')
        self.label_B.setText(f'B: {b_value}')

        self.main_window.update_image_rgb(r_value - self.r_value, g_value - self.g_value, b_value - self.b_value)


class Camera(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        while self.running:
            self.update.emit()
            time.sleep(0.1)

    def stop(self):
        self.running = False

from_class = uic.loadUiType("camera.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.isRecStart = False
        self.isCameraOn = False
        self.save.hide()
        self.dele.hide()
        self.blur.hide()
        self.widget.hide()

        self.label_rec.hide()
        
        self.pixmap = QPixmap()
        self.x,self.y = None,None
        self.pen = 'blue'
        self.pen_R.clicked.connect(lambda: self.setPenColor('red'))
        self.pen_G.clicked.connect(lambda: self.setPenColor('green'))
        self.pen_B.clicked.connect(lambda: self.setPenColor('blue'))


        self.camera = Camera(self)
        self.camera.daemon = True

        self.record = Camera(self)
        self.record.daemon = True

        self.count = 0
        self.c = 0
        self.h_value = 0
        self.s_value = 0
        self.v_value = 0


        self.cameraStart()

        self.load.clicked.connect(self.openFile)
        self.shoot.clicked.connect(self.clickCamera)
        self.camera.update.connect(self.updateCamera)
        self.btn_rec.clicked.connect(self.clickRecord)
        self.record.update.connect(self.updateRecording)
        self.save.clicked.connect(self.saveIMG)
        self.dele.clicked.connect(self.goBack)
        self.blur.clicked.connect(self.gray)


        self.widget.clicked.connect(self.openNewWindow)
    def openNewWindow(self):
        self.new_window = NewWindow(self)
        # self.new_window.slider_H.setValue(self.h_value)
        # self.new_window.slider_S.setValue(self.s_value)
        self.new_window.slider_V.setValue(self.v_value)
        self.new_window.show()
    def gray(self):
        image = self.pixmap.toImage()
        if self.c == 0 :
            image = image.convertToFormat(QImage.Format_Grayscale8)
            self.c += 1
        else :
            image = image.convertToFormat(QImage.Format_RGB32)
            self.c -= 1

        self.pic = QPixmap.fromImage(image)
        self.label.setPixmap(self.pic)

        self.cameraStop()
        self.btn_rec.hide()
        self.shoot.hide()
        self.save.show()
        self.dele.show()
        self.label.setPixmap(self.pic)

    def setPenColor(self, color):
        self.pen = color

    def mouseMoveEvent(self, event):
        if self.x is None:
            self.x = event.x()
            self.y = event.y()
            return
        
        painter = QPainter(self.label.pixmap())
        if self.pen == 'blue':
            painter.setPen(QPen(Qt.blue,5,Qt.SolidLine))
        elif self.pen == 'red':
            painter.setPen(QPen(Qt.red,5,Qt.SolidLine))
        else:
            painter.setPen(QPen(Qt.green,5,Qt.SolidLine))

        painter.drawLine(self.x,self.y,event.x(),event.y())
        painter.end()
        self.update()

        self.x = event.x()
        self.y = event.y()

    def mouseReleaseEvent(self, event):
        self.x = None
        self.y = None

    def saveIMG(self):
        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now + '.png'
        
        pixmap = self.label.pixmap()
        image = pixmap.toImage()
        image.save(filename)

        self.goBack()

    def updateRecording(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.writer.write(self.image)

    def clickRecord(self):
        if self.isRecStart == False:
            self.label_rec.show()
            self.btn_rec.setText('Stop')
            self.isRecStart = True

            self.recordingStart()
        else:
            self.label_rec.hide()
            self.btn_rec.setText('REC')
            self.isRecStart = False

            self.recordingStop()


    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.now+'.avi'
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.writer = cv2.VideoWriter(filename,self.fourcc,20.0,(w,h))


    def recordingStop(self):
        self.record.running = False

        if self.isRecStart == True:
            self.writer.release()


        
    def updateCamera(self):
        if hasattr(self, 'video') and self.video.isOpened():
            retval, image = self.video.read()
            if retval:
                self.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h,w,c = self.image.shape

                self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
                self.h_value, self.s_value, self.v_value = self.hsv_image[h // 2, w // 2]


                qimage = QImage(self.image.data, w, h, w*c, QImage.Format_RGB888)
                self.pixmap = self.pixmap.fromImage(qimage)
                self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())
                self.label.setPixmap(self.pixmap)
        self.count+=1

    def update_image_hsv(self, h_diff, s_diff, v_diff):
        edited_image = self.pic.toImage()

        for y in range(edited_image.height()):
            for x in range(edited_image.width()):
                color_hsv = edited_image.pixelColor(x, y)
                h, s, v, _ = QColor(color_hsv).getHsv()

                # h = max(0, min(180, h + h_diff))
                # s = max(0, min(255, s + s_diff))
                v = max(0, min(255, v + v_diff))

                edited_image.setPixelColor(x, y, QColor.fromHsv(h, s, v))

        edited_pixmap = QPixmap.fromImage(edited_image)
        self.label.setPixmap(edited_pixmap)

    
    def update_image_rgb(self, r_value, g_value, b_value):
        edited_image = self.pic.toImage()
        for y in range(edited_image.height()):
            for x in range(edited_image.width()):
                color_rgb = edited_image.pixelColor(x, y)
                r, g, b, _ = color_rgb.getRgb()

                r = max(0, min(255, r + r_value))
                g = max(0, min(255, g + g_value))
                b = max(0, min(255, b + b_value))

                edited_image.setPixelColor(x, y, QColor(r, g, b))
        edited_pixmap = QPixmap.fromImage(edited_image)
        self.label.setPixmap(edited_pixmap)


    def clickCamera(self):
        self.pic = self.pixmap
        self.cameraStop()
        self.btn_rec.hide()
        self.shoot.hide()
        self.save.show()
        self.dele.show()
        self.blur.show()
        self.widget.show()
        self.label.setPixmap(self.pic)
        self.label.setPixmap(self.label.pixmap())
        
    def goBack(self):
        self.shoot.show()
        self.btn_rec.show()
        self.save.hide()
        self.dele.hide()
        self.blur.hide()
        self.label_rec.hide()
        self.widget.hide()
        self.label.clear()

        self.cameraStart()

    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(0)

    def cameraStop(self):
        self.camera.running = False
        self.count = 0
        if hasattr(self, 'video') and self.video.isOpened():
            self.video.release()

    def openFile(self):
        self.cameraStop()
        self.btn_rec.hide()
        self.shoot.hide()
        self.save.show()
        self.dele.show()
        file = QFileDialog.getOpenFileName(filter='Image(*.*)')
        image=cv2.imread(file[0])
        if image is not None:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            h,w,c = image.shape
            qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
            self.pixmap = self.pixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())
            self.label.setPixmap(self.pixmap)
            self.save.show()
            self.dele.show()

            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())