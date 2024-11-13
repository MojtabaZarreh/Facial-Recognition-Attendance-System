# app/routes/routes.py
from app.views.pages.home_page import Home
from app.views.pages.login_page import Login
from app.views.pages.user_page import AddUser
from app.views.pages.employees_page import MyTable

routes = {
    "/": lambda page: Login(page).get_view(),
    "/home": lambda page: Home(page).get_view(),
    "/home/newuser": lambda page: AddUser(page).get_view(),
    "/home/employees": lambda page: MyTable(page).get_view(),
}

def get_route_view(route, page):
    view_function = routes.get(route)
    return view_function(page) if view_function else None
