import os.path
from datetime import datetime, date, timedelta

from DatabaseHandler import create_database, read_and_format
from config.settings import DATABASE_ROOT


def check_first_time():
    """
    检查是否第一次使用软件的函数，若为第一次使用则创建数据库
    """
    if not os.path.exists(DATABASE_ROOT):
        create_database()


def check_textedit(self, arg):
    """
    :param arg: 传过来表示应执行的动作的字符串，有 init 和 update 两种
    更新 textEdit 和 label_clocked 的内容
    """

    # 从 read_and_format 获取 time_list 和 message_list 两个列表
    time_list, message_list = read_and_format()
    # arg == "init" 时为打开软件时的初始化，将所有内容以遍历方式追加到 textEdit 中
    # arg == "update" 时为每次点击按钮时追加的内容，因此只需追加最新的 message_list[-1]
    if arg == "init":
        # 先做一次清理
        self.ui.textEdit.clear()
        for r in message_list:
            self.ui.textEdit.append(r)
    elif arg == "update":
        self.ui.textEdit.append(message_list[-1])

    # 函数内定义的方法，用来判断日期的连续，从列表的最后往前计算，若有一处不连续则停止计数并退出循环
    def check_continuous(self, time_list):
        i = 0
        # 由于每次都会和前一位进行比较，因此长度 -1 就能保证遍历完毕所有数完成计算，否则会数组越界
        for i in range(len(time_list) - 1):
            # 转换为 datetime.date 对象，利用其计算方式和 timedelta 相比较得出结果
            date_str1 = datetime.strptime(time_list[-(i + 1)], "%Y-%m-%d").date()
            date_str2 = datetime.strptime(time_list[-(i + 2)], "%Y-%m-%d").date()
            if (date_str1 - date_str2) == timedelta(days=1):
                i += 1
            else:
                break
        self.ui.label_clocked.setText(f"你已戒色共{len(time_list)}天！\n当前连续戒色第{i + 1}天！")

    # 根据数据库的数据量决定如何更新 label_clocked
    if len(time_list) > 1:
        check_continuous(self, time_list)
    elif len(time_list) == 1:
        self.ui.label_clocked.setText(f"你已戒色共{len(time_list)}天！当前连续戒色第{1}天！")
    elif len(time_list) == 0:
        self.ui.label_clocked.setText(f"戒色第0天！")


def check_button(self):
    """
    检查按钮是否可用，即今日是否已签到
    """
    # 获取日期列表，并忽略另一返回值列表
    time_list, _ = read_and_format()
    # 若数据量不为 0，即并非第一次使用时，通过比较系统时间是否存在于已读取数据中，判断是否为重复打卡
    # 若检查为重复打卡则将 button 设置为 disabled 并提示”今日已打卡“
    if len(time_list) != 0:
        if str(date.today()) in time_list:
            self.ui.button_clock_in.setDisabled(True)
            self.ui.button_clock_in.setText("今日已打卡")
