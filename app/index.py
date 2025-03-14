import json
import uuid
import hmac
import hashlib
#from crypt import methods
from functools import wraps
from flask import abort
import requests
import dao
from flask import Flask
from flask_login import LoginManager
from flask_login import login_required
from flask import Flask, render_template, request, redirect, url_for, session
from app import app, login
from app.dao import load_rooms
from flask_login import login_user, logout_user, current_user
from app.models import User
endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
accessKey = "F8BBA842ECF85"
secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
partnerCode = "MOMO"
orderInfo = "pay with MoMo"
redirectUrl = "http://127.0.0.1:5000/payment_success"
ipnUrl = "http://127.0.0.1:5000/payment_ipn"
amount = "50000"
partnerName = "MoMo Payment"
requestType = "payWithMethod"
storeId = "Test Store"
autoCapture = True
lang = "vi"



@app.route('/create_payment', methods=['POST'])
def create_payment():
   # Tạo các tham số yêu cầu
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    extraData = ""  # pass empty value or Encode base64 JsonString
    orderGroupId = ""

    #Tạo rawSignature
    rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"

    #Tạo chữ ký (signature)
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()

    #Chuẩn bị dữ liệu JSON gửi tới MoMo
    data = {
       'partnerCode': partnerCode,
       'orderId': orderId,
       'partnerName': partnerName,
       'storeId': storeId,
       'ipnUrl': ipnUrl,
       'amount': amount,
        'lang': lang,
        'requestType': requestType,
        'redirectUrl': redirectUrl,
        'autoCapture': autoCapture,
        'orderInfo': orderInfo,
        'requestId': requestId,
        'extraData': extraData,
        'signature': signature,
        'orderGroupId': orderGroupId
    }

    # Chuyển đổi dữ liệu sang JSON
    data = json.dumps(data)

    # Gửi yêu cầu POST tới MoMo
    clen = len(data)
    response = requests.post(endpoint, data=data, headers={'Content-Type': 'application/json', 'Content-Length': str(clen)})

    # Nhận URL thanh toán từ MoMo
    response_data = response.json()
    print(response_data)
    if response_data['resultCode'] == 0:
        payUrl = response_data['payUrl']
        return redirect(payUrl)  # Chuyển hướng người dùng tới MoMo để thanh toán
    else:
        return response_data['message']

@app.route('/payment_success')
def payment_success():
    return "Thanh toán thành công!"

@app.route('/payment_ipn')
def payment_ipn():
    # IPN (Instant Payment Notification) handler, nơi MoMo gửi thông tin kết quả thanh toán
    return "Thông báo thanh toán đã được nhận."

user = [
        {
            'name': 'Ly Manh Thang',
            'email': 'thang@gmail.com',
        }, {
            'name': 'Tran Thi Thao My',
            'email': 'my@gmail.com',
        }, {
            'name': 'Nguyen Phuong Nam',
            'email': 'nam@gmail.com',
        }
    ]

@app.route('/')
def index():
    u1 = []
    kw = request.args.get('keyword')
    if kw:
        for u in user:
            if u['name'].lower().__contains__(kw.lower()):
                u1.append(u)
    rooms = load_rooms()

    session['reservation'] = {
        '1': {
            'id': '1',
            'name': 'room001',
            'no_cus': '3',
            'price': '1500000'
        },
        '2': {
            'id': '2',
            'name': 'room002',
            'no_cus': '3',
            'price': '2500000'
        }
    }

    return render_template('index.html', name='manhthang', user=user, u1=u1, rooms=rooms)


# @app.route('/admin')
# def admin_dashboard():
#     # Kiểm tra nếu người dùng không phải là admin
#     if not current_user.is_authenticated or current_user.user.type != 'admin':
#         abort(403)  # Forbidden
#     return render_template('/admin')


@app.route('/login', methods=['GET', 'POST'])

def login_processor():
    if current_user.is_authenticated:
        return redirect('/')
    if request.method.__eq__("POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        acc = dao.auth_acc(username=username, password=password)
        if acc:

            session['user_id'] = acc.user.id
            session['role'] = acc.user.type
            login_user(acc)
            # return redirect_based_on_type(acc.user.type)
            user_type = acc.user.type  # acc.user là đối tượng liên kết từ bảng User
            if user_type == "admin":  # Nếu là admin, chuyển hướng đến trang admin
                return redirect('/admin')
            elif user_type == "employee":
                return redirect('/employee')
            elif user_type=="customer": # Người dùng thông thường
                return redirect('/')

    return render_template('login.html')
# def redirect_based_on_type(type):
#     if type == 'admin':
#         return redirect(url_for('login_admin_process'))
#     elif type == 'employee':
#         return redirect(url_for('employee_processor'))
#     elif type == 'customer':
#         return redirect(url_for('index'))
# def role_required(role):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if 'role' not in session or session['role'] != role:
#                 abort(403)  # Forbidden
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator
@app.route("/login-admin", methods=['POST'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')
    acc = dao.auth_acc(username=username, password=password, role='admin')  # Chỉ kiểm tra vai trò admin

    if acc:
        login_user(acc)  # Đăng nhập người dùng nếu hợp lệ
        return redirect('/admin')
    else:
        return redirect('/login')
    # print(acc.user.type)
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if current_user.user.type != 'admin':  # Nếu không phải admin
        return redirect('/')
    # Nội dung cho admin
    return redirect('/admin')
# @app.route('/admin', methods=['GET', 'POST'])
# def admin_processor():
#    return 'hello admin'


@app.route('/employee', methods=['GET', 'POST'])
def employee_processor():
    return 'hello employee'


@app.route('/logout')
def logout_acc():
    logout_user()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form.get('password')
        pswd_repeat = request.form.get('pswd_repeat')

        if password.__eq__(pswd_repeat):
            data = request.form.copy()
            print(data)
            del data['pswd_repeat']

            dao.add_Customer(**data)

            return redirect('/login')
        else:
            err_msg = 'Mật khẩu không khớp!'
    return render_template('register.html')


@app.route('/api/getuserid', methods=['GET'])
def get_userid():
    return current_user.id


@login.user_loader
def load_user(acc_id):
    return dao.get_acc_by_id(acc_id)



if __name__ == '__main__':
    with app.app_context():
        from app import admin


        app.run(debug=True, port=5000)
