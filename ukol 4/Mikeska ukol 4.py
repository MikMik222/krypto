import sys
import random
from funkce import generace, sifrovani, desifrovani
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QComboBox
from PyQt5 import  QtGui, uic, QtWidgets
qtCreatorFile = "gui_ukol_4.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

        

class MyApp(QMainWindow, Ui_MainWindow):
    
    def GeneraceKlicu(self):
        privatni, verejny = generace()
        self.lineEditD.setText(str(privatni[1]))
        self.lineEditN.setText(str(privatni[0]))
        self.lineEditE.setText(str(verejny[1]))
                
    
    def check(self):
        if len(self.lineEditE.text()) == 0 or len(self.lineEditD.text()) == 0 or len(self.lineEditN.text()) == 0:
            return "Chybý někde hodnoty"
        elif self.lineEditE.text().isdigit() == False or self.lineEditN.text().isdigit() == False or self.lineEditD.text().isdigit() == False:
            return "Klíče musí být číslo"
        temp = int(self.lineEditE.text()) * int(self.lineEditD.text())
        if(pow(65,temp,int(self.lineEditN.text()))!=65%int(self.lineEditN.text())):
            return "Špatné klíče"
        return "1"
    
    def Menu(self):
        N = self.lineEditN.text()
        vstup = self.plainTextEditVstup.toPlainText()
        poc_vstupy = self.check()
        if poc_vstupy == "1":
            if self.radioButtonSiforvat.isChecked():
                E = self.lineEditE.text()
                if (N.isdigit() and E.isdigit()):
                    result = sifrovani(vstup, int(E), int(N))
                    res = ""
                    for i in result:
                        res += str(i) + " "
                    res = res[:-1]
                    self.plainTextEditVystup.setPlainText(res)
                else:
                    self.plainTextEditVystup.setPlainText("Klíče musí být číslo")
            else:
                D = self.lineEditD.text()
                if (N.isdigit() and D.isdigit()):
                    result = desifrovani(vstup.split(" "), int(D), int(N))
                    res = ""
                    for i in result:
                        for t in i:
                            res += str(t)
                    self.plainTextEditVystup.setPlainText(res)
                else:
                    self.plainTextEditVystup.setPlainText("Špatné vstupy")
        else:
            self.plainTextEditVystup.setPlainText(poc_vstupy)
            
        
    
        
    def Nacti(self):        
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Vyber soubor", "","Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            f=open(fileName,"r")
            data = f.read()
            self.plainTextEditVstup.setPlainText(data)
            f.close()

    def Uloz(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"Ulož soubor", "","Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            f=open(fileName,"w")
            f.write(self.plainTextEditVystup.toPlainText())
            f.close()
    
    def UlozKlic(self):
        poc_vstupy = self.check()
        if poc_vstupy == "1":
            res = self.lineEditE.text() + " " + self.lineEditD.text() + " " + self.lineEditN.text()
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self,"Ulož soubor", "","Text Files (*.txt);;All Files (*)", options=options)
            
            if fileName:
                f=open(fileName,"w")
                f.write(res)
            f.close()
        else:
            self.plainTextEditVystup.setPlainText(poc_vstupy)
    
    def NactiKlic(self):        
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Vyber soubor", "","Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            f=open(fileName,"r")
            data = f.read()
            datapole = data.split( )
            if len(datapole) == 3:
                self.lineEditN.setText(datapole[0])
                self.lineEditD.setText(datapole[1])
                self.lineEditE.setText(datapole[2])
            else:
                self.plainTextEditVystup.setPlainText("Soubor je poškozen")
            f.close()
    
    def ZmenaD(self):
        self.lineEditROD.setText(self.lineEditD.text())
    
    def ZmenaN(self):
        self.lineEditRON.setText(self.lineEditN.text())
        self.lineEditRON_2.setText(self.lineEditN.text())
        
    def ZmenaE(self):
        self.lineEditROE.setText(self.lineEditE.text())
   
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButtonUloz.clicked.connect(self.Uloz)
        self.pushButtonNacist.clicked.connect(self.Nacti)
        self.pushButtonProved.clicked.connect(self.Menu)
        self.lineEditD.textChanged.connect(self.ZmenaD)
        self.lineEditN.textChanged.connect(self.ZmenaN)
        self.lineEditE.textChanged.connect(self.ZmenaE)
        self.pushButtonGEN.clicked.connect(self.GeneraceKlicu)
        self.pushButtonulozklice.clicked.connect(self.UlozKlic)
        self.pushButtonNactiklic.clicked.connect(self.NactiKlic)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())