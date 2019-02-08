
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory

from .models import BlogPost, Images
from .forms import BlogPostForm, ImageForm
from .simple_search import get_query

# Create your views here.

def index(request):
	'''Home page for the blogs.'''
	blogposts = BlogPost.objects.order_by('-date_added')

	context = {'blogposts':blogposts}
	return render(request, 'blogs/index.html', context)

# @login_required
# def new_post(request):
# 	'''Add a new post'''
# 	if request.method != 'POST':
# 		form = BlogPostForm()
# 	else:
# 		form = BlogPostForm(request.POST)
# 		if form.is_valid():
# 			new_post = form.save(commit=False)
# 			new_post.owner = request.user
# 			new_post.save()
# 			return HttpResponseRedirect(reverse('index'))

# 	context = {'form': form}
# 	return render(request, 'blogs/new_post.html', context)



@login_required
def new_post(request):
	ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=1)

	if request.method == 'POST':
		postForm = BlogPostForm(request.POST)
		formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

		if postForm.is_valid() and formset.is_valid():
			post_form = postForm.save(commit=False)
			post_form.owner = request.user
			post_form.save()

			for form in formset.cleaned_data:
				image = form['image']
				photo = Images(post=post_form, image=image)
				photo.save()
			messages.success(request, "Success")

			return HttpResponseRedirect(reverse('index'))
		else:
			print(postForm.errors, formset.errors)
	else:
		postForm = BlogPostForm()
		formset = ImageFormSet(queryset=Images.objects.none())

	context = {'form': postForm, 'formset': formset}
	return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, blogpost_id):
	'''Edit an existing post'''
	blogpost = BlogPost.objects.get(id=blogpost_id)
	if blogpost.owner != request.user:
		raise Http404

	title = blogpost.title
	text = blogpost.text

	if request.method != 'POST':
		form = BlogPostForm(instance=blogpost)
	else:
		form = BlogPostForm(instance=blogpost, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('index'))

	context = {'form': form, 'blogpost': blogpost}
	return render(request, 'blogs/edit_post.html', context)


def simple_search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['title', 'text',])

        found_entries = BlogPost.objects.filter(entry_query).order_by('-date_added')

        context = { 'query_string': query_string, 'found_entries': found_entries }
    return render(request, 'blogs/search_results.html', context)


@login_required
def like_blogpost(request):
	blog_id = None
	if(request.method == 'GET'):
		blog_id = request.GET['blogpost_id']

	likes = 0
	if blog_id:
		blogpost = BlogPost.objects.get(id=int(blog_id))
		if(blogpost):
			likes = blogpost.likes + 1
			blogpost.likes = likes
			blogpost.save()

	return HttpResponse(likes)