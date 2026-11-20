"""
TEST TÌM KIẾM (modules/search.py)
Chạy:  python -m unittest tests.test_search -v
"""
import unittest

from tests.helpers import CoSoTest, them_hoi_vien_sql
from modules import search


class TestTimKiem(CoSoTest):
    def setUp(self):
        super().setUp()
        self.an = them_hoi_vien_sql("Nguyễn Văn An", "0900000001")
        self.binh = them_hoi_vien_sql("Trần Thị Bình", "0912345678")
        self.duc = them_hoi_vien_sql("Lê Đức Thắng", "0987654321")

    def _ids(self, tu_khoa):
        return [hv["id"] for hv in search.tim_hoi_vien(tu_khoa)]

    def test_tim_theo_ten_khong_phan_biet_hoa_thuong(self):
        self.assertEqual(self._ids("văn an"), [self.an])
        self.assertEqual(self._ids("TRẦN THỊ"), [self.binh])

    def test_tim_theo_ten_khong_can_go_dau(self):
        self.assertEqual(self._ids("nguyen van an"), [self.an])
        self.assertEqual(self._ids("duc thang"), [self.duc])   # chữ Đ/đ
        self.assertEqual(self._ids("binh"), [self.binh])

    def test_tim_theo_so_dien_thoai(self):
        self.assertEqual(self._ids("0912345678"), [self.binh])   # đủ số
        self.assertEqual(self._ids("345678"), [self.binh])       # một phần
        self.assertEqual(self._ids("0900000001"), [self.an])

    def test_tim_theo_id(self):
        self.assertIn(self.duc, self._ids(str(self.duc)))

    def test_id_khop_chinh_xac_khong_khop_mot_phan(self):
        # Tạo đủ 11 hội viên để có id=1 và id=11: tìm "11" không được ra id=1
        for i in range(8):
            them_hoi_vien_sql(f"Người {i}", f"0933000{i:03d}")
        self.assertEqual(len(search.tim_hoi_vien("Người")), 8)
        ids = self._ids("11")
        self.assertIn(11, ids)
        self.assertNotIn(1, ids)

    def test_khong_tim_thay(self):
        self.assertEqual(search.tim_hoi_vien("khongcoai"), [])
        self.assertEqual(search.tim_hoi_vien("99999"), [])

    def test_ket_qua_co_day_du_cot(self):
        hv = search.tim_hoi_vien("văn an")[0]
        for cot in ("id", "ho_ten", "so_dien_thoai", "gioi_tinh", "email", "ngay_tao"):
            self.assertIn(cot, hv)

    def test_tu_khoa_rong(self):
        for tu_khoa in ("", "   ", None):
            with self.assertRaises(ValueError):
                search.tim_hoi_vien(tu_khoa)

    def test_ky_tu_dac_biet_khong_gay_loi(self):
        self.assertEqual(search.tim_hoi_vien("' OR 1=1 --"), [])
        self.assertEqual(search.tim_hoi_vien("%"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
