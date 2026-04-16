from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, LoginForm
from .models import User

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            
            print(f"DEBUG: Login attempt - Username: {username}, User Type: {user_type}")
            
            user = authenticate(request, username=username, password=password)
            print(f"DEBUG: Authentication result: {user}")
            
            if user is not None:
                print(f"DEBUG: User found - Type: {user.user_type}, Approved: {user.is_approved}")
                
                if user.user_type == user_type:
                    print(f"DEBUG: User type matches")
                    
                    if user.is_approved or user.is_superuser:
                        print(f"DEBUG: User approved - logging in")
                        login(request, user)
                        messages.success(request, f'Welcome back, {user.username}!')
                        
                        # Redirect based on user type
                        if user.is_admin_user():
                            return redirect('core:admin_dashboard')
                        elif user.is_college():
                            return redirect('core:college_dashboard')
                        else:
                            return redirect('core:student_dashboard')
                    else:
                        print(f"DEBUG: User not approved")
                        messages.error(request, 'Your account is pending approval.')
                else:
                    print(f"DEBUG: User type mismatch")
                    messages.error(request, 'Invalid credentials or user type mismatch.')
            else:
                print(f"DEBUG: Authentication failed")
                messages.error(request, 'Invalid credentials or user type mismatch.')
        else:
            print(f"DEBUG: Form invalid: {form.errors}")
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')

class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful! Please wait for admin approval.')
        return response

@login_required
def profile_view(request):
    user = request.user
    context = {'user': user}
    
    if user.is_student():
        try:
            context['student_profile'] = user.studentprofile
        except:
            pass
    elif user.is_college():
        try:
            context['college_profile'] = user.collegeprofile
        except:
            pass
    
    return render(request, 'accounts/profile.html', context)
