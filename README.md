# Dự án Quản lý phòng tập Gym (Python + SQLite)

Hạn hoàn thành: **trước 24/11/2026**. Công nghệ: Python 3.9+, VS Code, chỉ dùng thư viện có sẵn (`sqlite3`, `datetime`, `unittest`).

## 1. Cấu trúc thư mục

```
quan_ly_gym/
├── main.py                 # Cửa sổ Tkinter, cấu trúc chương trình và menu  (Cử)
├── utils.py                # Ngày tháng, định dạng, hàm tiện ích             (Hùng)
├── seed_data.py            # Tạo dữ liệu mẫu để demo                         (Trường)
├── config.py               # Đường dẫn DB, số ngày "sắp hết hạn"             (cả nhóm)
├── database.py             # Thiết kế dữ liệu: tạo bảng + 5 hàm truy vấn    (Hùng)
├── modules/                # LOGIC (không có giao diện)
│   ├── members.py          # Hội viên                                        (Trường)
│   ├── packages.py         # Gói tập                                         (Hùng)
│   ├── registrations.py    # Đăng ký gói + theo dõi hết hạn                  (Sơn)
│   ├── search.py           # Tìm kiếm hội viên                               (Việt)
│   └── statistics.py       # Thống kê                                        (Việt)
├── ui/                     # GIAO DIỆN Tkinter (mỗi file một lớp kế thừa tk.Frame, có lam_moi())
│   ├── member_view.py      # MemberView                                      (Trường)
│   ├── package_view.py     # PackageView                                     (Hùng)
│   ├── registration_view.py# RegistrationView                                (Sơn)
│   ├── search_view.py      # SearchView                                      (Việt)
│   └── statistics_view.py  # StatisticsView                                  (Việt)
├── tests/                  # Kiểm thử + HUONG_DAN_TICH_HOP.md               (Việt)
├── docs/TAI_LIEU.md        # Tài liệu / báo cáo (tổng hợp: Việt; mục 4: Hùng)
├── README.md
└── .vscode/launch.json     # Bấm F5 để chạy main.py
```

**Quy tắc vàng:** các file trong `modules/` **không import lẫn nhau**, chỉ dùng `database`, `utils`, `config`. File trong `ui/` chỉ gọi hàm của `modules/`, **không viết SQL**. Mỗi người chỉ sửa file của mình; `main.py` tự ghép tab, không cần sửa khi thêm view. Mẫu giao diện: xem `ui/search_view.py`. Hàm `menu_*` kiểu console trong các bảng bên dưới không còn dùng (giao diện là Tkinter).

## 2. Database (SQLite, file `gym.db` tự tạo)

```sql
members(id PK, ho_ten NOT NULL, gioi_tinh, ngay_sinh, so_dien_thoai NOT NULL UNIQUE, email, dia_chi, ngay_tao)
packages(id PK, ten_goi NOT NULL UNIQUE, gia >= 0, so_ngay > 0, mo_ta)
registrations(id PK, member_id -> members (CASCADE), package_id -> packages (RESTRICT),
              ngay_dang_ky, ngay_het_han, gia_luc_dang_ky)
```

- Ngày lưu dạng chuỗi `YYYY-MM-DD`; hiển thị `dd/mm/yyyy` (dùng `utils.dinh_dang_ngay`).
- Xóa hội viên thì đăng ký của họ bị xóa theo. Gói đã có đăng ký thì **không xóa được**.
- `ngay_het_han = ngay_dang_ky + so_ngay` của gói. "Gói hiện tại" của hội viên là đăng ký có `ngay_het_han` lớn nhất.

## 3. Quy ước chung

1. Hàm logic **không dùng `print`/`input`**: nhận tham số, trả dữ liệu.
2. Dữ liệu sai thì `raise ValueError("thông báo tiếng Việt")`. Hàm `menu_*` bắt lỗi và in bằng `utils.in_loi`.
3. Bản ghi luôn là `dict`, danh sách là `list[dict]`.
4. `sua_*` trả `True`/`False` (không tìm thấy), `xoa_*` trả `True`/`False`.
5. Chỉ sửa file của mình. Cần đổi API thì báo nhóm và sửa bảng ở mục 4.

## 4. API chung (đã khai báo sẵn trong từng file, kèm docstring)

