from django.contrib import admin
from account import models
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'password']


admin.site.register(models.User)
admin.site.register(models.Photo)
admin.site.register(models.Product)
