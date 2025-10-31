from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin (optional)
    path("api/auth/", include("accounts.urls")),
    path("api/", include("tickets.urls")),
    path("api/", include("notifications.urls")),
]
