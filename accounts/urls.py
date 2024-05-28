from django.urls import path
from . import views

urlpatterns = [
    path("registations/",views.userRegistation.as_view(),name="registation"),
    path("login/",views.UserLogin.as_view(),name="login"),
    path("logout/",views.UserLogout.as_view(), name="logout"),
    path("profile/",views.UpdateProfile.as_view(), name="Profile")
]
