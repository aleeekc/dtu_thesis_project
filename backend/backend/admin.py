from django.contrib import admin
from .models import *


class KeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'owner', 'meant_for', 'creation_date')
    empty_value_display = '-empty-'


class FolderAdmin(admin.ModelAdmin):
    list_display = ('uid', 'owner', 'name', 'creation_date')
    empty_value_display = '-empty-'


class FileAdmin(admin.ModelAdmin):
    list_display = ('uid', 'owner', 'name', 'file', 'creation_date')
    empty_value_display = '-empty-'


class LinkAdmin(admin.ModelAdmin):
    list_display = ('uid', 'owner', 'file', 'creation_date')
    empty_value_display = '-empty-'


class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('uid', 'userAlias', 'friends')
    empty_value_display = '-empty-'


admin.site.register(Key, KeyAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)
