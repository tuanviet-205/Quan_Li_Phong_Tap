"""
TEST TÍCH HỢP: ghép module của cả nhóm và chạy một quy trình hoàn chỉnh.
Người phụ trách: Luyện Tuấn Việt

Chạy:  python -m unittest tests.test_integration -v
Nếu test đầu tiên (API) báo lỗi, đọc phần "CÁCH SỬA" trong thông báo rồi sửa trước.
"""
import unittest

import utils
from tests import check_api
from tests.helpers import CoSoTest, import_dau_tien
from modules import search, statistics

members = import_dau_tien(["modules.members", "members"])
packages = import_dau_tien(["modules.packages", "packages"])
registrations = import_dau_tien(["modules.registrations", "registrations"])


class TestHopDongAPI(unittest.TestCase):
    def test_ten_ham_tham_so_cot_database_khop_nhau(self):
        cac_loi = check_api.kiem_tra_tat_ca()
        self.assertEqual(cac_loi, [], "\n\n" + "\n\n".join(cac_loi))


class TestNghiepVuCacModule(CoSoTest):
    """Thêm / sửa / xóa hội viên, gói tập, đăng ký - gọi đúng API chung của từng module."""

    def test_hoi_vien_them_sua_xoa(self):
        mid = members.them_hoi_vien("Nguyễn Văn A", "0901234567", email="a@gmail.com")
        self.assertEqual(members.lay_hoi_vien(mid)["ho_ten"], "Nguyễn Văn A")
        self.assertEqual(len(members.lay_tat_ca_hoi_vien()), 1)
        self.assertTrue(members.sua_hoi_vien(mid, ho_ten="Nguyễn Văn B", email="b@gmail.com"))
        self.assertEqual(members.lay_hoi_vien(mid)["email"], "b@gmail.com")
        self.assertTrue(members.xoa_hoi_vien(mid))
        self.assertIsNone(members.lay_hoi_vien(mid))

    def test_hoi_vien_du_lieu_sai(self):
        members.them_hoi_vien("A", "0901234567")
        for ten, sdt in (("B", "0901234567"), ("C", "123"), ("", "0911111111")):
            with self.assertRaises(ValueError, msg=f"({ten!r}, {sdt!r}) phải bị từ chối"):
                members.them_hoi_vien(ten, sdt)
        self.assertFalse(members.sua_hoi_vien(999, ho_ten="X"))
        self.assertFalse(members.xoa_hoi_vien(999))

    def test_goi_tap_them_sua_xoa(self):
        pid = packages.them_goi_tap("Gói 30 ngày", 300000, 30, "Tập 1 tháng")
        goi = packages.lay_goi_tap(pid)
        self.assertEqual((goi["gia"], goi["so_ngay"]), (300000, 30))
        self.assertTrue(packages.sua_goi_tap(pid, gia=350000))
        self.assertEqual(packages.lay_goi_tap(pid)["gia"], 350000)
        self.assertEqual(len(packages.lay_tat_ca_goi_tap()), 1)
        self.assertTrue(packages.xoa_goi_tap(pid))
        self.assertIsNone(packages.lay_goi_tap(pid))

    def test_goi_tap_du_lieu_sai_va_khong_xoa_goi_dang_dung(self):
        with self.assertRaises(ValueError):
            packages.them_goi_tap("Gói lỗi", -1, 30)
        with self.assertRaises(ValueError):
            packages.them_goi_tap("Gói lỗi", 100000, 0)
        pid = packages.them_goi_tap("Gói A", 100000, 30)
        with self.assertRaises(ValueError):
            packages.them_goi_tap("Gói A", 200000, 60)   # trùng tên
        mid = members.them_hoi_vien("A", "0901234567")
        registrations.dang_ky_goi_tap(mid, pid)
        with self.assertRaises(ValueError):
            packages.xoa_goi_tap(pid)                    # đang có người đăng ký

    def test_dang_ky_va_het_han(self):
        self.assertEqual(registrations.tinh_ngay_het_han("2026-11-20", 30), "2026-12-20")
        mid = members.them_hoi_vien("A", "0901234567")
        pid = packages.them_goi_tap("Gói 30 ngày", 300000, 30)
        rid = registrations.dang_ky_goi_tap(mid, pid)
        self.assertIsInstance(rid, int)
        hien_tai = registrations.lay_goi_hien_tai(mid)
        self.assertEqual(hien_tai["ngay_het_han"], utils.cong_ngay(utils.hom_nay(), 30))
        self.assertEqual(hien_tai["gia_luc_dang_ky"], 300000)
        self.assertEqual(len(registrations.lay_lich_su_dang_ky(mid)), 1)
        with self.assertRaises(ValueError):
            registrations.dang_ky_goi_tap(999, pid)
        with self.assertRaises(ValueError):
            registrations.dang_ky_goi_tap(mid, 999)

    def test_sap_het_han(self):
        a = members.them_hoi_vien("A", "0900000001")
        b = members.them_hoi_vien("B", "0900000002")
        goi_7 = packages.them_goi_tap("Gói 7 ngày", 100000, 7)
        goi_30 = packages.them_goi_tap("Gói 30 ngày", 300000, 30)
        registrations.dang_ky_goi_tap(a, goi_7)
        registrations.dang_ky_goi_tap(b, goi_30)
        ds = registrations.lay_sap_het_han(7)
        self.assertEqual([r["member_id"] for r in ds], [a])
        self.assertEqual(ds[0]["so_ngay_con_lai"], 7)

    def test_xoa_hoi_vien_xoa_luon_dang_ky(self):
        mid = members.them_hoi_vien("A", "0901234567")
        pid = packages.them_goi_tap("Gói A", 100000, 30)
        registrations.dang_ky_goi_tap(mid, pid)
        self.assertTrue(members.xoa_hoi_vien(mid))
        self.assertEqual(registrations.lay_lich_su_dang_ky(), [])
        self.assertTrue(packages.xoa_goi_tap(pid))   # hết người đăng ký thì xóa được


