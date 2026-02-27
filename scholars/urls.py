from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_scholar, name='submit_scholar'),
    path('success/', views.submission_success, name='submission_success'),
    path('scholars/', views.scholar_list, name='scholar_list'),
    path('scholars/<slug:slug>/', views.scholar_detail, name='scholar_detail'),
    path('', views.home, name='home'),
    path("profile/", views.profile, name="profile"),
]
