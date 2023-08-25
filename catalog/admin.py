from django.contrib import admin
from .models import Lure, Color, Brand


class LureAdmin(admin.ModelAdmin):
    filter_horizontal = ('colors',)


admin.site.register(Lure, LureAdmin)
admin.site.register(Color)
admin.site.register(Brand)

