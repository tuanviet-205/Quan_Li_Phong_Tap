"""
GIAO DIỆN THỐNG KÊ (Tkinter)
Người phụ trách: Luyện Tuấn Việt

Hiển thị: tổng quan (hội viên, gói tập, doanh thu), thống kê theo gói, theo tháng.
Quy ước view: lớp kế thừa tk.Frame, XxxView(parent), có lam_moi().
"""
import tkinter as tk
from tkinter import ttk

import utils
from modules import statistics


class StatisticsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # --- Nút làm mới ---
        khung_tren = tk.Frame(self)
        khung_tren.pack(fill="x", padx=10, pady=8)
        tk.Label(khung_tren, text="THỐNG KÊ TỔNG QUAN", font=("Arial", 12, "bold")).pack(side="left")
        tk.Button(khung_tren, text="Làm mới", width=10, command=self.lam_moi).pack(side="right")

        # --- Các ô số liệu tổng quan: (key trong dict, nhãn hiển thị) ---
        self.cac_o = [
            ("tong_hoi_vien", "Tổng hội viên"),
            ("dang_con_han", "Đang còn hạn"),
            ("sap_het_han", "Sắp hết hạn"),
            ("da_het_han", "Đã hết hạn"),
            ("tong_goi_tap", "Số gói tập"),
            ("tong_doanh_thu", "Tổng doanh thu"),
        ]
        self.nhan_so = {}  # key -> Label chứa con số
        khung_so = tk.Frame(self)
        khung_so.pack(fill="x", padx=10)
        for i, (khoa, nhan) in enumerate(self.cac_o):
            o = tk.LabelFrame(khung_so, text=nhan, padx=10, pady=6)
            o.grid(row=0, column=i, padx=4, sticky="nsew")
            khung_so.columnconfigure(i, weight=1)
            so = tk.Label(o, text="0", font=("Arial", 14, "bold"))
            so.pack()
            self.nhan_so[khoa] = so

        # --- Hai bảng chi tiết trong 2 tab nhỏ ---
        tab = ttk.Notebook(self)
        tab.pack(fill="both", expand=True, padx=10, pady=10)
        self.bang_goi = self._tao_bang(
            tab, "Theo gói tập",
            [("ten_goi", "Tên gói", 220), ("so_luot", "Lượt đăng ký", 120), ("doanh_thu", "Doanh thu", 160)])
        self.bang_thang = self._tao_bang(
            tab, "Theo tháng",
            [("thang", "Tháng", 120), ("so_luot", "Lượt đăng ký", 120), ("doanh_thu", "Doanh thu", 160)])

        self.lam_moi()

    def _tao_bang(self, tab, tieu_de_tab, cac_cot):
        """Tạo một tab chứa bảng Treeview, trả về bảng đó."""
        khung = tk.Frame(tab)
        tab.add(khung, text=tieu_de_tab)
        bang = ttk.Treeview(khung, columns=[c[0] for c in cac_cot], show="headings", height=8)
        for khoa, tieu_de, rong in cac_cot:
            bang.heading(khoa, text=tieu_de)
            bang.column(khoa, width=rong, anchor="w")
        bang.pack(fill="both", expand=True)
        return bang

    def lam_moi(self):
        """Đọc lại số liệu mới nhất từ database và vẽ lại."""
        tong_quan = statistics.thong_ke_tong_quan()
        for khoa, _nhan in self.cac_o:
            gia_tri = tong_quan[khoa]
            if khoa == "tong_doanh_thu":
                gia_tri = utils.dinh_dang_tien(gia_tri)
            self.nhan_so[khoa].config(text=str(gia_tri))

        self._do_bang(self.bang_goi, [
            (g["ten_goi"], g["so_luot"], utils.dinh_dang_tien(g["doanh_thu"]))
            for g in statistics.thong_ke_theo_goi()])
        self._do_bang(self.bang_thang, [
            (self._thang_hien_thi(t["thang"]), t["so_luot"], utils.dinh_dang_tien(t["doanh_thu"]))
            for t in statistics.thong_ke_dang_ky_theo_thang()])

    @staticmethod
    def _thang_hien_thi(thang):
        """'2026-11' -> '11/2026'."""
        nam, thang_so = thang.split("-")
        return f"{thang_so}/{nam}"

    @staticmethod
    def _do_bang(bang, cac_dong):
        for dong in bang.get_children():
            bang.delete(dong)
        for dong in cac_dong:
            bang.insert("", "end", values=dong)
