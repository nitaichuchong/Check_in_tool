import random
from datetime import datetime, timedelta


for i in range(20):
    rand_num = random.randint(-1, 1)  # 生成随机数
    # current_time = datetime.now().date()
    current_time = datetime.now() # 获取系统时间
    # 将系统时间 + timedelta（随机数）作为随机的时间
    # timedelta 默认参数为天数，即 rand_num 表示随机天数的范围
    test_date = current_time + timedelta(rand_num)
    test_date = test_date.strftime('%Y-%m-%d %H:%M:%S')
    message = "已于 " + str(test_date) + " 完成打卡\n"
    # 将数据进行 16 进制编码
    hex_message = message.encode().hex()
    # 在根目录下创建测试数据库使用 ../
    with open('../database', 'a') as f:
        f.write(hex_message)
    # 测试该 16 进制还原为 utf-8 的方法是否可行
    with open('../database', 'r') as f:
        asd = f.read()
        asd2 = bytes.fromhex(asd).decode('utf-8')

