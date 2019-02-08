from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [

	# Home page
	path('', views.index, name='index'),

	#New post
	path('new_post/', views.new_post, name='new_post'),

	#Edit existing post
	#path(r'^edit_post/(?P<blogpost_id>\d+)$', views.edit_post, name='edit_post'),
	path('edit_post/<blogpost_id>', views.edit_post, name='edit_post'),

	#Search
	path('search/', views.simple_search, name='simple_search'),

	#Like blogpost
	path('like_post/', views.like_blogpost, name='like_post'),
]