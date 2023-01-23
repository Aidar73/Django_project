from django import forms
from posts.models import Post, Group


class PostForm(forms.ModelForm):
    class Meta:
        # укажем модель, с которой связана создаваемая форма
        model = Post
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ("text", "group")
        # widgets = {'group': forms.ModelChoiceField(queryset=Group.objects.all()),
        #            'text': forms.Textarea(attrs={'cols': 60, 'rows': 10})}