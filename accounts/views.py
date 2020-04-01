from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.http import HttpResponseRedirect
from .models import UserProfile
from django.views.generic.edit import FormView
from .forms import UserRegisterForm
User = get_user_model()
# CLASS VIEW
# class UserDetailView(DetailView):
#     template_name = 'accounts/user_detail.html'
#     queryset = User.objects.all()
    # def get_object(self):
    #     return get_object_or_404(User, username__iexact=username)

class UserRegisterView(FormView):
    template_name = 'accounts/user_register_form.html'
    form_class = UserRegisterForm
    success_url = '/login'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return super(UserRegisterView, self).form_valid(form)



def userdetail(request, username):
    if request.user.is_authenticated:
        queryset = get_object_or_404(User, username__iexact=username)
        
        context = {
            "objecttt": queryset,
            "following": UserProfile.objects.is_following(request.user, queryset),
            "recommended": UserProfile.objects.recommended(request.user)
        }
        return render(request, "accounts/user_detail.html", context)
    return redirect("login")

# class UserFollowView(View):
#     def get(self, request, username, *args, **kwargs):
#         toggle_user = get_object_or_404(User, username__iexact=username)
#         if request.user.is_authenticated:
#             user_profile, created = UserProfile.objects.get_or_create(user=request.user) # (user_obj, True)
#             if toggle_user in user_profile.following.all():
#                 user_profile.following.remove(toggle_user)
#             else:
#                 user_profile.following.add(toggle_user)
#         return redirect("profiles:detail", username=username)

def userfollow(request, username):
    toggle_user = get_object_or_404(User, username__iexact=username)
    if request.user.is_authenticated:
         is_following=UserProfile.objects.toggle_follow(request.user, toggle_user)

    return redirect("profiles:detail", username=username)
