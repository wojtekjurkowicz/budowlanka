from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import UserCreationFormWithEmail, UserAuth


def login_view(request):
    if request.method == 'POST':
        form = UserAuth(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Pomyślnie zalogowano.')
                return redirect('mainapp:index')
            else:
                messages.error(request, 'Nieprawidłowe dane logowania.')
        else:
            messages.error(request, 'Nieprawidłowe dane logowania.')
    else:
        form = UserAuth()
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    # register a new user
    if request.method != 'POST':
        # Display blank registration form
        form = UserCreationFormWithEmail(data=request.POST)
    else:
        # Process completed form
        form = UserCreationFormWithEmail(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page
            login(request, new_user)
            messages.success(request, 'Rejestracja zakończona sukcesem.')
            return redirect('mainapp:index')
        else:
            messages.error(request, 'Hasła nie są takie same')
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'registration/register.html', context)