class TestQuyTrinhHoanChinh(CoSoTest):
    """Kịch bản demo: thêm dữ liệu bằng module -> tìm kiếm và thống kê phải thấy đúng."""

    def test_tu_them_du_lieu_den_thong_ke(self):
        an = members.them_hoi_vien("Nguyễn Văn An", "0901111111", gioi_tinh="Nam")
        binh = members.them_hoi_vien("Trần Thị Bình", "0902222222", gioi_tinh="Nữ")
        goi_thang = packages.them_goi_tap("Gói 1 tháng", 300000, 30)
        goi_tuan = packages.them_goi_tap("Gói 1 tuần", 100000, 7)
        registrations.dang_ky_goi_tap(an, goi_thang)
        registrations.dang_ky_goi_tap(binh, goi_tuan)

        # Tìm kiếm thấy hội viên vừa thêm bằng cả 3 cách
        self.assertEqual([h["id"] for h in search.tim_hoi_vien("nguyen van an")], [an])
        self.assertEqual([h["id"] for h in search.tim_hoi_vien("0902222222")], [binh])
        self.assertIn(an, [h["id"] for h in search.tim_hoi_vien(str(an))])

        tk = statistics.thong_ke_tong_quan()
        self.assertEqual(tk["tong_hoi_vien"], 2)
        self.assertEqual(tk["tong_goi_tap"], 2)
        self.assertEqual(tk["dang_con_han"], 2)
        self.assertEqual(tk["sap_het_han"], 1)       # gói 1 tuần còn 7 ngày
        self.assertEqual(tk["tong_doanh_thu"], 400000)
        theo_goi = {g["ten_goi"]: g for g in statistics.thong_ke_theo_goi()}
        self.assertEqual(theo_goi["Gói 1 tháng"]["so_luot"], 1)
        self.assertEqual(theo_goi["Gói 1 tuần"]["doanh_thu"], 100000)
        self.assertEqual(sum(t["so_luot"] for t in statistics.thong_ke_dang_ky_theo_thang()), 2)

        # Sửa tên -> tìm kiếm theo tên mới; xóa -> thống kê cập nhật
        members.sua_hoi_vien(an, ho_ten="Lê Minh Cường")
        self.assertEqual([h["id"] for h in search.tim_hoi_vien("minh cuong")], [an])
        self.assertEqual(search.tim_hoi_vien("nguyen van an"), [])
        members.xoa_hoi_vien(binh)
        tk = statistics.thong_ke_tong_quan()
        self.assertEqual((tk["tong_hoi_vien"], tk["tong_doanh_thu"]), (1, 300000))
        self.assertEqual(search.tim_hoi_vien("0902222222"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
