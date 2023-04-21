from PyQt5.QtWidgets import QApplication, QComboBox, QLabel, QVBoxLayout, QWidget


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 設置下拉式選單和 QLabel
        self.combobox = QComboBox()
        self.label = QLabel()

        # 將下拉式選單和 QLabel 添加到 QVBoxLayout 中
        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.label)

        # 設置 QWidget 的佈局
        self.setLayout(layout)

        # 設置下拉式選單選擇變更事件的處理程序
        self.combobox.currentIndexChanged.connect(self.on_combobox_index_changed)

        # 模擬從{型號:品名}對應關係字典中取得對應品名
        self.model_to_name = {"A-AA": "品名1", "B-BB": "品名2", "C-CC": "品名3"}

        # 將型號添加到下拉式選單中
        self.combobox.addItems(self.model_to_name.keys())

    def on_combobox_index_changed(self, index):
        # 根據選擇的型號更新對應的品名
        model = self.combobox.currentText()
        name = self.model_to_name.get(model, "")
        self.label.setText(name)


if __name__ == "__main__":
    app = QApplication([])
    widget = MyWidget()
    widget.show()
    app.exec_()
