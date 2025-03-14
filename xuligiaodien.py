from PyQt6 import QtWidgets, uic
import sys
import random
import string
from taikhoan import *


user_account = load_user_data()  # Nạp dữ liệu từ file vào bộ nhớ



class dangnhap(QtWidgets.QMainWindow):
    def __init__(self):
        super(dangnhap, self).__init__()
        uic.loadUi('giaodiendangnhap.ui', self)
        self.show()
        self.lienketnutlenh()

    def lienketnutlenh(self):
        self.btn_dk.clicked.connect(self.opengiaodiendangki)
        self.btn_dn.clicked.connect(self.check_account)  # Kiểm tra đăng nhập

    def opengiaodiendangki(self):
        self.register_window = dangki()
        self.register_window.show()
        self.close()  # Đóng cửa sổ đăng nhập

    def check_account(self):
        username = self.user_name.text()
        password = self.password.text()

        if username in user_account and user_account[username]["password"] == password:
            QtWidgets.QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")
            self.main_window = CafeManager()  # Mở giao diện chính
            self.main_window.current_user = username  # Lưu tên nhân viên
            self.main_window.show()
            self.close()  # Đóng giao diện đăng nhập
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Sai tài khoản hoặc mật khẩu!")




class dangki(QtWidgets.QMainWindow):
    def __init__(self):
        super(dangki, self).__init__()  # Đúng cú pháp
        uic.loadUi('giaodiendangki.ui', self)
        self.show()
        self.lienketnutlenh()


    def lienketnutlenh(self):
        self.btn_dk.clicked.connect(self.register_and_back)  # Khi bấm đăng ký
        self.btn_dxu.clicked.connect(self.dexuatusername)
        self.btn_dxp.clicked.connect(self.dexuatpassword)
        self.btn_ql.clicked.connect(self.back_to_login)

    def back_to_login(self):
        self.login_window = dangnhap()  # Mở lại giao diện đăng nhập
        self.login_window.show()
        self.close()

    def dexuatusername(self):
        random_username = "user" + str(random.randint(1000, 9999))
        while random_username in user_account:  # Kiểm tra trùng username
            random_username = "user" + str(random.randint(1000, 9999))
        self.user_name.setText(random_username)

    def dexuatpassword(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        random_password = ''.join(random.choice(characters) for _ in range(10))
        self.password.setText(random_password)

    from taikhoan import save_user_data  # Import hàm lưu tài khoản

    def register_and_back(self):
        username = self.user_name.text().strip()  # Lấy username từ ô nhập liệu
        password = self.password.text().strip()  # Lấy password từ ô nhập liệu
        email = self.email.text().strip()

        if username in user_account:  # Kiểm tra username đã tồn tại chưa
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Username đã tồn tại! Vui lòng chọn username khác.")
            return

        for user_info in user_account.values():
            if user_info["email"] == email:
                QtWidgets.QMessageBox.warning(self, "Lỗi", "Email đã tồn tại! Vui lòng chọn email khác.")
                return

        if username and password and email:
            if save_user_data(username, password, email):
                QtWidgets.QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
                user_account[username] = {"password": password, "email": email}
                self.login_window = dangnhap()
                self.login_window.show()
                self.close()


            self.login_window = dangnhap()  # Quay lại giao diện đăng nhập
            self.login_window.show()
            self.close()  # Đóng giao diện đăng ký
        else:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def login_account(self):
        username = self.ui.user_name.text()
        password = self.ui.password.text()

        # Tải dữ liệu tài khoản
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            QMessageBox.information(self, "Thành công", f"Chào mừng {username}!")
            self.current_user = username  # Lưu tên nhân viên vào session
            self.show_main_screen()  # Chuyển sang giao diện chính
        else:
            QMessageBox.warning(self, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng!")


# Chạy chương trình
app = QtWidgets.QApplication(sys.argv)
window = dangnhap()
app.exec()
