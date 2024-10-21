import os
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry
from lancedb.rerankers import RRFReranker

CURR_PATH = os.path.dirname(__file__)
WORK_PATH = os.path.abspath(os.path.dirname(CURR_PATH)).replace("\\", "/")

# 数据库
DB_URI = WORK_PATH + '/data/lancedb'
TABLE_NAME = "test_table"

db = lancedb.connect(DB_URI)
embedder = get_registry().get("sentence-transformers").create()
reranker = RRFReranker()

class Schema(LanceModel):
    text: str = embedder.SourceField()
    vector: Vector(embedder.ndims()) = embedder.VectorField()

# 判断表是否存在
def is_table_exist():
    if not os.path.exists(DB_URI):
        return False
    tables = db.table_names()
    if TABLE_NAME not in tables:
        return False
    return True

# 创建表
def create_table():
    tbl = db.create_table(TABLE_NAME, schema=Schema, mode="overwrite")
    return tbl

# 读取表
def read_table():
    if not is_table_exist():
        tbl = create_table()
    else:
        tbl = db.open_table(TABLE_NAME)
    return tbl

# 添加数据
def add_data():
    tbl = read_table()
    data = [
        {"text": "hello world"},
        {"text": "goodbye world"},
        {"text": "good morning"},
        {"text": "good night"},
        {"text": "good afternoon"},
        {"text": "welcome"},
        {"text": "with great power comes great responsibility"},
    ]
    tbl.add(data)
    tbl.create_fts_index("text", replace=True)

# 搜索数据
def search_data(query: str):
    tbl = read_table()
    result = tbl.search(query).select(["text"]).to_list()
    return result

def search_data_hybrid(query: str):
    tbl = read_table()
    result = tbl.search(query, query_type="hybrid").select(["text"]).to_list()
    return result

def search_rerank_data(query: str):
    tbl = read_table()
    result = tbl.search(query, query_type="hybrid").select(["text"]).rerank(reranker=reranker).to_list()
    return result

# 测试程序
def test():
    add_data()
    result = search_data("hello")
    rerank_result = search_rerank_data("hello")
    print("result: {}".format(result))
    print("rerank_result: {}".format(rerank_result))