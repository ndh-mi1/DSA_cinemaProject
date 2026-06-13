import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.data_structures import SeatMap, SeatStatus

def test_khoi_tao_va_dat_ghe_chuan():
    print("TEST SEATMAP")
    rap_phim = SeatMap(rows=5, cols=5) #Tạo rạp 5x5
    
    #Đặt một ghế ở (0, 0)
    thanh_cong = rap_phim.book_seat(0, 0)
    assert thanh_cong == True, "Không thể đặt ghế trống"
    assert rap_phim.is_available(0, 0) == False, "Ghế đã đặt nhưng trạng thái vẫn báo Trống"
    assert rap_phim.booked_count() == 1, "Đếm sai số ghế đã bán"
    print("Đặt ghế và cập nhật trạng thái ok")

def test_mang_2_chieu():
    print("\nTEST mảng 2 chiều")
    rap_phim = SeatMap(rows=8, cols=10) # Rạp mặc định 8x10
    
    #Đặt đè lên ghế đã có người
    rap_phim.book_seat(1, 1) #đặt lần 1
    ket_qua_dat_de = rap_phim.book_seat(1, 1) #đặt lần 2 vào cùng vị trí
    assert ket_qua_dat_de == False, "Hệ thống cho phép đặt đè 2 người vào 1 ghế"
    print("đã chặn được thao tác đặt đè ghế")

    #Lỗi Out of Bounds - Ghế không tồn tại
    #Đặt ghế ở hàng 9, cột 9 rạp chỉ có 8x10
    ket_qua_tran_mang = rap_phim.book_seat(9, 9)
    assert ket_qua_tran_mang == False, "Hệ thống cho phép đặt ghế ngoài phạm vi rạp"
    print("Hệ thống đã chặn được thao tác đặt ghế quá sức chứa")

    #Lỗi vị trí âm 
    #Tọa độ (-1, -1) không tồn tại trên thực tế
    ket_qua_am = rap_phim.book_seat(-1, -1)
    
    if ket_qua_am == True:
        print("Nhập tọa độ âm (-1, -1) nhưng hệ thống vẫn cho đặt vé")
        print("Vị trí ghế bị thay đổi ở cuối rạp:", rap_phim._grid[-1][-1])
    else:
        print("Hệ thống đã chặn được tọa độ âm.")

if __name__ == "__main__":
    test_khoi_tao_va_dat_ghe_chuan()
    test_mang_2_chieu()