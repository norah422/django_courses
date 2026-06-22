from django import forms
from .models import Comment # استيراد موديل التعليقات لربط الفورم به

# 💬 كلاس إنشاء نموذج التعليقات (ModelForm)
# يعتمد على توليد الحقول تلقائياً بناءً على هيكل جدول التعليقات في قاعدة البيانات
class CommentForm(forms.ModelForm):
    # كلاس الـ Meta (بيانات البيانات): يستخدم لتحديد الإعدادات والروابط الأساسية للفورم
    class Meta:
        model = Comment # إخبار جيانغو أن هذا الفورم مرتبطة بجدول الـ Comment
        fields = ['content'] # تحديد الحقول التي تظهر للمستخدم ليقوم بتعبئتها (حقل نص التعليق فقط)
        # الـ widgets: تستخدم لتخصيص كود الـ HTML والتنسيقات (CSS) لكل حقل على حدى
        widgets = {
            # تخصيص حقل الـ 'content' ليكون صندوق كتابة كبير وتمرير الخصائص التنسيقية له
            'content': forms.Textarea(attrs={
                'class': 'form-control', # إعطاؤه كلاس CSS (يفيد عند ربطه بإطارات مثل Bootstrap)
                'placeholder': 'Enter your comment here...', # النص التوضيحي الشفاف داخل الصندوق
                'rows': 3, # تحديد الارتفاع الافتراضي للصندوق بـ 3 أسطر لتوفير مساحة في الصفحة
                'style': 'width: 100%; padding: 10px; border-radius: 5px; border: 1px solid #ccc;'
                }),
        }