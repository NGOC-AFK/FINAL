from PyQt6.QtWidgets import QPushButton, QMessageBox

class TableManager:
    """Quản lý trạng thái bàn trong quán cà phê"""
    def __init__(self, buttons):
        """
        Khởi tạo quản lý bàn
        :param buttons: Dictionary chứa tên bàn và button tương ứng
        """
        self.tables = {name: "free" for name in buttons.keys()}  # Mặc định bàn trống
        self.buttons = buttons
        self.current_table = None

        # Gán sự kiện click cho từng nút bàn
        for table_name, button in self.buttons.items():
            button.setStyleSheet("background-color: green;")
            button.clicked.connect(lambda _, t=table_name: self.toggleTable(t))

    def toggleTable(self, table_name):
        """Thay đổi trạng thái bàn khi nhấn"""
        if self.tables[table_name] == "free":
            self.current_table = table_name
            self.tables[table_name] = "occupied"
            self.buttons[table_name].setStyleSheet("background-color: red;")
            QMessageBox.information(None, "Bàn đã chọn", f"Bạn đã chọn {table_name}")

        elif self.tables[table_name] == "occupied":
            self.current_table = None
            self.tables[table_name] = "free"
            self.buttons[table_name].setStyleSheet("background-color: green;")
            QMessageBox.information(None, "Trả bàn", f"Bàn {table_name} đã được trả lại")

    def get_current_table(self):
        """Lấy bàn đang được chọn"""
        return self.current_table
