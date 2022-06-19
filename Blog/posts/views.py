import imp
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.urls import reverse
from .forms import BlogForm,CommentForm
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib.auth.models import User
from .models import Blog,Comment,Likes,Category
from .templatetags import get_dict #this is a custom filter for showing replies on comment. but i have figured out another easy way so that's why not using this way
from django.core.paginator import Paginator 
#index page template rendering
def index(request):
    blogs=Blog.objects.all()
    category=Category.objects.all()
    categoryID= request.GET.get('category')
    if categoryID:
        blogs = Blog.get_all_products_by_id(categoryID)
    else:
        blogs=Blog.objects.all()
    print(category,categoryID)
    return render(request,'index.html',context={'category':category,'blogs':blogs})
#WriteBlog page template rendering
def Creating_blog(request):
    if request.user.is_authenticated:
        form=BlogForm()
        if request.method=='POST':
                form=BlogForm(request.POST,request.FILES)
                if form.is_valid:
                    blog_obj=form.save(commit=False)
                    blog_obj.author=request.user
                    title=blog_obj.blog_title
                    blog_obj.slug = title.replace(' ','-') + '-'+ str(uuid.uuid4())
                    blog_obj.save()
                    messages.success(request,'Blog has been Uploaded!')
                    return redirect('profile')
        return render(request,'blogs/creatingblog.html',context={'form':form})
    else:
        messages.info(request,'You have to login first!')
        return redirect('login')
        
#BlogList page template rendering
def bloglist(request):
    blog=Blog.objects.all()
    category=Category.objects.all()
    categoryID= request.GET.get('category')
    if categoryID:
        blog = Blog.get_all_products_by_id(categoryID)
    else:
        blog=Blog.objects.all()
    paginator=Paginator(blog,2)
    page_number=request.GET.get('page')
    blogFinal=paginator.get_page(page_number)
    if request.method == "GET":
        search= request.GET.get('search',' ')
        result = Blog.objects.filter(blog_title__icontains=search)#i am using this contains key to get related name user.  
    prddata={
        'blog':blogFinal,
        'category':category,
        'search':search,
        'result':result
    }
    return render(request,'blogs/blog.html',prddata)
#Blog details page template rendering
def blog_details(request, slug):
    blog = Blog.objects.get(slug=slug)
    
    if request.method == 'GET':
        #we use .get so it returns None rather than a key error if not set
        visited = request.session.get('visited')
        if not visited:
            blog.view_count =blog.view_count+1    
            blog.save()
            #we've updated the count so we make sure the code doesn't run next time.
            request.session['visited'] = True
    #fetching blogs by category
    blogCategory=blog.category.id
    SameCategoryBlog=Blog.get_all_products_by_id(blogCategory)
    #likes and comments part starts
    liked=False
    if request.user.is_authenticated:
        already_liked = Likes.objects.filter(blog=blog, user= request.user)
        if already_liked:
            liked = True
        else:
            liked = False
    comments=Comment.objects.filter(blog=blog,parent=None)
    replies=Comment.objects.filter(blog=blog).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.id not in replyDict.keys():#Here goes the main thing of this. by this 83 to 87 lines' code i have created a loop and stored all the reply by their parent's id as key in the dictionary
            replyDict[reply.parent.id]= [reply]
        else:
            replyDict[reply.parent.id].append(reply)
    
    if request.method=='POST':
        reply=request.POST.get('comment')
        commentId=request.POST.get('commentId')
        if commentId=="":
            commentObj=CommentForm(request.POST)
            if commentObj.is_valid():
                obj=commentObj.save(commit=False)
                obj.user=request.user
                obj.blog=blog
                obj.save()
                messages.success(request,'Comment has been Posted!')
                return HttpResponseRedirect(reverse('blog_details',kwargs={'slug':slug}))
        else:
            cmmntid=int(commentId)
            parentcomment=Comment.objects.get(pk=cmmntid)
            replyobj=CommentForm(request.POST)
            if replyobj.is_valid():
                reply=replyobj.save(commit=False)
                reply.user=request.user
                reply.blog=blog
                reply.parent=parentcomment
                reply.save()
                messages.success(request,'Reply has been Posted!')
                return HttpResponseRedirect(reverse('blog_details',kwargs={'slug':slug}))
    return render(request,'blogs/blogdetails.html',context={'blog':blog,'comments':comments,
                                                            'like':liked,'CategoryBlog':SameCategoryBlog,
                                                            'replyDict':replyDict,'replies':replies,})
    
#Like and button function
@login_required
def liked(request,slug):
    if request.user.is_authenticated:
        blog=Blog.objects.get(slug=slug)
        user=request.user
        already_liked=Likes.objects.filter(blog=blog,user=user)
        if not already_liked:
            like_post=Likes(blog=blog,user=user)
            like_post.save()
            messages.success(request,'You have liked this Blog!')
        return HttpResponseRedirect(reverse('blog_details',kwargs={'slug':slug}))
    else:
        messages.info(request,'You have to login first!')
        return redirect('login')
#UnLike and button function
@login_required
def unliked(request,slug):
    if request.user.is_authenticated:
        blog=Blog.objects.get(slug=slug)
        user=request.user
        already_liked=Likes.objects.filter(blog=blog,user=user)
        already_liked.delete()
        return HttpResponseRedirect(reverse('blog_details',kwargs={'slug':slug}))
    else:
        messages.info(request,'You have to login first!')
        return redirect('login')
#EditBlog page template rendering
def EditBlog(request,slug):
    txt="Edit Blog"
    if request.user.is_authenticated:
        current = Blog.objects.get(slug=slug)
        form = BlogForm(instance=current)
        if request.method =="POST":
            form=BlogForm(request.POST,request.FILES,instance=current)
            if form.is_valid():
                form.save(commit=True)
                form =BlogForm(instance=current)
            return redirect('profile')
    else:
        messages.info(request,'You have to login first!')
        return redirect('login')
        
    return render(request,'blogs/creatingblog.html',context={'form':form,'txt':txt})
#DeleteBlog page template rendering
def DeleteBlog(request,slug):
    if request.user.is_authenticated:
        this_blog=Blog.objects.get(slug=slug)
        this_blog.delete()
        messages.warning(request,'Blog has been Deleted.')
        return redirect('profile')
    else:
        messages.info(request,'You have to login first!')
        return redirect('login')
#Delete Comments function 
def DeleteComment(request,slug,id):
    delete_comment=Comment.objects.get(pk=id)
    delete_comment.delete()
    messages.warning(request,'Comment has been Deleted.')
    return HttpResponseRedirect(reverse('blog_details',kwargs={'slug':slug}))
    