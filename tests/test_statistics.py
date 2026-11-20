"""
TEST THỐNG KÊ (modules/statistics.py)
Chạy:  python -m unittest tests.test_statistics -v
"""
import unittest

import utils
from tests.helpers import CoSoTest, them_dang_ky_sql, them_goi_sql, them_hoi_vien_sql
from modules import statistics

SAU_KEY = {"tong_hoi_vien", "tong_goi_tap", "dang_con_han", "sap_het_han", "da_het_han", "tong_doanh_thu"}


def ngay_lui(so_ngay):
    """Ngày cách hôm nay so_ngay ngày về trước, dạng 'YYYY-MM-DD'."""
    return utils.cong_ngay(utils.hom_nay(), -so_ngay)


class TestTongQuan(CoSoTest):
    def test_database_trong(self):
        tk = statistics.thong_ke_tong_quan()
        self.assertEqual(set(tk), SAU_KEY)
        self.assertTrue(all(v == 0 for v in tk.values()))

    def test_dem_con_han_sap_het_han_da_het_han(self):
        goi = them_goi_sql("Gói 30 ngày", 300000, 30)
        a = them_hoi_vien_sql("A", "0900000001")   # còn 30 ngày
        b = them_hoi_vien_sql("B", "0900000002")   # còn 5 ngày -> sắp hết hạn
        c = them_hoi_vien_sql("C", "0900000003")   # hết hạn 10 ngày trước
        them_hoi_vien_sql("D", "0900000004")       # chưa đăng ký
        them_dang_ky_sql(a, goi)
        them_dang_ky_sql(b, goi, ngay_dang_ky=ngay_lui(25))
        them_dang_ky_sql(c, goi, ngay_dang_ky=ngay_lui(40))

        tk = statistics.thong_ke_tong_quan()
        self.assertEqual(tk["tong_hoi_vien"], 4)
        self.assertEqual(tk["tong_goi_tap"], 1)
        self.assertEqual(tk["dang_con_han"], 2)    # A và B (gồm cả người sắp hết hạn)
        self.assertEqual(tk["sap_het_han"], 1)     # B
        self.assertEqual(tk["da_het_han"], 1)      # C
        self.assertEqual(tk["tong_doanh_thu"], 900000)

    def test_dung_goi_hien_tai_khi_da_gia_han(self):
        # Hội viên có gói cũ đã hết hạn nhưng đã đăng ký gói mới -> tính là còn hạn, không tính hết hạn
        goi = them_goi_sql()
        a = them_hoi_vien_sql()
        them_dang_ky_sql(a, goi, ngay_dang_ky=ngay_lui(60))
        them_dang_ky_sql(a, goi)
        tk = statistics.thong_ke_tong_quan()
        self.assertEqual(tk["dang_con_han"], 1)
        self.assertEqual(tk["da_het_han"], 0)
        self.assertEqual(tk["tong_doanh_thu"], 600000)

    def test_ngay_het_han_la_hom_nay_van_con_han(self):
        goi = them_goi_sql("Gói 30 ngày", 300000, 30)
        a = them_hoi_vien_sql()
        them_dang_ky_sql(a, goi, ngay_dang_ky=ngay_lui(30))  # hết hạn đúng hôm nay
        tk = statistics.thong_ke_tong_quan()
        self.assertEqual(tk["dang_con_han"], 1)
        self.assertEqual(tk["sap_het_han"], 1)
        self.assertEqual(tk["da_het_han"], 0)


class TestTheoGoi(CoSoTest):
    def test_theo_goi_gom_ca_goi_chua_ai_dang_ky(self):
        a = them_hoi_vien_sql("A", "0900000001")
        b = them_hoi_vien_sql("B", "0900000002")
        g1 = them_goi_sql("Gói A", 100000, 30)
        g2 = them_goi_sql("Gói B", 200000, 60)
        them_goi_sql("Gói C", 500000, 90)           # chưa ai đăng ký
        them_dang_ky_sql(a, g2, 60, 200000)
        them_dang_ky_sql(b, g2, 60, 200000)
        them_dang_ky_sql(a, g1, 30, 100000)

        ds = statistics.thong_ke_theo_goi()
        self.assertEqual([d["ten_goi"] for d in ds], ["Gói B", "Gói A", "Gói C"])  # giảm dần theo lượt
        kq = {d["ten_goi"]: d for d in ds}
        self.assertEqual((kq["Gói B"]["so_luot"], kq["Gói B"]["doanh_thu"]), (2, 400000))
        self.assertEqual((kq["Gói A"]["so_luot"], kq["Gói A"]["doanh_thu"]), (1, 100000))
        self.assertEqual((kq["Gói C"]["so_luot"], kq["Gói C"]["doanh_thu"]), (0, 0))

    def test_doanh_thu_theo_gia_luc_dang_ky(self):
        # Giá gói tăng sau khi đăng ký thì doanh thu cũ không đổi
        a = them_hoi_vien_sql()
        g = them_goi_sql("Gói A", 100000, 30)
        them_dang_ky_sql(a, g, 30, 100000)
        import database
        database.execute("UPDATE packages SET gia = 999999 WHERE id = ?", (g,))
        self.assertEqual(statistics.thong_ke_theo_goi()[0]["doanh_thu"], 100000)

    def test_khong_co_goi_nao(self):
        self.assertEqual(statistics.thong_ke_theo_goi(), [])


class TestTheoThang(CoSoTest):
    def test_luot_va_doanh_thu_theo_thang(self):
        a = them_hoi_vien_sql("A", "0900000001")
        b = them_hoi_vien_sql("B", "0900000002")
        g = them_goi_sql("Gói A", 100000, 30)
        them_dang_ky_sql(a, g, 30, 100000, ngay_dang_ky="2026-10-15")
        them_dang_ky_sql(a, g, 30, 100000, ngay_dang_ky="2026-11-02")
        them_dang_ky_sql(b, g, 30, 150000, ngay_dang_ky="2026-11-20")

        ds = statistics.thong_ke_dang_ky_theo_thang()
        self.assertEqual([d["thang"] for d in ds], ["2026-11", "2026-10"])  # mới nhất trước
        self.assertEqual((ds[0]["so_luot"], ds[0]["doanh_thu"]), (2, 250000))
        self.assertEqual((ds[1]["so_luot"], ds[1]["doanh_thu"]), (1, 100000))

    def test_khong_co_dang_ky(self):
        self.assertEqual(statistics.thong_ke_dang_ky_theo_thang(), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
