from django.urls import path
from . import views

# urlpatterns = [
#     path('submit/', views.submit_scholar, name='submit_scholar'),
#     path('success/', views.submission_success, name='submission_success'),
#     path('scholars/', views.scholar_list, name='scholar_list'),
#     path('scholars/<slug:slug>/', views.scholar_detail, name='scholar_detail'),
#     path('', views.home, name='home'),
#     path("profile/", views.profile, name="profile"),
#     path("author/<str:username>/", views.author_profile, name="author_profile"),
#     path("editor/review/", views.editor_review, name="editor_review"),
#     path("editor/publish/<int:pk>/", views.editor_publish, name="editor_publish"),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_scholar, name='submit_scholar'),
    path('success/', views.submission_success, name='submission_success'),

    path('scholars/', views.scholar_list, name='scholar_list'),
    path('scholars/<slug:slug>/', views.scholar_detail, name='scholar_detail'),

    path('profile/', views.profile, name='profile'),
    path('author/<str:username>/', views.author_profile, name='author_profile'),

    path('editor/review/', views.editor_review, name='editor_review'),
    path('editor/publish/<int:pk>/', views.editor_publish, name='editor_publish'),

    # path("suggest/", views.scholar_suggest, name="scholar_suggest"),
    path("suggest/", views.scholar_suggest, name="scholar_suggest"),
]
