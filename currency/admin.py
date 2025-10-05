from django.contrib import admin
from .models import ExchangeRate

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("base_currency","currency","effective_date","buying","selling","created_at")
    list_filter = ("base_currency","effective_date","currency")
    search_fields = ("currency","base_currency")
    ordering = ("-effective_date","currency")
