import flet as ft
import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))
from app.database.db import DB

class MyTable:
    def __init__(self, page):
        self.page = page
        self.users = DB().FetchUsers()
        self.current_page = 1
        self.rows_per_page = 9

        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("نام و نام خانوادگی", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.colors.BLACK45))),
                ft.DataColumn(ft.Text("شماره پرسنلی", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.colors.BLACK45))),
                ft.DataColumn(ft.Text("تاریخ ثبت", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.colors.BLACK45)), numeric=True),
                ft.DataColumn(ft.Text("عملیات", style=ft.TextStyle(weight=ft.FontWeight.BOLD, color=ft.colors.BLACK45))),
            ],
            rows=self.get_current_page_rows()
        )

    def get_current_page_rows(self):
        start_index = (self.current_page - 1) * self.rows_per_page
        end_index = start_index + self.rows_per_page
        return [
            self.create_row(i[0], i[1], i[2], i[4]) for i in self.users[start_index:end_index]
        ]

    def create_row(self, id, name, personnel_number, registration_date):
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(name, style=ft.TextStyle(color=ft.colors.GREY))),
                ft.DataCell(ft.Text(personnel_number, style=ft.TextStyle(color=ft.colors.GREY))),
                ft.DataCell(ft.Text(registration_date, style=ft.TextStyle(color=ft.colors.GREY))),
                ft.DataCell(
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                tooltip="ویرایش",
                                on_click=lambda _: self.update_user(id, name, personnel_number),
                                icon_color=ft.colors.BLUE_900
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                tooltip="حذف",
                                on_click=lambda _: self.delete_row(id),
                                icon_color=ft.colors.RED
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    )
                ),
            ],
        )

    def delete_row(self, id):
        DB().DeleteUser(id)
        self.users = DB().FetchUsers()
        self.update_table()
    
    def edit_row(self, id, current_name, personnel_number):
        DB().UpdateUser(id, current_name, personnel_number)
        self.users = DB().FetchUsers()
        self.page.close(self.dialog)
        self.update_table()
    
    def update_user(self, id, current_name, personnel_number):
        name_field = ft.TextField(
            label="نام",
            value=current_name,
            width=200,
            text_align=ft.TextAlign.LEFT,
            color=ft.colors.BLACK38,

        )
        personnel_field = ft.TextField(
            label="شماره پرسنلی",
            value=personnel_number,
            width=200,
            text_align=ft.TextAlign.LEFT,
            color=ft.colors.BLACK38,
        )

        self.dialog = ft.AlertDialog(
            title=ft.Text(
                "ویرایش کاربر",
                style=ft.TextStyle(color=ft.colors.GREEN, size=24, weight=ft.FontWeight.BOLD),
                text_align=ft.TextAlign.CENTER,
            ),
            content=ft.Column(
                [
                    name_field,
                    personnel_field,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                width=250,
                height=150
            ),
            actions=[
                ft.ElevatedButton(
                    "تأیید",
                    on_click=lambda e: self.edit_row(id, name_field.value, personnel_field.value),
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.GREEN,
                        color=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),
                ft.ElevatedButton(
                    "لغو",
                    on_click=lambda e: self.page.close(self.dialog),
                    style=ft.ButtonStyle(
                        bgcolor=ft.colors.RED,
                        color=ft.colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor=ft.colors.WHITE,
        )
        self.page.show_dialog(self.dialog)

    def next_page(self, e):
        if self.current_page < (len(self.users) // self.rows_per_page) + 1:
            self.current_page += 1
            self.update_table()

    def previous_page(self, e):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()

    def update_table(self):
        self.table.rows = self.get_current_page_rows()
        self.page.update()

    def go_back(self, e):
        self.page.go('/home')

    def get_view(self):
        return ft.View(
            "/",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("لیست کاربران", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900),
                            ft.Divider(height=20, color="transparent"),
                            self.table,
                            ft.Row(
                                [
                                    ft.TextButton("صفحه قبلی", on_click=self.previous_page),
                                    # ft.Text(f"صفحه {self.current_page}"),
                                    ft.TextButton("صفحه بعدی", on_click=self.next_page),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=20,
                    border_radius=15,
                    width=700,
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