import flet as ft
import pathlib
from scripts.face_detection import CaptureFace
import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from app.database.db import DB
from app.services.deepface_api import add_user_face
from app.models.employees import Employee

def main(page: ft.Page):
    page.title = "افزودن کاربر جدید"
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.fonts = {
        "Vazir": "assets/fonts/Vazir.ttf",
    }
    
    dlg = ft.AlertDialog(
        # modal=True,
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
                on_click=lambda e: page.close(dlg),
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


    
    def newuser(e):
        name = name_field.value
        personnel_id = personnel_id_field.value
        employee = Employee(name, personnel_id)
        user_added = DB().AddUser(employee.name, employee.code)
        if user_added:
            face_added = add_user_face(image_control.src, personnel_id)
            if face_added:
                page.open(dlg)
            else:
                ...
            

    page.theme = ft.Theme(font_family="Vazir")
    
    login_button = ft.ElevatedButton(
        "ثبت کاربر", 
        on_click=newuser,
        width=300,
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    name_field = ft.TextField(
        label="نام و نام خانوادگی",
        width=300,
        border_radius=10,
        prefix_icon=ft.icons.PERSON,
        color=ft.colors.BLACK38,
    )
    
    personnel_id_field = ft.TextField(
        label="کد پرسنلی",
        width=300,
        border_radius=10,
        prefix_icon=ft.icons.LOCK,
        color=ft.colors.BLACK38,
    )

    image_control = ft.Image(src='app/views/assets/200w.gif', width=200, height=100, border_radius=12, fit=ft.ImageFit.COVER)

    def on_capture_click(e):
        CaptureFace(page, image_control, 'scan')

    capture_button = ft.IconButton(on_click=on_capture_click,
                           icon=ft.icons.ADD_A_PHOTO,
                           icon_color="Gray",
                           icon_size=50,
                           tooltip="افزودن چهره", )
    
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("افزودن کاربر جدید", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    ft.Divider(height=20, color="transparent"),
                    name_field,
                    personnel_id_field,
                    ft.Divider(height=5, color="transparent"),
                    capture_button,
                    ft.Divider(height=5, color="transparent"),
                    image_control, 
                    ft.Divider(height=10, color="transparent"),
                    login_button,
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
        )
    )

ft.app(target=main, assets_dir="assets")