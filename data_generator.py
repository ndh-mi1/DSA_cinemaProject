import json
import random
import uuid
import os
from datetime import datetime, timedelta

# --- CẤU HÌNH DỮ LIỆU ---
NUM_MOVIES = 50
NUM_SHOWTIMES = 5000
TARGET_BOOKINGS = [1000, 10000, 50000, 100000 ] # Số lượng vé cần tạo cho từng file

# --- DỮ LIỆU MẪU ĐỂ RANDOM ---
GENRES = ["Action", "Sci-Fi", "Comedy", "Drama", "Horror", "Romance", "Animation"]
ROOMS = [f"Phòng {i}" for i in range(1, 11)] # 10 phòng chiếu
PHONE_POOL = [f"090{random.randint(1000000, 9999999)}" for _ in range(2000)] # 2000 SĐT lặp lại

def random_date(start, end):
    """Sinh ngày ngẫu nhiên giữa 2 mốc thời gian"""
    delta = end - start
    random_days = random.randrange(delta.days)
    res = start + timedelta(days=random_days)
    return res.replace(hour=random.randint(8, 23), minute=random.randint(0, 59), second=0).isoformat(timespec="seconds")

def generate_dataset(num_bookings, filename):
    print(f"\nĐang tạo tập dữ liệu {num_bookings:,} bản ghi...")
    
    # 1. TẠO MOVIES
    movies = []
    for i in range(1, NUM_MOVIES + 1):
        movie_id = f"M{i:03d}"
        movies.append({
            "movie_id": movie_id,
            "title": f"Mock Movie {i}",
            "genre": random.choice(GENRES),
            "duration": random.randint(90, 180),
            "rating": round(random.uniform(5.0, 9.5), 1),
            "description": "Dữ liệu tự động sinh cho Performance Test.",
            "poster_color": f"#{random.randint(0, 0xFFFFFF):06x}"
        })

    # 2. TẠO SHOWTIMES VÀ SEATMAP
    showtimes = []
    showtime_dict = {} 
    now = datetime.now()
    start_date = now - timedelta(days=365) 
    
    for i in range(1, NUM_SHOWTIMES + 1):
        st_id = f"S{i:04d}"
        st_time = random_date(start_date, now)
        
        st = {
            "showtime_id": st_id,
            "movie_id": f"M{random.randint(1, NUM_MOVIES):03d}",
            "room": random.choice(ROOMS),
            "start_time": st_time,
            "price": random.choice([85000, 100000, 120000]),
            "rows": 8,
            "cols": 10,
            "seat_grid": [[0]*10 for _ in range(8)], # 0 là AVAILABLE
            "available_seats": [(r, c) for r in range(8) for c in range(10)] # Danh sách ghế trống để pick random
        }
        showtimes.append(st)
        showtime_dict[st_id] = st

    # 3. TẠO BOOKINGS
    bookings = []
    successful_bookings = 0
    
    while successful_bookings < num_bookings:
        st = random.choice(showtimes)
        
        num_seats_to_buy = random.randint(1, 4)
        
        if len(st["available_seats"]) < num_seats_to_buy:
            continue 
            
        chosen_coords = random.sample(st["available_seats"], num_seats_to_buy)
        for r, c in chosen_coords:
            st["available_seats"].remove((r, c))
            st["seat_grid"][r][c] = 1 
            
        seat_labels = [f"{chr(65+r)}{c+1}" for r, c in chosen_coords]
        
        show_datetime = datetime.fromisoformat(st["start_time"])
        booked_at = random_date(show_datetime - timedelta(days=7), show_datetime)
        
        booking = {
            "booking_id": str(uuid.uuid4())[:8].upper(),
            "customer_name": f"Khách Hàng {successful_bookings}",
            "customer_phone": random.choice(PHONE_POOL),
            "movie_id": st["movie_id"],
            "showtime_id": st["showtime_id"],
            "seats": seat_labels,
            "total_price": st["price"] * num_seats_to_buy,
            "booked_at": booked_at,
            "status": "CONFIRMED"
        }
        
        bookings.append(booking)
        successful_bookings += 1

    # Dọn dẹp trường 'available_seats' phụ trợ trước khi lưu file
    for st in showtimes:
        del st["available_seats"]

    # 4. XUẤT RA FILE JSON
    os.makedirs("data", exist_ok=True)
    payload = {
        "movies": movies,
        "showtimes": showtimes,
        "bookings": bookings
    }
    
    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False)
        
    print(f"Đã lưu file: data/{filename} (Size: ~{os.path.getsize(f'data/{filename}') / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    print("BẮT ĐẦU CHUẨN BỊ DỮ LIỆU KIỂM THỬ HIỆU NĂNG...")
    for target in TARGET_BOOKINGS:
        file_name = f"test_{target//1000}k.json"
        generate_dataset(target, file_name)
    print("\nĐÃ HOÀN TẤT VIỆC TẠO DỮ LIỆU!")