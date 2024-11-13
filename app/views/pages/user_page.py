import flet as ft
from flet import AppBar, ElevatedButton, Page, Text, View, colors, NavigationDrawer
import asyncio
from datetime import datetime
import threading
from app.views.scripts.face_detection import CaptureFace
from app.views.scripts.check_user import NewUser

class AddUser:
    def __init__(self, page):
        self.page = page
        
        self.name_field = ft.TextField(
            label="نام و نام خانوادگی",
            width=300,
            border_radius=10,
            prefix_icon=ft.icons.PERSON,
            color=ft.colors.BLACK38,
        )
        
        self.personnel_id_field = ft.TextField(
            label="کد پرسنلی",
            width=300,
            border_radius=10,
            prefix_icon=ft.icons.LOCK,
            color=ft.colors.BLACK38,
        )
        
        self.capture_button = ft.IconButton(on_click=lambda _: self.on_capture_click(),
                            icon=ft.icons.ADD_A_PHOTO,
                            icon_color="Gray",
                            icon_size=50,
                            tooltip="افزودن چهره", )

        self.image_control = ft.Image(src='app/views/assets/200w.gif', width=200, height=100, border_radius=12, fit=ft.ImageFit.COVER)
            
        self.login_button = ft.ElevatedButton(
            "ثبت کاربر", 
            on_click=lambda e: self.handle_new_user(self.name_field.value, self.personnel_id_field.value, self.image_control.src),
            width=300,
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        )
        
        self.dlg_ok = ft.AlertDialog(
            title=ft.Text(
                "عملیات موفق",
                style=ft.TextStyle(color=ft.colors.GREEN, size=24, weight=ft.FontWeight.BOLD),
                text_align=ft.TextAlign.CENTER,
            ),
            content=ft.Column(
                [
                    ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINE, color=ft.colors.GREEN, size=80),
                    ft.Text(
                        ".کاربر با موفقیت افزوده شد",
                        style=ft.TextStyle(size=18, color=ft.colors.BLACK87),
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                # spacing=20,
                width=80,
                height=100
            ),
            actions=[
                ft.ElevatedButton(
                    "باشه",
                    on_click=lambda e: page.close(self.dlg_ok),
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.GREEN,
                        color=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        # padding=ft.EdgeInsets.symmetric(vertical=12, horizontal=24),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER, 
            shape=ft.RoundedRectangleBorder(radius=20),  
            bgcolor=ft.colors.WHITE,
        )
        
        self.dlg_error = ft.AlertDialog(
            title=ft.Text(
                "عملیات ناموفق",
                style=ft.TextStyle(color=ft.colors.RED, size=24, weight=ft.FontWeight.BOLD),
                text_align=ft.TextAlign.CENTER,
            ),
            content=ft.Column(
                [
                    ft.Icon(name=ft.icons.ERROR_OUTLINE_SHARP, color=ft.colors.RED, size=80),
                    ft.Text(
                        ".خطا در افزودن کاربر جدید",
                        style=ft.TextStyle(size=18, color=ft.colors.BLACK87),
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                # spacing=20,
                width=80,
                height=130
            ),
            actions=[
                ft.ElevatedButton(
                    "باشه",
                    on_click=lambda e: page.close(self.dlg_error),
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.RED,
                        color=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        # padding=ft.EdgeInsets.symmetric(vertical=12, horizontal=24),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER, 
            shape=ft.RoundedRectangleBorder(radius=20),  
            bgcolor=ft.colors.WHITE,
        )
    
    def on_capture_click(self):
        capture_face_instance = CaptureFace(self.page, self.image_control, typee='scan')
        capture_face_instance()
        
    def handle_new_user(self,name, personnel_id, image_src):
        new_user = NewUser(name, personnel_id, image_src)
        if new_user.check():
            self.page.open(self.dlg_ok)
        else:
            self.page.open(self.dlg_error)
    
    def go_back(self, e):
        self.page.go('/home')
            
    def get_view(self):
        return View(
            "/home/newuser",
            controls=[
                ft.Container(
                content=ft.Column(
                    [
                        ft.Text("افزودن کاربر جدید", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                        ft.Divider(height=20, color="transparent"),
                        self.name_field,
                        self.personnel_id_field,
                        ft.Divider(height=5, color="transparent"),
                        self.capture_button,
                        ft.Divider(height=5, color="transparent"),
                        self.image_control, 
                        ft.Divider(height=10, color="transparent"),
                        self.login_button,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=20,
                border_radius=15,
                width=400,
                height=550, 
                bgcolor=ft.colors.WHITE,
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=2, blur_radius=15, color=ft.colors.BLACK12, offset=ft.Offset(2, 2)
                ),
            ),
            ft.IconButton(
                on_click=lambda e: self.page.open(self.go_back(e)),
                icon=ft.icons.ARROW_CIRCLE_LEFT_OUTLINED,
                icon_color="Gray",
                icon_size=50,
                tooltip="برگشت",
            )
        ],
        bgcolor=ft.colors.BLUE_GREY_50, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
        vertical_alignment=ft.MainAxisAlignment.CENTER,     
    )