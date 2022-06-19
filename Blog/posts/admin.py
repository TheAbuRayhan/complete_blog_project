from django.contrib import admin
from .models import Blog,Category,Comment
class BlogAdmin(admin.ModelAdmin):
    display=['author','blog_title','publish_date']
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Comment)


