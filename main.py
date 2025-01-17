import datetime
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QCoreApplication, Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QMessageBox

from DatabaseHandler import con, insert_database
from UI.main import Ui_Form
from showCalender import Calender_Window
from testTool.Toolbox import Toolbox_Window
from utils.calender_check import sorted_data
from utils.main_check import check_first_time, check_textedit, check_button


class UI_Logic_Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(UI_Logic_Window, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        # 绑定信号槽
        self.init_slots()

        # 检查是否为第一次使用该软件，并作相应处理
        check_first_time()

        # 初始化一个 QT 的定时器并绑定到 update_time 函数中，使其每秒更新
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 1000 即为 1 秒，若需要 1 分钟更新一次可设置 60 * 1000，其它同理
        self.update_time()

        # 打开软件时更新 textEdit 的内容并检查 button 是否可用
        check_textedit(self, "init")
        check_button(self)

        # 两个子窗口的初始化定义
        self.test_form = None
        self.calender_form = None

        # 关闭软件时触发事件，关闭数据库连接
        QCoreApplication.instance().aboutToQuit.connect(self.on_about_to_quit)

    def init_slots(self):
        """连接信号槽，点击按钮触发对应事件"""
        self.ui.button_clock_in.clicked.connect(self.clock_in)
        self.ui.pushButton_calendar.clicked.connect(self.open_calendar)
        self.ui.pushButton_test.clicked.connect(self.open_test)
        self.ui.commandLinkButton.clicked.connect(self.open_website)

    def clock_in(self):
        """
        current_time：从系统时间中获取并格式化为 2024-06-03 15：00：00 的样式
        调用 insert_database 完成数据的写入，每次点击按钮都即时将数据写入数据库，
        同时更新textEdit 和 button 的状态
        """
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_database(current_time)
        check_textedit(self, "update")
        check_button(self)
        # 为了防止点击过快产生的奇怪bug，设置一个 0.2 秒的停顿
        time.sleep(0.2)

    def update_time(self):
        """
        更新为当前系统时间，并显示在 label_time 中
        """
        local_time = datetime.datetime.now()
        formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S')
        self.ui.label_time.setText(formatted_time)

    def open_calendar(self):
        """打开日历功能，用未定义的 Form 继承已在别处写好的窗口，
        通过设置窗口的模态性（modal）来实现在子窗口打开时，
        用户不能与主窗口或其他窗口交互的效果"""
        # 没有数据时打开日历会抛异常，用 try except 进行处理
        try:
            self.calender_form = Calender_Window(self)
            # 从主窗口打开日历应当每次都先清除缓存，否则日历不会更改，影响配合测试工具箱使用时的结果
            sorted_data.cache_clear()
            self.calender_form.setWindowModality(Qt.ApplicationModal)  # 设置为应用模态
            self.calender_form.show()
        except ValueError:
            QMessageBox.information(self, '操作提示', '没有数据怎么画日历，打开不了，请先来点数据')

    def open_test(self):
        """打开测试工具箱功能，参考 open_calendar 的逻辑"""
        self.test_form = Toolbox_Window(self)
        self.test_form.setWindowModality(Qt.ApplicationModal)  # 设置为应用模态
        self.test_form.finished.connect(self.close_test)  # finished 信号是 QDialog 特有的
        self.test_form.show()

    def close_test(self):
        """关闭测试工具箱时应执行的操作"""
        # 由于在工具箱内可能进行了新数据生成和删除表，因此需要更新打卡状况
        check_textedit(self, "init")

    @staticmethod
    def open_website():
        """打开本项目的 GitHub 地址"""
        url = QUrl("https://github.com/nitaichuchong/Check_in_tool")
        if not QDesktopServices.openUrl(url):
            print("Failed to open URL:", url.toString())

    @staticmethod
    def on_about_to_quit():
        con.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = UI_Logic_Window()
    ui.show()
    sys.exit(app.exec_())
