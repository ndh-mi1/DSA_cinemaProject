import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.data_structures import BookingLinkedList, BookingNode

def tao_ve_ao(ma_ve):
    return BookingNode(
        booking_id=ma_ve,
        customer_name="Nguyễn Văn Test",
        customer_phone="0904614984",
        movie_id="M1",
        showtime_id="S1",
        seats=["A9"],
        total_price=50000,
        booked_at="2025-06-09T10:00:00"
    )

def test_thao_tac_them_node():
    print("TEST THÊM NODE")
    danh_sach = BookingLinkedList()

    #Thêm vé đầu tiên (Danh sách đang rỗng)
    ve_1 = tao_ve_ao("VE_01")
    danh_sach.append(ve_1)
    
    assert danh_sach.head == ve_1, "Head không trỏ vào VE_01"
    assert danh_sach.tail == ve_1, "Tail không trỏ vào VE_01"
    assert danh_sach._size == 1, "Kích thước phải là 1"
    assert ve_1.prev is None and ve_1.next is None, "Nối prev/next sai ở vé đầu"
    print("test thêm vé đầu tiên ok")

    #Thêm vé thứ hai vào cuối (test append)
    ve_2 = tao_ve_ao("VE_02")
    danh_sach.append(ve_2)
    
    assert danh_sach.tail == ve_2, "Tail chưa cập nhật sang VE_02"
    assert ve_1.next == ve_2, "Lỗi liên kết VE_01 -> VE_02"
    assert ve_2.prev == ve_1, "Lỗi liên kết VE_02 <- VE_01"
    assert danh_sach._size == 2, "Kích thước phải là 2"
    print("test append ok")

    #Thêm vé thứ ba vào ĐẦU danh sách (insert_head)
    ve_3 = tao_ve_ao("VE_03")
    danh_sach.insert_head(ve_3)
    
    assert danh_sach.head == ve_3, "Head chưa cập nhật sang VE_03"
    assert ve_3.next == ve_1, "Lỗi liên kết VE_03 -> VE_01"
    assert ve_1.prev == ve_3, "Lỗi liên kết VE_01 <- VE_03"
    assert danh_sach._size == 3, "Kích thước phải là 3"
    print("test insert_head ok")

    print("test insert_node done")

def test_thao_tac_xoa_node():
    print("\nTEST XÓA NODE")
    
    #Xóa vé duy nhất trong danh sách
    danh_sach_1 = BookingLinkedList()
    ve_duy_nhat = tao_ve_ao("VE_SINGLE")
    danh_sach_1.append(ve_duy_nhat)
    
    danh_sach_1.delete_node(ve_duy_nhat)
    assert danh_sach_1.head is None, "Head phải về None khi xóa vé duy nhất"
    assert danh_sach_1.tail is None, "Tail phải về None khi xóa vé duy nhất"
    assert danh_sach_1._size == 0, "Kích thước danh sách phải về 0"
    print("xóa vé duy nhất ok (Không kẹt bộ nhớ)")

    #Xóa vé ở các vị trí đầu, giữa, cuối
    danh_sach_2 = BookingLinkedList()
    ve_A = tao_ve_ao("VE_A") # Móc vào Đầu
    ve_B = tao_ve_ao("VE_B") # Móc vào Giữa
    ve_C = tao_ve_ao("VE_C") # Móc vào Cuối
    
    danh_sach_2.append(ve_A)
    danh_sach_2.append(ve_B)
    danh_sach_2.append(ve_C)

    #Xóa vé ở đầu (Head)
    danh_sach_2.delete_node(ve_A)
    assert danh_sach_2.head == ve_B, "Head chưa chuyển sang VE_B"
    assert ve_B.prev is None, "Con trỏ Prev của Head mới phải là None"
    assert danh_sach_2._size == 2, "Kích thước phải giảm còn 2"
    print("test xóa vé ở đầu ok")

    #Xóa vé ở cuối (Tail)
    danh_sach_2.delete_node(ve_C)
    assert danh_sach_2.tail == ve_B, "Tail chưa chuyển sang VE_B"
    assert ve_B.next is None, "Con trỏ Next của Tail mới phải là None"
    assert danh_sach_2._size == 1, "Kích thước phải giảm còn 1"
    print("test xóa vé ở cuối ok")

    #Xóa vé ở giữa
    #Danh sách chỉ còn [VE_B]. Ta thêm VE_D và VE_E vào thành B - D - E
    ve_D = tao_ve_ao("VE_D")
    ve_E = tao_ve_ao("VE_E")
    danh_sach_2.append(ve_D)
    danh_sach_2.append(ve_E)
    
    # Xóa VE_D đang nằm giữa B và E
    danh_sach_2.delete_node(ve_D)
    assert ve_B.next == ve_E, "B không trỏ tới E"
    assert ve_E.prev == ve_B, "E không trỏ ngược lại B"
    assert danh_sach_2._size == 2, "Kích thước danh sách cập nhật sai"
    print("test xóa vé ở giữa ok")

    print("test delete_node done")

def test_thao_tac_tim_kiem():
    print("\nTEST TÌM KIẾM NODE")
    danh_sach = BookingLinkedList()
    
    #Tạo vé
    ve_1 = tao_ve_ao("VE_HAALAND")
    ve_1.customer_name = "Erling Haaland"
    ve_1.customer_phone = "0111111111"
    
    ve_2 = tao_ve_ao("VE_BELLINGHAM")
    ve_2.customer_name = "Jude Bellingham"
    ve_2.customer_phone = "0222222222"
    
    #khách hàng Bellingham mua thêm 1 vé nữa
    ve_3 = tao_ve_ao("VE_BELLINGHAM_2")
    ve_3.customer_name = "Jude Bellingham"
    ve_3.customer_phone = "0222222222" 
    
    danh_sach.append(ve_1)
    danh_sach.append(ve_2)
    danh_sach.append(ve_3)

    #Tìm kiếm theo ID tồn tại
    ket_qua_id = danh_sach.search_by_id("VE_HAALAND")
    assert ket_qua_id is not None, "Không tìm thấy vé dù mã tồn tại"
    assert ket_qua_id.customer_name == "Erling Haaland", "Trả về sai thông tin khách hàng"
    print("test tìm kiếm theo ID tồn tại done")

    #Tìm theo ID KHÔNG tồn tại 
    ket_qua_id_sai = danh_sach.search_by_id("VE_MBAPPE")
    assert ket_qua_id_sai is None, "Mã vé không tồn tại nhưng hệ thống lại trả về dữ liệu ảo"
    print("đã trả về None thay vì crash")

    #Tìm kiếm theo Số điện thoại (đối với khách mua nhiều vé)
    ket_qua_phone = danh_sach.search_by_phone("0222222222")
    assert len(ket_qua_phone) == 2, "Khách hàng mua 2 vé nhưng hàm tìm kiếm bị sót"
    assert ket_qua_phone[0].booking_id == "VE_BELLINGHAM", "Sai thứ tự vé được lưu"
    print("test tìm theo sdt ok")

    #Tìm kiếm theo Số điện thoại KHÔNG tồn tại 
    ket_qua_phone_sai = danh_sach.search_by_phone("0999999999")
    assert len(ket_qua_phone_sai) == 0, "SĐT không có mà vẫn có vé trả về"
    print("đã trả về mảng rỗng []")
    
    print("test tìm kiếm done")


if __name__ == "__main__":
    test_thao_tac_them_node() 
    test_thao_tac_xoa_node()  
    test_thao_tac_tim_kiem()