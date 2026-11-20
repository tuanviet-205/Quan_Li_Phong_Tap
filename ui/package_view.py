"""
GIAO DIỆN QUẢN LÝ GÓI TẬP (Tkinter)
Người phụ trách: Nguyễn Hữu Hùng (hạng mục 3.1 - phần gói tập), review: Đặng Tiến Sơn
CHỈ Hùng sửa file này. Chỉ gọi hàm từ modules/packages.py, KHÔNG viết SQL ở đây.

Quy ước (để main.py tự ghép tab): lớp kế thừa tk.Frame, tạo bằng PackageView(parent),
có hàm lam_moi(). Xem ui/search_view.py làm mẫu.
"""
import tkinter as tk
from tkinter import messagebox, ttk  # noqa: F401

import utils  # noqa: F401
from modules import packages  # noqa: F401


class PackageView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # TODO (Hùng): bảng danh sách gói tập + ô nhập (tên, giá, số ngày, mô tả) + nút Thêm / Sửa / Xóa
        tk.Label(self, text="Quản lý gói tập - đang phát triển (Hùng)").pack(padx=20, pady=20)

    def lam_moi(self):
        """Tải lại danh sách từ packages.lay_tat_ca_goi_tap() khi người dùng bấm sang tab."""
        pass
