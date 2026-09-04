from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm

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

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('courses:course-detail', course_slug=course.slug)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})
@login_required
def course_update(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, instructor=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('courses:course-detail', course_slug=course.slug)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'form': form})


@login_required
def course_delete(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, instructor=request.user)
    if request.method == 'POST':
        course.delete()
        return redirect('courses:course-list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})


