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


class UI_Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UI_Window, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 在初始化 GUI 时就需要进行的操作
        self.con = sqlite3.connect(DATABASE_ROOT)
        self.cur = self.con.cursor()
        self.create_table()
        self.init_comboBox()

        self.init_slots()

        # 关闭软件时触发事件，关闭数据库连接
        QCoreApplication.instance().aboutToQuit.connect(self.on_about_to_quit)

    def init_slots(self):
        """绑定信号槽，点击按钮触发对应函数"""
        self.ui.pushButton_generate.clicked.connect(self.create_test_data)
        self.ui.pushButton_update.clicked.connect(self.read_and_format)
        self.ui.pushButton_delete.clicked.connect(self.delete_table)

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
        """创建测试数据，生成的数据量和数据范围都由控件的数字决定
        :param
            data_size：要生成的数据量
            left：随机数范围的下限，在此表示最多往前多少天
            right：随机数范围的上限，在此表示最多往后多少天
        """
        # 为了防止删除表后出现错误，先调用一次表创建
        self.create_table()

        # 用 or 给一个默认值，防止空值导致的异常
        data_size = int(self.ui.lineEdit_data_size.text()) or 10
        left = int(self.ui.spinBox_left.text()) or -2
        right = int(self.ui.spinBox_right.text()) or -2

        for i in range(data_size):
            rand_num = random.randint(left, right)  # 生成随机数
            # current_time = datetime.now().date()
            current_time = datetime.now()  # 获取系统时间
            # 将系统时间 + timedelta（随机数）作为随机的时间
            # timedelta 默认参数为天数，即 rand_num 表示随机天数的范围
            test_data = current_time + timedelta(rand_num)
            test_data = test_data.strftime('%Y-%m-%d %H:%M:%S')
            # base64 只接受 byte 类型，因此将数据转换为 utf-8 字节串后进行 base64 编码
            b64_data = base64.b64encode(test_data.encode('utf-8'))

            self.cur.execute("INSERT INTO my_database (datatime) VALUES (?);", (b64_data,))
            self.con.commit()

        QMessageBox.information(self, '操作提示', '已生成测试数据！去更新看看吧！')

    def read_and_format(self):
        """从表中读取数据并还原，更多注释请看 DatabaseHandler 中的正式版本"""
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
            self.ui.textEdit.append("已于 " + decoded_bytes + " 完成打卡")

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
    ui = UI_Window()
    ui.show()
    sys.exit(app.exec_())
