from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course


# def course_list(request):
#     courses = Course.objects.filter(is_published=True)
#     return render(request, 'courses/course_list.html', {'courses': courses})


# def course_detail(request, slug):
#     course = get_object_or_404(Course, slug=slug, is_published=True)
#     return render(request, 'courses/course_detail.html', {'course': course})


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'


    def get_queryset(self):
        return Course.objects.filter(is_published=True)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    slug_field = 'slug'
    slug_url_kwarg = 'course_slug'

