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


class Status(str, Enum):
    APPLY = 'apply'
    ACCEPT = 'accept'
    REJECT = 'reject'
    PROPOSAL = 'proposal'


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


@app.get('/user_items/')
def get_candidate_items_list(user_uuid: str, category_name: str = None):
    """
    物々交換候補商品一覧API
    """
    pass


@app.get('/barter/status/{current_status}')
def get_status_list(current_status: Status):
    """
    ステータス一覧API
    """
    pass


@app.get('/barter_trade/{item_uuid}')
def get_barter_trade_list(item_uuid: str):
    """
    物々交換取引一覧API
    """
    pass


@app.get('/barter_trade/')
def get_barter_trade_detail(item_uuid: str, buyer_uuid: str):
    """
    物々交換取引詳細API
    """
    pass


@app.post('/barter')
def berter(
    next_status: Status = Form(...),
    item_uuid: str = Form(...),
    candidate_item_uuid: str = Form(...),
    buyer_uuid: str = Form(...)):
    """
    物々交換API
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # 最新の履歴取得
    cursor.execute(
        "SELECT history_seq, item_uuid, candidate_item_uuid, status " \
        "FROM exchange_history " \
        "WHERE item_uuid = ? " \
        "AND buyer_uuid = ? " \
        "AND history_seq = ( " \
        "    SELECT MAX(history_seq) " \
        "    FROM exchange_history " \
        "    WHERE item_uuid = ? AND buyer_uuid = ? " \
        ")",
        (item_uuid, buyer_uuid, item_uuid, buyer_uuid)
    )
    latest_history = cursor.fetchall()
    length = len(latest_history)
    logger.debug(f'latest_history_len: {length}')
    if length > 0:
        latest_history = latest_history[0]
    # item取得
    cursor.execute(
        "SELECT * " \
        "FROM items " \
        "WHERE item_uuid = ?",
        (item_uuid, )
    )
    item = cursor.fetchone()
    # cadidate_item_uuid取得
    cursor.execute(
        "SELECT * " \
        "FROM items " \
        "WHERE item_uuid = ?",
        (candidate_item_uuid, )
    )
    is_valid = False
    candidate_item = cursor.fetchone()
    if next_status == Status.APPLY:
        is_valid = apply(latest_history)
    elif next_status == Status.ACCEPT:
        is_valid = accept(latest_history, item, candidate_item)
    elif next_status == Status.REJECT:
        is_valid = reject(latest_history)
    elif next_status == Status.PROPOSAL:
        is_valid = proposal(latest_history)
    else:
        raise HTTPException(status_code=404, detail='Status not Found')
    
    if not is_valid:
        raise HTTPException(status_code=400, detail='invalid trade')

    cursor.execute(
        "INSERT INTO exchange_history(" \
        "    item_uuid, " \
        "    history_seq, " \
        "    candidate_item_uuid, " \
        "    status, " \
        "    buyer_uuid " \
        ") VALUES ( " \
        "    ?, " \
        "    ?, " \
        "    ?, " \
        "    ?, " \
        "    ?" \
        ")",
        (
            item['item_uuid'],
            int(latest_history['history_seq'])+1 if len(latest_history) > 0 else 1,
            candidate_item['item_uuid'],
            next_status,
            buyer_uuid
        )
    )
    conn.commit()
    conn.close()
    
    return {'result': 'success', 'current_status': next_status}


def apply(latest_history):
    """
    Apply時の処理
    """
    return len(latest_history) == 0


def accept(latest_history, item, candidate_item):
    """
    Accept時の処理
    """
    if latest_history['status'] not in set([Status.APPLY, Status.PROPOSAL]):
        return False
    else:
        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE items " \
            "SET on_sale = 0 " \
            "WHERE item_uuid = ? " \
            "OR item_uuid = ? ",
            (item['item_uuid'], candidate_item['item_uuid'])
        )
        conn.commit()
        conn.close()

        return True


def reject(latest_history):
    """
    Reject時の処理
    """
    if latest_history['status'] not in set([Status.APPLY, Status.PROPOSAL]):
        return False
    return True



def proposal(latest_history):
    """
    Proposal時の処理
    """
    if latest_history['status'] != Status.APPLY:
        return False
    return True