from django.contrib import admin
from django.urls import path, include  # Include `include` for app URLs

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("web_scraper.urls")),  # Replace 'your_app_name' with the name of your app
]
