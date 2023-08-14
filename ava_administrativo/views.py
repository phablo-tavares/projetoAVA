from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ava.models import Aluno
from ava.views import CardFinanceiro, CardBoletimDeDesempenho
# Create your views here.


@login_required(login_url="/")
def Dashboard(request):
    userAuth = request.user

    context = {
        'user': userAuth,
        'urlCardGerenciarAlunos': '/card-gerenciar-alunos',
        'urlCardVisualizarDadosDoAluno': '/card-visualizar-dados-do-aluno',
    }

    return render(request, 'ava_administrativo.html', context)


@login_required(login_url="/")
def CardGerenciarAlunos(request):
    userAuth = request.user

    if Aluno.objects.exists():
        alunos = Aluno.objects.all()
    else:
        alunos = None

    context = {
        'user': userAuth,
        'alunos': alunos,
        'urlCardGerenciarAlunos': '/card-gerenciar-alunos',
        'urlExcluirAluno': '/excluir-aluno',
    }
    return render(request, 'cardGerenciarAlunos.html', context)


@login_required(login_url="/")
def CardVisualizarDadosDoAluno(request):
    idDoAluno = request.GET['id']
    aluno = Aluno.objects.get(id=idDoAluno)

    customRequestForAvaView = request
    customRequestForAvaView.user = aluno.user

    context = {
        'cardBoletimDeDesempenho': CardBoletimDeDesempenho(customRequestForAvaView),
        'cardFinanceiro': CardFinanceiro(customRequestForAvaView),
    }
    return render(request, 'cardVisualizarDadosDoAluno.html', context)


@login_required(login_url="/")
def ExcluirAluno(request):
    id = request.POST['id']
    aluno = Aluno.objects.get(id=id)
    user = User.objects.get(id=aluno.user.id)
    aluno.delete()
    user.delete()
