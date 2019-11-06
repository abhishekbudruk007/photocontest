
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


from . import views
app_name = 'photocontest'
urlpatterns = [
    #Api for Datatable Creation View
    path('contest_list', views.ContestList.as_view(), name='contest_list'),
    path('likeapi/', views.LikeApi.as_view(), name='like'),
    #Template for Upcoming Contests View
    path('contest_template/', views.ContestTemplate.as_view(), name='contest_template'),
    #Participate in contest View
    path('contest_template/<int:pk>/participate/',views.Participate.as_view() ,name="participate"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
