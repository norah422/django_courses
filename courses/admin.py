from django.contrib import admin
from django.db.models import Count
from .models import Course, Video, Comment, CourseOrder

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title_ar', 'title_en', 'course')
    list_filter = ['course']
    search_fields = ('title_ar', 'title_en')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title_ar', 'title_en', 'price', 'video_count')
    search_fields = ('title_ar', 'title_en', 'description_ar', 'description_en')
    
    def get_queryset(self, request):  
        queryset = super().get_queryset(request)
        return queryset.annotate(video_count=Count('videos'))

    def video_count(self, obj):
        return obj.video_count
    
    video_count.short_description = 'Number of Videos'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('course', 'created_at')


@admin.register(CourseOrder)
class CourseOrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'course', 'stripe_charge_id', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('customer__username', 'stripe_charge_id')
