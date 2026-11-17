from django.contrib import admin
from .models import Alumni

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('name', 'graduation_year', 'current_role', 'institution')
    list_filter = ('graduation_year',)
    search_fields = ('name', 'current_role', 'institution')