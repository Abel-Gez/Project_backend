from django.contrib import admin
from .models import VacancyApplication

@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position_applied', 'mobile_number', 'created_at')
    list_filter = ('position_applied', 'location_applied', 'created_at')
    search_fields = ('full_name', 'mobile_number', 'email', 'position_applied')
    readonly_fields = ('created_at', 'updated_at')

    def file_preview(self, obj):
        if obj.file_attachment:
            return f'<a href="{obj.file_attachment.url}" target="_blank">Download</a>'
        return '-'
    file_preview.allow_tags = True
    file_preview.short_description = 'Attachment'
