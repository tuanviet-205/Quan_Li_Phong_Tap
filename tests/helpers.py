"""
HÀM DÙNG CHUNG CHO CÁC FILE TEST
Người phụ trách: Luyện Tuấn Việt

- Test dùng file database riêng test_gym.db, KHÔNG đụng vào gym.db thật.
- Dữ liệu mẫu được thêm bằng SQL trực tiếp, nên test của module này không phụ thuộc module khác.
"""
import importlib
import os
import sys
import unittest

GOC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # thư mục quan_ly_gym
if GOC not in sys.path:
    sys.path.insert(0, GOC)

import config  # noqa: E402

config.DB_FILE = os.path.join(GOC, "test_gym.db")  # đổi sang database thử nghiệm

import database  # noqa: E402
import utils  # noqa: E402


def import_dau_tien(ung_vien):
    """Thử import lần lượt các tên module, trả về module đầu tiên có; không có -> None.
    Ví dụ: import_dau_tien(["modules.members", "members"])"""
    for ten in ung_vien:
        try:
            return importlib.import_module(ten)
        except ModuleNotFoundError as loi:
            if loi.name and (ten == loi.name or ten.startswith(loi.name + ".")):
                continue  # chỉ là chưa có file này, thử tên tiếp theo
            raise
    return None


# ----------------------------------------------------------- DỮ LIỆU MẪU BẰNG SQL
def them_hoi_vien_sql(ten="Nguyễn Văn A", sdt="0900000001", gioi_tinh="", email=""):
    return database.insert(
        "INSERT INTO members (ho_ten, so_dien_thoai, gioi_tinh, email) VALUES (?, ?, ?, ?)",
        (ten, sdt, gioi_tinh, email))


def them_goi_sql(ten="Gói 30 ngày", gia=300000, so_ngay=30):
    return database.insert(
        "INSERT INTO packages (ten_goi, gia, so_ngay) VALUES (?, ?, ?)", (ten, gia, so_ngay))


def them_dang_ky_sql(member_id, package_id, so_ngay=30, gia=300000, ngay_dang_ky=None):
    """ngay_dang_ky mặc định là hôm nay; ngay_het_han = ngay_dang_ky + so_ngay."""
    ngay_dang_ky = ngay_dang_ky or utils.hom_nay()
    return database.insert(
        "INSERT INTO registrations (member_id, package_id, ngay_dang_ky, ngay_het_han, gia_luc_dang_ky) "
        "VALUES (?, ?, ?, ?, ?)",
        (member_id, package_id, ngay_dang_ky, utils.cong_ngay(ngay_dang_ky, so_ngay), gia))


class CoSoTest(unittest.TestCase):
    """Mỗi test bắt đầu với database trống."""

    def setUp(self):
        if os.path.exists(config.DB_FILE):
            os.remove(config.DB_FILE)
        database.init_db()

    def tearDown(self):
        if os.path.exists(config.DB_FILE):
            os.remove(config.DB_FILE)
