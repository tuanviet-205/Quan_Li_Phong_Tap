# Hướng dẫn tích hợp, chạy và demo (Việt viết; hạng mục IV - Kiểm thử)

## 1. Cấu trúc sau khi ghép

```
quan_ly_gym/
├── main.py                  # cửa sổ Tkinter, ghép các tab         (Cử)
├── config.py  database.py  utils.py     # dùng chung (database.py chỉ có 1 file, 1 bộ bảng)
├── modules/                 # LOGIC, không có giao diện
│   ├── members.py (Trường)  packages.py (Hùng)  registrations.py (Sơn)
│   ├── search.py  statistics.py                    (Việt)
├── ui/                      # GIAO DIỆN Tkinter
│   ├── member_view.py (Trường)  package_view.py (Hùng)  registration_view.py (Sơn)
│   ├── search_view.py  statistics_view.py                      (Việt)
└── tests/                   # kiểm thử (Việt)
```

Nếu `members.py`, `packages.py`, `registrations.py` đang nằm ở thư mục gốc (theo bản khung ban đầu) thì chưa cần chuyển: `main.py` và test tự tìm cả `modules/xxx.py` lẫn `xxx.py`.

## 2. Cài đặt

- Python 3.9 trở lên. Tkinter đi kèm bản cài Python trên Windows/macOS (kiểm tra: `python -m tkinter` thấy cửa sổ nhỏ hiện ra).
- Ubuntu/Debian nếu thiếu: `sudo apt install python3-tk`.
- Không cần `pip install` gì thêm.

## 3. Chạy chương trình

```
cd quan_ly_gym
python main.py
```
Phải chạy **từ thư mục `quan_ly_gym`** (nếu không sẽ lỗi `No module named 'modules'`). Trong VS Code: mở thư mục `quan_ly_gym`, bấm F5.

`gym.db` tự tạo lần đầu. Muốn bắt đầu lại từ đầu: đóng chương trình, xóa file `gym.db`.

## 4. Quy trình tích hợp (làm đúng thứ tự)

| Bước | Lệnh | Mục đích |
|---|---|---|
| 1 | `python tests/check_api.py` | Tên hàm, tham số, cột database có khớp chuẩn không. Mỗi lỗi có dòng **CÁCH SỬA** |
| 2 | `python -m unittest discover -s tests -t . -v` | Chạy toàn bộ test (logic + tích hợp + giao diện) |
| 3 | `python main.py` | Chạy thật, bấm qua 5 tab |

Test riêng: `python -m unittest tests.test_search -v`, `tests.test_statistics`, `tests.test_integration`, `tests.test_ui_smoke`.
Test dùng `test_gym.db` riêng, không làm hỏng `gym.db`.

## 5. Quy ước để `main.py` tự ghép tab (cho Trường, Hùng, Sơn)

Mỗi giao diện là một file trong `ui/` với **một lớp kế thừa `tk.Frame`**, khởi tạo bằng `TenView(parent)` và có hàm `lam_moi()` (tải lại dữ liệu khi người dùng bấm sang tab).

| Tab | File | Lớp |
|---|---|---|
| Hội viên | `ui/member_view.py` | `MemberView` |
| Gói tập | `ui/package_view.py` | `PackageView` |
| Đăng ký | `ui/registration_view.py` | `RegistrationView` |

Đặt đúng tên là tab tự xuất hiện, không phải sửa `main.py`. Dùng tên khác thì báo Cử thêm một dòng vào danh sách `TABS` ở đầu `main.py`.
Tab chưa có file hiện dòng "chưa có file giao diện"; tab có file nhưng lỗi hiện nguyên văn lỗi (và in ra terminal) để sửa nhanh.

## 6. Lỗi thường gặp

| Thông báo | Nguyên nhân | Cách sửa |
|---|---|---|
| `No module named 'modules'` / `'ui'` | Chạy sai thư mục | `cd quan_ly_gym` rồi chạy lại |
| `No module named 'tkinter'` | Python chưa cài Tkinter | Cài lại Python (tick tcl/tk) hoặc `sudo apt install python3-tk` |
| `no such column: ...` / `has no column named ...` | `gym.db` cũ tạo trước khi đổi SCHEMA | Xóa `gym.db` |
| Tab hiện chữ đỏ "import lỗi" | File view/module có lỗi cú pháp hoặc import sai | Đọc dòng lỗi dưới tiêu đề đỏ, sửa file đó |
| `UNIQUE constraint failed` | Trùng SĐT hoặc tên gói | Module phụ trách phải bắt `sqlite3.IntegrityError` và đổi thành `ValueError` |
| Thống kê sai số | Đăng ký lưu `ngay_het_han` sai định dạng | Phải là `YYYY-MM-DD` (dùng `utils.cong_ngay`) |

## 7. Checklist demo (tối 23/11 chạy thử một lần, sáng 24/11 chạy lại)

**Trước giờ demo**
- [ ] Máy thuyết trình chạy được `python main.py` (thử trước, không thử lúc lên bục).
- [ ] Đã có dữ liệu mẫu: chạy `python seed_data.py` (Trường) hoặc nhập tay: ≥ 5 hội viên, 3 gói tập (vd 1 tuần / 1 tháng / 3 tháng), vài đăng ký, trong đó **1 người sắp hết hạn** và **1 người đã hết hạn**.
- [ ] Đã sao lưu `gym.db` mẫu để khôi phục nếu lỡ xóa nhầm.
- [ ] `python tests/check_api.py` báo "API khớp nhau"; `python -m unittest discover -s tests -t .` báo `OK`.

**Kịch bản demo (khoảng 5 phút)**
1. [ ] Mở chương trình: thấy 5 tab, không tab nào đỏ.
2. [ ] **Hội viên**: thêm 1 hội viên mới, sửa tên, thử nhập SĐT trùng → hiện thông báo lỗi, xóa hội viên vừa thêm.
3. [ ] **Gói tập**: thêm gói, sửa giá; thử giá âm → báo lỗi; thử xóa gói đang có người đăng ký → bị từ chối.
4. [ ] **Đăng ký**: đăng ký gói cho hội viên, thấy ngày hết hạn tự tính; mở danh sách sắp hết hạn.
5. [ ] **Tìm kiếm**: tìm theo tên (gõ không dấu cũng ra), theo ID, theo số điện thoại; thử từ khóa không có → "Không tìm thấy"; để trống → báo lỗi.
6. [ ] **Thống kê**: thấy tổng hội viên, còn hạn / sắp hết hạn / hết hạn, doanh thu; sang bảng theo gói và theo tháng.
7. [ ] Quay lại **Đăng ký** thêm 1 đăng ký, sang **Thống kê** → số liệu tự cập nhật.
8. [ ] Đóng chương trình bình thường, mở lại: dữ liệu vẫn còn.

**Nếu có sự cố khi demo:** tab nào đỏ thì bỏ qua tab đó, đi tiếp các tab còn lại (chương trình không sập); khôi phục `gym.db` sao lưu nếu dữ liệu hỏng.
