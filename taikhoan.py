import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem

# Đường dẫn file lưu tài khoản
USER_DATA_FILE = "user_account.txt"

# Tải dữ liệu tài khoản từ file (nếu có)
def load_user_data():
    user_account = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 3:  # Đảm bảo có đủ username, password, email
                    username, password, email = parts
                    user_account[username] = {"password": password, "email": email}
    return user_account

# Lưu tài khoản vào file
def save_user_data(username, password, email):
    user_data = load_user_data()

    # Kiểm tra email đã tồn tại chưa
    for user_info in user_data.values():
        if user_info["email"] == email:
            return False  # Email bị trùng, không lưu

    # Lưu thông tin tài khoản nếu email chưa tồn tại
    with open(USER_DATA_FILE, "a", encoding="utf-8") as file:
        file.write(f"{username}:{password}:{email}\n")
    return True
def register_account(self):
    username = self.ui.user_name.text()
    password = self.ui.password.text()
    email = self.ui.email.text()  # Nếu giao diện đăng ký có ô nhập email

    if not username or not password or not email:
        QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin!")
        return

    # Gọi hàm lưu tài khoản
    if save_user_data(username, password, email):
        QMessageBox.information(self, "Thành công", "Đăng ký tài khoản thành công!")
        self.show_login_screen()  # Quay lại màn hình đăng nhập
    else:
        QMessageBox.warning(self, "Lỗi", "Email đã tồn tại!")
