(*) MẬT KHẨU QUẢN TRỊ VIÊN: admin

(*) TEST:
    Test chạy data_generator.py trước để sinh ra file dữ liệu (nếu chưa có)
    Thêm file dữ liệu ở app_gui.py, ví dụ:
        self.manager.loadData("data/test_10k.json")

(*) Cấu Trúc Thư Mục (Project Structure):

    DSA_CINEMAPROJECT/
    │
    ├── assets/
    │   └── posters/              # Thư mục chứa hình ảnh poster phim
    ├── data/                     
    │   └── cinema_data.json      # File CSDL lưu trữ chính của hệ thống
    ├── modules/                  # Tầng Logic và Cấu trúc dữ liệu
    │   ├── __init__.py
    │   ├── cinema_manager.py     # Bộ điều phối trung tâm (Chứa giải thuật)
    │   └── data_structures.py    # Cấu trúc dữ liệu lõi (Linked List, SeatMap)
    ├── tests/                    # Tầng Kiểm thử tự động (Unit Tests)
    │   ├── test_linkedlist.py    # Kịch bản test Danh sách liên kết
    │   └── test_seatmap.py       # Kịch bản test Ma trận ghế
    │
    ├── app_gui.py                # File mã nguồn chạy giao diện Tkinter (Main)
    ├── APP.exe                   # File thực thi ứng dụng đã đóng gói
    ├── data_generator.py         # Script tự động sinh tập dữ liệu lớn
    ├── Execute_Cinebook.bat      # File batch hỗ trợ khởi chạy nhanh trên Windows
    ├── icon.ico                  # Icon hệ thống
    ├── performance_test.py       # Script đo đạc hiệu năng thuật toán (Benchmark)
    ├── README.md                 # Tài liệu hướng dẫn
    └── seed_data.py              # Script khởi tạo dữ liệu mẫu ban đầu
