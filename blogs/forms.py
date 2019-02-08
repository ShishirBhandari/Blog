from django import forms

from .models import BlogPost, Images

class BlogPostForm(forms.ModelForm):
	title = forms.CharField(max_length=128)
	class Meta:
		model = BlogPost
		fields = ['title', 'text']

class ImageForm(forms.ModelForm):
	image = forms.ImageField(label='Image')
	class Meta:
		model = Images
		fields = ['image',]