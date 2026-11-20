"""
TẠO DỮ LIỆU MẪU ĐỂ DEMO
Người phụ trách: Nguyễn Hữu Trường (hạng mục V - dữ liệu mẫu cho demo), review: Phạm Văn Cử

Chạy:  python seed_data.py
Sau khi các module xong, Trường dùng members.them_hoi_vien, packages.them_goi_tap,
registrations.dang_ky_goi_tap để tạo ~8 hội viên, 3-4 gói tập, vài đăng ký
(trong đó có người sắp hết hạn, người đã hết hạn) cho buổi thuyết trình.
"""
import database


def tao_du_lieu_mau():
    database.init_db()
    # TODO (Trường): thêm dữ liệu mẫu ở đây khi các module đã chạy được
    print("Chưa có dữ liệu mẫu (TODO).")


if __name__ == "__main__":
    tao_du_lieu_mau()
