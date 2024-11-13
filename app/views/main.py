import flet as ft
import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from app.routes.router import get_route_view
from flet import *

def main(page: ft.Page):
    page.title = "FletFace"
    page.bgcolor = ft.colors.BLUE_GREY_50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_height = 800
    page.window_width = 1024

    def route_change(e):
        print("Route change:", e.route)
        view = get_route_view(page.route, page)
        if view:
            page.views.clear()
            page.views.append(view)
            page.update()
        else:
            page.views.clear()
            page.views.append(
                ft.View(
                    "/404",
                    [ft.Text("صفحه مورد نظر یافت نشد", size=30, color=ft.colors.RED)]
                )
            )
            page.update()

    page.fonts = {
        "Vazir": "assets/fonts/Vazir.ttf",
    }

    page.theme = ft.Theme(font_family="Vazir")
    page.on_route_change = route_change
    page.go(page.route)

ft.app(target=main, assets_dir="assets", route_url_strategy="hash")