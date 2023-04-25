import sys
from PyQt5.QtWidgets import QTabWidget, QDesktopWidget, QTableWidgetItem, QTableWidget, QApplication, QWidget, \
    QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QSizePolicy, QSpacerItem, QPlainTextEdit
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption

class ExcelConverter(QWidget):
    def __init__(self):
        super().__init__()

        # GUI 元素初始化
        self.setWindowTitle('Excel 轉換器')  # 設定視窗標題為 "Excel 轉換器"
        self.setFixedSize(1600, 960)  # 設定視窗大小固定為 1440x960 像素
        screen = QDesktopWidget().availableGeometry()  # 取得可用的螢幕區域
        self.move(screen.width() // 2 - int(self.width() / 2), 30)  # 將視窗移動到螢幕中央偏上方
        self.left_group = QGroupBox('庫存')  # 創建一個名為 "庫存" 的分組框
        self.left_table = QTableWidget()  # 創建一個 QTableWidget 類型的物件，用於顯示表格
        # self.left_table.setStyleSheet("QTableWidget { gridline-color: gray; }")  # 設定表格網格顏色為灰色
        self.left_label = QLabel('批號庫存')  # 創建一個名為 "批號庫存" 的標籤
        self.left_bot_table = QTableWidget()  # 創建一個 QTableWidget 類型的物件，用於顯示表格
        self.left_bot_label = QLabel('總庫存')  # 創建一個名為 "總庫存" 的標籤
        self.right_group = QGroupBox('轉換器')  # 創建一個名為 "轉換器" 的分組框
        self.input_label = QLabel('輸入文字')  # 創建一個名為 "輸入文字" 的標籤
        self.line_widget = QWidget()  # 創建一個 QWidget 類型的物件，用於顯示 QLineEdit 控制項
        # self.input_edit = QLineEdit(self.line_widget)  # 創建一個 QLineEdit 控制項，用於輸入文字
        self.input_edit = QPlainTextEdit(self.line_widget)
        self.input_edit.setLineWrapMode(True)
        # self.input_edit.setAlignment(Qt.AlignTop | Qt.AlignLeft)  # 設定輸入框文字對齊方式為上方和左側
        self.input_edit.setFixedHeight(300)  # 設定輸入框高度為 200 像素
        self.convert_button = QPushButton('轉換')  # 創建一個名為 "轉換" 的按鈕
        self.result_label = QLabel('轉換結果')  # 創建一個名為 "轉換結果" 的標籤
        self.result_textedit = QTableWidget()  # 創建一個 QTextEdit 類型的物件，用於顯示轉換結果
        self.update_button = QPushButton('報刀(更新分頁pd_lot_num)')  # 創建
        self.left_total_table = QTableWidget()
        self.ic_names = ["日期", "型號", "系統", "品名", "簡稱", "尺寸", "批號", "批號數量", "保存期限", "出廠日期",
                         "金額(成本價)", "種類", "部位", "醫院", "醫生", "病患", "病歷號", "業務", "器械", "補貨"]
        self.label_group = QGroupBox('選項')

        self.label_layout = QGridLayout()
        self.row_num = 5
        self.col_num = 4
        for i in range(self.row_num):
            for j in range(self.col_num):
                index = i * self.col_num + j
                if index >= len(self.ic_names):
                    break
                label = QLabel(self.ic_names[index])
                line_edit = QLineEdit()
                line_edit.setFixedWidth(80)
                self.label_layout.addWidget(label, i, j*2)
                self.label_layout.addWidget(line_edit, i, j*2+1)
            else:
                continue
            break
        self.label_group.setLayout(self.label_layout)
        # 佈局設定
        layout = QGridLayout()

        # 建立兩個分頁，並將其加入到 TabWidget 中
        tab_widget1 = QTabWidget()
        tab1 = self.left_table
        tab2 = self.left_bot_table
        tab_widget1.addTab(tab1, "即時批號庫存")
        tab_widget1.addTab(tab2, "報刀記錄")
        # 左邊布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(tab_widget1)
        left_layout.addWidget(self.left_bot_label)
        left_layout.addWidget(self.left_total_table)
        self.left_group.setLayout(left_layout)
        # 右邊布局 -- Line文字轉換 & 報刀
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.input_label)
        right_layout.addWidget(self.input_edit)
        right_layout.addWidget(self.label_group)
        right_layout.addWidget(self.convert_button)
        right_layout.addWidget(self.result_label)
        right_layout.addWidget(self.result_textedit)
        right_layout.addWidget(self.update_button)
        # 右邊布局 -- 進貨 & 轉倉

        self.right_group.setLayout(right_layout)
        self.right_group.setFixedWidth(720)
        layout.addWidget(self.left_group, 0, 0, 2, 1)
        layout.addWidget(self.right_group, 0, 1)
        self.setLayout(layout)
        self.convert_button.clicked.connect(self.convert_text)
        self.update_button.clicked.connect(self.update_left_table)
        self.update_button.clicked.connect(self.update_total_table)
        # 檔案讀取按鈕
        file_button = QPushButton('讀取 Excel 檔案')
        file_button.clicked.connect(self.load_excel_file)
        layout.addWidget(file_button, 2, 0)
        # 事件綁定

    def text_parse(self, p_text):
        text_array = p_text.split('\n')
        text_array = [t.split() for t in text_array]
        print(text_array)
        return text_array

    # Line 文字解析
    def convert_text(self):
        input_text = self.input_edit.toPlainText()
        text_array = self.text_parse(input_text)

        # TODO: 在這裡加入您的轉換邏輯

        # put convert text in table
        try:
            self.result_textedit.setRowCount(1)
            self.result_textedit.setColumnCount(1)
            self.result_textedit.setHorizontalHeaderLabels(['HI'])
            self.result_textedit.setItem(0, 0, QTableWidgetItem(str(input_text)))
        except Exception as E:
            print(E.args)

    def lot_converter(self, c_df):
        # group 批號數量 by 型號
        print(c_df['批號數量'])
        c_df['批號數量'] = c_df['批號數量'].astype('int')
        grouped_df = c_df.groupby(['型號', '品名'])['批號數量'].sum().reset_index()
        # 創建新的欄位作為pivot_table的columns
        columns = ['日期', '型號', '品名', '批號數量', '倉別']
        pivot_df = c_df[columns].pivot_table(index=['日期', '型號', '品名'], columns='倉別', values='批號數量',
                                             aggfunc='sum').reset_index()
        # 合併兩個dataframe
        result_df = pd.merge(grouped_df, pivot_df, on=(['型號', '品名']))
        new_col_name = result_df.columns
        stack_col_name = new_col_name[4:]
        agg_func = {
            '日期': 'first',
            '批號數量': 'first',
        }
        agg_func.update({col: 'sum' for col in stack_col_name})
        # 將NaN值替換為0
        result_df = result_df.fillna(0)
        result_df = result_df[new_col_name].groupby(['型號', '品名']).agg(agg_func).reset_index()
        result_df = result_df.applymap(lambda x: int(x) if isinstance(x, (int, float)) else x)
        # 將欄位名稱中的空格替換為底線
        result_df.columns = result_df.columns.str.replace(' ', '_')
        result_df.columns = result_df.columns.str.replace('批號數量', '總數量')

        return result_df

    def update_left_table(self):
        # append template
        apd_list = ['4月18日', 'A', 'A-AA', 'BBBB', 2, '器械盒A']
        apd_df = pd.DataFrame(apd_list)
        for i, (sheet_name, sheet_data) in enumerate(apd_df.items()):
            self.left_table.insertRow(i)
            for j, value in enumerate(sheet_data.values.ravel()):
                self.left_table.setItem(i, j, QTableWidgetItem(str(value)))
                self.left_table.resizeColumnsToContents()

    def table_to_dataframe(self, table_widget):
        # 創建一個空的 DataFrame
        df = pd.DataFrame()
        # 獲取表格的行數和列數
        row_count = table_widget.rowCount()
        column_count = table_widget.columnCount()
        # 遍歷表格的所有單元格，將其內容插入到 DataFrame 對應的位置上
        for row in range(row_count):
            for column in range(column_count):
                item = table_widget.item(row, column)
                if item is not None:
                    df.at[row, column] = item.text()

        df.columns = ['日期', '型號', '品名', '批號', '批號數量', '倉別', '保存期限',	'出廠日期', '金額(成本價)', '種類']
        return df

    def update_total_table(self):
        tt_df = self.table_to_dataframe(self.left_table)
        try:
            df_total = self.lot_converter(tt_df)
        except Exception as E:
            print(E.args)
        self.left_total_table.setRowCount(0)
        self.left_total_table.setColumnCount(df_total.shape[1])
        self.left_total_table.setHorizontalHeaderLabels(list(df_total.columns))
        for index, row in df_total.iterrows():
            self.left_total_table.insertRow(index)
            for col, value in enumerate(row):
                self.left_total_table.setItem(index, col, QTableWidgetItem(str(value)))
                self.left_total_table.resizeColumnsToContents()

    def load_excel_file(self, df):
        self.left_table.setRowCount(0)
        self.left_table.setColumnCount(df['pd_lot_num'].shape[1])
        self.left_table.setHorizontalHeaderLabels(list(df['pd_lot_num'].columns))
        for index, row in df['pd_lot_num'].iterrows():
            self.left_table.insertRow(index)
            for col, value in enumerate(row):
                self.left_table.setItem(index, col, QTableWidgetItem(str(value)))
                self.left_table.resizeColumnsToContents()
        self.update_total_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExcelConverter()
    load_df = pd.read_excel('stack_house.xlsx', sheet_name=['pd_lot_num', 'pd_total'])
    ex.load_excel_file(load_df)
    ex.show()
    sys.exit(app.exec_())

'''
4/24 員基 柯博維
Hook 左18四洞(2208180001)
3.5CS 14*1(2208290011)
3.5LS 14*1(2211010005)16*1(2211010006)
2.7LS 16*3(2208290024)
曹麗滿
器械：寄庫
補貨：公司
'''

'''
"日期": key in
"型號": key in / 對應簡稱
"系統": 下拉式-[一代,萬向,MINI]
"品名": 對應型號/簡稱
"簡稱": key in / 對應型號
"骨釘尺寸": key in
"批號": key in
"批號數量": key in
"有效期限": 對應批號
"出廠日期": 對應批號
"金額(成本價)": 對應型號/簡稱
"種類": 對應型號/簡稱
"部位": 對應型號/簡稱
"醫院": key in
"醫生": 下拉式選單
"病患": key in
"病歷號": key in
"業務" key in
"器械": key in
"補貨": key in
'''
