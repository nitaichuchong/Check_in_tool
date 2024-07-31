import sys

from PyQt5 import QtWidgets
from UI.calendar import Ui_Form
from utils.calender_check import init_comboBox_year_and_month, button_enable_check, calendar_for_current_month, \
    calendar_change, check_open


class Calender_Window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Calender_Window, self).__init__(parent)
        # 先检查是否能正常打开日历，不能则直接抛出异常阻止
        flag = check_open()
        if not flag:
            raise ValueError("没有数据打开不了日历")

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # 必须先初始化的一些功能，具体说明请看对应函数的注释
        init_comboBox_year_and_month(self)
        button_enable_check(self)
        calendar_for_current_month(self)
        self.init_slots()

    def init_slots(self):
        """连接日历上方四个按钮的信号槽，然后再具体通过函数实现 clicked 信号的处理"""
        '''这里 lambda 被应用为一个包装器，它不接受任何参数，因为 clicked 信号本身也无法传递参数，
        但是在被调用时会将需要传递参数的函数包装为一个整体，从而绕开无法传递参数的限制'''
        self.ui.pushButton_last_month.clicked.connect(lambda: calendar_change(self, "button_last"))
        self.ui.pushButton_next_month.clicked.connect(lambda: calendar_change(self, "button_next"))
        self.ui.comboBox_year.currentTextChanged.connect(lambda: calendar_change(self, "comboBox_year"))
        self.ui.comboBox_month.currentTextChanged.connect(lambda: calendar_change(self, "comboBox_month"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Calender_Window()
    ui.show()
    sys.exit(app.exec_())
