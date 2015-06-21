from django.contrib import admin
from .models import Gmina, Obwod


class GminaAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Nazwa", {'fields': ['nazwa']})
    ]

admin.site.register(Gmina, GminaAdmin)
admin.site.register(Obwod)