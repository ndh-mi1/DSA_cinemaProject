"""
=======================================================================
MODULE: app_gui.py (Role-Based Access Control Version)
Mô tả : Giao diện đồ hoạ hiện đại – HỆ THỐNG ĐẶT VÉ XEM PHIM
        Tính năng: Phân quyền Đăng nhập (Khách hàng vs Quản lý)
        Màu sắc: Cinematic Dark Theme (Nền đen nhám + Đỏ Netflix)
=======================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from PIL import Image
import threading
import os
import sys

# Thêm thư mục gốc vào sys.path để import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.cinema_manager import CinemaManager
from modules.data_structures import SeatStatus

# ─── THIẾT LẬP GIAO DIỆN ─────────────────────────────────────────────
ctk.set_appearance_mode("dark")

# ─── BẢNG MÀU CHUẨN MODERN UI (NETFLIX STYLE) ───────────────────────
BG_APP      = "#0A0A0A"  
BG_PANEL    = "#141414"  
BG_CARD     = "#1E1E1E"  
ACCENT      = "#E50914"  
ACCENT_HOVER= "#B20710"  
TEXT_PRI    = "#FFFFFF"  
TEXT_SEC    = "#A0A0A0"  
BORDER      = "#2A2A2A"  
GOLD        = "#FFD700"  

SEAT_EMPTY  = "#2B2B36"  
SEAT_BOOKED = "#111111"  

# ─── HỆ THỐNG PHÔNG CHỮ ─────────────────────────────────────────────
FONT_LOGO   = ("Segoe UI Black", 24)
FONT_H1     = ("Segoe UI Black", 36)
FONT_H2     = ("Segoe UI", 20, "bold")
FONT_BTN    = ("Segoe UI", 14, "bold")
FONT_BODY   = ("Segoe UI", 14)
FONT_SMALL  = ("Segoe UI", 12)
FONT_MONO   = ("Consolas", 13)


class CinemaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.manager = CinemaManager()
        self.manager.loadData()

        self.title("CineBook - Hệ Thống Đặt Vé Xem Phim")
        self.geometry("1920x720")
        self.minsize(1400, 720)
        self.configure(fg_color=BG_APP)

        self._selected_movie = None
        self._selected_showtime = None
        self._selected_seats: list = []
        self.current_role = None  # Luu vai tro: "customer" hoac "manager"

        # Khởi chạy màn hình chọn vai trò trước tiên
        self._build_role_selection_screen()

    # =================================================================
    # MÀN HÌNH CHỌN VAI TRÒ (WELCOME SCREEN)
    # =================================================================
    def _build_role_selection_screen(self):
        self.role_frame = ctk.CTkFrame(self, fg_color=BG_APP, corner_radius=0)
        self.role_frame.pack(fill="both", expand=True)

        # Tiêu đề trung tâm
        title_container = ctk.CTkFrame(self.role_frame, fg_color="transparent")
        title_container.pack(pady=(80, 40))
        
        ctk.CTkLabel(title_container, text="CHÀO MỪNG ĐẾN VỚI CINEBOOK", font=FONT_H1, text_color=TEXT_PRI).pack()
        ctk.CTkLabel(title_container, text="Vui lòng lựa chọn vai trò truy cập hệ thống", font=FONT_BODY, text_color=TEXT_SEC).pack(pady=10)

        # Khung chứa 2 thẻ vai trò song song
        cards_container = ctk.CTkFrame(self.role_frame, fg_color="transparent")
        cards_container.pack(pady=10)

        # Thẻ 1: KHÁCH HÀNG
        card_customer = ctk.CTkFrame(cards_container, fg_color=BG_PANEL, width=350, height=250, corner_radius=16, border_width=1, border_color=BORDER)
        card_customer.pack(side="left", padx=30)
        card_customer.pack_propagate(False)
        
        ctk.CTkLabel(card_customer, text="KHÁCH HÀNG", font=FONT_H2, text_color=TEXT_PRI).pack(pady=(40, 10))
        ctk.CTkLabel(card_customer, text="Tra cứu danh sách phim rạp\nĐặt vé & xem lịch sử cá nhân", font=FONT_SMALL, text_color=TEXT_SEC, justify="center").pack(pady=10)
        
        ctk.CTkButton(card_customer, text="TRUY CẬP", command=lambda: self._login_as("customer"),
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, font=FONT_BTN, height=45, corner_radius=8).pack(side="bottom", fill="x", padx=30, pady=30)

        # Thẻ 2: QUẢN LÝ
        self.card_manager = ctk.CTkFrame(cards_container, fg_color=BG_PANEL, width=350, height=250, corner_radius=16, border_width=1, border_color=BORDER)
        self.card_manager.pack(side="left", padx=30)
        self.card_manager.pack_propagate(False)
        
        self.lbl_mgr_title = ctk.CTkLabel(self.card_manager, text="QUẢN TRỊ VIÊN", font=FONT_H2, text_color=TEXT_PRI)
        self.lbl_mgr_title.pack(pady=(40, 10))
        
        self.lbl_mgr_desc = ctk.CTkLabel(self.card_manager, text="Quản lý doanh thu rạp phim\nKiểm soát trạng thái giao dịch", font=FONT_SMALL, text_color=TEXT_SEC, justify="center")
        self.lbl_mgr_desc.pack(pady=10)
        
        self.btn_mgr_go = ctk.CTkButton(self.card_manager, text="ĐĂNG NHẬP", command=self._show_password_field,
                      fg_color=BG_CARD, hover_color=BORDER, text_color=TEXT_PRI, font=FONT_BTN, height=45, corner_radius=8, border_width=1, border_color=BORDER)
        self.btn_mgr_go.pack(side="bottom", fill="x", padx=30, pady=30)

    def _show_password_field(self):
        # Biến đổi thẻ Quản lý thành ô nhập mật khẩu bảo mật
        self.lbl_mgr_desc.pack_forget()
        self.btn_mgr_go.pack_forget()
        self.lbl_mgr_title.configure(text="XÁC THỰC QUẢN LÝ")

        self.entry_password = ctk.CTkEntry(self.card_manager, placeholder_text="Nhập mật khẩu...", show="*", fg_color=BG_CARD, border_color=BORDER, height=40, font=FONT_BODY)
        self.entry_password.pack(pady=15, padx=30, fill="x")
        self.entry_password.focus()

        # Cụm nút Xác nhận / Quay lại
        action_frame = ctk.CTkFrame(self.card_manager, fg_color="transparent")
        action_frame.pack(side="bottom", fill="x", padx=30, pady=25)

        ctk.CTkButton(action_frame, text="HỦY", command=self._reset_role_screen, fg_color="transparent", text_color=TEXT_SEC, hover_color=BG_CARD, width=80, height=40).pack(side="left")
        ctk.CTkButton(action_frame, text="VÀO", command=self._verify_manager_password, fg_color=ACCENT, hover_color=ACCENT_HOVER, font=FONT_BTN, width=180, height=40, corner_radius=6).pack(side="right")

    def _reset_role_screen(self):
        # Trở lại trạng thái ban đầu nếu ấn Hủy
        self.role_frame.destroy()
        self._build_role_selection_screen()

    def _verify_manager_password(self):
        # Mật khẩu bảo mật hệ thống quản trị
        pwd = self.entry_password.get().strip()
        if pwd == "admin":
            self._login_as("manager")
        else:
            messagebox.showerror("Sai mật khẩu", "Mật khẩu quản trị không chính xác!")
            self.entry_password.delete(0, 'end')

    def _login_as(self, role):
        self.current_role = role
        # Xóa màn hình chào, giải phóng tài nguyên để dựng UI chính
        self.role_frame.destroy()
        
        self._build_main_ui()
        self._load_movies()
        
        self.status_var.set(f"Đăng nhập thành công với vai trò: {role.upper()}")

    # =================================================================
    # XÂY DỰNG KHUNG UI CHÍNH (Đã được áp bộ lọc phân quyền)
    # =================================================================
    def _build_main_ui(self):
        # ── TOP NAVIGATION BAR ───────────────────────────────────────
        self.topbar = ctk.CTkFrame(self, height=70, corner_radius=0, 
                                   fg_color=BG_PANEL, border_color=BORDER, border_width=1)
        self.topbar.pack(side="top", fill="x")
        self.topbar.pack_propagate(False)

        # Logo
        ctk.CTkLabel(self.topbar, text="CINEBOOK", font=FONT_LOGO, text_color=ACCENT).pack(side="left", padx=(40, 40))

        # Khung chứa Tab
        self.nav_frame = ctk.CTkFrame(self.topbar, fg_color="transparent")
        self.nav_frame.pack(side="left", fill="y", pady=10)
        self.nav_btns = {}
        
        try:
            ic_movie   = ctk.CTkImage(Image.open("assets/icons/movie.png"), size=(20, 20))
            ic_ticket  = ctk.CTkImage(Image.open("assets/icons/ticket.png"), size=(20, 20))
            ic_history = ctk.CTkImage(Image.open("assets/icons/history.png"), size=(20, 20))
            ic_stats   = ctk.CTkImage(Image.open("assets/icons/stats.png"), size=(20, 20))
        except Exception:
            ic_movie = ic_ticket = ic_history = ic_stats = None

        # Định nghĩa bộ phân quyền truy cập cho từng Tab
        # Định dạng: (mã_tab, tên_hiển_thị, hàm_gọi, icon, danh_sách_quyền_được_vào)
        nav_items = [
            ("movies", "DANH SÁCH PHIM", self._show_tab_movies, ic_movie, ["customer", "manager"]),
            ("booking", "ĐẶT VÉ", self._show_tab_booking, ic_ticket, ["customer", "manager"]),
            ("history", "LỊCH SỬ BOOKING", self._show_tab_history, ic_history, ["customer", "manager"]),
            ("stats", "THỐNG KÊ", self._show_tab_stats, ic_stats, ["manager"]),
        ]

        for key, text, cmd, icon, allowed_roles in nav_items:
            # CHỈ TẠO NÚT NẾU VAI TRÒ HIỆN TẠI ĐƯỢC PHÉP TRUY CẬP
            if self.current_role in allowed_roles:
                btn = ctk.CTkButton(self.nav_frame, text=text, image=icon, command=cmd,
                                    compound="left", fg_color="transparent", text_color=TEXT_SEC, 
                                    hover_color=BG_CARD, font=FONT_BTN, width=160, height=45, corner_radius=8)
                btn.pack(side="left", padx=5)
                self.nav_btns[key] = btn

        # Chỉ Quản lý mới có nút bấm Lưu dữ liệu thủ công lên Topbar
        if self.current_role == "manager":
            btn_save = ctk.CTkButton(self.topbar, text="LƯU DỮ LIỆU", command=self._save,
                                     fg_color=BG_CARD, text_color=TEXT_PRI, hover_color=BORDER,
                                     font=FONT_BTN, width=140, height=45, corner_radius=8,
                                     border_width=1, border_color=BORDER)
            btn_save.pack(side="right", padx=40)

        # Nút Đăng xuất quay lại màn hình chọn vai trò
        btn_logout = ctk.CTkButton(self.topbar, text="ĐĂNG XUẤT", command=self._logout,
                                   fg_color="transparent", text_color=ACCENT, hover_color=BG_CARD,
                                   font=FONT_BTN, width=120, height=45, corner_radius=8)
        btn_logout.pack(side="right", padx=10)

        # ── MAIN CONTENT ─────────────────────────────────────────────
        self.main_content = ctk.CTkFrame(self, corner_radius=0, fg_color=BG_APP)
        self.main_content.pack(side="top", fill="both", expand=True)

        self.status_var = ctk.StringVar(value="Hệ thống sẵn sàng hoạt động.")
        self.status_bar = ctk.CTkLabel(self.main_content, textvariable=self.status_var, 
                                       fg_color=BG_PANEL, text_color=TEXT_SEC, 
                                       font=FONT_SMALL, anchor="w", height=35, padx=30)
        self.status_bar.pack(side="bottom", fill="x")

        self.frames: dict[str, ctk.CTkFrame] = {}
        for tab in ("movies", "booking", "history", "stats"):
            f = ctk.CTkFrame(self.main_content, corner_radius=0, fg_color="transparent")
            self.frames[tab] = f

        self._build_movies_tab()
        self._build_booking_tab()
        self._build_history_tab()
        self._build_stats_tab()

        self._show_tab_movies()

    def _show_tab(self, name: str):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[name].pack(fill="both", expand=True)
        for key, btn in self.nav_btns.items():
            if key == name:
                btn.configure(fg_color=BG_CARD, text_color=ACCENT)
            else:
                btn.configure(fg_color="transparent", text_color=TEXT_SEC)

    def _show_tab_movies(self):   self._show_tab("movies")
    def _show_tab_booking(self):  self._show_tab("booking"); self._load_booking_data()
    def _show_tab_history(self):  self._show_tab("history"); self._load_history()
    def _show_tab_stats(self):    self._show_tab("stats");   self._load_stats()

    # =================================================================
    # TAB 1 – DANH SÁCH PHIM (Horizontal + Hover Overlay)
    # =================================================================
    def _build_movies_tab(self):
        f = self.frames["movies"]

        hdr = ctk.CTkFrame(f, fg_color="transparent")
        hdr.pack(fill="x", padx=50, pady=(40, 10))
        
        ctk.CTkLabel(hdr, text="≡ MOVIE SELECTION ≡", text_color=TEXT_PRI, font=FONT_H1).pack(side="left")

        sf = ctk.CTkFrame(hdr, fg_color="transparent")
        sf.pack(side="right")
        self.movie_search = ctk.CTkEntry(sf, placeholder_text="Tìm kiếm phim...", 
                                         width=300, height=45, corner_radius=8,
                                         fg_color=BG_PANEL, border_color=BORDER, font=FONT_BODY)
        self.movie_search.pack(side="left", padx=10)
        ctk.CTkButton(sf, text="TÌM KIẾM", command=self._search_movies, 
                      fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=TEXT_PRI,
                      font=FONT_BTN, width=120, height=45, corner_radius=8).pack(side="left")

        self.movie_frame = ctk.CTkScrollableFrame(f, fg_color="transparent", orientation="horizontal")
        self.movie_frame.pack(fill="both", expand=True, padx=35, pady=(10, 30))

    def _load_movies(self, movies=None):
        for w in self.movie_frame.winfo_children(): w.destroy()
        movies = movies or list(self.manager.movies.values())
        
        for idx, movie in enumerate(movies):
            card = ctk.CTkFrame(self.movie_frame, fg_color=BG_PANEL, corner_radius=16, width=240, height=360)
            card.pack(side="left", padx=15, pady=10)
            card.pack_propagate(False) 
            
            poster_path = getattr(movie, 'poster_path', f"assets/posters/{movie.movie_id}.png")
            
            try:
                img_data = Image.open(poster_path)
                poster_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(240, 360))
                poster_lbl = ctk.CTkLabel(card, image=poster_img, text="")
                poster_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)
            except Exception:
                poster_lbl = ctk.CTkLabel(card, text="NO IMAGE\n\n" + movie.title.upper(), text_color=BORDER, font=("Segoe UI Black", 18), fg_color=BG_CARD)
                poster_lbl.place(relx=0, rely=0, relwidth=1, relheight=1)

            overlay = ctk.CTkFrame(card, fg_color="#0A0A0A", corner_radius=0)

            title_text = movie.title.upper()
            if len(title_text) > 16:  
                title_text = title_text[:14] + "..."

            ctk.CTkLabel(overlay, text=title_text, text_color=TEXT_PRI, font=FONT_H2).pack(pady=(15, 0))
            ctk.CTkLabel(overlay, text=f"★ {movie.rating}  •  {movie.duration} phút", text_color=GOLD, font=FONT_SMALL).pack(pady=(2, 10))
            
            btn_frame = ctk.CTkFrame(overlay, fg_color="transparent")
            btn_frame.pack(fill="x", padx=10, side="bottom", pady=(0, 15))

            btn_details = ctk.CTkButton(btn_frame, text="CHI TIẾT", command=lambda m=movie: self._show_movie_details(m),
                                        fg_color="transparent", hover_color=BG_CARD, text_color=TEXT_PRI, 
                                        font=FONT_BTN, height=35, width=95, corner_radius=6, border_width=1, border_color=BORDER)
            btn_details.pack(side="left", padx=5)

            btn_book = ctk.CTkButton(btn_frame, text="MUA VÉ", command=lambda m=movie: self._select_movie_book(m),
                                     fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color=TEXT_PRI, 
                                     font=FONT_BTN, height=35, width=95, corner_radius=6)
            btn_book.pack(side="right", padx=5)

            def on_enter(e, ov=overlay):
                ov.place(relx=0, rely=0.65, relwidth=1, relheight=0.35)
                ov.lift() 

            def on_leave(e, c=card, ov=overlay):
                x, y = c.winfo_pointerxy()
                cx, cy = c.winfo_rootx(), c.winfo_rooty()
                cw, ch = c.winfo_width(), c.winfo_height()
                if not (cx <= x <= cx + cw and cy <= y <= cy + ch):
                    ov.place_forget()

            poster_lbl.bind("<Enter>", on_enter)
            overlay.bind("<Leave>", on_leave)
            poster_lbl.bind("<Leave>", on_leave)

    def _search_movies(self):
        kw = self.movie_search.get().strip()
        results = self.manager.linear_search_movies(kw) if kw else list(self.manager.movies.values())
        self._load_movies(results)

    def _select_movie_book(self, movie):
        self._selected_movie = movie
        self._show_tab_booking()

    def _show_movie_details(self, movie):
        popup = ctk.CTkToplevel(self)
        popup.title("Thông tin phim")
        popup.geometry("650x450")
        popup.configure(fg_color=BG_APP)
        popup.attributes("-topmost", True)
        
        ctk.CTkLabel(popup, text=movie.title.upper(), font=FONT_H1, text_color=ACCENT).pack(pady=(30, 5))
        ctk.CTkLabel(popup, text=f"Thể loại: {movie.genre}  |  Thời lượng: {movie.duration} phút  |  Đánh giá: ★ {movie.rating}", 
                     font=FONT_BODY, text_color=TEXT_SEC).pack(pady=5)
        
        desc = getattr(movie, 'description', 'Chưa có thông tin mô tả cho bộ phim này.')
        desc_box = ctk.CTkTextbox(popup, width=550, height=180, fg_color=BG_PANEL, text_color=TEXT_PRI, font=FONT_BODY, corner_radius=12, wrap="word")
        desc_box.pack(pady=20)
        desc_box.insert("1.0", desc)
        desc_box.configure(state="disabled")
        
        ctk.CTkButton(popup, text="ĐÓNG", command=popup.destroy, fg_color=BG_CARD, hover_color=BORDER, text_color=TEXT_PRI, font=FONT_BTN, width=120, height=40, corner_radius=8).pack()

    # =================================================================
    # TAB 2 – ĐẶT VÉ (Luồng lọc 3 bước: Phim -> Ngày -> Giờ)
    # =================================================================
    def _build_booking_tab(self):
        f = self.frames["booking"]

        left_container = ctk.CTkFrame(f, fg_color=BG_PANEL, width=420, corner_radius=16, border_width=1, border_color=BORDER)
        left_container.pack(side="left", fill="y", padx=50, pady=30)
        left_container.pack_propagate(False)

        btn_frame = ctk.CTkFrame(left_container, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=30, pady=(0, 30))

        ctk.CTkButton(btn_frame, text="XÁC NHẬN", command=self._confirm_booking, fg_color=ACCENT, text_color=TEXT_PRI, hover_color=ACCENT_HOVER, font=FONT_BTN, height=45, corner_radius=8).pack(fill="x", pady=(0, 10))
        ctk.CTkButton(btn_frame, text="LÀM MỚI", command=self._reset_booking, fg_color="transparent", hover_color=BG_CARD, text_color=TEXT_SEC, height=40, corner_radius=8).pack(fill="x")

        form_frame = ctk.CTkScrollableFrame(left_container, fg_color="transparent")
        form_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(form_frame, text="THÔNG TIN ĐẶT VÉ", text_color=TEXT_PRI, font=FONT_H2).pack(padx=20, pady=(10, 10), anchor="w")

        def lbl(parent, text):
            ctk.CTkLabel(parent, text=text, text_color=TEXT_SEC, font=FONT_SMALL).pack(anchor="w", padx=20, pady=(5, 0))

        def entry(parent):
            e = ctk.CTkEntry(parent, fg_color=BG_CARD, border_color=BORDER, text_color=TEXT_PRI, font=FONT_BODY, height=40, corner_radius=8)
            e.pack(fill="x", padx=20, pady=(2, 5))
            return e
            
        def combo(parent, command):
            c = ctk.CTkComboBox(parent, state="readonly", font=FONT_BODY, height=40, fg_color=BG_CARD, border_color=BORDER, button_color=ACCENT, dropdown_fg_color=BG_CARD, dropdown_text_color=TEXT_PRI, command=command)
            c.pack(fill="x", padx=20, pady=(2, 5))
            return c

        lbl(form_frame, "Họ tên khách hàng")
        self.e_name = entry(form_frame)
        lbl(form_frame, "Số điện thoại liên lạc")
        self.e_phone = entry(form_frame)

        lbl(form_frame, "Chọn phim muốn xem")
        self.combo_movie = combo(form_frame, self._on_combo_movie_select)
        
        lbl(form_frame, "Chọn ngày chiếu")
        self.combo_date = combo(form_frame, self._on_combo_date_select)
        
        lbl(form_frame, "Chọn khung giờ và phòng phù hợp")
        self.combo_time = combo(form_frame, self._on_combo_time_select)

        lbl(form_frame, "Vị trí ghế đã chọn")
        self.lbl_seats = ctk.CTkLabel(form_frame, text="--", text_color=TEXT_PRI, font=FONT_BODY, wraplength=280, justify="left")
        self.lbl_seats.pack(anchor="w", padx=20, pady=(2, 5))

        self.lbl_total = ctk.CTkLabel(form_frame, text="0 ₫", text_color=ACCENT, font=("Segoe UI", 28, "bold"))
        self.lbl_total.pack(pady=(10, 10), padx=20, anchor="w")

        right = ctk.CTkFrame(f, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True, padx=(0, 50), pady=30)

        leg = ctk.CTkFrame(right, fg_color="transparent")
        leg.pack(pady=(0, 20))
        for color, label in [(SEAT_EMPTY, "Trống"), (SEAT_BOOKED, "Đã đặt"), (ACCENT, "Đang chọn")]:
            ctk.CTkFrame(leg, fg_color=color, width=24, height=24, corner_radius=6, border_color=BORDER, border_width=1).pack(side="left", padx=(30, 10))
            ctk.CTkLabel(leg, text=label, text_color=TEXT_SEC, font=FONT_BODY).pack(side="left")

        ctk.CTkFrame(right, fg_color=ACCENT, height=4, corner_radius=2).pack(fill="x", padx=100, pady=(20, 10))
        ctk.CTkLabel(right, text="M À N   H Ì N H", text_color=ACCENT, font=FONT_SMALL).pack(pady=(0, 30))

        self.seat_container = ctk.CTkFrame(right, fg_color="transparent")
        self.seat_container.pack()
        self._seat_buttons: dict = {}

    def _load_booking_data(self):
        self._movie_map = {m.title: m for m in self.manager.movies.values()}
        movie_titles = list(self._movie_map.keys())
        self.combo_movie.configure(values=movie_titles)
        
        self.combo_date.set("")
        self.combo_time.set("")
        self.combo_date.configure(values=[])
        self.combo_time.configure(values=[])
        
        if self._selected_movie and self._selected_movie.title in movie_titles:
            self.combo_movie.set(self._selected_movie.title)
            self._on_combo_movie_select(self._selected_movie.title)
        elif movie_titles:
            self.combo_movie.set(movie_titles[0])
            self._on_combo_movie_select(movie_titles[0])

    def _on_combo_movie_select(self, choice):
        selected_m = self._movie_map.get(choice)
        if not selected_m: return
        self._current_movie_showtimes = [st for st in self.manager.showtimes.values() if st.movie_id == selected_m.movie_id]
        
        dates = list(set(st.start_time.split("T")[0] for st in self._current_movie_showtimes))
        dates.sort()
        self.combo_date.configure(values=dates)
        self.combo_time.configure(values=[])
        self.combo_date.set("")
        self.combo_time.set("")
        
        if dates:
            self.combo_date.set(dates[0])
            self._on_combo_date_select(dates[0])
        else:
            self.combo_date.set("Không có lịch chiếu")
            self._selected_showtime = None
            self._update_seat_display()

    def _on_combo_date_select(self, choice):
        sts_for_date = [st for st in self._current_movie_showtimes if st.start_time.startswith(choice)]
        self._time_map = {}
        time_labels = []
        for st in sts_for_date:
            time_part = st.start_time.split("T")[1][:5]
            label = f"{time_part} — {st.room}"
            time_labels.append(label)
            self._time_map[label] = st
            
        time_labels.sort()
        self.combo_time.configure(values=time_labels)
        if time_labels:
            self.combo_time.set(time_labels[0])
            self._on_combo_time_select(time_labels[0])

    def _on_combo_time_select(self, choice):
        self._selected_showtime = self._time_map.get(choice)
        self._selected_seats = []
        self._update_seat_display()
        self._update_price()

    def _update_seat_display(self):
        for w in self.seat_container.winfo_children(): w.destroy()
        self._seat_buttons.clear()
        if not self._selected_showtime: return
        sm = self._selected_showtime.seat_map
        
        hdr_row = ctk.CTkFrame(self.seat_container, fg_color="transparent")
        hdr_row.pack()
        ctk.CTkLabel(hdr_row, text="", width=40).pack(side="left", padx=5)
        for c in range(sm.cols):
            ctk.CTkLabel(hdr_row, text=str(c + 1), text_color=TEXT_SEC, font=FONT_SMALL, width=55).pack(side="left", padx=4)

        for r in range(sm.rows):
            row_f = ctk.CTkFrame(self.seat_container, fg_color="transparent")
            row_f.pack(pady=4)
            ctk.CTkLabel(row_f, text=chr(65 + r), text_color=TEXT_SEC, font=FONT_BTN, width=40).pack(side="left", padx=5)
            
            for c in range(sm.cols):
                lbl_seat = sm.seat_label(r, c)
                status = sm._grid[r][c]
                is_booked = (status == SeatStatus.BOOKED) or (str(status) in ["1", "BOOKED", "SeatStatus.BOOKED"])
                
                if is_booked:
                    bg, hover, txt, state, bdr = SEAT_BOOKED, SEAT_BOOKED, "#555566", "disabled", SEAT_BOOKED
                elif lbl_seat in self._selected_seats:
                    bg, hover, txt, state, bdr = ACCENT, ACCENT_HOVER, TEXT_PRI, "normal", ACCENT
                else:
                    bg, hover, txt, state, bdr = SEAT_EMPTY, "#3A3A4A", TEXT_PRI, "normal", BORDER

                btn = ctk.CTkButton(row_f, text=lbl_seat, fg_color=bg, text_color=txt, hover_color=hover, font=FONT_SMALL, width=55, height=45, corner_radius=8, state=state, border_color=bdr, border_width=1, command=lambda lb=lbl_seat: self._toggle_seat(lb))
                btn.pack(side="left", padx=4)
                self._seat_buttons[lbl_seat] = btn

    def _toggle_seat(self, label: str):
        if label in self._selected_seats:
            self._selected_seats.remove(label)
            self._seat_buttons[label].configure(fg_color=SEAT_EMPTY, text_color=TEXT_PRI, border_color=BORDER)
        else:
            if len(self._selected_seats) >= 8:
                messagebox.showwarning("Giới hạn", "Chỉ được phép chọn tối đa 8 ghế/lượt!")
                return
            self._selected_seats.append(label)
            self._seat_buttons[label].configure(fg_color=ACCENT, text_color=TEXT_PRI, border_color=ACCENT)
        self._update_price()
        self.lbl_seats.configure(text=", ".join(self._selected_seats) or "--")

    def _update_price(self):
        if self._selected_showtime and self._selected_seats:
            total = self._selected_showtime.price * len(self._selected_seats)
            self.lbl_total.configure(text=f"{int(total):,} ₫")
        else:
            self.lbl_total.configure(text="0 ₫")

    def _confirm_booking(self):
        name  = self.e_name.get().strip()
        phone = self.e_phone.get().strip()
        if not name or not phone:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng hoàn thiện họ tên và SĐT!")
            return
        if not self._selected_showtime or not self._selected_seats:
            messagebox.showwarning("Chưa hoàn tất", "Vui lòng chọn suất chiếu và ghế ngồi.")
            return

        ok, msg, node = self.manager.book_seats(self._selected_showtime.showtime_id, name, phone, self._selected_seats)
        if ok:
            messagebox.showinfo("Thành công", f"Booking ID: {node.booking_id}\nSố lượng: {len(self._selected_seats)} ghế\nTổng phí: {int(node.total_price):,} ₫")
            self._reset_booking()
            self.manager.saveData() # Khách đặt vé hệ thống vẫn tự động lưu xuống DB
        else:
            messagebox.showerror("Thất bại", msg)

    def _reset_booking(self):
        self.e_name.delete(0, 'end')
        self.e_phone.delete(0, 'end')
        self._selected_seats = []
        self.lbl_seats.configure(text="--")
        self.lbl_total.configure(text="0 ₫")
        self._update_seat_display()

    # =================================================================
    # TAB 3 – LỊCH SỬ ĐẶT VÉ
    # =================================================================
    # =================================================================
    # TAB 3 – LỊCH SỬ ĐẶT VÉ
    # =================================================================
    def _build_history_tab(self):
        f = self.frames["history"]

        hdr = ctk.CTkFrame(f, fg_color="transparent")
        hdr.pack(fill="x", padx=50, pady=(50, 20))
        ctk.CTkLabel(hdr, text="QUẢN LÝ GIAO DỊCH", text_color=TEXT_PRI, font=FONT_H1).pack(side="left")

        sf = ctk.CTkFrame(hdr, fg_color="transparent")
        sf.pack(side="right")
        self.e_search_phone = ctk.CTkEntry(sf, placeholder_text="Tra cứu SĐT...", fg_color=BG_PANEL, border_color=BORDER, height=45)
        self.e_search_phone.pack(side="left", padx=10)
        
        ctk.CTkButton(sf, text="TÌM", width=70, height=45, command=self._search_history, fg_color=ACCENT, hover_color=ACCENT_HOVER).pack(side="left", padx=5)
        ctk.CTkButton(sf, text="TẤT CẢ", width=90, height=45, command=self._load_history, fg_color=BG_CARD, hover_color=BORDER, text_color=TEXT_PRI).pack(side="left", padx=5)
        
        # Chỉ Quản lý mới được phép nhìn thấy nút HỦY VÉ nguy hiểm
        if self.current_role == "manager":
            ctk.CTkButton(sf, text="HUỶ VÉ", width=90, height=45, command=self._cancel_selected, fg_color="transparent", border_width=1, border_color=ACCENT, text_color=ACCENT, hover_color=BG_CARD).pack(side="left", padx=(20, 0))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background=BG_PANEL, foreground=TEXT_PRI, fieldbackground=BG_PANEL, rowheight=45, borderwidth=0, font=FONT_BODY)
        style.map('Treeview', background=[('selected', ACCENT)])
        style.configure("Treeview.Heading", background=BG_CARD, foreground=TEXT_SEC, font=FONT_BTN, borderwidth=0, padding=12)

        tree_frame = ctk.CTkFrame(f, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=50, pady=(0, 50))

        # ĐÃ SỬA: Đổi "Phòng" thành "Khung Giờ"
        cols = ("Mã Giao Dịch", "Khách Hàng", "SĐT", "Tên Phim", "Khung Giờ", "Ghế", "Tổng Thanh Toán", "Thời Gian Đặt", "Trạng Thái")
        self.tree_history = ttk.Treeview(tree_frame, columns=cols, show="headings")
        
        # ĐÃ SỬA: Tăng độ rộng cột Khung Giờ (thứ 5) lên 120px để hiển thị chữ đẹp hơn
        widths = [140, 180, 130, 260, 120, 120, 150, 160, 100]
        for col, w in zip(cols, widths):
            self.tree_history.heading(col, text=col)
            self.tree_history.column(col, width=w, anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_history.yview)
        self.tree_history.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree_history.pack(fill="both", expand=True)

    def _load_history(self, nodes=None):
        self.tree_history.delete(*self.tree_history.get_children())
        nodes = nodes or list(self.manager.bookings)
        
        for node in nodes:
            movie = self.manager.movies.get(node.movie_id)
            mname = movie.title.upper() if movie else node.movie_id
            tag = "cancelled" if node.status == "CANCELLED" else "ok"
            
            # --- XỬ LÝ LẤY KHUNG GIỜ THỰC TẾ ---
            st = self.manager.showtimes.get(node.showtime_id)
            time_display = node.showtime_id # Fallback dự phòng nếu lỗi data
            
            if st:
                try:
                    # Bóc tách "2026-06-12T19:30:00" thành Giờ và Ngày
                    date_str, time_str = st.start_time.split("T")
                    y, m, d = date_str.split("-")
                    # Hiển thị theo chuẩn Việt Nam: "19:30 (12/06)"
                    time_display = f"{time_str[:5]} ({d}/{m})"
                except Exception:
                    pass
            
            self.tree_history.insert("", "end", iid=node.booking_id, values=(
                node.booking_id, node.customer_name, node.customer_phone,
                mname, time_display, ", ".join(node.seats),
                f"{int(node.total_price):,} ₫", node.booked_at[:16], node.status
            ), tags=(tag,))
            
        self.tree_history.tag_configure("cancelled", foreground=TEXT_SEC)
        self.tree_history.tag_configure("ok", foreground="#00C853")

    def _search_history(self):
        phone = self.e_search_phone.get().strip()
        nodes = self.manager.search_booking_by_phone(phone) if phone else list(self.manager.bookings)
        self._load_history(nodes)

    def _cancel_selected(self):
        sel = self.tree_history.selection()
        if not sel: return
        bid = sel[0]
        if messagebox.askyesno("Hệ thống cảnh báo", f"Thực hiện huỷ bỏ giao dịch {bid}?"):
            ok, msg = self.manager.cancel_booking(bid)
            if ok:
                self.manager.saveData()
                self._load_history()
            messagebox.showinfo("Thông báo", msg)

    # =================================================================
    # TAB 4 – THỐNG KÊ (Chỉ dành cho Manager)
    # =================================================================
    def _build_stats_tab(self):
        f = self.frames["stats"]
        hdr = ctk.CTkFrame(f, fg_color="transparent")
        hdr.pack(fill="x", padx=50, pady=(50, 40))
        ctk.CTkLabel(hdr, text="BÁO CÁO KINH DOANH", text_color=TEXT_PRI, font=FONT_H1).pack(side="left")
        self.stats_frame = ctk.CTkFrame(f, fg_color="transparent")
        self.stats_frame.pack(fill="both", expand=True, padx=30)

    def _load_stats(self):
        if self.current_role != "manager": return
        for w in self.stats_frame.winfo_children(): w.destroy()
        s = self.manager.get_statistics()

        cards = [
            ("TỔNG PHIM", str(s["total_movies"])), ("SUẤT CHIẾU", str(s["total_showtimes"])),
            ("TỔNG VÉ ĐẶT", str(s["total_bookings"])), ("ĐÃ THANH TOÁN", str(s["confirmed"])),
            ("VÉ ĐÃ HUỶ", str(s["cancelled"])), ("DOANH THU ƯỚC TÍNH", f"{int(s['total_revenue']):,} ₫"),
            ("PHIM HOT NHẤT", s["top_movie"]), ("TỶ LỆ LẤP ĐẦY", f"{s['seat_occupancy']}%"),
        ]

        for idx, (title, value) in enumerate(cards):
            r, c = divmod(idx, 4)
            card = ctk.CTkFrame(self.stats_frame, fg_color=BG_PANEL, corner_radius=16, border_width=1, border_color=BORDER)
            card.grid(row=r, column=c, padx=20, pady=20, sticky="nsew")
            self.stats_frame.columnconfigure(c, weight=1)
            ctk.CTkLabel(card, text=title, text_color=TEXT_SEC, font=FONT_BTN).pack(pady=(30, 10))
            ctk.CTkLabel(card, text=value, text_color=TEXT_PRI, font=("Segoe UI", 32, "bold"), wraplength=350).pack(pady=(0, 30))

    def _save(self):
        self.manager.saveData()
        self.status_var.set("Hệ thống đã lưu trữ File định dạng an toàn.")

    def _logout(self):
        # Hủy UI chính và quay về màn hình phân quyền đăng nhập ban đầu
        self.topbar.destroy()
        self.main_content.destroy()
        self._selected_movie = None
        self._selected_showtime = None
        self._selected_seats = []
        self._build_role_selection_screen()
    
if __name__ == "__main__":
    app = CinemaApp()
    app.mainloop()