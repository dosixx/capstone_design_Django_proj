from django.shortcuts import render
import hashlib
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import User

def index_view(request):
    return render(request, 'index.html')
def post_view(request):
    return render(request, 'post.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        hashed_pw = hashlib.md5(password.encode()).hexdigest()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid username')
            return render(request, 'login.html')
        if user.password == hashed_pw:
            request.session['user_id'] = user.id  # ✅ id 저장
            request.session['is_admin'] = user.is_admin
            return redirect('/post/')
        else:
            messages.error(request, 'Invalid password')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        #MD5 해시 처리 (salt 없이)
        hashed_pw = hashlib.md5(password.encode()).hexdigest()
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('/login/')

        User.objects.create(
            username=username,
            password=hashed_pw,
            email=email,
        )
        messages.success(request, 'User created successfully.')
        return redirect('/login/')

    return render(request, 'signup.html')