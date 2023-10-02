from .models import Post, Comment
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'body']
    
    category = forms.ChoiceField(choices=Post.CATEGORY_CHOICES)

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'body']

    category = forms.ChoiceField(choices=Post.CATEGORY_CHOICES)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)