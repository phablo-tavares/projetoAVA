from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout

from django.contrib.auth.models import User
from ava.models import Aluno


def login_page(request):
    return render(request, 'login.html')


def Logout_user(request):
    logout(request)
    return redirect('/')


@csrf_protect
def Autenticar(request):
    # return render(request,"forms.html")
    if request.POST:
        username = request.POST['cpf']
        password = request.POST['senha']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/ava', {'user': user})
        else:
            messages.error(request, ' Usuário/Senha inválidos!')
            return redirect('/')


# pagina = render(request,'index.html',{"alunos":alunos, "escolas":escolas ,"matriculas":matriculas})
