import time
import os
from modules.cinema_manager import CinemaManager

def run_performance_benchmark(filename):
    print(f"\n{'='*60}")
    print(f"TẬP DỮ LIỆU {filename}")
    print(f"{'='*60}")

    manager = CinemaManager()

    # ĐO THỜI GIAN NẠP DỮ LIỆU I/O (Bỏ qua khỏi đánh giá thuật toán)
    start_load = time.perf_counter()
    manager.loadData(f"data/{filename}")
    end_load = time.perf_counter()
    print(f"[I/O] Nạp file vào RAM mất: {(end_load - start_load) * 1000:.2f} ms")
    
    if len(manager.bookings) == 0:
        print("Lỗi: Không có dữ liệu vé!")
        return

    # MẢNG 2 CHIỀU (SeatMap)
    print("\n[1] TEST MẢNG 2 CHIỀU - KỲ VỌNG: O(1)")
    sample_st_id = list(manager.showtimes.keys())[-1]
    st = manager.showtimes[sample_st_id]
    
    start_o1 = time.perf_counter()
    _ = st.seat_map.is_available(0, 0)
    _ = st.seat_map.is_available(7, 9)
    end_o1 = time.perf_counter()
    print(f" tọa độ mảng 2 chiều: {(end_o1 - start_o1) * 1000:.6f} ms")

    # TÌM KIẾM TUYẾN TÍNH (Linked List) 
    print("\n[2] TEST LINEAR SEARCH (Linked List) - KỲ VỌNG: O(n)")
    worst_case_id = manager.bookings.tail.booking_id
    
    start_on = time.perf_counter()
    _ = manager.bookings.search_by_id(worst_case_id)
    end_on = time.perf_counter()
    print(f" Tìm mã vé (Worst-case): {(end_on - start_on) * 1000:.4f} ms")

    # SẮP XẾP QUICK SORT
    print("\n[3] TEST SẮP XẾP QUICK SORT - KỲ VỌNG: O(n log n)")
    arr_bookings = manager.bookings.to_list()
    
    start_sort = time.perf_counter()
    sorted_bookings = manager.quick_sort_bookings(arr_bookings)
    end_sort = time.perf_counter()
    print(f" Sắp xếp {len(arr_bookings):,} vé: {(end_sort - start_sort) * 1000:.4f} ms")

    # TÌM KIẾM NHỊ PHÂN (Binary Search) 
    print("\n[4] TEST BINARY SEARCH - KỲ VỌNG: O(log n)")
    target_date = sorted_bookings[len(sorted_bookings)//2].booked_at[:10]
    
    start_binary = time.perf_counter()
    _ = manager.binary_search_bookings_by_date(sorted_bookings, target_date)
    end_binary = time.perf_counter()
    print(f" Tìm nhị phân ngày {target_date}: {(end_binary - start_binary) * 1000:.4f} ms")

if __name__ == "__main__":
    files_to_test = ["test_1k.json", "test_10k.json", "test_50k.json", "test_100k.json"]
    
    for f in files_to_test:
        file_path = f"data/{f}"
        if os.path.exists(file_path):
            run_performance_benchmark(f)
        else:
            print(f"Chưa tìm thấy {file_path}")