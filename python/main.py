from enum import Enum
import logging
import os
import pathlib
import shutil
import json
import sqlite3
import hashlib
from fastapi import File, Request, UploadFile, Body
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.DEBUG
images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [os.environ.get("FRONT_URL", "http://localhost:3000")]
api_url = os.environ.get("API_URL", "http://localhost:9000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_my_headers(request: Request, call_next):
    origin = str(request.headers.get("origin"))
    response = await call_next(request)
    if origin == "http://localhost:3000":
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Vary"] = "Origin"
    return response


sqlite_path = str(
    pathlib.Path(__file__).resolve().parents[1].resolve() / "db" / "hackathon.sqlite3"
)


class Status(str, Enum):
    APPLY = "apply"
    ACCEPT = "accept"
    REJECT = "reject"
    PROPOSAL = "proposal"


@app.post("/login")
def login(user_id: str = Body(...), password: str = Body(...)):
    """
    ログインAPI
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_uuid " "FROM users " "WHERE user_id = ? " "AND password = ? ",
        (user_id, password),
    )
    result = cursor.fetchall()
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="User not Found")
    return result[0]


@app.get("/items")
def get_items_list():
    """
    商品一覧API
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = """SELECT items.item_uuid, items.item_name, categories.category_name AS category_name, items.price, items.on_sale, items.image, items.exchange_items 
        FROM items 
        INNER JOIN categories ON items.category_id = categories.category_id 
        WHERE items.is_public=1"""
    cursor.execute(sql)
    items_dic = {}
    items_dic["items"] = cursor.fetchall()
    conn.close()
    return items_dic


@app.get("/items/{item_uuid}")  ###is_publicを返すかどうか，今は返してます
def get_item(item_uuid: str):
    """
    商品詳細API
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = """SELECT items.item_uuid, items.item_name, categories.category_name AS category_name, items.is_public, items.price, items.on_sale, items.image, items.exchange_items, items.user_uuid
        FROM items
        INNER JOIN categories ON items.category_id = categories.category_id
        WHERE items.item_uuid=?"""
    cursor.execute(sql, (item_uuid,))
    item_dic = cursor.fetchall()[0]
    conn.close()
    return item_dic


@app.get(
    "/user_items/{user_uuid}"
)  ###is_public，user_uuid，exchange_items以外を返してます．一応on_sale=1という値は返します．
def get_user_items_list(user_uuid: str):
    """
    出品一覧API
    """
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    sql = """SELECT items.item_uuid, items.item_name, categories.category_name AS category_name, items.is_public, items.price, items.on_sale, items.image, items.exchange_items
        FROM items 
        INNER JOIN categories ON items.category_id = categories.category_id 
        WHERE items.user_uuid =?"""
    cursor.execute(sql, (user_uuid,))
    items_dic = {}
    items_dic["items"] = cursor.fetchall()
    conn.close()
    return items_dic


@app.get("/user_items/")
def get_candidate_items_list(user_uuid: str, category_name: str):
    """
    物々交換候補商品一覧API
    """
    pass


@app.get("/barter/status/{current_status}")
def get_status_list(current_status: Status):
    """
    ステータス一覧API
    """
    pass


@app.post("/barter")
def berter(next_status: Status, item_uuid: str, candidate_item_uuid: str):
    """
    物々交換API
    """
    pass


def apply():
    """
    Apply時の処理
    """
    pass


def accept():
    """
    Accept時の処理
    """
    pass


def reject():
    """
    Reject時の処理
    """
    pass


def proposal():
    """
    Proposal時の処理
    """
    pass


@app.get("/images/{items_image}")
async def get_image(items_image):
    # Create image path
    image = images / items_image
    if not items_image.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.setLevel(logging.DEBUG)
        logger.debug(f"Image not found: {image}")
        image = images / "images" / "default.jpg"
        logger.debug(f"default: {image}")

    return FileResponse(image)
