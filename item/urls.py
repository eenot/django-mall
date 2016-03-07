from django.conf.urls import url,include

from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.item_goods),
    url(r'^(?P<cat_url>[a-z]+)/$', views.item_cat),
    
    #(r'^ckeditor/', include('ckeditor_uploader.urls')),
    #(r'^ckeditor/', include('ckeditor.urls')),
]
