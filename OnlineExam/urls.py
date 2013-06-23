from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OnlineExam.views.home', name='home'),
    # url(r'^OnlineExam/', include('OnlineExam.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    url(r'^auth/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/exam/home'}),
    url(r'^exam/', include('exam.urls')),
)

urlpatterns += staticfiles_urlpatterns()
