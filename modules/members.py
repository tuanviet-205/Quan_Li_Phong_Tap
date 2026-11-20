"""
MODULE QUẢN LÝ HỘI VIÊN
Người phụ trách: Nguyễn Hữu Trường (hạng mục III - quản lý hội viên), review: Nguyễn Hữu Hùng
CHỈ Trường được sửa file này. KHÔNG import module khác (chỉ dùng database + utils).

QUY ƯỚC CHUNG (cả nhóm phải theo):
  - Hàm logic KHÔNG dùng print/input, chỉ nhận tham số và trả về dữ liệu.
  - Dữ liệu sai -> ném ValueError("thông báo tiếng Việt"). Menu sẽ bắt và in ra.
  - Một hội viên là dict: {id, ho_ten, gioi_tinh, ngay_sinh, so_dien_thoai, email, dia_chi, ngay_tao}
  - Ngày lưu 'YYYY-MM-DD'.
"""
import database
import utils

# Các cột được phép sửa
CAC_TRUONG_HOP_LE = ["ho_ten", "gioi_tinh", "ngay_sinh", "so_dien_thoai", "email", "dia_chi"]


def them_hoi_vien(ho_ten, so_dien_thoai, gioi_tinh="", ngay_sinh="", email="", dia_chi=""):
    """Thêm hội viên mới, trả về id (int).
    ValueError khi: họ tên rỗng, SĐT không phải 10 chữ số bắt đầu bằng 0,
    SĐT đã tồn tại (bắt sqlite3.IntegrityError rồi đổi thành ValueError)."""
    raise NotImplementedError("TODO (Trường): viết them_hoi_vien")


def lay_tat_ca_hoi_vien():
    """Trả về list[dict] tất cả hội viên, sắp xếp theo id."""
    raise NotImplementedError("TODO (Trường): viết lay_tat_ca_hoi_vien")


def lay_hoi_vien(member_id):
    """Trả về dict của hội viên, hoặc None nếu không có."""
    raise NotImplementedError("TODO (Trường): viết lay_hoi_vien")


def sua_hoi_vien(member_id, **cac_truong):
    """Sửa các trường truyền vào, ví dụ sua_hoi_vien(1, ho_ten="Nam", email="a@b.com").
    Trả về True nếu sửa được, False nếu không có hội viên đó.
    ValueError khi: không có trường nào, tên trường không nằm trong CAC_TRUONG_HOP_LE,
    SĐT sai định dạng hoặc trùng với người khác."""
    raise NotImplementedError("TODO (Trường): viết sua_hoi_vien")


def xoa_hoi_vien(member_id):
    """Xóa hội viên (các đăng ký của họ tự bị xóa theo nhờ ON DELETE CASCADE).
    Trả về True nếu xóa được, False nếu không có hội viên đó."""
    raise NotImplementedError("TODO (Trường): viết xoa_hoi_vien")
