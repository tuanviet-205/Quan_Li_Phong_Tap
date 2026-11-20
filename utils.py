"""
HÀM TIỆN ÍCH DÙNG CHUNG (nhập liệu, in bảng, xử lý ngày)
Người phụ trách: Nguyễn Hữu Hùng (hạng mục II - cấu trúc chương trình và menu, cùng Phạm Văn Cử phụ trách main.py), review: cả nhóm

Quy ước ngày:
  - Trong database và trong code logic: chuỗi 'YYYY-MM-DD'  (vd '2026-11-20')
  - Hiển thị cho người dùng:            'dd/mm/yyyy'        (vd '20/11/2026')
"""
from datetime import date, datetime, timedelta

DINH_DANG_DB = "%Y-%m-%d"
DINH_DANG_HIEN_THI = "%d/%m/%Y"


# ---------------------------------------------------------------- NGÀY THÁNG
def hom_nay():
    """Ngày hôm nay dạng 'YYYY-MM-DD'."""
    return date.today().strftime(DINH_DANG_DB)


def dinh_dang_ngay(ngay_db):
    """'2026-11-20' -> '20/11/2026'. Chuỗi rỗng/None -> ''."""
    if not ngay_db:
        return ""
    return datetime.strptime(ngay_db, DINH_DANG_DB).strftime(DINH_DANG_HIEN_THI)


def chuyen_ngay_ui_sang_db(chuoi_ui):
    """'20/11/2026' -> '2026-11-20'. Sai định dạng -> ValueError."""
    return datetime.strptime(chuoi_ui.strip(), DINH_DANG_HIEN_THI).strftime(DINH_DANG_DB)


def cong_ngay(ngay_db, so_ngay):
    """Cộng thêm so_ngay vào ngày 'YYYY-MM-DD', trả về 'YYYY-MM-DD'."""
    d = datetime.strptime(ngay_db, DINH_DANG_DB) + timedelta(days=so_ngay)
    return d.strftime(DINH_DANG_DB)


def so_ngay_con_lai(ngay_het_han_db):
    """Số ngày từ hôm nay đến ngày hết hạn (âm nếu đã hết hạn)."""
    han = datetime.strptime(ngay_het_han_db, DINH_DANG_DB).date()
    return (han - date.today()).days


def dinh_dang_tien(so):
    """300000 -> '300.000 đ'."""
    return f"{so:,}".replace(",", ".") + " đ"


# ------------------------------------------------------------------ NHẬP LIỆU
def nhap_chuoi(thong_bao, bat_buoc=True, mac_dinh=None):
    """Nhập chuỗi. bat_buoc=True: không cho để trống.
    mac_dinh: nếu có, bấm Enter sẽ giữ giá trị cũ (dùng khi sửa)."""
    hien_thi = f"{thong_bao} [{mac_dinh}]: " if mac_dinh not in (None, "") else f"{thong_bao}: "
    while True:
        gia_tri = input(hien_thi).strip()
        if gia_tri == "" and mac_dinh is not None:
            return mac_dinh
        if gia_tri == "" and bat_buoc:
            in_loi("Không được để trống, vui lòng nhập lại.")
            continue
        return gia_tri


def nhap_so_nguyen(thong_bao, toi_thieu=None, mac_dinh=None):
    """Nhập số nguyên, nhập sai thì hỏi lại."""
    hien_thi = f"{thong_bao} [{mac_dinh}]: " if mac_dinh is not None else f"{thong_bao}: "
    while True:
        gia_tri = input(hien_thi).strip()
        if gia_tri == "" and mac_dinh is not None:
            return mac_dinh
        try:
            so = int(gia_tri)
        except ValueError:
            in_loi("Vui lòng nhập một số nguyên.")
            continue
        if toi_thieu is not None and so < toi_thieu:
            in_loi(f"Giá trị phải >= {toi_thieu}.")
            continue
        return so


def nhap_ngay(thong_bao, bat_buoc=False):
    """Nhập ngày dạng dd/mm/yyyy, trả về 'YYYY-MM-DD'.
    Nếu bat_buoc=False và để trống -> trả về ''."""
    while True:
        gia_tri = input(f"{thong_bao} (dd/mm/yyyy): ").strip()
        if gia_tri == "" and not bat_buoc:
            return ""
        try:
            return chuyen_ngay_ui_sang_db(gia_tri)
        except ValueError:
            in_loi("Ngày không hợp lệ, ví dụ đúng: 20/11/2026.")


def xac_nhan(thong_bao):
    """Hỏi có/không. Trả về True nếu người dùng gõ 'y' hoặc 'c'."""
    tra_loi = input(f"{thong_bao} (y/n): ").strip().lower()
    return tra_loi in ("y", "c", "yes", "co", "có")


# -------------------------------------------------------------------- HIỂN THỊ
def in_tieu_de(tieu_de):
    """In tiêu đề một màn hình."""
    print()
    print("=" * 60)
    print(f"  {tieu_de.upper()}")
    print("=" * 60)


def in_loi(noi_dung):
    print(f"  [LỖI] {noi_dung}")


def in_thanh_cong(noi_dung):
    print(f"  [OK] {noi_dung}")


def in_thong_bao(noi_dung):
    print(f"  [i] {noi_dung}")


def tam_dung():
    input("\n  Nhấn Enter để tiếp tục...")


def in_bang(danh_sach, cot):
    """In danh sách dict thành bảng text.
    cot: list các cặp (ten_khoa, tieu_de_cot)
    Ví dụ: in_bang(ds, [("id", "ID"), ("ho_ten", "Họ tên")])"""
    if not danh_sach:
        print("  (Không có dữ liệu)")
        return
    do_rong = []
    for khoa, tieu_de in cot:
        gia_tri = [len(_chuoi(d.get(khoa))) for d in danh_sach]
        do_rong.append(max([len(tieu_de)] + gia_tri))
    dong_tieu_de = " | ".join(t.ljust(w) for (_, t), w in zip(cot, do_rong))
    print("  " + dong_tieu_de)
    print("  " + "-+-".join("-" * w for w in do_rong))
    for d in danh_sach:
        dong = " | ".join(_chuoi(d.get(k)).ljust(w) for (k, _), w in zip(cot, do_rong))
        print("  " + dong)


def _chuoi(gia_tri):
    return "" if gia_tri is None else str(gia_tri)
