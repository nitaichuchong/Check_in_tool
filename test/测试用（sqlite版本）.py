import base64
import random
import sqlite3
from datetime import datetime, timedelta

from config.settings import DATABASE_ROOT

con = sqlite3.connect(DATABASE_ROOT)
cur = con.cursor()

sql = '''
create table IF NOT EXISTS my_database 
(id INTEGER PRIMARY KEY AUTOINCREMENT , datatime TEXT NOT NULL );
'''
cur.execute(sql)


def create():
    """创建测试数据"""
    for i in range(5):
        rand_num = random.randint(-5, 10)  # 生成随机数
        # current_time = datetime.now().date()
        current_time = datetime.now()  # 获取系统时间
        # 将系统时间 + timedelta（随机数）作为随机的时间
        # timedelta 默认参数为天数，即 rand_num 表示随机天数的范围
        test_data = current_time + timedelta(rand_num)
        test_data = test_data.strftime('%Y-%m-%d %H:%M:%S')
        # base64 只接受 byte 类型，因此将数据转换为 utf-8 字节串后进行 base64 编码
        b64_data = base64.b64encode(test_data.encode('utf-8'))

        cur.execute("INSERT INTO my_database (datatime) VALUES (?);", (b64_data,))


def select():
    """读取表中的所有数据，未解码"""
    res = cur.execute("select datatime from my_database;")
    rows = res.fetchall()
    for r in rows:
        print(r)

def read_and_format():
    """从表中读取数据并解码，更多注释请看 DatabaseHandler 中的正式版本"""
    time_list = []
    message_list = []

    sql = "SELECT datatime FROM my_database;"
    res = cur.execute(sql)
    original_data = res.fetchall()

    print(original_data)

    for time_data in original_data:
        print(time_data[0])
        decoded_bytes = base64.b64decode(time_data[0]).decode('utf-8')

        time_list.append(decoded_bytes)
        message_list.append("已于 " + decoded_bytes + " 完成打卡")

    print(time_list)
    print(message_list)

def delete_table():
    """删除指定表"""
    cur.execute("drop table if exists my_database;")


if __name__ == '__main__':
    create()
    # select()
    # read_and_format()
    # delete_table()
    con.commit()
    con.close()
