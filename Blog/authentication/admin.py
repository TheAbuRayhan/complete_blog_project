from django.contrib import admin
from .models import UserProfile,UserBio,VisitorEmail

admin.site.register(VisitorEmail)
admin.site.register(UserProfile)
admin.site.register(UserBio)
# Register your models here.
