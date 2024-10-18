import flet as ft
from scripts.face_detection import CaptureFace
import threading

def main(page: ft.Page):
    page.title = "افزودن کاربر جدید"
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.fonts = {
        "Vazir": "assets/fonts/Vazir.ttf",
    }

    page.theme = ft.Theme(font_family="Vazir")
    
    
    login_button = ft.ElevatedButton(
        "ورود", 
        # on_click=login,
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
        # threading.Thread(target=capture_face_instance.capture).start()

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