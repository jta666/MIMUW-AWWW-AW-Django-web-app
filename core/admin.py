from django.contrib import admin

# Register your models here.

from .models import Directory, File, CompilationOption, FileSection, SectionStatus, SectionType, StatusData

admin.site.register(Directory)
admin.site.register(File)
admin.site.register(CompilationOption)
admin.site.register(FileSection)
admin.site.register(SectionType)
admin.site.register(SectionStatus)
admin.site.register(StatusData)