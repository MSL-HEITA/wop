from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse 


# Create your models here.
categories =[
    ('Developer / IT','Developer / IT'),
    ('Design / Creative','Design / Creative'),
    ('Engineer / Architect','Engineer / Architect'),
    ('Digital Media','Digital Media'),
    ('Marketing & sales','Marketing & sales')
]



class Blog(models.Model):
    title = models.CharField(max_length= 200, unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField()
    post_tag = models.TextField(choices=categories, default='tags')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    company_name = models.CharField(max_length=200,null=True, blank=True)
    web_address = models.URLField(null=True, blank=True)
    company_profile = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80, default='name')
    email = models.EmailField(default='e-mail')
    body = models.TextField(default='comment')
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE ,null=True, blank=True, related_name='replies')
    
    class Meta:
        ordering = ['created_on']

    def approve(self):
        self.active = True
        self.save()  

    def get_absoulute_url(self):
        return reverse('blog_details',kwargs={"pk":self.pk})

    def __str__(self):
        return 'Comment {} by {} '.format(self.body, self.name )



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    
    def __str__(self):
        return '{} , {} Profile'.format(self.user.username, self.image)

class Social(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='socials')
    facebook = models.CharField(max_length=255, blank=True, null=True)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    linkedin = models.CharField(max_length=255, blank=True, null=True)
    pinterest = models.CharField(max_length=255, blank=True, null=True)
    behance = models.CharField(max_length=255, blank=True, null=True)
    dribble = models.CharField(max_length=255, blank=True, null=True)


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name='messages')

class Message(models.Model):
    text = models.CharField(max_length=200, default='message')
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')

