from django.contrib import admin


from .models import * 

admin.site.register(Type)
admin.site.register(Document)
admin.site.register(Metadata)
admin.site.register(FileSharing)