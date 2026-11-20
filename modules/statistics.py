"""
MODULE THỐNG KÊ CƠ BẢN
Người phụ trách: Luyện Tuấn Việt

Chỉ đọc dữ liệu (SELECT) bằng database, không sửa gì trong database.
Quy ước: "gói hiện tại" của hội viên = đăng ký có ngay_het_han lớn nhất.

Lưu ý tên file: dùng `from modules import statistics` (không chạy trực tiếp file này
từ trong thư mục modules/ để tránh trùng với thư viện statistics của Python).
"""
import config
import database
import utils


def thong_ke_tong_quan():
    """Trả về dict gồm đúng 6 key (đều là số nguyên):
      tong_hoi_vien, tong_goi_tap,
      dang_con_han (gói hiện tại còn hạn, đã gồm cả sắp hết hạn),
      sap_het_han (còn <= config.NGAY_SAP_HET_HAN ngày),
      da_het_han (gói hiện tại đã hết hạn),
      tong_doanh_thu (tổng gia_luc_dang_ky, VNĐ).
    Hội viên chưa từng đăng ký không tính vào dang_con_han / da_het_han."""
    dang_con_han = 0
    sap_het_han = 0
    da_het_han = 0

    # Mỗi hội viên lấy ngày hết hạn xa nhất = gói hiện tại
    goi_hien_tai = database.query_all(
        "SELECT member_id, MAX(ngay_het_han) AS ngay_het_han "
        "FROM registrations GROUP BY member_id")
    for dong in goi_hien_tai:
        con_lai = utils.so_ngay_con_lai(dong["ngay_het_han"])
        if con_lai < 0:
            da_het_han += 1
        else:
            dang_con_han += 1
            if con_lai <= config.NGAY_SAP_HET_HAN:
                sap_het_han += 1

    return {
        "tong_hoi_vien": database.query_one("SELECT COUNT(*) AS n FROM members")["n"],
        "tong_goi_tap": database.query_one("SELECT COUNT(*) AS n FROM packages")["n"],
        "dang_con_han": dang_con_han,
        "sap_het_han": sap_het_han,
        "da_het_han": da_het_han,
        "tong_doanh_thu": database.query_one(
            "SELECT COALESCE(SUM(gia_luc_dang_ky), 0) AS n FROM registrations")["n"],
    }


def thong_ke_theo_goi():
    """list[dict] mỗi gói một dòng: {ten_goi, so_luot, doanh_thu}.
    Gói chưa ai đăng ký vẫn hiện (so_luot = 0). Sắp theo so_luot giảm dần."""
    return database.query_all(
        "SELECT p.ten_goi AS ten_goi, "
        "       COUNT(r.id) AS so_luot, "
        "       COALESCE(SUM(r.gia_luc_dang_ky), 0) AS doanh_thu "
        "FROM packages p LEFT JOIN registrations r ON r.package_id = p.id "
        "GROUP BY p.id ORDER BY so_luot DESC, p.ten_goi")


def thong_ke_dang_ky_theo_thang():
    """list[dict] mỗi tháng một dòng: {thang ('YYYY-MM'), so_luot, doanh_thu}.
    Tháng mới nhất đứng đầu."""
    return database.query_all(
        "SELECT substr(ngay_dang_ky, 1, 7) AS thang, "
        "       COUNT(*) AS so_luot, "
        "       COALESCE(SUM(gia_luc_dang_ky), 0) AS doanh_thu "
        "FROM registrations GROUP BY thang ORDER BY thang DESC")
