from django import forms
from .models import Blog,Comment
   
class BlogForm(forms.ModelForm):
    # blog_title= forms.TextInput(label='Title',widget=forms.TextInput(attrs={'class':'form-control'}))
    # blog_content= forms.Textarea(label='Blog Content',widget=forms.Textarea(attrs={'class':'form-control'}))
    # blog_image= forms.ImageField(label='Blog Thambnail',widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    

    class Meta:
        model=Blog
        fields=['blog_title','category','blog_content','blog_image']
        widgets={
            'blog_title':forms.TextInput(attrs={'class':'form-control'}),
            'blog_content':forms.Textarea(attrs={'class':'form-control'}),
            'blog_image':forms.FileInput(attrs={'class':'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('comment',)
        comment = forms.CharField(initial='Your comment',widget=forms.TextInput(attrs={'row':'3'}))   

        
        