"""
KIỂM TRA SỰ THỐNG NHẤT GIỮA CÁC MODULE (tên hàm, tham số, cột database)
Người phụ trách: Luyện Tuấn Việt

Chạy:  python tests/check_api.py
Kết quả: danh sách lỗi, mỗi lỗi kèm CÁCH SỬA cụ thể. Không có lỗi -> "API khớp nhau".
Khi ghép code của cả nhóm, chạy file này ĐẦU TIÊN.
"""
import importlib
import inspect
import os
import sys
import tempfile

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GOC not in sys.path:
    sys.path.insert(0, GOC)

# Module -> (các đường dẫn có thể có, {tên hàm: [các tham số đầu tiên bắt buộc đúng tên]})
CAC_MODULE = {
    "members": (["modules.members", "members"], {
        "them_hoi_vien": ["ho_ten", "so_dien_thoai"],
        "lay_tat_ca_hoi_vien": [],
        "lay_hoi_vien": ["member_id"],
        "sua_hoi_vien": ["member_id"],
        "xoa_hoi_vien": ["member_id"],
    }),
    "packages": (["modules.packages", "packages"], {
        "them_goi_tap": ["ten_goi", "gia", "so_ngay"],
        "lay_tat_ca_goi_tap": [],
        "lay_goi_tap": ["package_id"],
        "sua_goi_tap": ["package_id"],
        "xoa_goi_tap": ["package_id"],
    }),
    "registrations": (["modules.registrations", "registrations"], {
        "tinh_ngay_het_han": ["ngay_bat_dau", "so_ngay"],
        "trang_thai": ["ngay_het_han"],
        "dang_ky_goi_tap": ["member_id", "package_id"],
        "lay_lich_su_dang_ky": [],
        "lay_goi_hien_tai": ["member_id"],
        "lay_sap_het_han": [],
    }),
    "search": (["modules.search"], {"tim_hoi_vien": ["tu_khoa"]}),
    "statistics": (["modules.statistics"], {
        "thong_ke_tong_quan": [], "thong_ke_theo_goi": [], "thong_ke_dang_ky_theo_thang": []}),
}

# Hàm/hằng dùng chung mà code của Việt gọi tới
CAC_DUNG_CHUNG = {
    "database": ["init_db", "query_all", "query_one", "insert", "execute"],
    "utils": ["hom_nay", "cong_ngay", "so_ngay_con_lai", "dinh_dang_ngay", "dinh_dang_tien"],
    "config": ["DB_FILE", "NGAY_SAP_HET_HAN"],
}

# Cột bắt buộc của từng bảng
CAC_COT = {
    "members": ["id", "ho_ten", "gioi_tinh", "ngay_sinh", "so_dien_thoai", "email", "dia_chi", "ngay_tao"],
    "packages": ["id", "ten_goi", "gia", "so_ngay", "mo_ta"],
    "registrations": ["id", "member_id", "package_id", "ngay_dang_ky", "ngay_het_han", "gia_luc_dang_ky"],
}


def _import_module(ung_vien):
    """Trả về (module, None) hoặc (None, thông báo lỗi)."""
    cac_loi = []
    for ten in ung_vien:
        try:
            return importlib.import_module(ten), None
        except ModuleNotFoundError as loi:
            if loi.name and (ten == loi.name or ten.startswith(loi.name + ".")):
                continue
            cac_loi.append(f"{ten} import lỗi: {loi!r}")
        except Exception as loi:  # noqa: BLE001
            cac_loi.append(f"{ten} import lỗi: {loi!r}")
    if cac_loi:
        return None, " | ".join(cac_loi)
    return None, "không tìm thấy file " + " hoặc ".join(ung_vien)


