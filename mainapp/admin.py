from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Realization, RealizationImage
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.admin.actions import delete_selected
from django import forms
from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: <a href="%(initial_url)s">%(initial)s</a> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
    )
    initial_text = "Aktualne zdjęcie"
    input_text = "Zmień"


class RealizationAdminForm(forms.ModelForm):
    class Meta:
        model = Realization
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'cols': 100}),
            'image': CustomClearableFileInput(),
        }


class RealizationImageInline(admin.TabularInline):
    model = RealizationImage
    extra = 1
    verbose_name = "Zdjęcie dodatkowe"
    verbose_name_plural = "Zdjęcia dodatkowe"


# Admin class for Realization model with PDF export functionality
class RealizationAdmin(admin.ModelAdmin):
    form = RealizationAdminForm
    list_display = ('title', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'content')
    ordering = ('-date',)
    inlines = [RealizationImageInline]
    actions = ['custom_delete_selected']

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Informacje o realizacji', {
            'fields': ('content', 'date', 'image'),
            'description': 'Pola powiązane z realizacją'
        }),
    )

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @admin.action(description='Usuń wybrane realizacje')
    def custom_delete_selected(self, request, queryset):
        return delete_selected(self, request, queryset)


admin.site.site_header = "Admin Panel"
admin.site.site_title = "Panel Administracyjny"
admin.site.index_title = "Zarządzanie stroną"

# Register the models with their respective admin classes
admin.site.register(Realization, RealizationAdmin)

try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(Group, GroupAdmin)
except admin.sites.AlreadyRegistered:
    pass

admin.site.unregister(User)
admin.site.unregister(Group)
