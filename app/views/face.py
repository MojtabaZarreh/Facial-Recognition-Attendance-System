import flet as ft
import cv2
import threading
import asyncio
import random
import os
import time as t
from datetime import *
from scripts.face_detection import CaptureFace

if not os.path.exists('image'):
    os.makedirs('image')

async def update_time(page, time_display):
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        time_display.value = current_time
        page.update()
        await asyncio.sleep(1)

def main(page: ft.Page):
    page.title = "تشخیص چهره"
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.fonts = {
        "Vazir": "assets/fonts/Vazir.ttf",
    }

    page.theme = ft.Theme(font_family="Vazir")
    image_control = ft.Image(src='app/views/assets/sample.jpg', width=400, height=300, fit=ft.ImageFit.CONTAIN, border_radius=10)

    def on_button_click(e):
        capture_face_instance = CaptureFace(page, image_control)
        threading.Thread(target=capture_face_instance, args=(page, image_control)).start() 
    
    time_display = ft.Text(
        datetime.now().strftime("%H:%M:%S"),
        size=24,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.BLUE_900,
    )
    
    end_drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.START,
        bgcolor=ft.colors.WHITE,
        controls=[
            ft.Divider(height=30, color="transparent"),
            ft.Row(
                [ft.Text("تنظیمات", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=30, color="transparent"),
            ft.NavigationDrawerDestination(icon=ft.icons.VERIFIED_USER_SHARP, label="مدیریت کاربران"),
            ft.NavigationDrawerDestination(icon=ft.icons.ADD_COMMENT, label="افزودن کاربر جدید"),
        ],
    )

    start_button = ft.ElevatedButton(
        "شروع ضبط چهره",
        on_click=on_button_click,
        width=300,
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    page.add(
        time_display,
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("تشخیص چهره", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    ft.Divider(height=20, color="transparent"),
                    image_control,
                    ft.Divider(height=20, color="transparent"),
                    start_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            border_radius=15,
            width=350,
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=2, blur_radius=15, color=ft.colors.BLACK12, offset=ft.Offset(2, 2)
            ),
        )
    )
        
    page.add(ft.IconButton(on_click=lambda e: page.open(end_drawer),
                           icon=ft.icons.SETTINGS,
                           icon_color="Gray",
                           icon_size=50,
                           tooltip="تنظیمات", ))

    asyncio.run(update_time(page, time_display))

ft.app(target=main, assets_dir="assets")
