

from app.models import Customer, Employee, Room, Reservation, User, Account
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_login import current_user, logout_user
from app import app, db
from flask_admin import BaseView, expose
from flask import redirect
admin = Admin(app=app, name='Hotel-Admin', template_mode='bootstrap4')

class All(ModelView):
 def is_accessible(self):
     if not current_user.is_authenticated or current_user.user.type != 'admin':
         return False
     return True
 def inaccessible_callback(self, name, **kwargs):
        # Chuyển hướng người dùng không có quyền
        return redirect('/')
can_export = True
class CustomerView(All):
  #  column_list = ['firstName']
    can_export = True
    page_size = 10
    #column_filters = ['firstName']

class ReservationView(All):
    page_size = 5


class LogoutView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return redirect('/admin')

admin.add_view(CustomerView(Customer, db.session))
admin.add_view(All(Employee, db.session))
admin.add_view(All(Room, db.session))
admin.add_view(ReservationView(Reservation, db.session))

admin.add_view(All(User, db.session))
admin.add_view(All(Account, db.session))

admin.add_view(LogoutView(name='Đăng xuất'))
