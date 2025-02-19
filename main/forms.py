from django import forms

class ImageUploadForm(forms.Form):
    images = forms.FileField(widget=forms.FileInput(), required=True)
