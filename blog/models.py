from django.db import models
from django.contrib.auth.models import User # استيراد موديل المستخدمين الجاهز من جيانغو لربطه بالمنشورات

# 📝 كلاس جدول المنشورات (Post Model) الذي يتحول تلقائياً إلى جدول في قاعدة البيانات
class Post(models.Model):
    # 🌍 دعم ثنائية اللغة لعنوان المنشور (أقصى طول 200 حرف)
    title_en = models.CharField(max_length=200, verbose_name='Post Title (english)')
    title_ar = models.CharField(max_length=200, verbose_name='Post Title (arabic)')

    # 📝 حقول نصية طويلة ومفتوحة لكتابة محتوى المقال باللغتين
    content_en = models.TextField(verbose_name='Post Content (english)')
    content_ar = models.TextField(verbose_name='Post Content (arabic)')

    # 👥 ربط المنشور بالكاتب عبر علاقة (ForeignKey) ربط طرف بطرفين (مستخدم واحد يمكنه كتابة عدة منشورات)
    # الـ on_delete=models.CASCADE تعني: إذا حُذف حساب الكاتب من المنصة، تُحذف جميع مقالاته تلقائياً لحفظ سلامة البيانات
    # الـ related_name='posts' تسمح لنا بجلب جميع مقالات الكاتب بسهولة من موديل المستخدم نفسه
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Author')

    # 🖼️ حقل اختياري لرفع صورة تعبيرية للمقال، وتُخزن الملفات في مجلد فرعي باسم 'blog_images'
    # الـ null=True و blank=True تعني أن الصورة ليست إجبارية ويمكن نشر المقال بدونها
    image = models.ImageField(upload_to='blog_images/', verbose_name='Post Image', null=True, blank=True)

    # ⏱️ حقل لتسجيل تاريخ ووقت إنشاء المقال تلقائياً (auto_now_add=True تثبت الوقت لحظة الضغط على نشر)
    created_at = models.DateTimeField(auto_now_add=True)

    # 🎯 دالة تمثيل الموديل كنص (String Representation)
    # وظيفتها: تجعل المقال يظهر باسمه الفعلي (العنوان العربي) داخل لوحة تحكم الإدارة (Django Admin) بدلاً من ظهور كلمة "Post object"
    def __str__(self):
        return self.title_ar