from sqlalchemy.testing.suite.test_reflection import users
import hashlib
from app import db, app#, password
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin
from datetime import datetime



RoomStates = db.Table('room_states',
                      Column('room_id', Integer, ForeignKey('room.id'), primary_key=True),
                      Column('state_id', Integer, ForeignKey('roomstate.id'), primary_key=True))


class Room(db.Model):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String(255))
    img = Column(String(500))
    room_type_id = Column(Integer, ForeignKey('roomtype.id'), nullable=False, default=1)
    states = relationship('RoomState', secondary='room_states', lazy='subquery', backref=backref('rooms', lazy=True))
    rentalroom = relationship('RoomRental', backref='room', lazy=True)
    reservationroom = relationship('RoomReservation', backref='room', lazy=True)



class RoomState(db.Model):
    __tablename__ = 'roomstate'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class RoomType(db.Model):
    __tablename__ = 'roomtype'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    rooms = relationship('Room', backref='type')


class Reservation(db.Model):  # dat phong
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booker_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    booking_date = Column(DateTime, default=datetime.now())
    checkin_date = Column(DateTime, nullable=False)
    checkout_date = Column(DateTime, nullable=False)
    roomreservations = relationship('RoomReservation', backref='reservation')
    reser_invoice = relationship('ReservationInvoice', backref='reservation', lazy=True, uselist=False)


class RoomReservation(db.Model): #phòng trong phieu dat
    __tablename__ = 'room_reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    reservation_id = Column(Integer, ForeignKey('reservation.id'), nullable=False)
    price = Column(Integer, nullable=False)
    cus_room_reservation = relationship('CustomerRoomReservation', backref='room_reservation')


class CustomerRoomReservation(db.Model): #kh trong phong trong phieu dat
    __tablename__ = 'customer_room_reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_reservation_id = Column(Integer, ForeignKey('room_reservation.id'), nullable=False)
    cus_id = Column(Integer, ForeignKey('customer.id'), nullable=False)


class ReservationInvoice(db.Model):
    __tablename__ = 'reser_invoice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'), nullable=False)
    # reservation = relationship('Reservation', backref='reservation_invoice')
    created_date = Column(DateTime, default=datetime.now(), nullable=False)
    total_amount = Column(Float, nullable=False)


class Rental(db.Model):  # Thue phong
    __tablename__ = 'rental'
    id = Column(Integer, primary_key=True, autoincrement=True)
    booker_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    checkin_date = Column(DateTime, nullable=False)
    checkout_date = Column(DateTime, nullable=False)
    roomrentals = relationship('RoomRental', backref='rental')
    reservation_id = Column(Integer, ForeignKey('reservation.id'), nullable=True)
    reservation = relationship('Reservation', backref=backref('rental', uselist=False))
    rental_invoices = relationship('RentalInvoice', backref='rental', lazy=True, uselist=False)


