from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Entry)


# @admin.register(models.Entry)
# class CarAdmin(admin.ModelAdmin):

