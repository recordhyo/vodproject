
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("vod/", include("contents.urls")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home")
]
