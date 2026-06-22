import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Video, Comment, CourseOrder
from .forms import CommentForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# تهيئة وإعداد مفتاح الاتصال السري الخاص ببوابة Stripe للقراءة من ملف الإعدادات الآمن
stripe.api_key = settings.STRIPE_SECRET_KEY

# 1️⃣ دالة الصفحة الرئيسية للمنصة: تجلب أول 3 كورسات فقط كـ (Featured Courses) للعرض الإعلاني
def home_page(request):
    featured_courses = Course.objects.all()[:3]
    return render(request, 'courses/home.html', {'featured_courses': featured_courses})

# 2️⃣ دالة قائمة الكورسات: تجلب جميع الدورات المتاحة في قاعدة البيانات ليعرضها الطالب
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

# 3️⃣ دالة تفاصيل الكورس: تعرض الفيديوهات والتعليقات، وتفحص حالة شراء الطالب الحالية
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()

# جلب التعليقات الرئيسية فقط (التي ليس لها أب parent__isnull=True) وترتيبها من الأحدث
    comments = course.comments.filter(parent__isnull=True).order_by('-created_at')

# فحص أمني: التحقق ما إذا كان الطالب الحالي قد اشترى هذا الكورس مسبقاً لإتاحة المحتوى له
    has_purchased = False
    if request.user.is_authenticated:
        has_purchased = CourseOrder.objects.filter(customer=request.user, course=course).exists()

    context = {
        'course': course,
        'videos': videos,
        'comments': comments,
        'has_purchased': has_purchased,
    }

    return render(request, 'courses/course_detail.html', context)
    

# 4️⃣ دالة إنشاء جلسة الدفع عبر Stripe (Stripe Checkout Session)
def create_checkout_session(request, course_id):
        # حماية: منع الزوار غير المسجلين من الشراء وتوجيههم لصفحة تسجيل الدخول
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to purchase a course.")
        return redirect('login')
    
    course = get_object_or_404(Course, id=course_id)

# تحويل السعر من ريال إلى هللة (الضرب في 100) لأن Stripe يستقبل المبالغ بالوحدة الصغرى للعملة
    amount_in_halals = int(course.price * 100)  

# بناء روابط العودة التلقائية (مطلقاً) بعد نجاح العملية أو إلغائها
    success_url = request.build_absolute_uri(reverse('courses:payment_success', args=[course.id]))
    cancel_url = request.build_absolute_uri(reverse('courses:course_detail', args=[course.id]))

    try:
        # إنشاء الجلسة رسمياً عبر إرسال بيانات الكورس والعملة (SAR) والسعر إلى سيرفرات Stripe
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'sar',
                    'product_data': {
                        'name': course.title_ar,
                    },
                    'unit_amount': amount_in_halals,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_url,
        )
# توجيه المتصفح تلقائياً بترميز (303 Redirect) إلى واجهة الدفع الآمنة الخاصة بـ Stripe
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"An error occurred while creating the checkout session: {str(e)}")
        return redirect('courses:course_detail', course_id=course.id)
    
# 5️⃣ دالة معالجة نجاح الدفع وتأكيد الطلب
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    session_id = request.GET.get('session_id') # التقاط المعرّف القادم من Stripe بعد الدفع

    if session_id:
        try:
            # استدعاء واسترجاع بيانات الجلسة من Stripe للتأكد من إتمام العملية
            session = stripe.checkout.Session.retrieve(session_id)
            charge_id = session.payment_intent # سحب رقم الإيصال المالي (Payment Intent ID)

            # تسجيل عملية الشراء رسمياً في قاعدة البيانات للربط بين الطالب والكورس
            # get_or_create تضمن عدم تكرار الفاتورة لنفس الطالب لنفس الكورس في حال أعاد تنشيط الصفحة

            CourseOrder.objects.get_or_create(
                customer=request.user,
                course=course,
                defaults={'stripe_charge_id': charge_id}
            )
            messages.success(request, f"You have successfully purchased the course: {course.title_ar}")
        except Exception:
            pass

    return render(request, 'courses/order_success.html', {'course': course})

# 6️⃣ دالة إضافة تعليق أو رد داخل صفحة الكورس
def add_comment(request, course_id):
    if request.method == 'POST' and request.user.is_authenticated:
        course = get_object_or_404(Course, id=course_id)

# حماية المحتوى: التحقق من أن الطالب قد اشترى الكورس فعلياً قبل السماح له بالتعليق
        has_purchased = CourseOrder.objects.filter(customer=request.user, course=course).exists()
        if not has_purchased:
            messages.error(request, "You need to purchase the course to comment.")
            return redirect('courses:course_detail', course_id=course.id)
        
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)

# إنشاء وحفظ كائن التعليق الجديد في قاعدة البيانات
        Comment.objects.create(
            course=course,
            user=request.user,
            content=content,
            parent=parent_comment
        )

        messages.success(request, "Your comment has been added.")
        return redirect('courses:course_detail', course_id=course.id)

# 7️⃣ دالة عرض الكورسات المملوكة للطالب (لوحة تحكم الطالب المشترى)
@login_required # حارس حماية يمنع دخول غير المسجلين (توجيه تلقائي لصفحة الـ Login)
def my_courses(request):
    # جلب جميع طلبات الشراء الناجحة الخاصة بهذا الطالب بالتحديد
    orders = CourseOrder.objects.filter(customer=request.user)
    # استخراج الكورسات من داخل الطلبات وحفظها في قائمة مجمعة لعرضها
    purchased_courses = [order.course for order in orders]
    return render(request, 'courses/my_courses.html', {'purchased_courses': purchased_courses})