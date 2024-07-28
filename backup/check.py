import os
from datetime import datetime, date, timedelta


def check_first_time(self):
    '''
    检查是否第一次使用软件的函数，若为第一次使用则创建数据库，并写入空字符
    '''
    if not os.path.exists('database'):
        with open('database', 'w') as f:
            f.write('')
            return True
    return False


def check_textEdit(self, arg):
    '''
    :param arg: 传过来表示应执行的动作的字符串，有 init 和 update 两种
    更新 textEdit 和 label_clocked 的内容
    '''
    # 从 read_database_and_format 获取 time_list 和 message_list_clear 两个列表
    time_list, message_list_clear = read_database_and_format()
    # arg == "init" 时为打开软件时的初始化，将所有内容以遍历方式追加到 textEdit 中
    # arg == "update" 时为每次点击按钮时追加的内容，因此只需追加最新的 message_list_clear[-1]
    if arg == "init":
        for r in message_list_clear:
            self.ui.textEdit.append(r)
    elif arg == "update":
        self.ui.textEdit.append(message_list_clear[-1])
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
        self.ui.label_clocked.setText(f"你已戒色共{len(time_list)}天！当前连续戒色第{i + 1}天！")
    # 根据数据库的数据量决定如何更新 label_clocked
    if len(time_list) > 1:
        check_continuous(self, time_list)
    elif len(time_list) == 1:
        self.ui.label_clocked.setText(f"你已戒色共{len(time_list)}天！当前连续戒色第{1}天！")
    elif len(time_list) == 0:
        self.ui.label_clocked.setText(f"戒色第0天！")


def check_button(self):
    '''
    检查按钮是否可用，即今日是否已签到
    '''
    # 获取两个列表
    time_list, message_list_clear = read_database_and_format()
    # 若数据量不为 0，即并非第一次使用时，通过比较系统时间和最新的数据，判断是否为同一天重复打卡
    # 若检查为重复打卡则将 button 设置为 disabled 并提示”今日已打卡“
    if len(time_list) != 0:
        if str(date.today()) == time_list[-1]:
            self.ui.button_clock_in.setDisabled(True)
            self.ui.button_clock_in.setText("今日已打卡")


def read_database_and_format():
    '''
    因需要重复调用而单独模块化的函数，从数据库中读取数据并进行处理，由于存储时使用了
    16 进制的编码方式，因此读取时也需要从 16 进制还原为 utf-8
    :return: time_list, message_list_clear
             time_list 为数据全部处理过后的日期列表，只包含类似 2024-06-03 的信息
             message_list_clear 为从数据库中读取并经过处理的新列表，包含完整的信息
    '''
    time_list = []

    with open('database', 'r') as f:
        hex_data = f.read()
    # 将从数据库中读取的内容从 hex 转化为 byte，然后还原为 utf-8
    orginal_data = bytes.fromhex(hex_data).decode('utf-8')
    # 由于 orginal_data 还原后的数据是一整个长串，因此使用 \n 分割为列表
    message_list = orginal_data.split('\n')
    # 使用列表推导式，将 message_list 中不为 ”“ 的内容更新进新的列表，即 clear 的含义
    # 原因是如果不对 ”“ 进行去除，会由于创建文件时自动写入的 ”“ 而需要大量额外的处理
    message_list_clear = [x for x in message_list if x and x != ""]
    # 遍历 message_list_clear，并通过对空格的分割获取其中仅有日期的信息，追加进 time_list
    for r in message_list_clear:
        date_message = r.split()[1]
        time_list.append(date_message)

    return time_list, message_list_clear
