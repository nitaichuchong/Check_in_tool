import os


# 抄的 Django 的路径用法
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_ROOT = os.path.join(BASE_DIR, "database.db")


# 为了先检查路径是否正确
def check_dir():
    print(BASE_DIR)
    print(DATABASE_ROOT)
