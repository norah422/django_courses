from django.shortcuts import render, get_object_or_404
from .models import Post    # استيراد موديل المنشورات (جدول قاعدة البيانات) لجلب البيانات منه

# 1️⃣ دالة عرض قائمة جميع المنشورات (Blog Homepage)
def post_list(request):
    # جلب جميع المنشورات من قاعدة البيانات وترتيبها تنازلياً من الأحدث إلى الأقدم بناءً على تاريخ الإنشاء
    # علامة السالب (-) قبل 'created_at' تعني الترتيب التنازلي (Descending Order)
    posts = Post.objects.all().order_by('-created_at')
    # تمرير قائمة المنشورات (posts) داخل قاموس (Context) إلى قالب الـ HTML لعرضها للمستخدم
    return render(request, 'blog/post_list.html', {'posts': posts})

# 2️⃣ دالة عرض تفاصيل منشور واحد محدد (Post Detail Page)
# تستقبل الـ (post_id) القادم من رابط الـ URL لمعرفة أي مقال طلب المستخدم قراءته
def post_detail(request, post_id):
    # دالة ذكية: تبحث عن المنشور برقم التعريف (id).
    # إذا كان المنشور موجوداً تجلبه، وإذا لم يكن موجوداً (رابط خطأ) ترفع تلقائياً استجابة 404 (Page Not Found) لحماية أمان الموقع
    post = get_object_or_404(Post, id=post_id)
    # تمرير بيانات المنشور المفرد إلى قالب التفاصيل المخصص له
    return render(request, 'blog/post_detail.html', {'post': post})

