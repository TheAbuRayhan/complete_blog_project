
from django.urls import path
from .import views
urlpatterns = [
    path('signup.html',views.AuthSignUp,name='signup'),
    path('login.html',views.AuthLogIn,name='login'),
    path('logout/',views.authlogout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('add-user-profile-picture.html', views.add_pro_pic, name='add_pro_pic'),
    path('change-user-profile-picture.html', views.change_pro_pic, name='change_pro_pic'),
    path('update-user-bio.html', views.Userbio, name='update_bio'),
    path('change-user-bio.html',views.ChangeUserbio,name='change_bio'),
    path('change-profile-info.html', views.user_change, name='user_change'),
    path('change-user-password.html', views.pass_change, name='pass_change'),
]
