from django import forms
from posts.models import Post, Group, Comment, Follow


class PostForm(forms.ModelForm):
    class Meta:
        # укажем модель, с которой связана создаваемая форма
        model = Post
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("text", "group", 'image')


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        # укажем модель, с которой связана создаваемая форма
        model = Comment
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("text",)