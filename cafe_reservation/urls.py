from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from reservation.views import CustomLoginView, CustomLogoutView, SignUpView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("reservation.urls")),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
