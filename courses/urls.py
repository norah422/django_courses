from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('courses/', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/checkout/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/<int:course_id>/', views.payment_success, name='payment_success'),
    path('<int:course_id>/add-comment/', views.add_comment, name='add_comment'),
    path('my-courses/', views.my_courses, name='my_courses'),
]