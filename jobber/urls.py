from django.conf.urls import url
from jobber import views
from django.urls import path
# got to set "app_name" to something
# before you can use relative paths in your templates
app_name = 'jobber'
urlpatterns = [
    path('', views.index, name='index'),
    #path('startJobTest', views.startJobTest, name='startJobTest'),
]