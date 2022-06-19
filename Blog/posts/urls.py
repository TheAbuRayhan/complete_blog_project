
from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('Write/',views.Creating_blog,name='write'),
    path('blogs.html',views.bloglist,name="showing_blogs"),
    path('details/<slug>/', views.blog_details, name='blog_details'),
    path('liked/<slug>/',views.liked,name="liked_post"),
    path('unliked/<slug>/',views.unliked,name="unliked_post"),
    path('edit/<slug>/',views.EditBlog,name="edit_blog"),
    path('delete/<slug>/',views.DeleteBlog,name="delete_blog"),
    path('deleteComment/<int:id>/<slug>/',views.DeleteComment,name="delete_comment")
    
]
