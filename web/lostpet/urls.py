from django.conf.urls import url, include

from lostpet_auth import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),

    url(r'^main/$', views.main, name="main"),
    url(r'^admin_main/$', views.admin_main, name="admin_main"),

    url(r'^new-client/$', views.create, name="new-client"),
    url(r'^remove-client/$', views.remove, name="remove-client"),

    url(r'^remove-history-lostpet/$', views.remove_history),

    url(r'^signup/$', views.signup, name="signup"),
    url(r'^duplication/$', views.check_duplication, name="duplication"),

    url(r'^pricing/$', views.pricing, name="pricing"),
    url(r'^setup_pricing/$', views.setup_pricing, name="setup_pricing"),
    url(r'^setup_info/$', views.setup_info, name="setup_info"),

    url(r'^blog/(?P<blog_id>[0-9a-z]+)/$', views.blog, name="blog"),
    url(r'^comment/$', views.comment, name="post_comment")
]

