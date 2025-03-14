import cloudinary
import secrets

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

sql_sv_pwd = '325040'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:%s@localhost/hoteldb?charset=utf8mb4" % quote(sql_sv_pwd)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8
app.secret_key = secrets.token_hex(16)

#MOMO config
app.config['MM_PARTNER_CODE'] = 'your_partner_code'
app.config['MM_ACCESS_KEY'] = 'F8BBA842ECF85'
app.config['MM_SECRET_KEY'] = 'K951B6PE1waDMi640xX08PD3vg6EkVlz'
app.config['MM_URL'] = 'https://test-payment.momo.vn/gw_payment/transactionProcessor'


cloudinary.config(
    cloud_name = 'djskafzqr',
    api_key = '965529918623125',
    api_secret = 'kbAOynBOiewYoLA76pOWQo4ktV0'
)

db = SQLAlchemy(app)
login = LoginManager(app=app)