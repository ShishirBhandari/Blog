from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BlogPost(models.Model):
	'''Blog post'''
	title = models.CharField(max_length=100)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	likes = models.IntegerField(default=0)

	def __str__(self):
		return self.title

def get_image_filename(instance, filename):
	title = instance.post.title
	slug = slugify(title)
	return "post_images/%s-%s" % (slug, filename)

class Images(models.Model):
	post = models.ForeignKey(BlogPost, default=None, on_delete=models.SET_NULL, null=True)
	image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')