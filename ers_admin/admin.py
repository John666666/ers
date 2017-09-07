from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Client, admin_class=models.ClientAdmin)