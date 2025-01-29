import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt5 import  QtGui, uic, QtWidgets
from funkce import initodsifruj, initzasifruj
qtCreatorFile = "gui_ukol_2.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QMainWindow, Ui_MainWindow):
    
    def Menu(self):

        klic = self.lineEditklic.text()
        vstup = self.plainTextEditVstup.toPlainText()
        volba = self.comboBoxjazyk.currentIndex()
        if self.radioButtonSiforvat.isChecked():
            result, zasabc = initzasifruj(vstup,klic, volba)
            self.plainTextEditVystup.setPlainText(result)
            if zasabc != 1:
                for x in range(25):
                    self.tableWidget.setItem(x//5,x%5,QtWidgets.QTableWidgetItem(zasabc[x]))
            else:
                self.plainTextEditVystup.setPlainText("Špatné vstupy")
        else:
            result, zasabc = initodsifruj(vstup,klic, volba)
            self.plainTextEditVystup.setPlainText(result)
            if zasabc != 1:
                for x in range(25):
                    self.tableWidget.setItem(x//5,x%5,QtWidgets.QTableWidgetItem(zasabc[x]))
            else:
                self.plainTextEditVystup.setPlainText("Špatné vstupy")


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
                  
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButtonUloz.clicked.connect(self.Uloz)
        self.pushButtonNacist.clicked.connect(self.Nacti)
        self.pushButtonProved.clicked.connect(self.Menu)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

