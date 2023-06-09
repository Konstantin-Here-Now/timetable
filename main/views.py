import json
import logging

from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import PasswordResetView

from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Lesson
from .forms import LessonCreateForm, LessonUpdateForm, UserRegistrationForm, UserLoginForm

from .dates_and_time import TODAY, DATES_JSON_PATH, update

logger = logging.getLogger(__name__)

CONTACTS = settings.CONTACTS


def index(request):
    with open(DATES_JSON_PATH, 'r', encoding='UTF-8') as dates_f:
        dates_data = json.loads(dates_f.read())
    return render(request, 'main/index.html', context={'days_dataset': dates_data})


def contacts(request):
    context = CONTACTS
    return render(request, 'main/contacts.html', context)


def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            logger.info(f'{user.username} registered!')
            user.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            logger.info(f'{user.username} logs in!')
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'main/users/login.html', {'form': form})


def user_logout(request):
    logger.info(f'{request.user.username} logs out!')
    logout(request)
    return redirect('index')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'main/users/password_reset/password_reset.html'
    email_template_name = 'main/users/password_reset/password_reset_email.html'
    subject_template_name = 'main/users/password_reset/password_reset_subject.txt'
    success_message = 'Мы отправили письмо с дальнейшими инструкциями по смене пароля'
    success_url = reverse_lazy('index')


@login_required
def profile(request):
    user = request.user
    lessons = Lesson.objects.filter(user_id=user.id, date_lesson__gte=TODAY).order_by('date_lesson')

    paginator = Paginator(lessons, 3)
    pag_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(pag_num)

    context = {
        'user': user,
        'lessons': lessons,
        'page_obj': page_objects
    }
    return render(request, 'main/users/profile.html', context=context)


class LessonCreateView(CreateView):
    model = Lesson
    form_class = LessonCreateForm
    template_name = 'main/enroll.html'
    context_object_name = 'form'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        pupil = self.request.user
        date_lesson = form.instance.date_lesson
        time_lesson = f'{form.instance.time_lesson_start} - {form.instance.time_lesson_end}'

        form.instance.user = pupil
        logger.info(f'{pupil} created lesson request at {date_lesson} {time_lesson}')

        # Sending email to settings.EMAIL_ADMIN
        message_to_send = f'{pupil.first_name} {pupil.last_name} предложил(-а) провести занятие {date_lesson} ' \
                          f'в промежуток {time_lesson}.'
        additional_message = form.instance.desc
        if additional_message:
            message_to_send += f'\nУченик оставил следующее сообщение:\n {additional_message}'
        else:
            message_to_send += f'\nУченик не оставил дополнительных сообщений.'
        send_mail(
            subject='Новая запись на занятие',
            message=message_to_send,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_ADMIN],
            fail_silently=False
        )
        return super().form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LessonListView(ListView):
    model = Lesson
    template_name = 'main/lessons_list.html'
    context_object_name = 'lessons'
    pk_url_kwarg = 'lesson_id'

    paginate_by = 6

    def get_queryset(self):
        return Lesson.objects.filter(date_lesson__gte=TODAY).order_by('date_lesson')

    @method_decorator(permission_required('main.view_lesson'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LessonUpdateView(UpdateView):
    model = Lesson
    form_class = LessonUpdateForm
    template_name = 'main/lesson_update.html'
    context_object_name = 'form'

    def form_valid(self, form):
        pupil = form.instance.user
        time_lesson = f'{form.instance.time_lesson_start} - {form.instance.time_lesson_end}'
        date_lesson = form.instance.date_lesson
        approved = 'APPROVED' if form.instance.approved is True else 'DISAPPROVED'
        logger.info(f'<<{approved}>> {pupil} {time_lesson} {date_lesson}')
        if approved == 'APPROVED':
            send_mail(
                subject='Ваше занятие одобрено',
                message=f'Одобрено занятие {date_lesson} в промежуток {time_lesson}.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[pupil.email],
                fail_silently=False
            )
        return super().form_valid(form)

    def get_success_url(self):
        update()
        return reverse_lazy('lessons_list')

    @method_decorator(permission_required('main.change_lesson'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

# class LessonDeleteView(DeleteView):
#     model = Lesson
#
#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         success_url = self.get_success_url()
#         user = request.user
#         if user.is_staff or self.object.user == user:
#             print('GOOD')
#         else:
#             print('BAD')
#         # self.object.delete()
#         return HttpResponseRedirect(success_url)
#
#     def get_success_url(self):
#         user = self.request.user
#         if user.is_staff:
#             return reverse_lazy('lessons_list')
#         elif not user.is_staff:
#             return reverse_lazy('profile')
