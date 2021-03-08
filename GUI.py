import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from Downloader import main as Download


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(690, 471)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 0, 181, 161))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("YouTubeLogo.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(260, 50, 401, 81))
        font = QtGui.QFont()
        font.setFamily("Fira Code")
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(150, 190, 491, 41))
        font = QtGui.QFont()
        font.setFamily("Fira Code")
        font.setPointSize(18)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 190, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Fira Code")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(170, 250, 161, 23))
        font = QtGui.QFont()
        font.setFamily("Fira Code")
        font.setPointSize(16)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(350, 250, 271, 23))
        self.radioButton_2.click()
        font = QtGui.QFont()
        font.setFamily("Fira Code Medium")
        font.setPointSize(16)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 330, 211, 81))
        font = QtGui.QFont()
        font.setFamily("Fira Code Retina")
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.download)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "YouTube Downloader"))
        self.label_3.setText(_translate("MainWindow", "URL"))
        self.radioButton.setText(_translate("MainWindow", "Audio only"))
        self.radioButton_2.setText(_translate(
            "MainWindow", "Video (With Audio)"))
        self.pushButton.setText(_translate("MainWindow", "Download"))

    def download(self):
        link = self.lineEdit.text()
        mode = "a" if self.radioButton.isChecked() else "v"
        print(link, mode)
        Download(link, mode)
        self.lineEdit.setText("Done!")


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
