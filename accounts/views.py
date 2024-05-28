from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views import View
from .forms import RegistationForm,UserUpdateForm
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
# Create your views here.

class userRegistation(FormView):
    form_class=RegistationForm
    template_name="accounts/Registation.html"
    success_url=reverse_lazy("login")

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return super().form_valid(form) # form valid function call hbe jdi sob thik thak thake
    
class UserLogin(LoginView):
    template_name="accounts/login.html"
    def get_success_url(self):
        return reverse_lazy("Profile")

class UserLogout(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy("login")

class UpdateProfile(View):
    template_name="accounts/profile.html"

    def get(self,request):
        form=UserUpdateForm(instance=request.user)
        return render(request,self.template_name, {"form":form})
    
    def post(self,request):
        form=UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("Profile")
        return render(request, self.template_name, {"form":form})