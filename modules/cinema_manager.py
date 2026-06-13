"""
MODULE: cinema_manager.py
Mô tả : Lớp CinemaManager – trung tâm xử lý nghiệp vụ hệ thống.
        Chứa tất cả thuật toán tìm kiếm, sắp xếp, CRUD và I/O file.
"""

from __future__ import annotations

import json
import os
import random
import string
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from modules.data_structures import (
    BookingLinkedList, BookingNode, Movie,
    SeatMap, Showtime, new_booking,
)


# ─────────────────────────────────────────────────────────────────────
# CINEMA MANAGER
# ─────────────────────────────────────────────────────────────────────
class CinemaManager:
    DATA_DIR = "data"

    def __init__(self):
        self.movies: Dict[str, Movie] = {}
        self.showtimes: Dict[str, Showtime] = {}
        self.bookings = BookingLinkedList()
        self._phone_index: Dict[str, List[str]] = {}   # phone → booking_ids

    # =================================================================
    # I/O FILE  (loadData / saveData)
    # =================================================================
    def loadData(self, path: str = "data/cinema_data.json") -> None:
        os.makedirs(self.DATA_DIR, exist_ok=True)
        if not os.path.exists(path):
            self._seed_default_data()
            self.saveData(path)
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # --- Nạp phim ---
        for m in data.get("movies", []):
            movie = Movie(**{k: v for k, v in m.items()})
            self.movies[movie.movie_id] = movie

        # --- Nạp suất chiếu ---
        for s in data.get("showtimes", []):
            grid = s.pop("seat_grid", None)
            rows = s.pop("rows", 8)
            cols = s.pop("cols", 10)
            sm = SeatMap(rows=rows, cols=cols)
            if grid:
                sm.load_grid(grid)
            st = Showtime(seat_map=sm, **s)
            self.showtimes[st.showtime_id] = st

        # --- Nạp bookings ---
        for b in data.get("bookings", []):
            node = BookingNode(**{k: v for k, v in b.items()
                                  if k not in ("prev", "next")})
            self.bookings.append(node)
            self._index_phone(node.customer_phone, node.booking_id)

        print(f"[LoadData] {len(self.movies)} phim | "
              f"{len(self.showtimes)} suất | "
              f"{len(self.bookings)} booking")

    def saveData(self, path: str = "data/cinema_data.json") -> None:
        os.makedirs(self.DATA_DIR, exist_ok=True)

        movies_data = [
            {k: v for k, v in m.__dict__.items()}
            for m in self.movies.values()
        ]

        showtimes_data = []
        for st in self.showtimes.values():
            d = {
                "showtime_id": st.showtime_id,
                "movie_id": st.movie_id,
                "room": st.room,
                "start_time": st.start_time,
                "price": st.price,
                "rows": st.seat_map.rows,
                "cols": st.seat_map.cols,
                "seat_grid": st.seat_map.grid_snapshot(),
            }
            showtimes_data.append(d)

        bookings_data = []
        for node in self.bookings:
            bookings_data.append({
                "booking_id":     node.booking_id,
                "customer_name":  node.customer_name,
                "customer_phone": node.customer_phone,
                "movie_id":       node.movie_id,
                "showtime_id":    node.showtime_id,
                "seats":          node.seats,
                "total_price":    node.total_price,
                "booked_at":      node.booked_at,
                "status":         node.status,
            })

        payload = {
            "movies":    movies_data,
            "showtimes": showtimes_data,
            "bookings":  bookings_data,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"[SaveData] Đã lưu → {path}")

    # =================================================================
    # BOOKING OPERATIONS
    # =================================================================
    def book_seats(self, showtime_id: str, customer_name: str,
                   customer_phone: str, seat_labels: List[str]
                   ) -> Tuple[bool, str, Optional[BookingNode]]:
        if showtime_id not in self.showtimes:
            return False, "Suất chiếu không tồn tại.", None
        if not seat_labels:
            return False, "Chưa chọn ghế.", None

        st = self.showtimes[showtime_id]
        # Kiểm tra tất cả ghế còn trống trước
        for label in seat_labels:
            try:
                r, c = SeatMap.label_to_index(label)
            except Exception:
                return False, f"Mã ghế không hợp lệ: {label}", None
            if not st.seat_map.is_available(r, c):
                return False, f"Ghế {label} đã được đặt.", None

        # Đặt ghế
        for label in seat_labels:
            r, c = SeatMap.label_to_index(label)
            st.seat_map.book_seat(r, c)

        node = new_booking(customer_name, customer_phone,
                           st.movie_id, showtime_id,
                           seat_labels, st.price)
        self.bookings.insert_head(node)
        self._index_phone(customer_phone, node.booking_id)
        return True, "Đặt vé thành công!", node

    def cancel_booking(self, booking_id: str) -> Tuple[bool, str]:
        """
        Huỷ booking: cập nhật status và giải phóng ghế trên SeatMap.
        """
        node = self.bookings.search_by_id(booking_id)
        if not node:
            return False, "Không tìm thấy mã booking."
        if node.status == "CANCELLED":
            return False, "Booking này đã bị huỷ trước đó."

        node.status = "CANCELLED"
        if node.showtime_id in self.showtimes:
            sm = self.showtimes[node.showtime_id].seat_map
            for label in node.seats:
                r, c = SeatMap.label_to_index(label)
                sm.release_seat(r, c)
        return True, f"Đã huỷ booking {booking_id}."

    # =================================================================
    # SEARCH ALGORITHMS
    # =================================================================
    def linear_search_movies(self, keyword: str) -> List[Movie]:
        """
        Tìm kiếm tuyến tính phim theo tiêu đề hoặc thể loại.
        """
        kw = keyword.lower()
        return [m for m in self.movies.values()
                if kw in m.title.lower() or kw in m.genre.lower()]

    def search_booking_by_phone(self, phone: str) -> List[BookingNode]:
        ids = self._phone_index.get(phone, [])
        if ids:
            result = []
            for bid in ids:
                node = self.bookings.search_by_id(bid)
                if node:
                    result.append(node)
            return result
        return self.bookings.search_by_phone(phone)

    def binary_search_bookings_by_date(self,
                                        sorted_list: List[BookingNode],
                                        target_date: str
                                        ) -> List[BookingNode]:
        """
        Tìm kiếm nhị phân trên danh sách đã sắp xếp theo ngày đặt.
        """
        lo, hi = 0, len(sorted_list) - 1
        found_idx = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            mid_date = sorted_list[mid].booked_at[:10]
            if mid_date == target_date:
                found_idx = mid
                break
            elif mid_date < target_date:
                lo = mid + 1
            else:
                hi = mid - 1

        if found_idx == -1:
            return []

        results = [sorted_list[found_idx]]
        # Mở rộng sang trái
        i = found_idx - 1
        while i >= 0 and sorted_list[i].booked_at[:10] == target_date:
            results.append(sorted_list[i])
            i -= 1
        # Mở rộng sang phải
        i = found_idx + 1
        while i < len(sorted_list) and sorted_list[i].booked_at[:10] == target_date:
            results.append(sorted_list[i])
            i += 1
        return results

    # =================================================================
    # SORT ALGORITHMS
    # =================================================================
    def quick_sort_bookings(self, arr: List[BookingNode],
                            key=lambda x: x.booked_at
                            ) -> List[BookingNode]:
        """
        Quick Sort sắp xếp danh sách booking.
        """
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left  = [x for x in arr if key(x) < key(pivot)]
        mid   = [x for x in arr if key(x) == key(pivot)]
        right = [x for x in arr if key(x) > key(pivot)]
        return (self.quick_sort_bookings(left, key) + mid +
                self.quick_sort_bookings(right, key))

    def merge_sort_showtimes(self, arr: List[Showtime]) -> List[Showtime]:
        """
        Merge Sort sắp xếp suất chiếu theo giờ chiếu.
        """
        if len(arr) <= 1:
            return arr
        mid   = len(arr) // 2
        left  = self.merge_sort_showtimes(arr[:mid])
        right = self.merge_sort_showtimes(arr[mid:])
        return self._merge(left, right)

    def _merge(self, left: List[Showtime], right: List[Showtime]) -> List[Showtime]:
        result, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i].start_time <= right[j].start_time:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    # =================================================================
    # STATISTICS / REPORT
    # =================================================================
    def get_statistics(self) -> Dict:
        """Thống kê tổng quan hệ thống – O(B + S)."""
        total_revenue = 0.0
        confirmed = cancelled = 0
        movie_counter: Dict[str, int] = {}

        for node in self.bookings:
            if node.status == "CONFIRMED":
                confirmed += 1
                total_revenue += node.total_price
                movie_counter[node.movie_id] = (
                    movie_counter.get(node.movie_id, 0) + len(node.seats))
            else:
                cancelled += 1

        top_movie_id = max(movie_counter, key=movie_counter.get) if movie_counter else None
        top_movie = self.movies.get(top_movie_id) if top_movie_id else None

        total_seats = sum(st.seat_map.rows * st.seat_map.cols
                          for st in self.showtimes.values())
        booked_seats = sum(st.seat_map.booked_count()
                           for st in self.showtimes.values())

        return {
            "total_movies":    len(self.movies),
            "total_showtimes": len(self.showtimes),
            "total_bookings":  len(self.bookings),
            "confirmed":       confirmed,
            "cancelled":       cancelled,
            "total_revenue":   total_revenue,
            "top_movie":       top_movie.title if top_movie else "N/A",
            "seat_occupancy":  round(booked_seats / total_seats * 100, 1) if total_seats else 0,
        }

    def get_showtimes_by_movie(self, movie_id: str) -> List[Showtime]:
        sts = [st for st in self.showtimes.values() if st.movie_id == movie_id]
        return self.merge_sort_showtimes(sts)

    # =================================================================
    # HELPERS
    # =================================================================
    def _index_phone(self, phone: str, booking_id: str) -> None:
        self._phone_index.setdefault(phone, []).append(booking_id)
