from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        # Telling our form what model to use
        # and what field we want displayed
        model = Comment
        # comment is neccessary so python interprets
        # as a tuple and not a string
        fields = ('body',)
