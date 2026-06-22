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
    
    # دالة تحسين الأداء وجلب البيانات ديناميكياً
    def get_queryset(self, request):  
        queryset = super().get_queryset(request)
        # استخدام الـ annotate وعمل Count لحساب عدد الفيديوهات المرتبطة بكل كورس في استعلام واحد (Query) لتوفير جهد قاعدة البيانات
        return queryset.annotate(video_count=Count('videos'))

    # دالة برمجية لقراءة القيمة المحسوبة (video_count) وعرضها داخل عمود الجدول
    def video_count(self, obj):
        return obj.video_count
    
    video_count.short_description = 'Number of Videos'

# 3️⃣ تخصيص لوحة تحكم التعليقات (Comment Admin)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('course', 'created_at')


@admin.register(CourseOrder)
class CourseOrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'course', 'stripe_charge_id', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('customer__username', 'stripe_charge_id')
