"""
MODULE QUẢN LÝ GÓI TẬP
Người phụ trách: Nguyễn Hữu Hùng (hạng mục 3.1 - phần gói tập), review: Đặng Tiến Sơn
CHỈ Hùng được sửa file này. KHÔNG import module khác (chỉ dùng database + utils).

Một gói tập là dict: {id, ten_goi, gia, so_ngay, mo_ta}
  - gia: số nguyên VNĐ (>= 0)
  - so_ngay: thời hạn của gói tính bằng ngày (> 0)
Dữ liệu sai -> ném ValueError("thông báo tiếng Việt").
"""
import database
import utils

CAC_TRUONG_HOP_LE = ["ten_goi", "gia", "so_ngay", "mo_ta"]


def them_goi_tap(ten_goi, gia, so_ngay, mo_ta=""):
    """Thêm gói tập mới, trả về id (int).
    ValueError khi: tên rỗng, gia < 0, so_ngay <= 0, tên gói đã tồn tại."""
    raise NotImplementedError("TODO (Hùng): viết them_goi_tap")


def lay_tat_ca_goi_tap():
    """Trả về list[dict] tất cả gói tập, sắp xếp theo id."""
    raise NotImplementedError("TODO (Hùng): viết lay_tat_ca_goi_tap")


def lay_goi_tap(package_id):
    """Trả về dict của gói tập, hoặc None nếu không có."""
    raise NotImplementedError("TODO (Hùng): viết lay_goi_tap")


def sua_goi_tap(package_id, **cac_truong):
    """Sửa các trường truyền vào. Trả về True nếu sửa được, False nếu không có gói đó.
    ValueError khi: không có trường nào, tên trường sai, giá/số ngày không hợp lệ, tên trùng.
    Lưu ý: đăng ký cũ giữ nguyên giá cũ (cột gia_luc_dang_ky)."""
    raise NotImplementedError("TODO (Hùng): viết sua_goi_tap")


def xoa_goi_tap(package_id):
    """Xóa gói tập. Trả về True nếu xóa được, False nếu không có gói đó.
    ValueError("Gói đang có hội viên đăng ký, không thể xóa") nếu gói đã được đăng ký
    (kiểm tra bảng registrations hoặc bắt sqlite3.IntegrityError)."""
    raise NotImplementedError("TODO (Hùng): viết xoa_goi_tap")
