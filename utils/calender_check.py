import calendar
from datetime import datetime, timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem

from DatabaseHandler import read_and_format


def init_comboBox_year_and_month(self):
    """调用函数获取数据，根据数据更新 comboBox 选项"""
    years_sorted, month_sorted = sorted_data()
    for year in years_sorted:
        self.ui.comboBox_year.addItem(year)
    for month in month_sorted:
        self.ui.comboBox_month.addItem(month)


def button_enable_check(self):
    """对于月份往前以及月份往后按钮的可用性检查"""
    current_month = get_current_month(self)
    years_sorted, month_sorted = sorted_data()
    '''
    若日历中当前月份不是所有数据中最早的（即最小 min)，那么就设置往前的按钮可用,
    若日历中当前月份不是所有数据中最晚的（即最大 max)，那么就设置往后的按钮可用,
    反之，若等于最早或最晚，对应按钮更改为不可用，上述判定皆包含年份。
    需要注意，必须进行 int 强制转换，否则举例而言， min(years_sorted) 的类型
    为 str，而 curren_time.year 为 int，两者无法正常进行关系运算。
    '''
    if (current_month.year != int(min(years_sorted))) and (current_month.month != int(min(month_sorted))):
        self.ui.pushButton_last_month.setEnabled(True)
    if (current_month.year != int(max(years_sorted))) and (current_month.month != int(max(month_sorted))):
        self.ui.pushButton_next_month.setEnabled(True)
    if (current_month.year == int(min(years_sorted))) and (current_month.month == int(min(month_sorted))):
        self.ui.pushButton_last_month.setDisabled(True)
    if (current_month.year == int(min(years_sorted))) and (current_month.month == int(min(month_sorted))):
        self.ui.pushButton_next_month.setDisabled(True)


def sorted_data():
    """从数据库中读取，然后转换成从小到大排序的年和月列表并返回"""
    time_list, _ = read_and_format()
    # 在生成式中使用 split 提取年份，并转换为集合去重，再用 sorted 排序
    # 提取月份同理
    years_sorted = sorted({year.split('-')[0] for year in time_list})
    month_sorted = sorted({month.split('-')[1] for month in time_list})

    return years_sorted, month_sorted


def get_current_month(self):
    """获取当前下拉框所表示的年和月
    :return curren_month：包含当前年月的有效信息，以及被 datetime 自动补全的部分
                          利用这个自动补全的特性，可以直接得到本月的的一天"""
    curren_month = self.ui.comboBox_year.currentText() + self.ui.comboBox_month.currentText()
    curren_month = datetime.strptime(curren_month, '%Y%m')

    return curren_month


def calendar_for_current_month(self):
    """绘制当前所示月份的日历"""
    # 7 列表示周一到周日，6 行表示一个月最多需要 6 行日历
    self.ui.tableWidget.setColumnCount(7)
    self.ui.tableWidget.setRowCount(6)
    # 设置表头
    self.ui.tableWidget.setHorizontalHeaderLabels(['Mon', 'Tue', 'Wed', 'Thu',
                                                   'Fri', 'Sat', 'Sun'])

    current_month = get_current_month(self)
    time_list, _ = read_and_format()

    '''使用calendar模块获取月份的天数和第一天是周几，calendar.monthrange(year, month) 返回一个元组，
    第一个元素是第一天是周几（0代表星期一，6代表星期日），第二个元素是该月有多少天'''
    start_weekday, total_days = calendar.monthrange(current_month.year, current_month.month)
    # 默认设置从第一行开始，也就是0，而列的开始则根据本月的第一天是周几
    row = 0
    col = start_weekday
    '''前面确定本月第一天是周几，共多少天后。受迭代思想的启发，每个月的日历只需确定第一天的绘制位置，
    然后通过条件控制行和列（row，col）逐格绘制，一直持续到本月日历的最后一天，这样就不需要考虑一些很复杂
    的日期绘制逻辑，只要专注于表格中每个格子是否满足特定条件即可'''
    for i in range(total_days):
        # 因 i 的值从 0 开始，那么借用 timedelta 对象就能从本月第一天一直往后推导至最后一天
        # current_date 会自动补全为本月第一天的 datetime 对象
        current_date = current_month + timedelta(days=i)
        # 设置表格内容格式，并默认每个格子都是禁用不可选的
        item = QTableWidgetItem(current_date.strftime("%Y-%m-%d"))
        item.setFlags(Qt.NoItemFlags)
        # 根据对应格子是否能匹配上数据库中的数据，决定表格的差异
        if current_date.strftime("%Y-%m-%d") not in time_list:
            item.setBackground(QColor(200, 200, 200))  # 不匹配则设置背景色为灰色
        else:
            item.setBackground(QColor(255, 255, 255))  # 匹配则设置背景色为白色
            item = QTableWidgetItem(item.text() + "✔")  # 匹配还会加个✔

        self.ui.tableWidget.setItem(row, col, item)
        # 行列的控制逻辑，若列的已绘制数为 7 ，则认为当前所在行的一周已绘制完毕，到下一行重新绘制
        col += 1
        if col == 7:
            row += 1
            col = 0


def calendar_change(self, args):
    """控制日历重新绘制的方式，其中若是因为按钮而需要重新绘制，
    则做一些特殊处理，若是因为下拉框而重新绘制，则可以省略一些处理"""
    if args == "button_last":
        month_change_last(self)
    elif args == "button_next":
        month_change_next(self)
    # 每次重新绘制日历，即每次点下按钮或下拉框时，都应再次检查按钮可用性，然后进行绘制
    button_enable_check(self)
    calendar_for_current_month(self)

def month_change_last(self):
    """月份往前按钮的特殊处理，其中分为三部分：月份为 1，往前的话还需要考虑年的更改；
    月份 < 10，进行完计算后还需要在前面添 0 以符合格式要求；
    剩下情况只需处理正常月份往前"""
    month = int(self.ui.comboBox_month.currentText())
    if month == 1:
        month = 12
        year = int(self.ui.comboBox_year.currentText())
        year -= 1
        # 通过 findText 查找对应的 index，以方便修改
        index = self.ui.comboBox_year.findText(year)
        # 若 ！= -1，则表示能找到，那么就将目前 index 变更为目标 index 即可满足
        if index != -1:
            self.ui.comboBox_year.setCurrentIndex(index)

    elif month < 10:
        month -= 1
        month = '0' + str(month)

    else:
        month -= 1
    # 上面是年，这个是月，都是同理
    index = self.ui.comboBox_month.findText(month)
    if index != -1:
        self.ui.comboBox_year.setCurrentIndex(index)


def month_change_next(self):
    """与月份往前的处理如出一辙，仅是一点小修改"""
    month = int(self.ui.comboBox_month.currentText())
    if month == 12:
        month = 1
        year = int(self.ui.comboBox_year.currentText())
        year += 1

        index = self.ui.comboBox_year.findText(year)
        if index != -1:
            self.ui.comboBox_year.setCurrentIndex(index)

    elif month < 9:
        month += 1
        month = '0' + str(month)

    else:
        month += 1

    index = self.ui.comboBox_month.findText(month)
    if index != -1:
        self.ui.comboBox_year.setCurrentIndex(index)
