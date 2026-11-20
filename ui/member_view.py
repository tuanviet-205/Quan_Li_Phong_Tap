"""
GIAO DIỆN QUẢN LÝ HỘI VIÊN (Tkinter)
Người phụ trách: Nguyễn Hữu Trường (hạng mục III - quản lý hội viên), review: Nguyễn Hữu Hùng
CHỈ Trường sửa file này. Chỉ gọi hàm từ modules/members.py, KHÔNG viết SQL ở đây.

Quy ước (để main.py tự ghép tab): lớp kế thừa tk.Frame, tạo bằng MemberView(parent),
có hàm lam_moi(). Xem ui/search_view.py làm mẫu (bảng Treeview, bắt ValueError).
"""
import tkinter as tk
from tkinter import messagebox, ttk  # noqa: F401

import utils  # noqa: F401
from modules import members  # noqa: F401


class MemberView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # TODO (Trường): bảng danh sách hội viên + ô nhập + nút Thêm / Sửa / Xóa
        tk.Label(self, text="Quản lý hội viên - đang phát triển (Trường)").pack(padx=20, pady=20)

    def lam_moi(self):
        """Tải lại danh sách từ members.lay_tat_ca_hoi_vien() khi người dùng bấm sang tab."""
        pass
