import json
import os

class MenuItem:
    """Lớp biểu diễn một món ăn/uống"""
    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"{self.name} ({self.category}): {self.price:.2f} VND"

class MenuManager:
    def __init__(self, filename="menu.json"):
        self.menu_items = []  # Danh sách món ăn/uống
        self.filename = filename  # Tên file lưu trữ menu

        # Tải menu từ file khi khởi tạo
        self.load_menu_from_file()

    def add_item(self, name: str, price: float, category: str):
        """Thêm món mới vào menu."""
        for item in self.menu_items:
            if item.name == name:
                raise ValueError(f"Món '{name}' đã tồn tại trong menu!")

        self.menu_items.append(MenuItem(name, price, category))
        self.save_menu_to_file()  # Lưu menu sau khi thêm

    def remove_item(self, name: str):
        """Xóa món khỏi menu."""
        self.menu_items = [item for item in self.menu_items if item.name != name]
        self.save_menu_to_file()  # Lưu menu sau khi xóa

    def update_item(self, old_name: str, new_name: str, new_price: float, new_category: str):
        """Cập nhật thông tin món."""
        for item in self.menu_items:
            if item.name == old_name:
                item.name = new_name
                item.price = new_price
                item.category = new_category
                self.save_menu_to_file()  # Lưu menu sau khi cập nhật
                return
        raise ValueError(f"Không tìm thấy món có tên '{old_name}' để cập nhật!")

    def save_menu_to_file(self):
        """Lưu menu hiện tại vào file."""
        with open(self.filename, "w", encoding="utf-8") as file:
            data = [
                {"name": item.name, "price": item.price, "category": item.category}
                for item in self.menu_items
            ]
            json.dump(data, file, ensure_ascii=False, indent=4)

    def load_menu_from_file(self):
        """Đọc menu từ file."""
        if os.path.exists(self.filename):  # Kiểm tra nếu file tồn tại
            try:
                with open(self.filename, "r", encoding="utf-8") as file:
                    data = json.load(file)  # Đọc dữ liệu từ file JSON
                    self.menu_items = [
                        MenuItem(item["name"], item["price"], item["category"])
                        for item in data
                    ]
            except (json.JSONDecodeError, KeyError):
                # Nếu file trống hoặc lỗi JSON, tạo menu rỗng và lưu lại
                self.menu_items = []
                self.save_menu_to_file()
        else:
            # Nếu file không tồn tại, khởi tạo menu rỗng và lưu
            self.menu_items = []
            self.save_menu_to_file()

    def get_menu(self):
        """Trả về danh sách các đối tượng MenuItem"""
        return self.menu_items




