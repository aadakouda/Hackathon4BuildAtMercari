import os
import logging
import pathlib
import shutil
import json
import sqlite3
import hashlib
from fastapi import File, UploadFile, Body
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.DEBUG
images = pathlib.Path("image")
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
api_url = os.environ.get('API_URL', 'http://localhost:9000')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

sqlite_path = str(pathlib.Path(os.path.dirname(__file__)).parent.resolve() / "db" / "hackathon.sqlite3")


@app.post('/login')
def login(user_id: str = Body(...), password: str = Body(...)):
    """
    ログインAPI
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_uuid " \
        "FROM users " \
        "WHERE user_id = ? " \
        "AND password = ? ", 
        (user_id, password)
    )
    result = cursor.fetchall()
    if len(result) == 0:
        raise HTTPException(status_code=404, detail='User not Found')
    return result[0]

@app.get('/items')
def get_items_list():
    """
    商品一覧API
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = '''SELECT items.item_uuid, items.item_name, categories.category_name AS category_name, items.price, items.on_sale, items.image, items.exchange_items 
        FROM items 
        INNER JOIN categories ON items.category_id = categories.category_id 
        WHERE items.is_public=1'''
    cursor.execute(sql)
    items_dic = {}
    items_dic["items"] = cursor.fetchall()
    conn.close()
    return items_dic


@app.get('/items/{item_uuid}')  ###is_publicを返すかどうか，今は返してます
def get_item(item_uuid: str):
    """
    商品詳細API
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = '''SELECT items.item_uuid, items.item_name, categories.category_name AS category_name, items.is_public, items.price, items.on_sale, items.image, items.exchange_items, items.user_uuid
        FROM items
        INNER JOIN categories ON items.category_id = categories.category_id
        WHERE items.item_uuid=?'''
    cursor.execute(sql, (item_uuid,))
    item_dic = cursor.fetchall()[0]
    conn.close()
    return item_dic


@app.get('/user_items/{user_uuid}')  ###is_public，user_uuid，exchange_items以外を返してます．一応on_sale=1という値は返します．
def get_user_items_list(user_uuid: str):
    """
    出品一覧API
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = '''SELECT items.item_uuid, items.item_name, categories.category_name AS category_name, items.is_public, items.price, items.on_sale, items.image, items.exchange_items
        FROM items 
        INNER JOIN categories ON items.category_id = categories.category_id 
        WHERE items.user_uuid =?'''
    cursor.execute(sql, (user_uuid,))
    items_dic = {}
    items_dic["items"] = cursor.fetchall()
    conn.close()
    return items_dic
