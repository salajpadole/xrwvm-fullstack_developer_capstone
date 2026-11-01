from pathlib import Path

from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

FRONTEND_STATIC = Path(__file__).resolve().parent.parent / "frontend" / "static"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("djangoapp/", include("djangoapp.urls")),
    path("", serve, {"document_root": str(FRONTEND_STATIC), "path": "Home.html"}, name="home"),
    path("about", serve, {"document_root": str(FRONTEND_STATIC), "path": "About.html"}, name="about"),
    path("contact", serve, {"document_root": str(FRONTEND_STATIC), "path": "Contact.html"}, name="contact"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
