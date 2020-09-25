from django.urls import path
from django.conf.urls import url
from . import views
from django_downloadview import ObjectDownloadView
from .models import ApplicationDocument
from django.views.generic import TemplateView


app_name = 'appsapp'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.JobAppDetailView.as_view(), name="details"),
    path('<int:pk>/update/', views.JobAppUpdateView.as_view(), name="update"),
    url('^download/(?P<slug>[A-Za-z0-9_-]+)/$', ObjectDownloadView.as_view(model=ApplicationDocument, file_field='file')
        , name='download'),
    url(r'^about', TemplateView.as_view(template_name='appsapp/about.html'), name='about'),

]