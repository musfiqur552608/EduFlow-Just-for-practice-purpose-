# courses/admin.py
from django.contrib import admin
from .models import Course, Lesson, Profile, Enrollment, Payment, Review, Certificate

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Profile)
admin.site.register(Enrollment)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Certificate)