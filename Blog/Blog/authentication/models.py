from operator import mod
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user=models.OneToOneField(User,related_name='user_profile',on_delete=models.CASCADE)#here is important thing related_name. when i need profile_pic i can just write {{user.user_profile}}. and if i want Profile_pic i can just write {{user.user_profile.profile_pic}}
    profile_pic=models.ImageField(upload_to='profile_pics')
    
    def __str__(self):
        return self.user.username
class UserBio(models.Model):
    user=models.OneToOneField(User,related_name='user_bio', on_delete=models.CASCADE)
    user_profile_bio=models.TextField(max_length=200,null=True,default='This user has no Bio yet')
    
    def __str__(self):
        return self.user.username +"s' bio"
class VisitorEmail(models.Model):
    email=models.EmailField()