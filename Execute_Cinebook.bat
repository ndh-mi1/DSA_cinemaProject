::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFBVYQwqFAE+1EbsQ5+n//NakrUANRucsa4rf5pC9Ad8Q40vheJcdxHVQncgYQUkILET7OF5mnT4a5THUZf3R4EKxGhm1wngRJGZ9iWbdjRspb9ltmdc/1yGq/XH2nKoen3H8Uck=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFBVYQwqFAE+1EbsQ5+n//NakrUANRucsa4rf5pC9Ad8Q40vheJcdxHVQncgYQUkILET7OF5mnT4a5THUZf3R4EKxGhm1wngRJGZ9iWbdjRspb9ltmdc/8AmQ2W/QsI5e1GD6Pg==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
chcp 65001 >nul
title CineBook - Ung dung Dat ve Xem phim

cd /d "%~dp0"

echo ===================================================
echo        HE THONG DAT VE XEM PHIM - CINEBOOK
echo ===================================================
echo.
echo [*] Dang kiem tra moi truong va dong bo du lieu...
echo Vui long doi trong giay lat...

:: Cài đặt thư viện
pip install customtkinter pillow --quiet >nul 2>&1

:: Quét tìm và chạy file seed
if exist "seed_data.py" (
    python seed_data.py
) else if exist "data\seed_data.py" (
    python data\seed_data.py
) else (
    echo [LOI] Khong tim thay file seed_data.py trong he thong!
)

echo.
echo [*] Dong bo hoan tat! Dang mo ung dung...
start python app_gui.py

exit