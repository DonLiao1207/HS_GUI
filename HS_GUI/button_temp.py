from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, QWidget

class MyLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 200)
        self.label = QLabel("我的QLabel", self)
        self.btn1 = QPushButton("報刀", self)
        self.btn2 = QPushButton("進貨", self)
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["型號1", "型號2", "型號3"])
        self.warehouse1 = QComboBox(self)
        self.warehouse1.addItems(["倉庫A", "倉庫B", "倉庫C", "倉庫D", "倉庫E"])
        self.warehouse2 = QComboBox(self)
        self.warehouse2.addItems(["倉庫A", "倉庫B", "倉庫C", "倉庫D", "倉庫E"])
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.btn1)
        hbox1.addWidget(self.btn2)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.comboBox)
        hbox2.addWidget(self.warehouse1)
        hbox2.addWidget(self.warehouse2)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

if __name__ == '__main__':
    app = QApplication([])
    window = MyLabel()
    window.show()
    app.exec_()
