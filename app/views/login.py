import flet as ft

def main(page: ft.Page):
    page.title = "صفحه لاگین"
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.fonts = {
        "Vazir": "assets/fonts/Vazir.ttf",
    }

    page.theme = ft.Theme(font_family="Vazir")

    email_field = ft.TextField(
    label="ایمیل",
    width=300,
    border_radius=10,
    prefix_icon=ft.icons.EMAIL,
    keyboard_type=ft.KeyboardType.EMAIL,
    )
    
    password_field = ft.TextField(
        label="رمز عبور",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=10,
        prefix_icon=ft.icons.LOCK,
    )

    def login(e):
        if email_field.value == "user@example.com" and password_field.value == "12345":
            page.snack_bar = ft.SnackBar(ft.Text("ورود موفقیت آمیز بود!"), bgcolor=ft.colors.GREEN)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("ایمیل یا رمز عبور اشتباه است"), bgcolor=ft.colors.RED)
        page.snack_bar.open = True
        page.update()

    login_button = ft.ElevatedButton(
        "ورود", 
        on_click=login,
        width=300,
        bgcolor=ft.colors.BLUE_500,
        color=ft.colors.WHITE,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )
    
    forgot_password_link = ft.TextButton("فراموشی رمز عبور؟", on_click=lambda _: print("فراموشی رمز عبور کلیک شد!"))

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("به سیستم خوش آمدید", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                    ft.Divider(height=20, color="transparent"),
                    email_field,
                    password_field,
                    ft.Divider(height=10, color="transparent"),
                    login_button,
                    ft.Divider(height=10, color="transparent"),
                    forgot_password_link,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=20,
            border_radius=15,
            width=350,
            height=400,
            bgcolor=ft.colors.WHITE,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(
                spread_radius=2, blur_radius=15, color=ft.colors.BLACK12, offset=ft.Offset(2, 2)
            ),
        )
    )

ft.app(target=main, assets_dir="assets")
