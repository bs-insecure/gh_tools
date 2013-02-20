from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'gh_tools.views.home'),
     url(r'^home/$', 'gh_tools.views.home'),
     url(r'^about/$', 'gh_tools.views.about_page'),
     url(r'^contact/$', 'gh_tools.views.contact_page'),
     url(r'^home/$', 'gh_tools.views.home'),
     url(r'^login/$', 'gh_tools.views.login_page'),
     url(r'^logout/$', 'gh_tools.views.logout_page'),
     url(r'^account/$', 'gh_tools.views.account_page'),
     url(r'^upload_article/$', 'gh_tools.views.upload_article'),
     url(r'^post_article/$', 'gh_tools.views.post_article'),
     url(r'^article_list/(?P<blog_id>\d*)$', 'gh_tools.views.article_list'),
     url(r'^manage_articles/$', 'gh_tools.views.manage_articles'),
     url(r'^manage_blogs/(?P<blog_id>\d*)$', 'gh_tools.views.manage_blogs'),
     url(r'^remove_blog/(?P<blog_id>\d*)$', 'gh_tools.views.remove_blog'),
     url(r'^pr_check/$', 'gh_tools.views.pr_check'),
     url(r'^bing_grab/$', 'gh_tools.views.bing_grabber'),
     url(r'^process_pack/(?P<pack_id>.*)/$', 'gh_tools.views.process_pack'),
    # url(r'^gh_tools/', include('gh_tools.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
            (r'site_media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )