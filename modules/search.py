"""
MODULE TÌM KIẾM HỘI VIÊN
Người phụ trách: Luyện Tuấn Việt

Chỉ dùng database + (không import module khác).
Tìm theo: họ tên, ID, số điện thoại.
  - Họ tên: tìm "chứa", không phân biệt hoa/thường, KHÔNG cần gõ dấu
            (gõ "nguyen van an" vẫn ra "Nguyễn Văn An").
  - ID:     khớp chính xác (gõ 3 -> hội viên có id = 3).
  - SĐT:    tìm "chứa" (gõ 0912 hoặc 456789 đều được).
"""
import unicodedata

import database


def _chuan_hoa(chuoi):
    """Bỏ dấu tiếng Việt + chuyển chữ thường. Ví dụ: 'Nguyễn Đức' -> 'nguyen duc'."""
    chuoi = str(chuoi or "").replace("đ", "d").replace("Đ", "D")
    chuoi = unicodedata.normalize("NFD", chuoi)
    chuoi = "".join(c for c in chuoi if unicodedata.category(c) != "Mn")  # bỏ dấu
    return chuoi.lower().strip()


def tim_hoi_vien(tu_khoa):
    """Trả về list[dict] hội viên khớp từ khóa (cùng cấu trúc bảng members).
    ValueError("Từ khóa không được để trống") nếu từ khóa rỗng."""
    tu_khoa_goc = str(tu_khoa or "").strip()
    if tu_khoa_goc == "":
        raise ValueError("Từ khóa không được để trống")
    tu_khoa_chuan = _chuan_hoa(tu_khoa_goc)

    # Số lượng hội viên của phòng tập nhỏ, nên lấy hết rồi lọc bằng Python cho dễ hiểu
    ket_qua = []
    for hv in database.query_all("SELECT * FROM members ORDER BY id"):
        khop_ten = tu_khoa_chuan in _chuan_hoa(hv["ho_ten"])
        khop_sdt = tu_khoa_goc in str(hv["so_dien_thoai"])
        khop_id = tu_khoa_goc == str(hv["id"])
        if khop_ten or khop_sdt or khop_id:
            ket_qua.append(hv)
    return ket_qua
