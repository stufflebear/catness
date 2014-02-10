from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'webapp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^about/', 'catness.views.explanation', name='about'),
    url(r'^result/', 'catness.views.result', name='result'),
    url(r'^$', 'catness.views.index', name='index'),
    url(r'', 'catness.views.show404', name='show404'),
)
