# core/forms.py

from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

# core/forms.py

from django import forms

class ChatbotForm(forms.Form):
    user_input = forms.CharField(label='Ask the chatbot', widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your message...'}))
