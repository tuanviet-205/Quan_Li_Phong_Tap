"""
DATABASE DÙNG CHUNG (SQLite - thư viện có sẵn của Python)
Người phụ trách: Nguyễn Hữu Hùng (hạng mục 1.1 - thiết kế dữ liệu), review: Phạm Văn Cử

Các module KHÔNG tự viết sqlite3, mà dùng 4 hàm bên dưới:
    init_db()                  -> tạo bảng nếu chưa có
    query_all(sql, params)     -> list[dict]   (nhiều dòng)
    query_one(sql, params)     -> dict | None  (một dòng)
    insert(sql, params)        -> int          (id vừa thêm)
    execute(sql, params)       -> int          (số dòng bị ảnh hưởng, dùng cho UPDATE/DELETE)

Lỗi trùng dữ liệu (UNIQUE) sẽ ném sqlite3.IntegrityError;
module nào gọi thì tự bắt và đổi thành ValueError("thông báo tiếng Việt").
"""
import sqlite3
from contextlib import closing

import config

# Câu lệnh tạo 3 bảng. Ngày lưu dạng chuỗi 'YYYY-MM-DD'.
SCHEMA = """
CREATE TABLE IF NOT EXISTS members (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ho_ten         TEXT NOT NULL,
    gioi_tinh      TEXT DEFAULT '',
    ngay_sinh      TEXT DEFAULT '',
    so_dien_thoai  TEXT NOT NULL UNIQUE,
    email          TEXT DEFAULT '',
    dia_chi        TEXT DEFAULT '',
    ngay_tao       TEXT DEFAULT (date('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS packages (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ten_goi   TEXT NOT NULL UNIQUE,
    gia       INTEGER NOT NULL CHECK (gia >= 0),
    so_ngay   INTEGER NOT NULL CHECK (so_ngay > 0),
    mo_ta     TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS registrations (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id        INTEGER NOT NULL REFERENCES members(id)  ON DELETE CASCADE,
    package_id       INTEGER NOT NULL REFERENCES packages(id) ON DELETE RESTRICT,
    ngay_dang_ky     TEXT NOT NULL,
    ngay_het_han     TEXT NOT NULL,
    gia_luc_dang_ky  INTEGER NOT NULL
);
"""


def get_connection():
    """Mở kết nối mới. Đọc config.DB_FILE mỗi lần gọi (để test đổi sang file khác)."""
    conn = sqlite3.connect(config.DB_FILE)
    conn.row_factory = sqlite3.Row            # cho phép truy cập cột theo tên
    conn.execute("PRAGMA foreign_keys = ON")  # bật ràng buộc khóa ngoại
    return conn


def init_db():
    """Tạo các bảng nếu chưa tồn tại. Gọi 1 lần khi chương trình khởi động."""
    with closing(get_connection()) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def query_all(sql, params=()):
    """Chạy SELECT, trả về list[dict]. Không có dòng nào -> []."""
    with closing(get_connection()) as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def query_one(sql, params=()):
    """Chạy SELECT, trả về dict của dòng đầu tiên, hoặc None nếu không có."""
    rows = query_all(sql, params)
    return rows[0] if rows else None


def insert(sql, params=()):
    """Chạy INSERT, trả về id của dòng vừa thêm."""
    with closing(get_connection()) as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid


def execute(sql, params=()):
    """Chạy UPDATE / DELETE, trả về số dòng bị ảnh hưởng (0 = không tìm thấy)."""
    with closing(get_connection()) as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.rowcount
