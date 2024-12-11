import flet as ft
from flet import View
import asyncio
from datetime import datetime
import threading
import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from app.views.scripts.face_detection import *
from app.views.scripts.iran_time import current_time

class Home:
    def __init__(self, page):
        self.page = page
        self.image_control = ft.Image(
            src='app/views/assets/1376-face-id.gif',
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            border_radius=10
        )
        self.time_display = ft.Text(
            datetime.now().strftime("%H:%M:%S"),
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_900,
        )
        self.capturing = False
        self.capture_thread = None
        self.action_sheet = self.action_sheet()
        self.bottom_sheet = ft.CupertinoBottomSheet(self.action_sheet)
    
    def action_sheet(self):
        return ft.CupertinoActionSheet(
            title=ft.Row(
                [ft.Text("تنظیمات", style=ft.TextStyle(font_family="Vazir"))], 
                alignment=ft.MainAxisAlignment.CENTER
            ),
            message=ft.Row(
                [ft.Text("لطفا روی گزینه مورد نظر کلیک کنید", style=ft.TextStyle(font_family="Vazir"))], 
                alignment=ft.MainAxisAlignment.CENTER
            ),
            cancel=ft.CupertinoActionSheetAction(
                content=ft.Text("بستن", style=ft.TextStyle(font_family="Vazir")),
                on_click=lambda e: self.handle_click_close(e),
            ),
            actions=[
                ft.CupertinoActionSheetAction(
                    content=ft.Text("لیست کاربران", style=ft.TextStyle(font_family="Vazir")),
                    on_click=lambda e: self.handle_click_employees(),
                ),
                ft.CupertinoActionSheetAction(
                    content=ft.Text("افزودن کاربر", style=ft.TextStyle(font_family="Vazir")),
                    on_click=lambda e: self.handle_click_newuser(),
                ),
                ft.CupertinoActionSheetAction(
                    content=ft.Text("دریافت گزارش تردد", style=ft.TextStyle(font_family="Vazir")),
                    on_click=lambda e: self.handle_click_log(e),
                ),
            ],
        )


    async def update_time(self):
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_display.value = current_time
            self.page.update()
            await asyncio.sleep(1)
            
    def start_capture(self):
        self.capturing = True
        self.capture_button.text = "توقف شناسایی"
        self.capture_button.bgcolor = ft.colors.RED
        self.page.update()
        self.capture_face_instance = CaptureFace(self.page, self.image_control, '')
        self.capture_thread = threading.Thread(target=self.capture_face_instance)
        self.capture_thread.start()

    def toggle_capture(self, e):
        if self.capturing:
            self.stop_capture()
        else:
            self.start_capture()
        
    def stop_capture(self):
        self.capture_button.text = "شروع ضبط چهره"
        self.capture_button.bgcolor = ft.colors.BLUE_500
        self.page.update()
        if getattr(self, "capture_face_instance", None):
            self.capture_face_instance.stop() 
        self.capturing = False  
 
    def run_update_time(self):
        asyncio.run(self.update_time())

    def get_view(self):
        threading.Thread(target=self.run_update_time).start()
        self.capture_button = ft.ElevatedButton(
            "شروع ضبط چهره",
            on_click=self.toggle_capture,
            width=300,
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        )
        
    def handle_click_newuser(self):
        self.page.go('/home/newuser')
        self.stop_capture()
    
    def handle_click_employees(self):
        self.page.go('/home/employees')
        self.stop_capture()
        
    def handle_click_close(self, e):
        self.page.close(self.bottom_sheet)
    
    def handle_click_log(self, e):
        DB().ExportLog()
        alert = ft.AlertDialog(
            title=ft.Text(
                "دریافت شد",
                style=ft.TextStyle(color=ft.colors.GREEN, size=24, weight=ft.FontWeight.BOLD),
                text_align=ft.TextAlign.CENTER,
            ),
            content=ft.Column(
                [
                    ft.Icon(name=ft.icons.CHECK_CIRCLE_OUTLINE, color=ft.colors.GREEN, size=80),
                    ft.Text(
                        'گزارش در دسکتاپ شما ذخیره شد',
                        style=ft.TextStyle(size=15, color=ft.colors.BLACK87),
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=80,
                height=120
            ),
            actions_alignment=ft.MainAxisAlignment.CENTER, 
            shape=ft.RoundedRectangleBorder(radius=20),  
            bgcolor=ft.colors.WHITE,
        )
        self.page.show_dialog(alert)
        threading.Timer(2, lambda: self.page.close_dialog()).start()
        
    
    def go_back(self, e):
        self.page.go('/')
        
    def get_view(self):
        threading.Thread(target=self.run_update_time).start()
        self.capture_button = ft.ElevatedButton(
            "شروع ضبط چهره",
            on_click=self.toggle_capture,
            width=300,
            bgcolor=ft.colors.BLUE_500,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        )
    
        return View(
            "/home",
            controls=[
                self.time_display,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(current_time('weekday'), size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                            ft.Text(current_time('date').replace('-', '/'), size=15, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                            ft.Divider(height=20, color="transparent"),
                            self.image_control,
                            ft.Divider(height=20, color="transparent"),
                            self.capture_button,
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
                ),
                ft.IconButton(
                    on_click=lambda e: self.page.open(self.bottom_sheet),
                    icon=ft.icons.SETTINGS,
                    icon_color="Gray",
                    icon_size=50,
                    tooltip="تنظیمات",
                )
            ],
            bgcolor=ft.colors.BLUE_GREY_50,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )