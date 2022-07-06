from django.contrib import admin

# Register your models here.
#user_login,user_details,file_store, file_share, auditor_details

from .models import user_login,user_details,file_store, file_share, auditor_details, org_files
admin.site.register(user_login)
admin.site.register(user_details)
admin.site.register(file_store)
admin.site.register(file_share)
admin.site.register(auditor_details)
admin.site.register(org_files)
