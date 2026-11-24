from django.contrib import admin
from .models import (
    News,
    Gallery,
    TopStudent,
    SchoolStructure,
    ContactMessage,
    Event,
    Subscriber,
    SchoolHighlight,
)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')


@admin.register(TopStudent)
class TopStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'score', 'grade')
    list_filter = ('year',)
    search_fields = ('name', 'year')


@admin.register(SchoolStructure)
class SchoolStructureAdmin(admin.ModelAdmin):
    list_display = ('role', 'name')


# --- CONTACT MESSAGE ADMIN ---

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'sent_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject')


# --- EVENT ADMIN ---

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')
    list_filter = ('date',)
    search_fields = ('title', 'description')


# --- SUBSCRIBER ADMIN ---

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)


# --- SCHOOL HIGHLIGHTS ADMIN ---

@admin.register(SchoolHighlight)
class SchoolHighlightAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_recorded', 'is_published')
    list_filter = ('category', 'is_published', 'date_recorded')
    list_editable = ('is_published',)
    search_fields = ('title', 'summary')