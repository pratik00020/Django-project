from django import forms
from django import Video

class VideoForm(Forms.ModelForm):
    class Meta:
        model=Video
        fields = ['title', 'file']