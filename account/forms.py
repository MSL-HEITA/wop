from django import forms
from .models import *


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title' , 'content', 'post_tag', 'company_name', 'web_address', 'company_profile']
       
    
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ( 'email', 'body')
       