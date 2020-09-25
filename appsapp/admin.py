from django.contrib import admin
from .models import JobApplication, ApplicationDocument

# Register your models here.

admin.site.register(JobApplication)
admin.site.register(ApplicationDocument)
