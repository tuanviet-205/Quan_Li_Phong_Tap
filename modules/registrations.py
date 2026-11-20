"""
MODULE ĐĂNG KÝ GÓI TẬP + THEO DÕI HẾT HẠN
Người phụ trách: Đặng Tiến Sơn (hạng mục 3.1 - phần đăng ký và theo dõi thời hạn), review: Nguyễn Hữu Hùng
CHỈ Sơn được sửa file này. KHÔNG import members/packages: tự truy vấn bảng bằng database.

Một đăng ký là dict:
  {id, member_id, package_id, ngay_dang_ky, ngay_het_han, gia_luc_dang_ky,
   ho_ten, so_dien_thoai, ten_goi}          (ba cột cuối lấy bằng JOIN)

QUY ƯỚC:
  - ngay_het_han = ngay_dang_ky + so_ngay của gói (dùng utils.cong_ngay)
    Ví dụ đăng ký 2026-11-20, gói 30 ngày -> hết hạn 2026-12-20.
  - "Gói hiện tại" của hội viên = đăng ký có ngay_het_han lớn nhất.
  - Trạng thái: ngay_het_han < hôm nay -> "Hết hạn";
                còn <= config.NGAY_SAP_HET_HAN ngày -> "Sắp hết hạn"; còn lại -> "Còn hạn".
"""
import config
import database
import utils


def tinh_ngay_het_han(ngay_bat_dau, so_ngay):
    """('2026-11-20', 30) -> '2026-12-20'."""
    raise NotImplementedError("TODO (Sơn): viết tinh_ngay_het_han")


def trang_thai(ngay_het_han):
    """Trả về 'Còn hạn' | 'Sắp hết hạn' | 'Hết hạn' theo quy ước ở đầu file."""
    raise NotImplementedError("TODO (Sơn): viết trang_thai")


def dang_ky_goi_tap(member_id, package_id, ngay_dang_ky=None):
    """Đăng ký gói cho hội viên, trả về id đăng ký (int).
    ngay_dang_ky=None -> dùng utils.hom_nay().
    ValueError khi: hội viên không tồn tại, gói không tồn tại.
    Lưu giá gói tại thời điểm đăng ký vào gia_luc_dang_ky."""
    raise NotImplementedError("TODO (Sơn): viết dang_ky_goi_tap")


def lay_lich_su_dang_ky(member_id=None):
    """list[dict] đăng ký (mới nhất trước). member_id=None -> tất cả hội viên."""
    raise NotImplementedError("TODO (Sơn): viết lay_lich_su_dang_ky")


def lay_goi_hien_tai(member_id):
    """dict đăng ký có ngay_het_han lớn nhất của hội viên (kèm key 'trang_thai'),
    hoặc None nếu chưa từng đăng ký."""
    raise NotImplementedError("TODO (Sơn): viết lay_goi_hien_tai")


def lay_sap_het_han(so_ngay=None):
    """Danh sách hội viên có GÓI HIỆN TẠI hết hạn trong khoảng [hôm nay, hôm nay + so_ngay].
    so_ngay=None -> dùng config.NGAY_SAP_HET_HAN.
    Mỗi phần tử dict gồm: member_id, ho_ten, so_dien_thoai, ten_goi, ngay_het_han, so_ngay_con_lai.
    Sắp xếp theo ngay_het_han tăng dần."""
    raise NotImplementedError("TODO (Sơn): viết lay_sap_het_han")
