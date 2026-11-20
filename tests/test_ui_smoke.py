"""
SMOKE TEST GIAO DIỆN TKINTER: mở thử các màn hình, kiểm tra không bị lỗi.
Người phụ trách: Luyện Tuấn Việt

Chạy:  python -m unittest tests.test_ui_smoke -v
Tự bỏ qua (skip) nếu máy không có tkinter hoặc không có màn hình.
"""
import unittest

from tests.helpers import CoSoTest, them_dang_ky_sql, them_goi_sql, them_hoi_vien_sql

try:
    import tkinter as tk
    _GOC = tk.Tk()
    _GOC.withdraw()
    CO_MAN_HINH = True
except Exception:  # không có tkinter hoặc không có display
    tk = None
    _GOC = None
    CO_MAN_HINH = False


def tat_ca_gia_tri(bang):
    return [bang.item(d)["values"] for d in bang.get_children()]


@unittest.skipUnless(CO_MAN_HINH, "Máy không có tkinter/màn hình")
class TestGiaoDien(CoSoTest):
    def test_tim_kiem_hien_dung_ket_qua(self):
        from ui.search_view import SearchView
        them_hoi_vien_sql("Nguyễn Văn An", "0900000001")
        them_hoi_vien_sql("Trần Thị Bình", "0900000002")
        view = SearchView(_GOC)

        view.o_nhap.insert(0, "nguyen van")
        view.tim()
        self.assertEqual(len(view.bang.get_children()), 1)
        self.assertIn("Tìm thấy 1", view.nhan_ket_qua.cget("text"))

        view.o_nhap.delete(0, "end")
        view.o_nhap.insert(0, "khongco")
        view.tim()
        self.assertEqual(len(view.bang.get_children()), 0)
        self.assertIn("Không tìm thấy", view.nhan_ket_qua.cget("text"))

        view.o_nhap.delete(0, "end")
        view.tim()   # để trống -> báo lỗi nhẹ nhàng, không văng chương trình
        self.assertIn("Lỗi", view.nhan_ket_qua.cget("text"))
        view.xoa_tim()
        view.lam_moi()

    def test_thong_ke_hien_dung_so(self):
        from ui.statistics_view import StatisticsView
        a = them_hoi_vien_sql()
        g = them_goi_sql("Gói A", 100000, 30)
        them_dang_ky_sql(a, g, 30, 100000)
        view = StatisticsView(_GOC)
        self.assertEqual(view.nhan_so["tong_hoi_vien"].cget("text"), "1")
        self.assertEqual(view.nhan_so["dang_con_han"].cget("text"), "1")
        self.assertEqual(view.nhan_so["tong_doanh_thu"].cget("text"), "100.000 đ")
        self.assertEqual(tat_ca_gia_tri(view.bang_goi)[0][0], "Gói A")

        them_dang_ky_sql(a, g, 30, 100000)
        view.lam_moi()   # thêm dữ liệu rồi làm mới -> số phải tăng
        self.assertEqual(view.nhan_so["tong_doanh_thu"].cget("text"), "200.000 đ")

    def test_main_tao_tab_khong_sap_khi_thieu_file(self):
        import main
        khung = main.tao_tab(_GOC, "Thử", [("ui.khong_ton_tai_view", "KhongCo")])
        self.assertIsInstance(khung, tk.Frame)
        khung_ok = main.tao_tab(_GOC, "Tìm kiếm", dict(main.TABS)["Tìm kiếm"])
        self.assertTrue(hasattr(khung_ok, "lam_moi"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
