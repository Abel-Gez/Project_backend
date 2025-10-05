from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html

from .models import Branch, AccountApplication, BranchManagerProfile

User = get_user_model()


# ----------------- Branch -----------------
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ----------------- Account Application -----------------
@admin.register(AccountApplication)
class AccountApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'branch', 'account_type', 'status', 'created_at')
    list_filter = ('branch', 'account_type', 'status', 'created_at')
    search_fields = ('full_name', 'mother_name', 'fayda_number', 'phone')
    readonly_fields = ('created_at', 'updated_at',)

    # Show link to uploaded file in admin
    def national_id_preview(self, obj):
        if obj.national_id_file:
            return format_html('<a href="{}" target="_blank">Download</a>', obj.national_id_file.url)
        return "-"
    national_id_preview.short_description = "National ID"


# ----------------- Inline Form for Validation -----------------
class BranchManagerProfileForm(forms.ModelForm):
    class Meta:
        model = BranchManagerProfile
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        is_manager = cleaned_data.get('is_branch_manager')
        branch = cleaned_data.get('branch')
        if is_manager and not branch:
            raise forms.ValidationError("Branch is required for branch managers.")
        return cleaned_data


# ----------------- Branch Manager Inline -----------------
class BranchManagerProfileInline(admin.StackedInline):
    model = BranchManagerProfile
    form = BranchManagerProfileForm
    can_delete = False
    verbose_name_plural = 'Branch Manager Profile'
    fk_name = 'user'
    extra = 0


# ----------------- User Admin -----------------
class UserAdmin(DefaultUserAdmin):
    inlines = (BranchManagerProfileInline,)

    # Replace list_display entirely with attributes of StaffUser + branch info
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'is_branch_manager', 'branch_name')

    def is_branch_manager(self, obj):
        profile = getattr(obj, 'branch_profile', None)
        return profile.is_branch_manager if profile else False
    is_branch_manager.boolean = True
    is_branch_manager.short_description = 'Branch Manager'

    def branch_name(self, obj):
        profile = getattr(obj, 'branch_profile', None)
        return profile.branch.name if profile and profile.branch else "-"
    branch_name.short_description = 'Branch'

# Unregister default User and register custom UserAdmin
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)
