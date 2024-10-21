import lancedb
import os

CURR_PATH = os.path.dirname(__file__)
WORK_PATH = os.path.abspath(os.path.dirname(CURR_PATH)).replace("\\", "/")

# 数据库
DB_URI = WORK_PATH + '/data/test_db'


# 连接数据库
def connect(uri):
    is_db_exist = os.path.exists(uri)
    if not is_db_exist:
        os.makedirs(uri)
    return lancedb.connect(uri)

# 测试
def test():
    db = connect(DB_URI)
    print(db)
