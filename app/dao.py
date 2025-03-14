from app.models import *
from app.models import User
from app import app, db
import hashlib


def load_rooms():
    return Room.query.all()


def add_Customer(firstName, lastName, tel, optradio, id_no, username, password):
    exist_acc = Account.query.filter_by(username=username).first()
    exist_cus = Customer.query.filter_by(id_card_no=id_no).first()
    if not exist_acc and not exist_cus:
        pswd = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        if (optradio == 'domestic'):
            cus_type_id = 1
        elif (optradio == 'foreign'):
            cus_type_id = 2
        cus = Customer(first_name=firstName, last_name=lastName, customer_type_id=cus_type_id, id_card_no=id_no,
                       phone=tel)
        acc = Account(username=username, password=pswd, user=cus)

        db.session.add(cus)
        db.session.add(acc)
        db.session.commit()


# def auth_acc(username, password,):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#     u = Account.query.join(User).filter(
#         Account.username.__eq__(username.strip()),
#         Account.password.__eq__(password))
#
#     # if role:
#     #     u = u.filter(User.type.__eq__(role))
#     return u.first()

def auth_acc(username, password, role=None):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Account.query.join(User).filter(
        Account.username.__eq__(username.strip()),
        Account.password.__eq__(password)
    )

    if role:  # Kiểm tra nếu vai trò được yêu cầu
        u = u.filter(User.type.__eq__(role))

    return u.first()


def get_acc_by_id(acc_id):
    return Account.query.get(acc_id)
