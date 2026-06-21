from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title_en = models.CharField(max_length=200, verbose_name='Course Title (english)')
    title_ar = models.CharField(max_length=200, verbose_name='Course Title (arabic)')

    description_en = models.TextField(verbose_name='Course Description (english)')
    description_ar = models.TextField(verbose_name='Course Description (arabic)')

    price = models.DecimalField(max_length=10 ,max_digits=10, decimal_places=2, verbose_name='Price (SAR)')
    image = models.ImageField(upload_to='course_images/', verbose_name='Course Image')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_ar


class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos', verbose_name='Course')
    title_en = models.CharField(max_length=200, verbose_name='Video Title (english)')
    title_ar = models.CharField(max_length=200, verbose_name='Video Title (arabic)')
    video_url = models.URLField(max_length=200, null=True, blank=True, verbose_name='Video File')

    def __str__(self):
        return f"{self.title_ar} - {self.course.title_ar}"

class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments', verbose_name='Course')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    content = models.TextField(verbose_name='Comment Content')
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.course.title_ar}"
    
class CourseOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_orders', verbose_name='Customer')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='orders', verbose_name='Course')
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='Stripe Charge ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Order Date')

    class Meta:
        unique_together = ('customer', 'course')
        verbose_name = 'Course Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order by {self.customer.username} for {self.course.title_ar}"