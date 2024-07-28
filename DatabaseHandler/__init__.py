import base64
import sqlite3

from config.settings import DATABASE_ROOT

con = sqlite3.connect(DATABASE_ROOT)
cur = con.cursor()


def create_database():
    """
    如果不存在所需表，则创建该表
    :return: None
    """
    sql = '''
        CREATE TABLE IF NOT EXISTS my_database
        (id INTEGER PRIMARY KEY AUTOINCREMENT ,
        datatime TEXT NOT NULL );
    '''
    cur.execute(sql)
    con.commit()


def read_and_format():
    """
    从数据库中读取 datatime ，因数据库中使用 base64 编码存储，所以读取时需要解码
    :return:
        time_list: 只有 年-月-日 信息的列表
        message_list：包含 年-月-日 时-分-秒 信息，且在前后添加提示供打卡提示用的列表
    """
    time_list = []
    message_list = []

    sql = "SELECT datatime FROM my_database;"
    res = cur.execute(sql)
    original_data = res.fetchall()

    for time_data in original_data:
        # 将从数据库中读取的内容从 base64 解码还原为 utf-8
        decoded_bytes = base64.b64decode(time_data[0]).decode('utf-8')
        # 解码后的数据含有 年-月-日 时-分-秒，但我们的 time_list 只需要日期信息，因此使用 split 分割
        time_list.append(decoded_bytes.split()[0])
        # 前后添加完整提示
        message_list.append("已于 " + decoded_bytes + " 完成打卡")

    return time_list, message_list


def insert_database(time_data):
    """
    标准的数据库插入操作，一次仅插入一行，插入时将时间数据进行 base64 编码
    :param time_data: 传入的时间信息，格式为 %Y-%m-%d %H:%M:%S
    :return: None
    """
    b64_data = base64.b64encode(time_data.encode('utf-8'))

    cur.execute("INSERT INTO my_database (datatime) VALUES (?);", (b64_data,))
    con.commit()


