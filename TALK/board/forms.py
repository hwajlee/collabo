from django import forms
from .models import Article, Reply

class ArtForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content')

class ReplyForm(forms.ModelForm):
    comment = forms.CharField(min_length=2, max_length=200)
    class Meta:
        model = Reply
        fields = ('comment',)