import flet as ft
from flet import View, colors

class Login:
    def __init__(self, page):
        self.page = page
        self.email_field = ft.TextField(
            label="ایمیل",
            width=300,
            border_radius=10,
            prefix_icon=ft.icons.EMAIL,
            keyboard_type=ft.KeyboardType.EMAIL,
            color=ft.colors.BLACK38,
        )
        self.password_field = ft.TextField(
            label="رمز عبور",
            password=True,
            can_reveal_password=True,
            width=300,
            border_radius=10,
            prefix_icon=ft.icons.LOCK,
            color=ft.colors.BLACK38,
        )
        self.login_button = ft.ElevatedButton(
            "ورود", 
            on_click=self.login,
            width=300,
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        )
        self.forgot_password_link = ft.TextButton(
            "فراموشی رمز عبور؟", on_click=lambda _: print("فراموشی رمز عبور کلیک شد!"))

    def login(self, e):
        if self.email_field.value == "user@example.com" and self.password_field.value == "12345":
            self.page.snack_bar = ft.SnackBar(ft.Text("ورود موفقیت آمیز بود!"), bgcolor=ft.colors.GREEN)
            self.page.go("/home")
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("ایمیل یا رمز عبور اشتباه است"), bgcolor=ft.colors.RED)
            self.page.go("/home")
        self.page.snack_bar.open = True
        self.page.update()

    def get_view(self):
        return View(
            "/",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("به سیستم خوش آمدید", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                            ft.Divider(height=20, color="transparent"),
                            self.email_field,
                            self.password_field,
                            ft.Divider(height=10, color="transparent"),
                            self.login_button,
                            ft.Divider(height=10, color="transparent"),
                            self.forgot_password_link,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    border_radius=15,
                    width=350,
                    # height=400,
                    bgcolor=ft.colors.WHITE,
                    alignment=ft.alignment.center,
                    shadow=ft.BoxShadow(
                        spread_radius=2, blur_radius=15, color=ft.colors.BLACK12, offset=ft.Offset(2, 2)
                    ),
                )
            ],
            bgcolor=ft.colors.BLUE_GREY_50, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
            vertical_alignment=ft.MainAxisAlignment.CENTER,     
        )