"""
CHƯƠNG TRÌNH CHÍNH - QUẢN LÝ PHÒNG TẬP GYM (Tkinter + SQLite)
Người phụ trách: Phạm Văn Cử (hạng mục II - cấu trúc chương trình và menu, cùng Nguyễn Hữu Hùng phụ trách utils.py), review: cả nhóm
Khung ban đầu do Luyện Tuấn Việt viết khi tích hợp; Cử tiếp quản và chỉnh sửa tiếp.

Chạy:  python main.py      (đứng trong thư mục quan_ly_gym)

Cách ghép: mỗi tab = một "view" (lớp kế thừa tk.Frame, tạo bằng XxxView(parent)).
Danh sách TABS bên dưới ghi các tên module/lớp mà nhóm đã thống nhất.
  - Chưa có file của bạn trong nhóm  -> tab hiện dòng "chưa có", chương trình vẫn chạy.
  - File có nhưng bị lỗi khi import  -> tab hiện nguyên văn lỗi để sửa nhanh.
Người làm view khác chỉ cần đặt đúng tên file/lớp là tự xuất hiện, không phải sửa main.py.
"""
import importlib
import traceback
import tkinter as tk
from tkinter import messagebox, ttk

import database

# (tên tab, [(module, tên lớp), ...])  - thử lần lượt, lấy cái đầu tiên import được
TABS = [
    ("Hội viên", [("ui.member_view", "MemberView"),
                  ("ui.members_view", "MembersView"),
                  ("ui.hoi_vien_view", "HoiVienView")]),
    ("Gói tập", [("ui.package_view", "PackageView"),
                 ("ui.packages_view", "PackagesView"),
                 ("ui.goi_tap_view", "GoiTapView")]),
    ("Đăng ký", [("ui.registration_view", "RegistrationView"),
                 ("ui.registrations_view", "RegistrationsView"),
                 ("ui.dang_ky_view", "DangKyView")]),
    ("Tìm kiếm", [("ui.search_view", "SearchView")]),
    ("Thống kê", [("ui.statistics_view", "StatisticsView")]),
]


def tao_tab(notebook, ten_tab, ung_vien):
    """Tạo nội dung một tab. Luôn trả về Frame, không bao giờ làm sập chương trình."""
    chua_co = []
    for ten_module, ten_lop in ung_vien:
        try:
            module = importlib.import_module(ten_module)
        except ModuleNotFoundError as loi:
            # Chỉ coi là "chưa có file" khi thiếu đúng module này (hoặc package cha của nó)
            if loi.name and (ten_module == loi.name or ten_module.startswith(loi.name + ".")):
                chua_co.append(ten_module)
                continue
            return _khung_loi(notebook, f"{ten_module} import lỗi (thiếu thư viện/module '{loi.name}')",
                              traceback.format_exc())
        except Exception:
            return _khung_loi(notebook, f"{ten_module} import lỗi", traceback.format_exc())

        lop = getattr(module, ten_lop, None)
        if lop is None:
            return _khung_loi(notebook, f"{ten_module} không có lớp {ten_lop}",
                              f"Sửa: đặt tên lớp là {ten_lop}(tk.Frame) hoặc báo Cử thêm tên vào TABS trong main.py.")
        try:
            return lop(notebook)
        except Exception:
            return _khung_loi(notebook, f"{ten_module}.{ten_lop} khởi tạo lỗi", traceback.format_exc())

    return _khung_loi(notebook, f"Tab '{ten_tab}' chưa có file giao diện",
                      "Cần một trong các file: " + ", ".join(chua_co) +
                      "\nMỗi file cần một lớp kế thừa tk.Frame, khởi tạo bằng XxxView(parent), có hàm lam_moi().")


def _khung_loi(parent, tieu_de, chi_tiet):
    """Frame hiển thị thông báo lỗi/thiếu thay cho tab bị hỏng."""
    print(f"[CẢNH BÁO] {tieu_de}\n{chi_tiet}\n")
    khung = tk.Frame(parent)
    tk.Label(khung, text=tieu_de, fg="red", font=("Arial", 11, "bold")).pack(anchor="w", padx=12, pady=(12, 4))
    tk.Label(khung, text=chi_tiet, justify="left", anchor="w", wraplength=820).pack(anchor="w", padx=12)
    return khung


def main():
    database.init_db()  # tạo gym.db + 3 bảng nếu chưa có (không tạo database nào khác)

    cua_so = tk.Tk()
    cua_so.title("Quản lý phòng tập Gym")
    cua_so.geometry("920x560")

    # Lỗi bất ngờ trong lúc dùng -> hiện hộp thoại, không đóng chương trình khi đang demo
    def bao_loi(loai, gia_tri, _vet):
        messagebox.showerror("Có lỗi xảy ra", f"{loai.__name__}: {gia_tri}")
    cua_so.report_callback_exception = bao_loi

    notebook = ttk.Notebook(cua_so)
    notebook.pack(fill="both", expand=True, padx=6, pady=6)

    cac_tab = []
    for ten_tab, ung_vien in TABS:
        khung = tao_tab(notebook, ten_tab, ung_vien)
        notebook.add(khung, text=ten_tab)
        cac_tab.append(khung)

    # Bấm sang tab nào thì tab đó tải lại dữ liệu mới nhất
    def khi_doi_tab(_su_kien):
        khung = cac_tab[notebook.index(notebook.select())]
        if hasattr(khung, "lam_moi"):
            khung.lam_moi()
    notebook.bind("<<NotebookTabChanged>>", khi_doi_tab)

    cua_so.mainloop()


if __name__ == "__main__":
    main()
