"""
CẤU HÌNH CHUNG CỦA DỰ ÁN
Người phụ trách: cả nhóm (chỉ sửa khi báo trong nhóm)
"""
import os

# Thư mục chứa dự án (để file database luôn nằm cạnh code, chạy ở đâu cũng được)
THU_MUC_DU_AN = os.path.dirname(os.path.abspath(__file__))

# File database SQLite (tự tạo khi chạy lần đầu)
DB_FILE = os.path.join(THU_MUC_DU_AN, "gym.db")

# Số ngày còn lại <= giá trị này thì coi là "sắp hết hạn"
NGAY_SAP_HET_HAN = 7
