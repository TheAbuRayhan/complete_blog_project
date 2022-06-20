from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    title= models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural= "Catogories"
    
class Blog(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='post_author')
    blog_title=models.CharField(max_length=264,verbose_name='Put a Title')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category',default=None)
    slug= models.SlugField(max_length=264,unique=True,null=True,allow_unicode=True)
    blog_content=models.TextField(verbose_name='what is on your mind?')
    blog_image=models.ImageField(upload_to='blog_images',verbose_name='Image')
    publish_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    view_count=models.IntegerField(null=True,default=0,blank=True)
    class Meta:
        ordering = ('-publish_date',)
    
    def __str__(self):
        return self.blog_title+'  From :'+str(self.author)+str(self.publish_date)
    @staticmethod
    def get_all_products_by_id(category_id):
        if category_id :

            return Blog.objects.filter(category=category_id)
        else:
            return Blog.objects.all()

    
class ViewCount(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_view')
    count=models.IntegerField(default=0)
class Comment(models.Model):
    blog= models.ForeignKey(Blog, on_delete=models.CASCADE,related_name='Blog_comment')
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='user_comment')
    comment=models.TextField(default='Your Comment')
    parent =  models.ForeignKey('self', on_delete=models.CASCADE,null=True,related_name='paren_comment')
    comment_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering= ('-comment_date',)
    def __str__(self):
        return self.comment

class Likes(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE, related_name='liked_blog')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='liker_user')
     
    def __str__(self):
        return self.user+ "likes"+self.blog
