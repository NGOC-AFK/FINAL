import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem
from PyQt6 import QtWidgets, uic
from order import Ui_MainWindow  # Giao diện chính
from Menu_edit import UpdateMenu  # Giao diện chỉnh sửa menu
from dthu import RevenueWindow
from menu_manager import MenuManager  # Lớp quản lý menu
from table import TableManager  # Lớp quản lý bàn
from OrderManager import OrderManager  # Lớp quản lý hóa đơn
from taikhoan import *

user_account = load_user_data()  # Nạp dữ liệu từ file vào bộ nhớ


class CafeManager(QMainWindow):
    def __init__(self, current_user):
        super(CafeManager, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Khởi tạo giá trị `current_user`
        self.current_user = current_user  # Lưu tên nhân viên đăng nhập hiện tại

        # Khởi tạo MenuManager
        self.menu_manager = MenuManager()

        # Tạo cửa sổ doanh thu
        self.revenue_window = RevenueWindow()

        # Kết nối nút btn_dthu để mở giao diện doanh thu
        self.ui.btn_dthu.clicked.connect(self.show_revenue_window)

        # Khởi tạo quản lý hóa đơn với giảm giá
        self.order_manager = OrderManager(self.ui.tblorder, self.ui.txt_total, self.ui.txt_discount)

        # Gắn sự kiện cho nút chỉnh sửa menu
        self.ui.btn_menufix.clicked.connect(self.open_update_menu)

        # Khởi tạo quản lý bàn
        self.table_manager = TableManager({
            "Bàn 1": self.ui.btn_ban1,
            "Bàn 2": self.ui.btn_ban2,
            "Bàn 3": self.ui.btn_ban3,
            "Bàn 4": self.ui.btn_ban4,
            "Bàn 5": self.ui.btn_ban5,
            "Bàn 6": self.ui.btn_ban6,
            "Bàn 7": self.ui.btn_ban7,
            "Bàn 8": self.ui.btn_ban8,
            "Take away": self.ui.btn_take
        })

        # Kết nối sự kiện
        for table_name, button in self.table_manager.tables.items():
            if isinstance(button, QtWidgets.QPushButton):  # Kiểm tra nếu button là QPushButton
                button.clicked.connect(lambda _, name=table_name: self.select_table(name))
        self.load_categories()

        self.ui.mainmenu.cellDoubleClicked.connect(self.add_item_to_order)
        self.ui.btn_delete.clicked.connect(self.remove_item)
        self.ui.btn_save.clicked.connect(self.save_order)
        self.ui.txt_discount.textChanged.connect(self.order_manager.apply_discount)  # Áp dụng giảm giá
        self.ui.category.currentTextChanged.connect(self.load_menu_items)
        self.ui.btn_dangxuat.clicked.connect(self.logout)
        self.ui.hienthiNV.setText(f"Nhân viên: {self.current_user}")

        # Tải menu từ file
        self.menu_manager.load_menu_from_file()
        self.load_menu_items()


    def open_update_menu(self):
        """Mở giao diện chỉnh sửa menu"""
        from menuedit import Ui_Form  # Import UpdateMenu tại đây để tránh vòng lặp import
        self.update_menu_window = UpdateMenu(self.menu_manager, self)
        self.update_menu_window.show()

    def show_revenue_window(self):
        """Hiển thị giao diện doanh thu"""
        try:
            self.revenue_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở giao diện doanh thu: {str(e)}")

    def load_menu_items(self):
        """Hiển thị danh sách món trong bảng menu theo danh mục được chọn"""
        selected_category = self.ui.category.currentText()
        self.ui.mainmenu.setRowCount(0)  # Xóa dữ liệu cũ

        for item in self.menu_manager.get_menu():  # Lấy danh sách các đối tượng MenuItem
            # Lọc theo danh mục (hoặc hiển thị tất cả nếu chọn "Tất cả")
            if selected_category == "Tất cả" or item.category == selected_category:
                row_position = self.ui.mainmenu.rowCount()
                self.ui.mainmenu.insertRow(row_position)
                self.ui.mainmenu.setItem(row_position, 0, QTableWidgetItem(item.name))  # Tên món
                self.ui.mainmenu.setItem(row_position, 1, QTableWidgetItem(f"{item.price:,.0f} VND"))  # Giá

    def select_table(self, table_name):
            """Xử lý khi chọn bàn"""
            self.table_manager.select_table(table_name)
            QMessageBox.information(self, "Bàn đã chọn", f"Bạn đã chọn {table_name}")

    def add_item_to_order(self, row, column):
        """Thêm món từ menu vào hóa đơn khi nhấn đúp"""
        try:
            # Lấy thông tin từ bảng menu
            item_name = self.ui.mainmenu.item(row, 0).text()
            item_price_text = self.ui.mainmenu.item(row, 1).text()
            item_price = float(item_price_text.replace(" VND", "").replace(",", ""))

            # Gọi trực tiếp phương thức từ OrderManager
            self.order_manager.add_to_order(item_name, item_price)
            QMessageBox.information(self, "Thêm món", f"Đã thêm {item_name} vào hóa đơn!")
        except (AttributeError, ValueError) as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể thêm món: {str(e)}")

    def remove_item(self):
        """Xóa món được chọn khỏi hóa đơn"""
        selected_row = self.ui.tblorder.currentRow()
        self.order_manager.remove_item(selected_row)  # Gọi hàm từ OrderManager

    def clear_order(self):
        """Xóa sạch bảng hóa đơn để bắt đầu một hóa đơn mới"""
        self.ui.tblorder.setRowCount(0)  # Xóa tất cả các hàng trong bảng order
        self.ui.txt_total.clear()  # Xóa tổng tiền
        self.ui.txt_discount.clear()  # Xóa giảm giá
        self.order_manager.clear_order()  # Xóa dữ liệu hóa đơn trong OrderManager

    def save_order(self):
        """Lưu hóa đơn hiện tại vào file và reset bảng hóa đơn"""
        try:
            current_table = self.table_manager.get_current_table()
            if not current_table:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn bàn trước khi lưu hóa đơn!")
                return

            if not self.current_user:
                QMessageBox.warning(self, "Lỗi", "Không thể lưu hóa đơn vì chưa đăng nhập!")
                return

            # Truyền current_user (tên nhân viên hiện tại) vào hàm save_to_excel
            self.order_manager.save_to_excel(current_table, self.current_user)

            # Reset bảng hóa đơn và các giá trị
            self.clear_order()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi lưu hóa đơn: {str(e)}")

    def load_categories(self):
        """Tải danh mục sản phẩm vào QComboBox"""
        categories = {"Tất cả"}  # Tập hợp để tránh trùng lặp
        for item in self.menu_manager.get_menu():  # Lấy danh sách các đối tượng MenuItem
            categories.add(item.category)  # Sử dụng thuộc tính category của MenuItem

        self.ui.category.clear()
        self.ui.category.addItems(sorted(categories))  # Thêm danh mục vào QComboBox

    def logout(self):
        """Đăng xuất và quay lại giao diện đăng nhập"""
        try:
            # Reset current user
            self.current_user = None
            self.order_manager.clear_order()  # Clear current order data (if applicable)

            # Open login window
            self.login_window = dangnhap()
            self.login_window.show()

            # Close current window (CafeManager)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đã xảy ra lỗi khi đăng xuất: {str(e)}")


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
            self.main_window = CafeManager(username)  # Truyền tên nhân viên vào CafeManager
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

        if username in user_account:
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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Hiển thị giao diện đăng nhập trước
    login_window = dangnhap()
    login_window.show()

    sys.exit(app.exec())
