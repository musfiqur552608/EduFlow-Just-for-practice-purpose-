# courses/urls.py

from django.urls import path
from . import views
from .views import CourseListView, CourseDetailView

app_name = 'courses' 

urlpatterns = [
    # path('', views.course_list, name='course-list'),
    # path('<slug:course_slug>/', views.course_detail, name='course-detail'),
    path('', CourseListView.as_view(), name='course-list'),
    path('<slug:course_slug>/', CourseDetailView.as_view(), name='course-detail'),
    path('create/', views.course_create, name='course-create'),
    path('<slug:course_slug>/edit/', views.course_update, name='course-update'),
    path('<slug:course_slug>/delete/', views.course_delete, name='course-delete'),
]