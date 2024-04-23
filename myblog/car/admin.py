from django.contrib import admin
from .models import*
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create','is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'cat')
    prepopulated_fields = {'slug': ('title',)} 


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} 

admin.site.register(Car, CarAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ContactMessage)
admin.site.register(Message)