| Module | Hàm | Trả về |
|---|---|---|
| members | `them_hoi_vien(ho_ten, so_dien_thoai, gioi_tinh="", ngay_sinh="", email="", dia_chi="")` | id |
| | `lay_tat_ca_hoi_vien()` / `lay_hoi_vien(id)` | list[dict] / dict hoặc None |
| | `sua_hoi_vien(id, **truong)` / `xoa_hoi_vien(id)` | bool |
| | `menu_hoi_vien()` | |
| packages | `them_goi_tap(ten_goi, gia, so_ngay, mo_ta="")` | id |
| | `lay_tat_ca_goi_tap()` / `lay_goi_tap(id)` | list[dict] / dict hoặc None |
| | `sua_goi_tap(id, **truong)` / `xoa_goi_tap(id)` | bool |
| | `menu_goi_tap()` | |
| registrations | `tinh_ngay_het_han(ngay_bat_dau, so_ngay)` | 'YYYY-MM-DD' |
| | `trang_thai(ngay_het_han)` | 'Còn hạn' / 'Sắp hết hạn' / 'Hết hạn' |
| | `dang_ky_goi_tap(member_id, package_id, ngay_dang_ky=None)` | id |
| | `lay_lich_su_dang_ky(member_id=None)` | list[dict] |
| | `lay_goi_hien_tai(member_id)` | dict hoặc None |
| | `lay_sap_het_han(so_ngay=None)` | list[dict] (member_id, ho_ten, so_dien_thoai, ten_goi, ngay_het_han, so_ngay_con_lai) |
| | `menu_dang_ky()` | |
| search | `tim_hoi_vien(tu_khoa)` | list[dict] |
| | `menu_tim_kiem()` | |
| stats | `thong_ke_tong_quan()` | dict: tong_hoi_vien, tong_goi_tap, dang_con_han, sap_het_han, da_het_han, tong_doanh_thu |
| | `thong_ke_theo_goi()` | list[dict]: ten_goi, so_luot, doanh_thu |
| | `menu_thong_ke()` | |
| database | `init_db()`, `query_all()`, `query_one()`, `insert()`, `execute()` | xem docstring |
| utils | `nhap_chuoi`, `nhap_so_nguyen`, `nhap_ngay`, `xac_nhan`, `in_bang`, `in_tieu_de`, `in_loi`, `in_thanh_cong`, `in_thong_bao`, `tam_dung`, `hom_nay`, `cong_ngay`, `dinh_dang_ngay`, `dinh_dang_tien`, `so_ngay_con_lai` | xem docstring |

## 5. Phân công (theo bảng công việc của nhóm - Báo cáo Nhóm 7 lần 1)

| STT | Hạng mục | Người thực hiện | Người review | File liên quan |
|---|---|---|---|---|
| I | Phân tích: thống nhất đề tài, mục tiêu, phạm vi (đã xong 13/11) | Cả nhóm | Phạm Văn Cử | - |
| 1.1 | Phân tích yêu cầu và thiết kế dữ liệu (hội viên, gói tập, đăng ký) | Nguyễn Hữu Hùng | Phạm Văn Cử | `database.py`, `docs/TAI_LIEU.md` mục 4 |
| II | Thiết kế: lập cấu trúc chương trình và menu | Phạm Văn Cử, Nguyễn Hữu Hùng | Cả nhóm | `main.py` (Cử), `utils.py` (Hùng) |
| III | Lập trình: quản lý hội viên (thêm, xem, sửa, xóa) | Nguyễn Hữu Trường | Nguyễn Hữu Hùng | `modules/members.py`, `ui/member_view.py` |
| 3.1a | Quản lý gói tập (thêm, xem, sửa, xóa, giá, thời hạn) | Nguyễn Hữu Hùng | Đặng Tiến Sơn | `modules/packages.py`, `ui/package_view.py` |
| 3.1b | Đăng ký gói tập, tính ngày hết hạn, theo dõi sắp hết hạn | Đặng Tiến Sơn | Nguyễn Hữu Hùng | `modules/registrations.py`, `ui/registration_view.py` |
| 3.2 | Tìm kiếm và thống kê cơ bản | Luyện Tuấn Việt | Nguyễn Hữu Trường | `modules/search.py`, `modules/statistics.py`, `ui/search_view.py`, `ui/statistics_view.py` |
| IV | Kiểm thử: lập danh sách ca kiểm thử, chạy thử các chức năng | Luyện Tuấn Việt | Đặng Tiến Sơn, Nguyễn Hữu Trường | `tests/` |
| V | Demo thử: tích hợp các phần, chạy thử và sửa lỗi | Cả nhóm | Phạm Văn Cử | `seed_data.py` (Trường), `tests/HUONG_DAN_TICH_HOP.md` |
| VI | Xây dựng slide trình bày theo mẫu | Phạm Văn Cử | Luyện Tuấn Việt | (ngoài code) |
| VII | Viết tài liệu báo cáo .docx: tổng hợp, hoàn thiện báo cáo và biên bản họp | Luyện Tuấn Việt | Cả nhóm | `docs/TAI_LIEU.md` |