class RoomRental(db.Model): #phong trong phieu thue
    __tablename__ = 'room_rental'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rental_id = Column(Integer, ForeignKey('rental.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    price = Column(Integer, nullable=False)
    cus_room_rental = relationship('CustomerRentalRoom', backref='room_rental')


class CustomerRentalRoom(db.Model): #kh trong phòng trong phiếu thuê
    __tablename__ = 'customer_rental_room'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_rental_id = Column(Integer, ForeignKey('room_rental.id'), nullable=False)
    cus_id = Column(Integer, ForeignKey('customer.id'), nullable=False)


class RentalInvoice(db.Model):
    __tablename__ = 'rental_invoice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)
    rental_id = Column(Integer, ForeignKey('rental.id'), nullable=False)
    # rental = relationship('Rental', backref=backref('rental_invoice', uselist=False))
    created_date = Column(DateTime, default=datetime.now(), nullable=False)
    total_amount = Column(Float, nullable=False)


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(12), nullable=False)
    address = Column(String(255))
    # avt_url = Column(String(255), default='')
    type = Column(String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Customer(User):
    __tablename__ = 'customer'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    id_card_no = Column(String(12), unique=True, nullable=False)
    customer_type_id = Column(Integer, ForeignKey('customertype.id'), nullable=False, default=1)
    customersrentalroom = relationship('CustomerRentalRoom', backref='customer')
    customersroomreservation = relationship('CustomerRoomReservation', backref='customer')
    reservations = relationship('Reservation', backref='customer')
    rentals = relationship('Rental', backref='customer')

    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }


class CustomerType(db.Model):
    __tablename__ = 'customertype'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    coefficient = Column(Float, nullable=False)
    customers = relationship('Customer', backref='customer_type')

#
# Cus_CusRoomRental = db.Table('cus_cusroomrental',
#                              Column('cus_id', Integer, ForeignKey('customer.id'), primary_key=True),
#                              Column('cus_rental_room_id', Integer, ForeignKey('customer_rental_room.id'),
#                                     primary_key=True)
#                              )
# Cus_CusRoomReservation = db.Table('cus_cusroomreservation',
#                                   Column('cus_id', Integer, ForeignKey('customer.id'), primary_key=True),
#                                   Column('cus_room_reservation_id', Integer, ForeignKey('customer_room_reservation.id'),
#                                          primary_key=True)
#                                   )


class Employee(User):
    __tablename__ = 'employee'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    retal_invoices = relationship('RentalInvoice', backref='employee')

    __mapper_args__ = {
        'polymorphic_identity': 'employee',
    }


class Admin(User):
    __tablename__ = 'admin'
    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    privileges = Column(String(255), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }


class Account(db.Model, UserMixin):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref=backref('account', uselist=False))



if __name__ == '__main__':

    with app.app_context():
        # pass
        db.create_all()
        khach_nd = CustomerType(name='Khách nội địa', coefficient=1.0)
        khach_nn = CustomerType(name='Khách nước ngoài', coefficient=1.25)
        db.session.add(khach_nd)
        db.session.add(khach_nn)
        db.session.commit()
        # #roomstate, roomtype, room
        roomstate = ['Trống', 'Đang thuê', 'Đã đặt', 'Bảo trì']
        roomtype = ['Thường', 'VIP', 'View biển', 'View cao']
        for rs in roomstate:
            rs1 = RoomState(name=rs)
            db.session.add(rs1)

        for rt in roomtype:
            rt1 = RoomType(name=rt)
            db.session.add(rt1)

        r1 = Room(name='001', price='2000000', description='',
                  img='https://res.cloudinary.com/djskafzqr/image/upload/v1734441270/n0klrik4czzoecowdeis.jpg',
                  room_type_id=1)
        r2 = Room(name='002', price='3000000', description='',
                  img='https://res.cloudinary.com/djskafzqr/image/upload/v1734441326/gtzf0lnc00kurtqprm2y.jpg',
                  room_type_id=2)
        r3 = Room(name='003', price='4000000', description='',
                  img='https://res.cloudinary.com/djskafzqr/image/upload/v1734441388/qkrdcagoaiwefnxn4s5f.jpg',
                  room_type_id=3)
        #
        roomlist = [r1, r2, r3]

        for r in roomlist:
            db.session.add(r)

        db.session.commit()
        # #
        # # # db.create_all()
        # #
        # #
        r1 = db.session.get(Room, 1)
        print(r1.name)
        ad = Admin(first_name='Manh', last_name='Thang', phone='0999999', privileges='sysadmin')
        ad_acc = Account(username='mthang', password='123', user=ad)
        db.session.add(ad)
        db.session.add(ad_acc)
        db.session.commit()

        employee = Employee(first_name='Quyet', last_name='Thang', phone='08888')
        acc_em = Account(username='quyetthang', password=str(hashlib.md5('1234'.strip().encode('utf-8')).hexdigest()),
                         user=employee)
        db.session.add(employee)
        db.session.add(acc_em)
        db.session.commit()

        account = Account.query.filter_by(username="mthang").first()

        if account:
            account.password = str(hashlib.md5(
                '123'.strip().encode('utf-8')).hexdigest())  # Cập nhật password (băm mật khẩu trước khi lưu)

            db.session.commit()
            print("Cập nhật thành công!")
        else:
            print("Không tìm thấy tài khoản!")
