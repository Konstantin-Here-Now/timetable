from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *
from .forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('', index, name='index'),
    path('enroll/', LessonCreateView.as_view(), name='enroll'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),
    path('password_reset/', ResetPasswordView.as_view(form_class=EmailValidationOnForgotPassword),
         name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='main/users/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='main/users/password_reset/password_reset_complete.html'), name='password_reset_complete'),

    path('profile/', profile, name='profile'),
    path('faq/', faq, name='faq'),
    path('mail/', mail, name='mail'),

    path('materials/', materials, name='materials'),
    path('download/<str:path>', download, name='download'),

    path('lessons_list/', LessonListView.as_view(), name='lessons_list'),
    path('lesson_update/<int:pk>/', LessonUpdateView.as_view(), name='lesson_update'),

    path('update_time_manual/', update_time_manual, name='update_time_manual')
]
