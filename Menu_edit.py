from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem
from menuedit import Ui_Form
class MenuItem:
    def __init__(self, name: str, price: float, category: str):

        self.name = name
        self.price = price
        self.category = category  # Phân loại sản phẩm


class UpdateMenu(QWidget):
    def __init__(self, menu_manager, order_ui):
        super(UpdateMenu, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.menu_manager = menu_manager
        self.order_ui = order_ui  # Tham chiếu đến giao diện Order

        # Gắn sự kiện cho các nút
        self.ui.btn_themmon.clicked.connect(self.add_item)
        self.ui.btn_xoamon.clicked.connect(self.remove_item)
        self.ui.btn_capnhat.clicked.connect(self.update_item)
        self.ui.list_danhmuc.itemDoubleClicked.connect(self.filter_items_by_category)

        # Hiển thị danh sách menu ban đầu
        self.load_items()

    def load_items(self):
        """Hiển thị danh sách món lên bảng"""
        self.ui.tableWidget.setRowCount(0)
        for item in self.menu_manager.get_menu():
            row_position = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_position)
            self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(item.name))
            self.ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(f"{item.price:.2f} VND"))

    def add_item(self):
        """Thêm món vào menu"""
        name = self.ui.txt_tenmon.toPlainText().strip()
        price = self.ui.txt_.toPlainText().strip()
        category = self.ui.chon_danhmuc.currentText()

        if not name or not price:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ tên món và giá!")
            return

        try:
            price = float(price)
            self.menu_manager.add_item(name, price, category)
            self.load_items()
            self.order_ui.load_menu_items()  # Cập nhật giao diện Order
            QMessageBox.information(self, "Thành công", f"Đã thêm món: {name}")
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def remove_item(self):
        """Xóa món từ menu"""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn món để xóa!")
            return

        name = self.ui.tableWidget.item(selected_row, 0).text()
        try:
            self.menu_manager.remove_item(name)
            self.load_items()
            self.order_ui.load_menu_items()  # Cập nhật giao diện Order
            QMessageBox.information(self, "Thành công", f"Đã xóa món: {name}")
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def update_item(self):
        """Cập nhật thông tin món trong menu"""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn món để cập nhật!")
            return

        old_name = self.ui.tableWidget.item(selected_row, 0).text()
        new_name = self.ui.txt_tenmon.toPlainText().strip()
        price = self.ui.txt_.toPlainText().strip()
        category = self.ui.chon_danhmuc.currentText()

        if not new_name or not price:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin món!")
            return

        try:
            price = float(price)
            self.menu_manager.update_item(old_name, new_name, price, category)
            self.load_items()
            self.order_ui.load_menu_items()  # Cập nhật giao diện Order
            QMessageBox.information(self, "Thành công", f"Đã cập nhật món: {new_name}")
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi", str(e))

    def filter_items_by_category(self, item):
        """Hiển thị sản phẩm theo danh mục được chọn khi double-click"""
        selected_category = item.text()  # Lấy danh mục được double-click
        self.ui.tableWidget.setRowCount(0)  # Xóa dữ liệu cũ trong bảng

        # Lọc sản phẩm theo danh mục và hiển thị
        for product in self.menu_manager.get_menu():
            if selected_category == "Tất cả" or product.category == selected_category:
                row_position = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(row_position)
                self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(product.name))  # Tên sản phẩm
                self.ui.tableWidget.setItem(row_position, 1,
                                            QTableWidgetItem(f"{product.price:,.0f} VND"))  # Giá sản phẩm

