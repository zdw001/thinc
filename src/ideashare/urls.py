from django.conf.urls import url
from django.contrib import admin
from ideashare import views

urlpatterns = [
	url(r'^$', views.index, name='ideashare_home'),
	url(r'^browse/$',
        views.browse, name='browse'),
    url(r'^browse/(?P<initial>[-\w]+)/$',
        views.browse, name='browse'),
    url(r'^my_ideas/$', views.my_ideas, name='my_ideas'),
 	url(r'^create_idea/$', views.create_idea, name='create_idea'),
 	url(r'^ideas/(?P<slug>[-\w]+)/$', views.idea_detail, name='idea_detail'),
 	url(r'^ideas/(?P<slug>[-\w]+)/edit/$', views.edit_idea, name='edit_idea'),
 	url(r'^profile/(?P<username>\w+)/$', views.profile_view, name='user_profile'),
 	url(r'^profile/(?P<username>\w+)/edit/$', views.edit_profile, name='edit_profile'),
]