Quy tắc: mỗi người chỉ **sửa file thuộc hạng mục của mình**; người review đọc code/tài liệu, góp ý và chạy thử, không tự sửa file của người khác (góp ý qua nhóm). Đổi tên hàm/cột database phải báo cả nhóm.

## 6. Timeline (hôm nay 20/11 là thứ Sáu)

| Ngày | Mục tiêu |
|---|---|
| **Thứ Sáu 20/11 (tối)** | Cả nhóm nhận bộ khung, cài Python/VS Code, chạy `python main.py` thấy menu. Đọc kỹ mục 3 và 4. Chốt API, không đổi nữa. |
| **Thứ Bảy 21/11** | Mỗi người code file của mình + chạy test riêng của mình. Cử: hoàn thiện `main`, dàn ý slide. Hùng: `utils`, rà soát `database`, code gói tập. Trường: code hội viên. Sơn: code đăng ký. **20:00: nộp file lên nhóm**, dù chưa xong vẫn phải import được. |
| **Chủ Nhật 22/11** | Sáng: **tích hợp lần 1** (Việt ghép, chạy toàn bộ test). Chiều: sửa lỗi, hoàn thiện menu và thông báo lỗi. Trường viết `seed_data.py`. Tối: slide bản nháp. |
| **Thứ Hai 23/11** | Sáng: tích hợp lần 2 + kiểm thử tay theo checklist. **12:00 chốt tính năng**. Chiều: sửa bug, tập demo. **20:00 đóng băng code**, chỉ sửa lỗi nghiêm trọng. |
| **Thứ Ba 24/11** | Ngày dự phòng: chạy thử trên máy thuyết trình, nộp bài. Nếu hạn nộp tính hết 23/11 thì tối 23/11 là bản nộp. |

## 7. Cách ghép, chạy, test

1. Gom toàn bộ file vào **một thư mục** `quan_ly_gym` (dùng Git/GitHub hoặc Drive; mỗi người chỉ ghi đè file của mình).
2. Mở VS Code: **File > Open Folder** > chọn `quan_ly_gym`.
3. Chạy chương trình: mở terminal trong VS Code, gõ `python main.py` (hoặc bấm F5).
4. Test riêng từng người (không cần chờ ai):
   - Trường (hội viên): `python -m unittest tests.test_integration -k hoi_vien -v`
   - Hùng (gói tập): `python -m unittest tests.test_integration -k goi_tap -v`
   - Sơn (đăng ký): `python -m unittest tests.test_integration -k dang_ky -k het_han -v`
   - Việt: `python -m unittest tests.test_search tests.test_statistics -v`
   - Hùng (database): `python -m unittest tests.test_database -v`
5. Trước khi test, chạy `python tests/check_api.py` để kiểm tra tên hàm/cột có khớp nhau. Test toàn bộ khi tích hợp: `python -m unittest discover -s tests -t . -v` (tất cả phải `OK`).
6. Test dùng `test_gym.db` riêng, không đụng `gym.db`. Muốn xóa dữ liệu demo: xóa file `gym.db`.

**Checklist kiểm thử tay (23/11):** thêm/sửa/xóa hội viên; nhập SĐT trùng và sai; thêm gói giá âm; xóa gói đã có người đăng ký; đăng ký gói; xem sắp hết hạn; tìm theo tên và SĐT; xem thống kê; nhập chữ khi cần số; thoát bằng 0.
