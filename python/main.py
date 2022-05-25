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
def login(user_uuid: str = Body(...), password: str = Body(...)):
    """
    ログインAPI
    """
    # passは消してよし
    #pass


@app.get('/items')
def get_items_list():
    """
    商品一覧API
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = '''SELECT items.item_uuid, items.item_name, categories.category_name AS categories, items.price, items.on_sale, items.image, items.exchange_items 
        FROM items 
        INNER JOIN categories ON items.category_id = categories.category_id 
        WHERE items.is_public=?'''
    cursor.execute(sql, (1,))
    items_dic = {}
    items_dic["items"] = cursor.fetchall()
    conn.close()
    return items_dic


@app.get('/items/{item_uuid}')
def get_item(item_uuid: str):
    """
    商品詳細API
    """
    #pass


@app.get('/user_items/{user_uuid}')
def get_user_items_list(user_uuid: str):
    """
    出品一覧API
    """
    #pass