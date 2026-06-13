"""
MODULE: data_structures.py
Mô tả : Định nghĩa các cấu trúc dữ liệu cốt lõi của hệ thống:
        - Node / DoublyLinkedList  : quản lý danh sách đặt chỗ
        - SeatMap (mảng 2 chiều)   : sơ đồ ghế của từng suất chiếu
        - Movie / Showtime          : dữ liệu phim và suất chiếu
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import uuid


# ─────────────────────────────────────────────────────────────────────
# 1. BOOKING NODE  (nút của danh sách liên kết đôi)
# ─────────────────────────────────────────────────────────────────────
@dataclass
class BookingNode:
    """Một nút trong danh sách liên kết đôi lưu thông tin đặt chỗ."""
    booking_id: str
    customer_name: str
    customer_phone: str
    movie_id: str
    showtime_id: str
    seats: List[str]          
    total_price: float
    booked_at: str             
    status: str = "CONFIRMED"  

    prev: Optional["BookingNode"] = field(default=None, compare=False, repr=False)
    next: Optional["BookingNode"] = field(default=None, compare=False, repr=False)


# ─────────────────────────────────────────────────────────────────────
# 2. DOUBLY LINKED LIST  (danh sách liên kết đôi các booking)
# ─────────────────────────────────────────────────────────────────────
class BookingLinkedList:
    """
    Danh sách liên kết đôi lưu toàn bộ lịch sử đặt chỗ.
    """

    def __init__(self):
        self.head: Optional[BookingNode] = None
        self.tail: Optional[BookingNode] = None
        self._size: int = 0

    # ---------- INSERT ----------
    def insert_head(self, node: BookingNode) -> None:
        """Chèn booking mới vào đầu danh sách – O(1)."""
        node.prev = None
        node.next = self.head
        if self.head:
            self.head.prev = node
        self.head = node
        if self.tail is None:
            self.tail = node
        self._size += 1

    def append(self, node: BookingNode) -> None:
        """Thêm booking vào cuối – O(1)."""
        node.next = None
        node.prev = self.tail
        if self.tail:
            self.tail.next = node
        self.tail = node
        if self.head is None:
            self.head = node
        self._size += 1

    # ---------- DELETE ----------
    def delete_node(self, node: BookingNode) -> None:
        """Xoá một node khỏi danh sách – O(1)."""
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev
        node.prev = node.next = None
        self._size -= 1

    # ---------- SEARCH ----------
    def search_by_id(self, booking_id: str) -> Optional[BookingNode]:
        """Tìm booking theo ID – O(n)."""
        current = self.head
        while current:
            if current.booking_id == booking_id:
                return current
            current = current.next
        return None

    def search_by_phone(self, phone: str) -> List[BookingNode]:
        """Tìm tất cả booking của một khách – O(n)."""
        results: List[BookingNode] = []
        current = self.head
        while current:
            if current.customer_phone == phone:
                results.append(current)
            current = current.next
        return results

    def to_list(self) -> List[BookingNode]:
        result = []
        cur = self.head
        while cur:
            result.append(cur)
            cur = cur.next
        return result

    def __len__(self) -> int:
        return self._size

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur
            cur = cur.next


# ─────────────────────────────────────────────────────────────────────
# 3. SEAT MAP  (mảng 2 chiều)
# ─────────────────────────────────────────────────────────────────────
class SeatStatus:
    AVAILABLE = 0
    BOOKED    = 1
    SELECTED  = 2   


@dataclass
class SeatMap:
    """
    Sơ đồ ghế ngồi dưới dạng mảng 2 chiều rows × cols.
    """
    rows: int = 8
    cols: int = 10
    _grid: List[List[int]] = field(default_factory=list)

    def __post_init__(self):
        if not self._grid:
            self._grid = [[SeatStatus.AVAILABLE] * self.cols
                          for _ in range(self.rows)]

    @staticmethod
    def seat_label(row: int, col: int) -> str:
        return f"{chr(65 + row)}{col + 1}"

    @staticmethod
    def label_to_index(label: str):
        row = ord(label[0].upper()) - 65
        col = int(label[1:]) - 1
        return row, col

    def is_available(self, row: int, col: int) -> bool:
        if row < 0 or col < 0 or row >= self.rows or col >= self.cols:
            return False
        return self._grid[row][col] == SeatStatus.AVAILABLE

    def book_seat(self, row: int, col: int) -> bool:
        """Đặt ghế – trả True nếu thành công."""
        if self.is_available(row, col):
            self._grid[row][col] = SeatStatus.BOOKED
            return True
        return False

    def release_seat(self, row: int, col: int) -> None:
        self._grid[row][col] = SeatStatus.AVAILABLE

    def available_count(self) -> int:
        return sum(
            self._grid[r][c] == SeatStatus.AVAILABLE
            for r in range(self.rows)
            for c in range(self.cols)
        )

    def booked_count(self) -> int:
        return self.rows * self.cols - self.available_count()

    def grid_snapshot(self) -> List[List[int]]:
        """Trả về bản sao của lưới (để serialize)."""
        return [row[:] for row in self._grid]

    def load_grid(self, grid: List[List[int]]) -> None:
        self._grid = [row[:] for row in grid]


# ─────────────────────────────────────────────────────────────────────
# 4. MOVIE & SHOWTIME  (dữ liệu phim và suất chiếu)
# ─────────────────────────────────────────────────────────────────────
@dataclass
class Movie:
    movie_id: str
    title: str
    genre: str
    duration: int          
    rating: float          
    description: str = ""
    poster_color: str = "#e50914"  


@dataclass
class Showtime:
    showtime_id: str
    movie_id: str
    room: str              
    start_time: str        
    price: float           
    seat_map: SeatMap = field(default_factory=SeatMap)


# ─────────────────────────────────────────────────────────────────────
# 5. FACTORY HELPERS
# ─────────────────────────────────────────────────────────────────────
def new_booking(customer_name: str, customer_phone: str,
                movie_id: str, showtime_id: str,
                seats: List[str], price_per_seat: float) -> BookingNode:
    return BookingNode(
        booking_id=str(uuid.uuid4())[:8].upper(),
        customer_name=customer_name,
        customer_phone=customer_phone,
        movie_id=movie_id,
        showtime_id=showtime_id,
        seats=seats,
        total_price=price_per_seat * len(seats),
        booked_at=datetime.now().isoformat(timespec="seconds"),
    )
