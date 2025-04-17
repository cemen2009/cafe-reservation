from django.urls import path

from accounts.views import SignUpView, CustomLogoutView, CustomLoginView

app_name = "accounts"

urlpatterns =[
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
]
