from django.contrib import admin

# Register your models here.
from .models import Room


admin.site.register(
    Room,
    list_display=["id", "title", ],
    list_display_links=["id", "title"],
)