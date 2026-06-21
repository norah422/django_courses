import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Video, Comment, CourseOrder
from .forms import CommentForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required


stripe.api_key = settings.STRIPE_SECRET_KEY

def home_page(request):
    featured_courses = Course.objects.all()[:3]
    return render(request, 'courses/home.html', {'featured_courses': featured_courses})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    videos = course.videos.all()

    comments = course.comments.filter(parent__isnull=True).order_by('-created_at')

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
    

def create_checkout_session(request, course_id):
        
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to purchase a course.")
        return redirect('login')
    
    course = get_object_or_404(Course, id=course_id)

    amount_in_halals = int(course.price * 100)  

    success_url = request.build_absolute_uri(reverse('courses:payment_success', args=[course.id]))
    cancel_url = request.build_absolute_uri(reverse('courses:course_detail', args=[course.id]))

    try:
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

        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"An error occurred while creating the checkout session: {str(e)}")
        return redirect('courses:course_detail', course_id=course.id)
    

def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    session_id = request.GET.get('session_id')

    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            charge_id = session.payment_intent

            CourseOrder.objects.get_or_create(
                customer=request.user,
                course=course,
                defaults={'stripe_charge_id': charge_id}
            )
            messages.success(request, f"You have successfully purchased the course: {course.title_ar}")
        except Exception:
            pass

    return render(request, 'courses/order_success.html', {'course': course})

def add_comment(request, course_id):
    if request.method == 'POST' and request.user.is_authenticated:
        course = get_object_or_404(Course, id=course_id)

        has_purchased = CourseOrder.objects.filter(customer=request.user, course=course).exists()
        if not has_purchased:
            messages.error(request, "You need to purchase the course to comment.")
            return redirect('courses:course_detail', course_id=course.id)
        
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        parent_comment = None
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)

        Comment.objects.create(
            course=course,
            user=request.user,
            content=content,
            parent=parent_comment
        )

        messages.success(request, "Your comment has been added.")
        return redirect('courses:course_detail', course_id=course.id)


@login_required
def my_courses(request):
    orders = CourseOrder.objects.filter(customer=request.user)
    purchased_courses = [order.course for order in orders]
    return render(request, 'courses/my_courses.html', {'purchased_courses': purchased_courses})