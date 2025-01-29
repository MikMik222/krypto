import sys
import random
from funkce import initodsifruj, initzasifruj
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QComboBox
from PyQt5 import  QtGui, uic, QtWidgets
qtCreatorFile = "gui_ukol_3.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
pole = ["A","D","F","G","X"]
vsechnyznaky = False
zbytekabc = ["0","1","2","3","4","5","6","7","8","9","Q"]
abeceda = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
volneznaky = [" "]
znaky = []
znaky += abeceda
znaky.remove("Q")
random.shuffle(znaky)
class comboCompanies(QComboBox):
    def __init__(self, parent,index):
        super().__init__(parent)
        self.__name__=str(index)
        self.addItem(str(znaky[index]))
        self.activated.connect(self.updatedata)
        

        
    def mousePressEvent(self, event):
        if(self.currentText() != " "):
            volneznaky.append(self.currentText())
            znaky[znaky.index(self.currentText())] = ""
        volneznaky.sort()
        self.clear()
        self.addItems(volneznaky)
        self.showPopup()
        
    def wheelEvent(self, event):
        nefungujescroll = True
        
        
    def updatedata(self):
        if(self.currentText() != " "):
            volneznaky.remove(self.currentText())
            znaky[int(self.__name__)] = self.currentText()
        
        

