from django.urls import path
from . import views


urlpatterns = [

    # Customer Registration
    path(
        "register/",
        views.register,
        name="register"
    ),

    # Customer Login
    path(
        "login/",
        views.user_login,
        name="login"
    ),

    # Mechanic Login
    path(
        "mechanic-login/",
        views.mechanic_login,
        name="mechanic_login"
    ),

    # Customer Dashboard
    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # Logout
    path(
        "logout/",
        views.user_logout,
        name="logout"
    ),
]