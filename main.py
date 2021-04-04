#создай тут фоторедактор Easy Editor!
#from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication 
from PyQt5.QtWidgets import (
        QApplication, QWidget, 
        QHBoxLayout, QVBoxLayout, 
        QGroupBox, QButtonGroup, QRadioButton,  
        QPushButton, QLabel, QListWidget, QFileDialog,
        )
import os
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import (
    BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
    EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
    GaussianBlur, UnsharpMask
)


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy editor')




photo = QLabel('Картинка')

gor_4 = QHBoxLayout()
gor_2 = QHBoxLayout()

ver_1 = QVBoxLayout()
ver_3 = QVBoxLayout()

list_1 = QListWidget()

poisk_button = QPushButton('Поиск')
levo_button = QPushButton('Лево')
pravo_button = QPushButton('Право')
zerkalo_button = QPushButton('Зеркало')
rezkost_button = QPushButton('Резкость')
chb_button = QPushButton('Ч / Б')

gor_2.addWidget(levo_button)
gor_2.addWidget(pravo_button)
gor_2.addWidget(zerkalo_button)
gor_2.addWidget(rezkost_button)
gor_2.addWidget(chb_button)

ver_1.addWidget(poisk_button)
ver_1.addWidget(list_1)

ver_3.addWidget(photo)

# Тут что-то должно быть вроде

ver_3.addLayout(gor_2)
gor_4.addLayout(ver_1)
gor_4.addLayout(ver_3)

main_win.setLayout(gor_4)

workdir = ''

def filter(files, extentions):
    result = list()
    for filename in files:
        for ext in extentions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def showFilenameslist():
    extentions = ['.png', '.jpg', '.jpeg']
    chooseWorkDir()
    filenames = filter(os.listdir(workdir), extentions)
    for filename in filenames: 
        list_1.addItem(filename)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadImage(self, filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def showImage(self, path):
        photo.hide()
        pixmapimage = Qpixmap(path)
        w = photo.width()
        h = photo.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        photo.setPixmap(pixmapimage)
        photo.show()
    
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
workimage = ImageProcessor()
def showChosenImage():
    if list_1.currentRow() >= 0:
        filename = list_1.currentItem().text()
        workimage.loadImage(filename)
        #image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(os.path.join(workimage.dir, workimage.filename))
        
workimage = ImageProcessor()

list_1.currentRowChanged.connect(showChosenImage)
chb_button.clicked.connect(workimage.do_bw)
poisk_button.clicked.connect(showFilenameslist)
levo_button.clicked.connect(workimage.do_left)
pravo_button.clicked.connect(workimage.do_right)
rezkost_button.clicked.connect(workimage.do_sharpen)
zerkalo_button.clicked.connect(workimage.do_flip)

    #lb_image - QListWidget

main_win.show()
app.exec_()