class MyApp(QMainWindow, Ui_MainWindow):
    
    
    
    def InitTabulky(self):
        for index in range(0,25):
            combo = comboCompanies(self,index)
            self.tableWidget.setCellWidget(index//5,index%5,combo)
        self.tableWidget.setVerticalHeaderLabels(pole)
        self.tableWidget.setHorizontalHeaderLabels(pole)
        self.tableWidget.setGeometry(460, 40, 221, 181)
        

    def Menu(self):
        klic = self.lineEditklic.text()
        vstup = self.plainTextEditVstup.toPlainText()
        vstup = vstup.upper()
        if self.radioButtonSiforvat.isChecked():
            if len(volneznaky)==1:
                if self.comboBoxjazyk.currentIndex() == 0:
                    vstup=vstup.replace("Q","K")
                elif self.comboBoxjazyk.currentIndex() == 1:
                    vstup=vstup.replace("J","I")
                    
                result = initzasifruj(vstup, klic, znaky, pole)
                self.plainTextEditVystup.setPlainText(result)
            else:
                self.plainTextEditVystup.setPlainText("Není vyplněnná celá tabulka")
        else:
            if len(volneznaky)==1:
                if self.comboBoxjazyk.currentIndex() == 0:
                    vstup=vstup.replace("Q","K")
                elif self.comboBoxjazyk.currentIndex() == 1:
                    vstup=vstup.replace("J","I")
                    
                result = initodsifruj(vstup, klic, znaky, pole)
                self.plainTextEditVystup.setPlainText(result)
    
    def Clear(self):
        global znaky
        global volneznaky
        znaky = []
        volneznaky = [" "]
        if vsechnyznaky == False:
            for index in range(0,25):
                self.tableWidget.cellWidget(index//5,index%5).clear()
                self.tableWidget.cellWidget(index//5,index%5).addItem(" ")
                znaky.append("")
            volneznaky += abeceda
            volneznaky.remove(zbytekabc[10])
        else:
            for index in range(0,36):
                self.tableWidget.cellWidget(index//6,index%6).clear()
                self.tableWidget.cellWidget(index//6,index%6).addItem(" ")
                znaky.append("")
            volneznaky+=abeceda
            volneznaky+=zbytekabc
        
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
    
    def UlozTabulku(self):
        if(len(volneznaky)==1):
            options = QFileDialog.Options()
            result = ""
            for i in znaky:
                result += i
            fileName, _ = QFileDialog.getSaveFileName(self,"Ulož soubor", "","Text Files (*.txt);;All Files (*)", options=options)
            if fileName:
                f=open(fileName,"w")
                f.write(result)
                f.close()
        else:
            self.plainTextEditVystup.setPlainText("Není vyplněnná celá tabulka")
    
    def NactiTabulku(self):
        global znaky
        global volneznaky
        options = QFileDialog.Options()
        result = []
        fileName, _ = QFileDialog.getOpenFileName(self,"Vyber soubor", "","Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            f=open(fileName,"r")
            data = f.read()
            data = list(data)
            for q in data:
                if q not in result:
                    result.append(q)
            f.close()
        if(len(result)==25):
            rozdil = list(set(abeceda) - set(result))
            if (len(rozdil)==1):
                #cz
                if rozdil[0]=="Q":
                    volneznaky = [" "]
                    zbytekabc[10]="Q"
                    znaky = []
                    znaky += result
                    self.comboBoxjazyk.setCurrentIndex(0)
                    self.VyplnTabulku()
                elif rozdil[0]=="J":
                    volneznaky = [" "]
                    zbytekabc[10]="J"
                    znaky = []
                    znaky += result
                    znaky.remove("J")
                    self.comboBoxjazyk.setCurrentIndex(1)
                    self.VyplnTabulku()
                else:
                    self.plainTextEditVystup.setPlainText("Data jsou poškozené")
            else:
                self.plainTextEditVystup.setPlainText("Data jsou poškozené")
        elif len(result)==36:
            listnarozdil = []
            listnarozdil += abeceda
            listnarozdil += zbytekabc
            rozdil = list(set(listnarozdil) - set(result))
            if len(rozdil)==0:
                volneznaky = [" "]
                znaky = []
                znaky += result
                self.VyplnTabulku()
            else:
                self.plainTextEditVystup.setPlainText("Data jsou poškozené")
        else:
            self.plainTextEditVystup.setPlainText("Data jsou poškozené")
    
    def VyplnTabulku(self):
        global vsechnyznaky
        if len(znaky)==25:
            if len(pole)==6:
                vsechnyznaky=False
                self.comboBoxjazyk.setVisible(True)
                self.zmenaTabulky.setText("Abeceda 6x6")
                pole.remove("V")
                self.tableWidget.setRowCount(5)
                self.tableWidget.setColumnCount(5)
                self.tableWidget.setVerticalHeaderLabels(pole)
                self.tableWidget.setHorizontalHeaderLabels(pole)
                self.tableWidget.setGeometry(460, 40, 221, 181)
            for index in range(0,25):
                combo = comboCompanies(self,index)
                self.tableWidget.setCellWidget(index//5,index%5,combo)
        else:
            if len(pole)==5:
                pole.insert(4, "V")
                self.tableWidget.setVerticalHeaderLabels(pole)
                self.tableWidget.setHorizontalHeaderLabels(pole)
                self.tableWidget.setGeometry(460, 40, 260, 210)
                self.comboBoxjazyk.setVisible(False)
                self.zmenaTabulky.setText("Abeceda 5x5")
                vsechnyznaky = True
                self.tableWidget.setRowCount(6)
                self.tableWidget.setColumnCount(6)
            for index in range(0,36):
                combo = comboCompanies(self,index)
                self.tableWidget.setCellWidget(index//6,index%6,combo)
    
    def ZmenTabulku(self):
        global vsechnyznaky
        global znaky
        global volneznaky
        if vsechnyznaky == False:
            self.comboBoxjazyk.setVisible(False)
            self.zmenaTabulky.setText("Abeceda 5x5")
            vsechnyznaky = True
            znaky = []
            znaky += abeceda
            znaky += zbytekabc[:10]
            random.shuffle(znaky)
            self.tableWidget.setRowCount(6)
            self.tableWidget.setColumnCount(6)
            
            for index in range(0,36):
                combo = comboCompanies(self,index)
                self.tableWidget.setCellWidget(index//6,index%6,combo)
            pole.insert(4, "V")
            volneznaky = [" "]

            self.tableWidget.setVerticalHeaderLabels(pole)
            self.tableWidget.setHorizontalHeaderLabels(pole)
            self.tableWidget.setGeometry(460, 40, 260, 210)
                
        else:
            
            self.comboBoxjazyk.setVisible(True)
            self.zmenaTabulky.setText("Abeceda 6x6")
            pole.remove("V")
            volneznaky = [" "]
            vsechnyznaky = False
            znaky = []
            znaky += abeceda
            znaky.remove(zbytekabc[10])
            random.shuffle(znaky)
            self.tableWidget.setRowCount(5)
            self.tableWidget.setColumnCount(5)
            self.InitTabulky()
    
    def ZmenaJazyka(self):
        ##CZ
        if self.comboBoxjazyk.currentIndex() == 0:
            zbytekabc[10]="Q"
            if "Q" in znaky:
                temp = znaky.index("Q")
                znaky[temp]="J"
                mezery = 0
                for i in range(0,25):
                    if self.tableWidget.cellWidget(i//5,i%5).currentText() == " ":
                        mezery +=1
                    elif self.tableWidget.cellWidget(i//5,i%5).currentText() == "Q":
                        break
                    
                temp += mezery
                self.tableWidget.cellWidget(temp//5,temp%5).clear()
                self.tableWidget.cellWidget(temp//5,temp%5).addItem("J")
                
            else:
                if "J" not in volneznaky:
                    volneznaky.append("J")
                if "Q" in volneznaky:
                    volneznaky.remove("Q")
        else:
            zbytekabc[10]="J"
            if "J" in znaky:
                temp = znaky.index("J")
                znaky[temp]="Q"
                mezery = 0
                for i in range(0,25):
                    if self.tableWidget.cellWidget(i//5,i%5).currentText() == " ":
                        mezery +=1
                    elif self.tableWidget.cellWidget(i//5,i%5).currentText() == "J":
                        break
                temp += mezery
                self.tableWidget.cellWidget(temp//5,temp%5).clear()
                self.tableWidget.cellWidget(temp//5,temp%5).addItem("Q")
                
            else:
                if "Q" not in volneznaky:
                    volneznaky.append("Q")
                if "J" in volneznaky:
                    volneznaky.remove("J")
    
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.InitTabulky()
        self.pushButtonUloz.clicked.connect(self.Uloz)
        self.pushButtonNacist.clicked.connect(self.Nacti)
        self.pushButtonProved.clicked.connect(self.Menu)
        self.zmenaTabulky.clicked.connect(self.ZmenTabulku)
        self.comboBoxjazyk.activated.connect(self.ZmenaJazyka)
        self.pushButtonclear.clicked.connect(self.Clear)
        self.pushButtonuloztabulku.clicked.connect(self.UlozTabulku)
        self.pushButtonnactitabulku.clicked.connect(self.NactiTabulku)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())