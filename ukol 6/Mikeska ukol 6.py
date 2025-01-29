import sys
import os
from os.path import basename
import hashlib
import zipfile
import base64
from funkce import generace, sifrovani, desifrovani
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QComboBox, QMessageBox
from PyQt5 import  QtGui, uic, QtWidgets
qtCreatorFile = "gui_ukol_6.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

podpis = True
data = ""
skname = "RSA SOUKROMÝ_KLÍČ_V_BASE64"
vkname = "RSA VEŘEJNÝ_KLÍČ_V_BASE64"
podpisname = "RSA_SHA256 PODPIS_V_BASE64.sign"
klic = ""
hashrsadata = ""
cesta = ""
class MyApp(QMainWindow, Ui_MainWindow):

    def InfoError(self, zprava):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(zprava)
        msg.setWindowTitle("Error")
        msg.exec_()
        
    def Info(self, zprava):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("")
        msg.setInformativeText(zprava)
        msg.setWindowTitle("Info")
        msg.exec_()

    def InfoVarovani(self, zprava):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Varování")
        msg.setInformativeText(zprava)
        msg.setWindowTitle("Varování")
        msg.exec_()

    def GeneraceKlicu(self):
        privatni, verejny = generace()
        self.lineEditROD.setText(str(privatni[1]))
        self.lineEditRON.setText(str(privatni[0]))
        self.lineEditRON_2.setText(str(privatni[0]))
        self.lineEditROE.setText(str(verejny[1]))

    def Menu(self):
        global hashrsadata
        if self.radioButtonSiforvat.isChecked():
            N = self.lineEditRON_2.text()
            D = self.lineEditROD.text()
            if len(N)==0 or len(D)==0:
                self.InfoVarovani("Chybý klíčový pár")
            elif (N.isdigit() and D.isdigit()):
                result = sifrovani(str(data), int(D), int(N))
                res = ""
                for i in result:
                    res += str(i) + " "
                res = res[:-1]
                hashrsadata = res
                self.pushButtonUloz.setVisible(True)
            else:
                self.InfoVarovani("Klíče musí být číslo")
        else:
            N = self.lineEditRON.text()
            E = self.lineEditROE.text()
            if len(N)==0 or len(E)==0:
                self.InfoVarovani("Chybý klíčový pár")
            elif (N.isdigit() and E.isdigit()):
                result = desifrovani(data.split(" "), int(E), int(N))
                res = ""
                for i in result:
                    for t in i:
                        res += str(t)
                if hashrsadata == res:
                    self.Info("Podpis je v pořádku")
                else:
                    self.InfoError("Někdo se souborem manipuloval")
                hashrsadata = res
            else:
                self.InfoVarovani("Klíče musí být číslo")

    def InfoOSouboru(self, jmeno):
        self.label.setText("Soubor načten")
        text = "Info o souboru\n"
        text += "Cesta: " + jmeno + "\n"
        text += "Přípona: ." + jmeno.split(".")[-1] + "\n"
        text += "Velikost: " + str(os.path.getsize(jmeno))+" bajtů"
        self.label_2.setText(text)

    def Nacti(self):
        global data
        global cesta
        global hashrsadata
        if podpis == True:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,"Vyber soubor", "","All Files (*)", options=options)
            if fileName:
                cesta = fileName
                f=open(fileName,"rb")
                byt = f.read()
                data = hashlib.sha3_512(byt).hexdigest()
                print(data)
                f.close()
                self.InfoOSouboru(fileName)
                self.pushButtonpodpis.setVisible(True)
                self.pushButtonUloz.setVisible(False)
        else:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self,"Vyber soubor", "","Zip file (*.zip)", options=options)
            if fileName:
                cesta = fileName
                z = zipfile.ZipFile(fileName, 'r')
                seznamsouboru = []
                for info in z.namelist():
                    seznamsouboru.append(info)
                if len(seznamsouboru)==2 and podpisname in seznamsouboru:
                    for i in seznamsouboru:
                        if i == podpisname:
                            data = base64.b64decode(z.read(i)).decode("utf-8")
                        else:
                            byt = z.read(i)
                            hashrsadata = hashlib.sha3_512(byt).hexdigest()
                    self.pushButtonover.setVisible(True)
                    self.InfoOSouboru(fileName)
                else:
                    self.pushButtonover.setVisible(False)
                    self.Info("Špatný soubor")

    def Uloz(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"Ulož soubor", "","Zip file (*.zip)", options=options)
        if fileName:
            t=open(podpisname,"wb")
            t.write(base64.b64encode(hashrsadata.encode("utf-8")))
            t.close()
            f=zipfile.ZipFile(fileName,"w")
            f.write(podpisname)
            f.write(cesta,basename(cesta))
            f.close()
            os.remove(podpisname)
    
    def UlozKlic(self):
        if len(self.lineEditROE.text()) == 0 or len(self.lineEditROD.text()) == 0 or len(self.lineEditRON.text()) == 0:
            self.InfoVarovani("musí se vygenerovat klíče")
        else:
            file = str(QFileDialog.getExistingDirectory(self, "Vybrat složku"))
            if file:
                f=open(file+"/"+vkname+".pub","wb")
                f.write(base64.b64encode(self.lineEditRON.text().encode("utf-8"))+(" ".encode("utf-8"))+base64.b64encode(self.lineEditROE.text().encode("utf-8")))
                f.close()
                f=open(file+"/"+skname+".priv","wb")
                f.write(base64.b64encode(self.lineEditRON.text().encode("utf-8"))+(" ".encode("utf-8"))+base64.b64encode(self.lineEditROD.text().encode("utf-8")))
                f.close()
    
    def NactiKlic(self):        
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Vyber soubor", "","Klíč (*.pub;*.priv);;All Files (*)", options=options)
        if fileName:
            f=open(fileName,"r")
            data = f.read()
            datapole = data.split( )
            if len(datapole) == 2:
                if fileName[-3:]=="pub":
                    self.lineEditRON.setText(base64.b64decode(datapole[0]).decode("utf-8"))
                    self.lineEditROE.setText(base64.b64decode(datapole[1]).decode("utf-8"))
                else:
                    self.lineEditRON_2.setText(base64.b64decode(datapole[0]).decode("utf-8"))
                    self.lineEditROD.setText(base64.b64decode(datapole[1]).decode("utf-8"))
            else:
                self.Info("Soubor je poškozen")
            f.close()
    
    def Zmena(self):
        global podpis
        if podpis == False:
            podpis = True
            self.pushButtonover.setVisible(False)
            self.label_2.setText("")
            self.label.setText("Žádný soubor není načtený")

    def Zmena2(self):
        global podpis
        if podpis == True:
            self.label_2.setText("")
            self.pushButtonUloz.setVisible(False)
            self.pushButtonpodpis.setVisible(False)
            self.label.setText("Žádný soubor není načtený")
            podpis = False
   
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButtonUloz.setVisible(False)
        self.pushButtonpodpis.setVisible(False)
        self.pushButtonover.setVisible(False)
        self.pushButtonpodpis.clicked.connect(self.Menu)
        self.pushButtonover.clicked.connect(self.Menu)
        self.pushButtonUloz.clicked.connect(self.Uloz)
        self.pushButtonNacist.clicked.connect(self.Nacti)
        self.pushButtonGEN.clicked.connect(self.GeneraceKlicu)
        self.pushButtonulozklice.clicked.connect(self.UlozKlic)
        self.pushButtonNactiklic.clicked.connect(self.NactiKlic)
        self.radioButtonSiforvat.clicked.connect(self.Zmena)
        self.radioButtonOdsifrovat.clicked.connect(self.Zmena2)   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())