def _kiem_tra_module():
    cac_loi = []
    for ten, (ung_vien, cac_ham) in CAC_MODULE.items():
        module, loi = _import_module(ung_vien)
        if module is None:
            cac_loi.append(
                f"LỖI: module '{ten}' {loi}. CÁCH SỬA: tạo/sửa file {ung_vien[0].replace('.', '/')}.py "
                f"đúng tên và import được (chạy thử: python -c \"import {ung_vien[0]}\").")
            continue
        for ten_ham, tham_so_dau in cac_ham.items():
            ham = getattr(module, ten_ham, None)
            if not callable(ham):
                cac_loi.append(
                    f"LỖI: {module.__name__} thiếu hàm {ten_ham}(). "
                    f"CÁCH SỬA: thêm hàm đúng tên {ten_ham}({', '.join(tham_so_dau)}) vào file; "
                    f"nếu đã đặt tên khác thì đổi lại theo README (mục 4) để khỏi sửa chỗ gọi.")
                continue
            kinds = (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
            thuc_te = [p.name for p in inspect.signature(ham).parameters.values() if p.kind in kinds]
            if thuc_te[:len(tham_so_dau)] != tham_so_dau:
                cac_loi.append(
                    f"LỖI: {module.__name__}.{ten_ham} có tham số {thuc_te}, "
                    f"chuẩn là bắt đầu bằng {tham_so_dau}. CÁCH SỬA: đổi tên/thứ tự tham số cho đúng chuẩn.")
    return cac_loi


def _kiem_tra_dung_chung():
    cac_loi = []
    for ten, cac_ten in CAC_DUNG_CHUNG.items():
        module, loi = _import_module([ten])
        if module is None:
            cac_loi.append(f"LỖI: module '{ten}' {loi}. CÁCH SỬA: đặt {ten}.py ở thư mục gốc quan_ly_gym.")
            continue
        for thanh_phan in cac_ten:
            if not hasattr(module, thanh_phan):
                cac_loi.append(
                    f"LỖI: {ten}.py thiếu '{thanh_phan}'. CÁCH SỬA: thêm '{thanh_phan}' vào {ten}.py "
                    f"(xem bản gốc trong khung dự án) hoặc báo người phụ trách file đó.")
    return cac_loi


def _kiem_tra_database():
    """Tạo database tạm bằng database.init_db() rồi so cột với chuẩn."""
    import config
    import database
    cac_loi = []
    goc = config.DB_FILE
    config.DB_FILE = os.path.join(tempfile.mkdtemp(), "kiem_tra.db")
    try:
        database.init_db()
        for bang, cac_cot in CAC_COT.items():
            thuc_te = {d["name"] for d in database.query_all(f"PRAGMA table_info({bang})")}
            if not thuc_te:
                cac_loi.append(
                    f"LỖI: database thiếu bảng '{bang}'. CÁCH SỬA: thêm CREATE TABLE {bang} vào SCHEMA "
                    f"trong database.py, rồi xóa file gym.db để tạo lại.")
                continue
            thieu = [c for c in cac_cot if c not in thuc_te]
            if thieu:
                cac_loi.append(
                    f"LỖI: bảng '{bang}' thiếu cột {thieu} (đang có {sorted(thuc_te)}). CÁCH SỬA: thêm cột "
                    f"vào SCHEMA trong database.py rồi xóa gym.db; hoặc sửa code đang dùng tên cột khác "
                    f"cho khớp tên chuẩn.")
    except Exception as loi:  # noqa: BLE001
        cac_loi.append(f"LỖI: database.init_db() không chạy được: {loi!r}. CÁCH SỬA: kiểm tra SCHEMA trong database.py.")
    finally:
        config.DB_FILE = goc
    return cac_loi


def kiem_tra_tat_ca():
    """Trả về list thông báo lỗi (rỗng = mọi thứ khớp)."""
    cac_loi = _kiem_tra_dung_chung()
    if not cac_loi:  # database/utils/config hỏng thì các kiểm tra sau vô nghĩa
        cac_loi += _kiem_tra_database()
    cac_loi += _kiem_tra_module()
    return cac_loi


if __name__ == "__main__":
    ket_qua = kiem_tra_tat_ca()
    if ket_qua:
        print(f"Phát hiện {len(ket_qua)} chỗ chưa thống nhất:\n")
        for i, dong in enumerate(ket_qua, 1):
            print(f"{i}. {dong}\n")
        sys.exit(1)
    print("API khớp nhau: tên hàm, tham số và cột database đều đúng chuẩn.")
