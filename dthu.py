from PyQt6.QtWidgets import QMainWindow
from Doanhthu import Ui_MainWindow2  # Giả sử đây là tệp giao diện doanh thu
import pandas as pd
from PyQt6.QtWidgets import QMessageBox
import matplotlib.pyplot as plt


class RevenueWindow(QMainWindow):
    def __init__(self):
        super(RevenueWindow, self).__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)

        # Gắn sự kiện cho các nút trong giao diện doanh thu
        self.ui.btn_dthungay.clicked.connect(self.calculate_daily_revenue)
        self.ui.btn_dthuthang.clicked.connect(self.calculate_monthly_revenue)
        self.ui.btn_bddthuthang.clicked.connect(self.plot_monthly_revenue)
        self.ui.btn_bddthunam.clicked.connect(self.plot_annual_revenue)

    def calculate_daily_revenue(self):
        """Tính doanh thu ngày"""
        try:
            date = self.ui.txt_ngay.text()  # Lấy ngày từ ô txt_ngay (định dạng dd-mm-YYYY)
            data = pd.read_excel("hoadon.xlsx")

            # Chuyển cột 'Ngày giờ' thành datetime
            data['Ngày giờ'] = pd.to_datetime(data['Ngày giờ'], format="%Y-%m-%d %H:%M:%S")
            data['Ngày'] = data['Ngày giờ'].dt.date  # Tách riêng phần ngày

            selected_date = pd.to_datetime(date,
                                           format="%d-%m-%Y").date()  # Chuyển ngày nhập sang datetime (chỉ phần ngày)

            # Lọc dữ liệu theo ngày
            filtered_data = data[data['Ngày'] == selected_date].copy()  # Tạo bản sao an toàn

            # Tính tổng doanh thu
            filtered_data['Thành tiền'] = filtered_data['Thành tiền'].str.replace(' VND', '').str.replace(',',
                                                                                                          '').astype(
                float)
            total_revenue = filtered_data['Thành tiền'].sum()

            # Hiển thị kết quả trong txt_dthungay
            self.ui.txt_dthungay.setText(f"{total_revenue:,.0f} VND")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể tính doanh thu ngày: {str(e)}")

    def calculate_monthly_revenue(self):
        """Tính doanh thu tháng"""
        try:
            month = self.ui.txt_thang.text()  # Lấy tháng từ ô txt_thang (định dạng YYYY-MM, ví dụ: 2025-03)
            data = pd.read_excel("hoadon.xlsx")

            # Chuyển cột 'Ngày giờ' thành datetime
            data['Ngày giờ'] = pd.to_datetime(data['Ngày giờ'])
            data['Tháng'] = data['Ngày giờ'].dt.to_period('M')  # Trích xuất tháng từ ngày giờ

            # Lọc dữ liệu theo tháng
            selected_month = pd.Period(month, freq='M')
            filtered_data = data[data['Tháng'] == selected_month]

            # Tính tổng doanh thu
            filtered_data['Thành tiền'] = filtered_data['Thành tiền'].str.replace(' VND', '').str.replace(',',
                                                                                                          '').astype(
                float)
            total_revenue = filtered_data['Thành tiền'].sum()

            # Hiển thị kết quả trong txt_dthuthang
            self.ui.txt_dthuthang.setText(f"{total_revenue:,.0f} VND")
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Không thể tính doanh thu tháng: {str(e)}")

    def plot_monthly_revenue(self):
        """Vẽ biểu đồ đường doanh thu giữa các ngày trong một tháng"""
        try:
            month = self.ui.txt_thang.text()  # Lấy tháng từ ô txt_thang (định dạng YYYY-MM, ví dụ: 2025-03)
            data = pd.read_excel("hoadon.xlsx")

            # Chuyển đổi cột 'Ngày giờ' thành datetime và trích xuất thông tin ngày
            data['Ngày giờ'] = pd.to_datetime(data['Ngày giờ'])
            data['Ngày'] = data['Ngày giờ'].dt.date  # Lấy riêng phần ngày

            # Thêm cột "Thành tiền" dưới dạng số để tính toán
            data['Thành tiền'] = data['Thành tiền'].str.replace(' VND', '').str.replace(',', '').astype(float)

            # Lọc dữ liệu theo tháng
            data['Tháng'] = data['Ngày giờ'].dt.to_period('M')  # Trích xuất tháng
            selected_month = pd.Period(month, freq='M')
            filtered_data = data[data['Tháng'] == selected_month]

            if filtered_data.empty:
                QMessageBox.warning(self, "Thông báo", f"Không có dữ liệu cho tháng {month}.")
                return

            # Cộng dồn doanh thu theo ngày
            daily_revenue = filtered_data.groupby('Ngày')['Thành tiền'].sum()

            # Vẽ biểu đồ đường doanh thu
            plt.figure(figsize=(10, 6))
            plt.plot(daily_revenue.index, daily_revenue.values, marker='o', linestyle='-', color='blue',
                     label='Doanh thu')
            plt.title(f"Biến động doanh thu trong tháng {month}", fontsize=16)
            plt.xlabel("Ngày", fontsize=14)
            plt.ylabel("Doanh thu (VND)", fontsize=14)
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể vẽ biểu đồ doanh thu: {str(e)}")

    def plot_annual_revenue(self):
        """Vẽ biểu đồ cột so sánh doanh thu giữa các tháng trong một năm"""
        try:
            year = self.ui.txt_bddthunam.text()  # Lấy năm từ ô txt_bddthunam (định dạng YYYY, ví dụ: 2025)
            data = pd.read_excel("hoadon.xlsx")

            # Chuyển cột 'Ngày giờ' thành datetime và trích xuất thông tin năm, tháng
            data['Ngày giờ'] = pd.to_datetime(data['Ngày giờ'])
            data['Năm'] = data['Ngày giờ'].dt.year  # Trích xuất năm
            data['Tháng'] = data['Ngày giờ'].dt.month  # Trích xuất tháng dưới dạng số (1, 2, 3,...)

            # Lọc dữ liệu theo năm
            data['Thành tiền'] = data['Thành tiền'].str.replace(' VND', '').str.replace(',', '').astype(float)
            filtered_data = data[data['Năm'] == int(year)]

            if filtered_data.empty:
                QMessageBox.warning(self, "Thông báo", f"Không có dữ liệu cho năm {year}.")
                return

            # Tính tổng doanh thu cho từng tháng
            monthly_revenue = filtered_data.groupby('Tháng')['Thành tiền'].sum()

            # Đảm bảo đủ 12 tháng hiển thị (thêm các tháng không có dữ liệu với giá trị 0)
            monthly_revenue = monthly_revenue.reindex(range(1, 13), fill_value=0)

            # Vẽ biểu đồ cột
            plt.figure(figsize=(10, 6))
            monthly_revenue.plot(kind='bar', color='skyblue', edgecolor='black')
            plt.title(f"Doanh thu từng tháng trong năm {year}", fontsize=16)
            plt.xlabel("Tháng", fontsize=14)
            plt.ylabel("Doanh thu (VND)", fontsize=14)
            plt.xticks(range(0, 12), labels=[f"Tháng {i}" for i in range(1, 13)], rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể vẽ biểu đồ doanh thu theo năm: {str(e)}")
