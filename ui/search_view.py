"""
GIAO DIỆN TÌM KIẾM HỘI VIÊN (Tkinter)
Người phụ trách: Luyện Tuấn Việt

Quy ước chung cho MỌI view trong dự án (để main.py ghép được):
  - Là một lớp kế thừa tk.Frame, khởi tạo bằng  XxxView(parent)
  - Có hàm lam_moi() để tải lại dữ liệu (main.py gọi khi người dùng bấm sang tab)
"""
import tkinter as tk
from tkinter import ttk

import utils
from modules import search

# (tên cột trong database, tiêu đề hiển thị, độ rộng)
CAC_COT = [
    ("id", "ID", 50),
    ("ho_ten", "Họ tên", 200),
    ("so_dien_thoai", "Số điện thoại", 120),
    ("gioi_tinh", "Giới tính", 80),
    ("email", "Email", 180),
    ("ngay_tao", "Ngày tạo", 90),
]


class SearchView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # --- Hàng nhập từ khóa ---
        khung_tren = tk.Frame(self)
        khung_tren.pack(fill="x", padx=10, pady=10)

        tk.Label(khung_tren, text="Tìm theo tên / ID / số điện thoại:").pack(side="left")
        self.o_nhap = tk.Entry(khung_tren, width=30)
        self.o_nhap.pack(side="left", padx=8)
        self.o_nhap.bind("<Return>", lambda _e: self.tim())  # bấm Enter cũng tìm
        tk.Button(khung_tren, text="Tìm", width=8, command=self.tim).pack(side="left")
        tk.Button(khung_tren, text="Xóa ô tìm", width=10, command=self.xoa_tim).pack(side="left", padx=6)

        # --- Bảng kết quả ---
        khung_bang = tk.Frame(self)
        khung_bang.pack(fill="both", expand=True, padx=10)
        self.bang = ttk.Treeview(khung_bang, columns=[c[0] for c in CAC_COT],
                                 show="headings", height=14)
        for khoa, tieu_de, do_rong in CAC_COT:
            self.bang.heading(khoa, text=tieu_de)
            self.bang.column(khoa, width=do_rong, anchor="w")
        thanh_cuon = ttk.Scrollbar(khung_bang, orient="vertical", command=self.bang.yview)
        self.bang.configure(yscrollcommand=thanh_cuon.set)
        self.bang.pack(side="left", fill="both", expand=True)
        thanh_cuon.pack(side="right", fill="y")

        # --- Dòng thông báo kết quả ---
        self.nhan_ket_qua = tk.Label(self, text="Nhập từ khóa rồi bấm Tìm.", anchor="w")
        self.nhan_ket_qua.pack(fill="x", padx=10, pady=8)

    def tim(self):
        """Tìm theo từ khóa trong ô nhập và hiển thị kết quả."""
        try:
            danh_sach = search.tim_hoi_vien(self.o_nhap.get())
        except ValueError as loi:
            self.hien_thi([])
            self.nhan_ket_qua.config(text=f"Lỗi: {loi}", fg="red")
            return
        self.hien_thi(danh_sach)
        if danh_sach:
            self.nhan_ket_qua.config(text=f"Tìm thấy {len(danh_sach)} hội viên.", fg="green")
        else:
            self.nhan_ket_qua.config(text="Không tìm thấy hội viên nào.", fg="red")

    def xoa_tim(self):
        self.o_nhap.delete(0, "end")
        self.hien_thi([])
        self.nhan_ket_qua.config(text="Nhập từ khóa rồi bấm Tìm.", fg="black")

    def hien_thi(self, danh_sach):
        """Xóa bảng cũ rồi đổ danh sách mới vào."""
        for dong in self.bang.get_children():
            self.bang.delete(dong)
        for hv in danh_sach:
            gia_tri = []
            for khoa, _tieu_de, _rong in CAC_COT:
                if khoa == "ngay_tao":
                    gia_tri.append(utils.dinh_dang_ngay(hv.get(khoa)))
                else:
                    gia_tri.append(hv.get(khoa, ""))
            self.bang.insert("", "end", values=gia_tri)

    def lam_moi(self):
        """Khi quay lại tab: nếu đang có từ khóa thì tìm lại (dữ liệu có thể đã đổi)."""
        if self.o_nhap.get().strip():
            self.tim()
