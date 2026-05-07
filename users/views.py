from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Post
from .models import Notification
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Registratsiya muvaffaqiyatli! Login qilishingiz mumkin.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profil muvaffaqiyatli yangilandi!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/edit_profile.html', context)

def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user, status='published').order_by('-created_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    is_following = False
    if request.user.is_authenticated:
        if user.profile.followers.filter(id=request.user.id).exists():
            is_following = True
            
    context = {
        'profile_user': user,
        'page_obj': page_obj,
        'is_following': is_following,
    }
    return render(request, 'users/profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        if user_to_follow.profile.followers.filter(id=request.user.id).exists():
            user_to_follow.profile.followers.remove(request.user)
        else:
            user_to_follow.profile.followers.add(request.user)
            # Create notification
            Notification.objects.create(
                recipient=user_to_follow,
                sender=request.user,
                notification_type='follow',
                text=f'{request.user.username} sizga obuna bo\'ldi.'
            )
    return HttpResponseRedirect(reverse('user-profile', args=[username]))

@login_required
def notifications(request):
    user_notifications = request.user.notifications.all()
    # Mark all as read when user visits the page
    user_notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'users/notifications.html', {'notifications': user_notifications})

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/dashboard.html', {'page_obj': page_obj})
