from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from .forms import (
	IdeaForm, 
	ContactForm, 
	RegistrationForm, 
	UserForm, 
	ProfileForm
	)
from .models import Idea
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import get_template
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.contrib import messages
from registration.backends.simple.views import RegistrationView
from django import forms
from django.conf import settings

def browse(request, initial=None):
	if initial: 
		ideas = Idea.objects.filter(name__istartswith=initial)
		ideas = ideas.order_by('name')
	else:
		ideas = Idea.objects.all().order_by('name')

	ideas_by_vote = Idea.objects.all().order_by('-votes')

	return render(request, 'ideashare/browse.html', {
			'ideas': ideas,
			'initial': initial,
			'ideas_by_vote': ideas_by_vote,
		})

def contact(request): 
	form_class = ContactForm

	if "cancel" in request.POST:
		return redirect('index')

	# new logic!
	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = form.cleaned_data['contact_name'] 
			contact_email = form.cleaned_data['contact_email'] 
			form_content = form.cleaned_data['content']

			subject = form.cleaned_data['subject']

			from_email = settings.EMAIL_HOST_USER
			to_email = [from_email]
			contact_message = "%s:\n %s \n via %s"%(
					contact_name,
					form_content,
					contact_email)

			send_mail(subject,
					contact_message,
					contact_email,
					to_email,
					fail_silently=False)
			messages.success(request, 'Email Sent!')
			return redirect('contact')

	return render(request, 'contact.html', { 
		'form': form_class,
	})

def create_idea(request):
	form_class = IdeaForm

	if not request.user.is_authenticated():
		return redirect('login')

	if "cancel" in request.POST:
		return redirect('index')

	# if we're coming from a submitted form, do this
	if request.method == 'POST':
		# grab the date from the submitted form and apply to the form
		form = form_class(data=request.POST)

		if form.is_valid():
			# create an instance but don't save yet
			idea = form.save(commit=False)

			# set the additional details
			idea.user = request.user
			idea.slug = slugify(idea.name)

			# save the object
			idea.save()

			# redirect to our newly created idea
			return redirect('idea_detail', slug=idea.slug)

	# otherwise just create the form
	else:
		form = form_class()

	return render(request, 'ideashare/ideas/create_idea.html', {
			'form': form,
		})

@login_required
def edit_idea(request, slug):
	# grab the object 
	idea = Idea.objects.get(slug=slug)

	# make sure the logged in user is the onwer of the idea
	if idea.user != request.user:
		raise Http404

	# set the form we're using 
	form_class = IdeaForm

	if "cancel" in request.POST:
		return redirect('index')

	# if we're coming to this view from a submitted form
	if request.method == 'POST':
		# grab the data from the submitted form and apply to the form
		form = form_class(data=request.POST, instance=idea)
		if form.is_valid():
			# save the new data
			form.save()
			return redirect('idea_detail', slug=idea.slug)
	# otherwise just create the form
	else:
		form = form_class(instance=idea)

	# and render the template
	return render(request, 'ideashare/ideas/edit_idea.html', {
			'idea': idea,
			'form': form,
	})

# @login_required
def edit_profile(request, username):
	profile = User.objects.get(username=username)
	user = User.objects.get(username=username)

	if user != request.user:
		raise Http404

	form_class = ProfileForm

	if "cancel" in request.POST:
		return redirect('index')

	if request.method == 'POST':
		form = ProfileForm(data=request.POST, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('user_profile', user=profile.user)
	else:
		form = form_class(instance=user)

	return render(request, 'edit_profile.html', {
				'profile': profile,
				'form': form,
		})

def index(request):
	# ideas = Idea.objects.order_by('-published_date')
	ideas = Idea.objects.all()
	top_ideas = ideas.order_by('-votes')
	recent_ideas = ideas.order_by('-published_date')
	users = User.objects.all()

	user_count = 0
	idea_count = 0

	for user in users:
		user_count += 1

	for idea in ideas:
		idea_count += 1

	return render(request, 'ideashare/index.html', {
		'users': users,
		'ideas': ideas,
		'top_ideas': top_ideas,
		'recent_ideas': recent_ideas,
		'user_count': user_count,
		'idea_count': idea_count,
	})
	

def idea_detail(request, slug):
	# grab the object...
	idea = Idea.objects.get(slug=slug)

	# and pass to the template
	return render(request, 'ideashare/ideas/idea_detail.html', {
			'idea': idea,
	})

def my_ideas(request):
	logged_in_user = request.user
	ideas = Idea.objects.filter(user = logged_in_user)
	ideas = ideas.order_by("-votes")

	return render(request, 'ideashare/ideas/my_ideas.html', {
			'ideas': ideas
		})

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')

			email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = RegistrationForm()
	return render(request, 'registration/register.html', {
			'form': form
		})

def profile_view(request, username):
	user = User.objects.get(username=username)

	ideas = Idea.objects.filter(user=user)
	ideas = ideas.order_by("-votes")

	return render(request, 'user_profile.html', {
			'user': user,
			'ideas': ideas,
		})
