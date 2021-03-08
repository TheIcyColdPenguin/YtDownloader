import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from Downloader import main as Download
from QThreading import Worker


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

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(200, 355, 30, 30))
        self.label_4.setText("")
        self.loading = QMovie("Loading.gif")
        self.label_4.setMovie(self.loading)
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")

        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.start_spin)

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

    def start_spin(self):
        self.label_4.setHidden(False)
        self.loading.start()
        self.threadpool = QtCore.QThreadPool()
        worker = Worker(self.download)
        self.threadpool.start(worker)

    def download(self):
        link = self.lineEdit.text()
        mode = "a" if self.radioButton.isChecked() else "v"
        Download(link, mode)
        self.lineEdit.setText("Done!")
        self.loading.stop()
        self.label_4.setHidden(True)


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
