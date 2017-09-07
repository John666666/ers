from django.contrib import admin
from .models import Locus, LocusAdmin

admin.site.register(Locus, LocusAdmin)