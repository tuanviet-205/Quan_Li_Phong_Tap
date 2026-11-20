"""
TEST DATABASE (database.py)
Người phụ trách: Luyện Tuấn Việt (hạng mục IV - kiểm thử), review: Đặng Tiến Sơn, Nguyễn Hữu Trường
Gợi ý: Hùng (thiết kế database) có thể hỗ trợ viết các ca test này nếu rảnh.

Chạy:  python -m unittest tests.test_database -v
Dùng test_gym.db riêng (CoSoTest lo việc tạo/xóa), không đụng gym.db thật.
Dữ liệu mẫu: dùng các hàm them_*_sql trong tests/helpers.py.

Mỗi test dưới đây đang bị bỏ qua (skip). Khi viết xong test nào, xóa dòng self.skipTest(...).
"""
import unittest

from tests.helpers import CoSoTest, them_dang_ky_sql, them_goi_sql, them_hoi_vien_sql  # noqa: F401
import database  # noqa: F401


class TestDatabase(CoSoTest):
    def test_init_db_chay_nhieu_lan_khong_loi(self):
        """Gọi database.init_db() 2-3 lần liên tiếp: không lỗi, không mất dữ liệu đã có."""
        self.skipTest("TODO (Việt)")

    def test_sdt_trung_bi_tu_choi(self):
        """Thêm 2 hội viên cùng so_dien_thoai -> sqlite3.IntegrityError."""
        self.skipTest("TODO (Việt)")

    def test_ten_goi_trung_bi_tu_choi(self):
        """Thêm 2 gói cùng ten_goi -> sqlite3.IntegrityError."""
        self.skipTest("TODO (Việt)")

    def test_gia_am_hoac_so_ngay_khong_hop_le(self):
        """gia < 0 hoặc so_ngay <= 0 -> sqlite3.IntegrityError (ràng buộc CHECK)."""
        self.skipTest("TODO (Việt)")

    def test_xoa_hoi_vien_xoa_luon_dang_ky(self):
        """Xóa hội viên -> các dòng registrations của họ tự bị xóa (ON DELETE CASCADE)."""
        self.skipTest("TODO (Việt)")

    def test_khong_xoa_duoc_goi_dang_co_dang_ky(self):
        """Xóa gói đã có đăng ký -> sqlite3.IntegrityError (ON DELETE RESTRICT)."""
        self.skipTest("TODO (Việt)")

    def test_cac_ham_truy_van(self):
        """query_all trả list[dict]; query_one trả dict hoặc None; insert trả id; execute trả số dòng."""
        self.skipTest("TODO (Việt)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
