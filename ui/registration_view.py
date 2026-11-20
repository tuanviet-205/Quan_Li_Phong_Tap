"""
GIAO DIỆN ĐĂNG KÝ GÓI TẬP + THEO DÕI SẮP HẾT HẠN (Tkinter)
Người phụ trách: Đặng Tiến Sơn (hạng mục 3.1 - phần đăng ký và theo dõi thời hạn), review: Nguyễn Hữu Hùng
CHỈ Sơn sửa file này. Chỉ gọi hàm từ modules/registrations.py (và modules/members.py,
modules/packages.py nếu cần lấy danh sách để chọn), KHÔNG viết SQL ở đây.

Quy ước (để main.py tự ghép tab): lớp kế thừa tk.Frame, tạo bằng RegistrationView(parent),
có hàm lam_moi(). Xem ui/search_view.py làm mẫu.
"""
import tkinter as tk
from tkinter import messagebox, ttk  # noqa: F401

import utils  # noqa: F401
from modules import registrations  # noqa: F401


class RegistrationView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # TODO (Sơn): chọn hội viên + chọn gói + nút Đăng ký; bảng lịch sử; bảng sắp hết hạn
        tk.Label(self, text="Đăng ký gói tập - đang phát triển (Sơn)").pack(padx=20, pady=20)

    def lam_moi(self):
        """Tải lại lịch sử đăng ký và danh sách sắp hết hạn khi người dùng bấm sang tab."""
        pass
