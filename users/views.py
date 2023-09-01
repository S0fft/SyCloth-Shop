from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from users.models import User
from common.views import TitleMixin


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    title = 'SyCloth - Регистрация'
    success_url = reverse_lazy('users:login')
    success_message = 'Поздравляем! Вы успешно зарегистрированы!'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'SyCloth - Личный кабинет'

    def get_context_data(self):
        context = super().get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.object)

        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'SyCloth - Авторизация'


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - подтверждение электронной почты'

    # def login(request):
    #     if request.method == 'POST':
    #         form = UserLoginForm(data=request.POST)

    #         if form.is_valid():
    #             username = request.POST['username']
    #             password = request.POST['password']
    #             user = auth.authenticate(username=username, password=password)

    #             if user:
    #                 auth.login(request, user)
    #                 return HttpResponseRedirect(reverse('index'))
    #     else:
    #         form = UserLoginForm()

    #     context = {'form': form}
    #     return render(request, 'users/login.html', context)

    # def registration(request):
    #     if request.method == 'POST':
    #         form = UserRegistrationForm(data=request.POST)

    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, 'Поздравляем! Вы успешно зарегистрированы!')
    #             return HttpResponseRedirect(reverse('users:login'))
    #     else:
    #         form = UserRegistrationForm()

    #     context = {'form': form}
    #     return render(request, 'users/registration.html', context)

    # @login_required
    # def profile(request):
    #     if request.method == 'POST':
    #         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)

    #         if form.is_valid():
    #             form.save()
    #             return HttpResponseRedirect(reverse('users:profile'))
    #         else:
    #             print(form.errors)
    #     else:
    #         form = UserProfileForm(instance=request.user)

    #     context = {
    #         'title': 'Store - Профиль',
    #         'form': form,
    #         'baskets': Basket.objects.filter(user=request.user),
    #     }
    #     return render(request, 'users/profile.html', context)

    # def logout(request):
    #     auth.logout(request)

    #     return HttpResponseRedirect(reverse('index'))
