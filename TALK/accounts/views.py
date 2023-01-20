# accounts
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.http import HttpResponseBadRequest
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

@require_http_methods(['GET', 'POST'])
def signup(request):
    # 이미 login한 user라면 -> '로그인하셨습니다.' 출력
    if request.user.is_authencicated:
        return HttpResponseBadRequest('로그인 하셨습니다.')
    # POST 요청일 경우 회원가입 폼 저장 > 로그인 > 홈화면 redirect 
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) 
            return redirect('board:art_index')
    # GET 요청일 경우 
    else:
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request,'accounts/signup.hml', context)

@require_http_methods(['GET', 'POST'])
def login(request):
    # login한 user라면 -> '로그인하셨습니다.' 출력
    if request.user.is_authencicated:
        return HttpResponseBadRequest('로그인 하셨습니다.')
    # POST 요청일 경우, 로그인 폼에 사용자가 입력한 값이 유효할 경우 이를 저장해서 로그인  
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST) # 로그인을 해주는 폼
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) # 로그인(쿠키 세팅)
    # GET 요청일 경우
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


# 로그아웃은 어떤 상태이든 권장되므로, method 따로 조건두지 않음 
def logout(request):
    auth_logout(request)
    return redirect('board:art_index')


# 사용자 profile
@require_safe
def profile(request, username):
    me = request.user # request의 유저
    profile_user = get_object_or_404(User, username=username)
    # 요청 보낸 사용자가 로그인 했다면
    if me.is_authenticated:
        is_following = me.following.filter(pk=profile_user.pk).exists()
    else:
        is_following = None
    context = {
        'profile_user': profile_user,
        'is_following': is_following,
    }
    return render(request, 'accounts/profile.html', context)


# follow 기능 추가 
@require_POST
def follow(request, username):
    me = request.user 
    you = get_object_or_404(User, username=username)
    # 본인 계정 팔로우 x 
    if me == you:
        return HttpResponseBadRequest('본인 계정입니다.')
    is_following = me.following.filter(pk=you.pk).exists()
    if is_following:
        me.following.remove(you)
    else:
        me.following.add(you)
    return redirect('accounts:profile', you.username)

