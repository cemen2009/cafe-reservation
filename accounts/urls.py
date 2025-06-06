from django.urls import path

from accounts.views import SignUpView, CustomLogoutView, CustomLoginView, VisitorUpdateView

app_name = "accounts"

urlpatterns =[
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", VisitorUpdateView.as_view(), name="profile"),
]
