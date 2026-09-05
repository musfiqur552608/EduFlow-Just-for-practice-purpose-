from django.db import models
from django.conf import settings

class Profile(models.Model):
    STUDENT, INSTRUCTOR = 'student', 'instructor'
    ROLE_CHOICES = [(STUDENT, 'student'), (INSTRUCTOR, 'instructor')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name = 'profile')
    role = models.CharField(max_length=20, choices = ROLE_CHOICES, default=STUDENT)
    bio = models.TextField(blank = True)

class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses_taught'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    ACTIVE, COMPLETED, CANCELLED = 'active', 'completed', 'cancelled'
    STATUS_CHOICES = [(ACTIVE, 'active'), (COMPLETED, 'completed'), (CANCELLED, 'cancelled')]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = 'enrollments')
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'enrollments')
    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default=ACTIVE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    comleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints =[
            models.UniqueConstraint(fields = ['student', 'course'], name='unique_enrollment')
        ]

class Payment(models.Model):
    PENDING, SUCCESS, FAILED = 'pending', 'success', 'failed'
    STATUS_CHOICES = [(PENDING, 'pending'), (SUCCESS, 'success'), (FAILED, 'failed')]
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    
class Review(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()   # validated 1-5 at the form/serializer layer
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course'], name='unique_review')
        ]

class Certificate(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    certificate_code = models.CharField(max_length=50, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = 'lessons')
    title = models.CharField(max_length = 200)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"