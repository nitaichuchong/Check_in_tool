import base64
import random
import sqlite3
import sys
from datetime import datetime, timedelta

from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox

from UI.toolbox import Ui_Form
from config.settings import DATABASE_ROOT


class Toolbox_Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Toolbox_Window, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 在初始化 GUI 时就需要进行的操作
        self.con = sqlite3.connect(DATABASE_ROOT)
        self.cur = self.con.cursor()
        self.create_table()
        self.init_comboBox()
        # 初始化测试数据的时间范围，默认为当前日期到十天后
        self.ui.dateTimeEdit_start.setDateTime(datetime.now())
        self.ui.dateTimeEdit_end.setDateTime(datetime.now() + timedelta(days=10))

        self.init_slots()

        # 关闭软件时触发事件，关闭数据库连接
        QCoreApplication.instance().aboutToQuit.connect(self.on_about_to_quit)

    def init_slots(self):
        """绑定信号槽，点击按钮触发对应函数"""
        self.ui.pushButton_generate.clicked.connect(self.create_test_data)
        self.ui.pushButton_update.clicked.connect(self.read_and_format)
        self.ui.pushButton_delete.clicked.connect(self.delete_table)
        self.ui.dateTimeEdit_start.dateTimeChanged.connect(self.dateTimeEdit_start_check)
        self.ui.dateTimeEdit_end.dateTimeChanged.connect(self.dateTimeEdit_end_check)

    def create_table(self):
        """创建表"""
        sql = '''
        create table IF NOT EXISTS my_database 
                (id INTEGER PRIMARY KEY AUTOINCREMENT , 
                datatime TEXT NOT NULL );
                '''
        self.cur.execute(sql)
        self.con.commit()

    def create_test_data(self):
        """创建测试数据，生成的数据范围由控件决定
        :param
        """
        # 为了防止删除表后出现错误，先调用一次表创建
        self.create_table()

        '''先获取两个 dateTimeEdit 中的值，注意这里为 QDateTIme 对象
        也有自带的方法 toPyDateTime() 来转换为 DateTime 对象，如下：        
        date_start = self.ui.dateTimeEdit_start.dateTime().toPyDateTime()
        data_end = self.ui.dateTimeEdit_end.dateTime().toPyDateTime()
        但是想多用一下新方法试试'''
        date_start = self.ui.dateTimeEdit_start.dateTime()
        data_end = self.ui.dateTimeEdit_end.dateTime()

        # 设置 i 作为日期增加的天数
        i = 0
        while True:
            # addDays(i) 即可逐天处理，直至满足条件
            current_time = date_start.addDays(i)
            # 若当前时间的 date 已跟终止时间一致，说明满足退出循环的条件，结束生成
            if current_time.date() == data_end.date():
                break
            i += 1
            # 转换为符合格式要求的 DateTime 对象，QDateTime 对象没有合适的方法
            current_time = current_time.toPyDateTime().strftime('%Y-%m-%d %H:%M:%S')
            # base64 只接受 byte 类型，因此将数据转换为 utf-8 字节串后进行 base64 编码
            b64_data = base64.b64encode(current_time.encode('utf-8'))

            self.cur.execute("INSERT INTO my_database (datatime) VALUES (?);", (b64_data,))
            self.con.commit()

        QMessageBox.information(self, '操作提示', '已生成测试数据！去更新看看吧！')

    def read_and_format(self):
        """从表中读取数据并还原，更多注释请看 DatabaseHandler 中的正式版本"""
        # 每次更新前都先清空原先内容
        self.ui.textEdit.clear()
        con = sqlite3.connect(DATABASE_ROOT)
        cur = con.cursor()

        # 为了防止删除表后出现错误，先调用一次表创建
        self.create_table()

        sql = "SELECT datatime FROM my_database;"
        res = cur.execute(sql)
        original_data = res.fetchall()

        for time_data in original_data:
            decoded_bytes = base64.b64decode(time_data[0]).decode('utf-8')

            self.ui.textEdit.append(decoded_bytes)

        QMessageBox.information(self, '操作提示', '已更新完毕！')

        # 若 textEdit 中为空（或只有 空格/空行 ），则表示当前表中没有数据
        if not self.ui.textEdit.toPlainText().strip():
            QMessageBox.information(self, '操作提示', '当前表中还没有任何数据，先去生成吧')

    def init_comboBox(self):
        """初始化 comboBox，将数据库中存在的表添加到 comboBox 选项中"""
        # sqlite_master 和 sqlite_sequence 都是 sqlite 自行创建的表，因此应当忽略
        # 从 sqlite_master 进行 SELECT 操作本身就忽略掉了 sqlite_master 表
        sql = '''
        SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';
        '''
        res = self.cur.execute(sql)
        # 列表生成式
        tables = [row[0] for row in res.fetchall()]
        for table in tables:
            self.ui.comboBox.addItem(table)

    def dateTimeEdit_start_check(self):
        """检查起始时间是否符合要求"""
        if self.ui.dateTimeEdit_start.date() >= self.ui.dateTimeEdit_end.date():
            QMessageBox.information(self, '时间异常！', '你的起始时间已经 >= 终止时间了，已重置为默认值')
            self.ui.dateTimeEdit_start.setDate(datetime.now().date())

    def dateTimeEdit_end_check(self):
        """检查终止时间是否符合要求"""
        if self.ui.dateTimeEdit_end.date() <= self.ui.dateTimeEdit_start.date():
            QMessageBox.information(self, '时间异常！', '你的终止时间已经 <= 起始时间了，已重置为默认值')
            self.ui.dateTimeEdit_end.setDate(datetime.now().date() + timedelta(days=10))

    def delete_table(self):
        """删除指定表"""
        # 表名只能从控件 comboBox 的选项中选择
        table_name = self.ui.comboBox.currentText()
        self.cur.execute(f"drop table if exists {table_name};")
        self.con.commit()
        # 完成一次删除后要更新 comboBox 的选项
        self.init_comboBox()

        QMessageBox.information(self, '操作提示', '你已删除指定表！（但实际上等同清空表）')

    def on_about_to_quit(self):
        self.con.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Toolbox_Window()
    ui.show()
    sys.exit(app.exec_())
