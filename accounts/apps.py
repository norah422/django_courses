from django.apps import AppConfig

# 🌟 كلاس إعدادات تطبيق الحسابات (Accounts Application Configuration)
# وظيفته الأساسية هي تسجيل وتعريف تطبيق الـ 'accounts' داخل مشروع جيانغو ليتم التعرف عليه تلقائياً
class AccountsConfig(AppConfig):
    # تحديد النوع الافتراضي للحقول التي تولد مفاتيح التعريف التلقائية (ID) في قاعدة البيانات لهذا التطبيق.
    # الـ BigAutoField يضمن توليد أرقام تعريفية (IDs) كبيرة جداً ومقاومة للنفاد مع زيادة عدد المستخدمين مستقبلاً.
    default_auto_field = 'django.db.models.BigAutoField'
    # الاسم البرمجي الفعلي للتطبيق والمستخدم في الإعدادات المشتركة للمشروع (settings.py)
    name = 'accounts'
