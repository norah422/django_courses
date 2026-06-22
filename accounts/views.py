from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm # استيراد نموذج إنشاء المستخدم الجاهز والمؤمن من جيانغو
from django.contrib.auth import login, logout # استيراد دالتي تسجيل الدخول والخروج الداخلية

# 1️⃣ دالة تسجيل مستخدم (طالب) جديد في المنصة
def signup_view(request):
    # الفحص: هل الطالب ضغط على زر الإرسال وأرسل بياناته؟ (POST)
    if request.method == 'POST':
        # استقبال البيانات القادمة من الفورم وتعبئتها في النموذج
        form = UserCreationForm(request.POST)
        # التحقق من صحة البيانات (هل كلمة المرور قوية ومتطابقة؟ هل اسم المستخدم متاح؟)
        if form.is_valid():
            user = form.save() # حفظ الطالب الجديد تلقائياً في قاعدة البيانات وتشفير باسوورده
            login(request, user) # تسجيل دخول الطالب تلقائياً فور إنشائه للحساب لتوفير تجربة سلسة
            return redirect('/') # توجيه الطالب مباشرة إلى الصفحة الرئيسية للموقع
    # إذا كان الطالب يتصفح الصفحة فقط ولم يضغط إرسال بعد (GET)
    else:
        form = UserCreationForm() # إنشاء نسخة فارغة ونظيفة من استمارة التسجيل
    # عرض صفحة التسجيل وإرسال الـ form لها ليظهر داخل كود الـ HTML
    return render(request, 'accounts/signup.html', {'form': form})

# 2️⃣ دالة تسجيل الخروج من المنصة
def logout_view(request):
    logout(request) # إنهاء جلسة المستخدم الحالية (Session) وحذف بياناته المؤقتة من المتصفح بأمان
    return redirect('/') # توجيه المستخدم تلقائياً للصفحة الرئيسية بعد خروجه