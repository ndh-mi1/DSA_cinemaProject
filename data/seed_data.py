import json
import os
from datetime import datetime, timedelta

def seed_cinema_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "cinema_data.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ KHÔNG TÌM THẤY FILE TẠI ĐƯỜNG DẪN: {file_path}")
        return

    movies = data.get("movies", [])
    if not movies:
        print("❌ Không tìm thấy dữ liệu phim! Hãy kiểm tra lại file JSON.")
        return

    new_showtimes = []
    showtime_id_counter = 1
    empty_grid = [[0 for _ in range(10)] for _ in range(8)]

    # Cấu hình các loại phòng và giá vé cố định cho ca chiếu đó
    rooms = [
        {"name": "Phòng 1 (Standard)", "price": 85000},
        {"name": "Phòng 2 (Standard)", "price": 85000},
        {"name": "Phòng 3 (IMAX)", "price": 120000},
        {"name": "Phòng 4 (Sweetbox)", "price": 150000}
    ]

    # Khung giờ chiếu đa dạng trải dài trong ngày
    time_slots = [
        ("08:30", 0),  # Ca sáng sớm (Standard)
        ("11:15", 1),  # Ca trưa (Standard)
        ("14:00", 2),  # Ca chiều (IMAX)
        ("16:45", 0),  # Ca chiều muộn (Standard)
        ("19:30", 2),  # Ca tối giờ vàng (IMAX)
        ("22:15", 3)   # Ca đêm muộn (Sweetbox)
    ]

    # Sinh ca chiếu phong phú cho 3 ngày liên tiếp kể từ ngày mai
    start_date = datetime.now() + timedelta(days=1)

    for day_offset in range(3):
        current_date = start_date + timedelta(days=day_offset)
        date_str = current_date.strftime("%Y-%m-%d")

        for movie_idx, movie in enumerate(movies):
            m_id = movie["movie_id"]
            
            # Mỗi phim vào mỗi ngày sẽ nhận 3 ca chiếu ngẫu nhiên tịnh tiến 
            # Quy trình này giúp lịch chiếu giữa các phim không bị trùng lặp khung giờ lên nhau
            assigned_slots = [
                time_slots[(movie_idx + day_offset) % len(time_slots)],
                time_slots[(movie_idx + day_offset + 2) % len(time_slots)],
                time_slots[(movie_idx + day_offset + 4) % len(time_slots)]
            ]

            for time_str, room_idx in assigned_slots:
                room_info = rooms[room_idx]
                
                new_showtimes.append({
                    "showtime_id": f"S{showtime_id_counter:03d}",
                    "movie_id": m_id,
                    "room": room_info["name"],
                    "start_time": f"{date_str}T{time_str}:00",
                    "price": room_info["price"],
                    "rows": 8,
                    "cols": 10,
                    "seat_grid": empty_grid
                })
                showtime_id_counter += 1

    data["showtimes"] = new_showtimes
    data["bookings"] = []  # Reset lịch sử cũ chống lệch ID ca chiếu

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Đã tạo thành công {len(new_showtimes)} ca chiếu đa dạng cho {len(movies)} phim trong 3 ngày!")

if __name__ == "__main__":
    seed_cinema_data()