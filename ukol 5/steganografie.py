import sys
import os
import random, math
from PyQt5.QtGui import QPixmap
from PIL import *
from funkce import pil2pixmap, ziskejtext, upravrRGB
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox,  QLabel, QPlainTextEdit
from PyQt5 import  QtGui, uic, QtWidgets, QtCore
qtCreatorFile = "steganoGUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
data = []
ukoncovacitextvb = "000011001000000110100000001100111000011101000000110110100001101100"
ukoncovacitext = "dhgtml"
maxdat = 0
png = False
im2 = ""
vkladani = True
vypocitano = False

class MyApp(QMainWindow, Ui_MainWindow):
    def NactiObrazek(self):
        global png
        global im2
        global data
        global maxdat
        global vypocitano
        width = 1
        height = 1
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Vyber", "","Image (*.png;*.bmp)", options=options)
        if fileName:
            self.label_2.setVisible(True)
            self.label_3.setVisible(True)
            self.label_6.setVisible(True)
            self.label_7.setVisible(True)
            
            if vypocitano == True:
                self.pushButtonuloz.setVisible(False)
                self.pushButtonzapsat.setEnabled(True)
                self.labelOUTIMG.clear()
                vypocitano = False
            data = []
            if fileName[-3:]=="png":
                png = True
            else:
                png = False
            im2 = Image.open(fileName)
            pixmap = pil2pixmap(im2)
            self.label_4.setText(str(im2.size[0])+"x"+str(im2.size[1]))
            self.label_5.setText(fileName[-3:])
            self.label_9.setText(fileName)
            self.label_8.setText(str(os.path.getsize(fileName))+" bajtů")

            self.labelINIMG.setPixmap(pixmap.scaled(self.labelINIMG.size(),QtCore.Qt.KeepAspectRatio))
            width = pixmap.width()
            height = pixmap.height()
            neco = list(im2.getdata())
            for i in neco:
                data.append(list(i))
            pocetbitu = width * height * 3
            maxdat = pocetbitu//11 - len(ukoncovacitext)
            self.pushButtonzapsat.setEnabled(True)
            
            self.labelinfo.setText(str(len(self.plainTextEdit.toPlainText()))+"/"+str(maxdat))

    def Ulozsoubor(self):
        global im2
        options = QFileDialog.Options()
        if png == True:
            fileName, _ = QFileDialog.getSaveFileName(self,"Ulož soubor", "","Image (*.png)", options=options)
        else:
            fileName, _ = QFileDialog.getSaveFileName(self,"Ulož soubor", "","Image (*.bmp)", options=options)
        if fileName:
            im2.save(fileName)
    
    def UlozObrazek(self):
        global im2
        global vypocitano
        if len(self.plainTextEdit.toPlainText()) > maxdat:
            self.ChybovaHlaska("Příliš dlouhé slovo")
        else:
            if vypocitano == False:
                finres = upravrRGB(data, self.plainTextEdit.toPlainText())
                im2.putdata(finres)
                pixmap = pil2pixmap(im2)
                self.labelOUTIMG.setPixmap(pixmap.scaled(self.labelOUTIMG.size(),QtCore.Qt.KeepAspectRatio))
                self.pushButtonuloz.setVisible(True)
                self.pushButtonzapsat.setEnabled(False)
                vypocitano = True
        
    def UpravInfo(self):
        global vypocitano
        if vypocitano == True:
            self.pushButtonuloz.setVisible(False)
            self.pushButtonzapsat.setEnabled(True)
            self.labelOUTIMG.clear()
            vypocitano = False
        self.labelinfo.setText(str(len(self.plainTextEdit.toPlainText()))+"/"+str(maxdat))
    
    def ZiskejData(self):
        res,temp = ziskejtext(data)
        if temp == 0:
            self.plainTextEdit.setPlainText(res)
        else:
            self.ChybovaHlaska(res)
        
    def Uloz(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"Ulož soubor", "","Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            f=open(fileName,"w")
            f.write(self.plainTextEdit.toPlainText())
            f.close()
    
    def Nacti(self):        
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Vyber soubor", "","Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            f=open(fileName,"r")
            data = f.read()
            self.plainTextEdit.setPlainText(data)
            f.close()
            
    def ChybovaHlaska(self, chyba):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(chyba)
        msg.setWindowTitle("Error")
        msg.exec_()
    
    def updamode(self):
        global vkladani
        if vkladani == True:
            self.plainTextEdit.setPlainText("")
            self.labelinfo.setVisible(False)
            self.label.setText("Data po přečtení")
            self.pushButtonZiskejdata.setVisible(True)
            self.pushButtonzapsat.setVisible(False)
            vkladani = False
        else:
            self.labelinfo.setVisible(True)
            self.label.setText("Data pro vložení")
            self.pushButtonZiskejdata.setVisible(False)
            self.pushButtonzapsat.setVisible(True)
            vkladani = True
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButtonzapsat.clicked.connect(self.UlozObrazek)
        self.pushButtonnacist.clicked.connect(self.NactiObrazek)
        self.pushButtonuloz.clicked.connect(self.Ulozsoubor)
        self.pushButtonuloz.setVisible(False)
        self.pushButtonZiskejdata.setVisible(False)
        self.label_2.setVisible(False)
        self.label_3.setVisible(False)
        self.label_6.setVisible(False)
        self.label_7.setVisible(False)
        self.pushButtonZiskejdata.clicked.connect(self.ZiskejData)
        self.pushButtonsave.clicked.connect(self.Uloz)
        self.pushButtonload.clicked.connect(self.Nacti)
        self.plainTextEdit.textChanged.connect(self.UpravInfo)
        self.comboBox.activated.connect(self.updamode)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())