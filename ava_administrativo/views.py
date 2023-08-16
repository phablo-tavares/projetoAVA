from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ava.models import Aluno, ProvaRealizadaPeloAluno, Prova, Questao, Materia, BoletimDeDesempenhoDoAluno
from ava.views import CardFinanceiro, CardBoletimDeDesempenho
import json
from django.http import JsonResponse
from ava.util.util import gerarDadosBoletimDeDesempenhoDeUmAluno, gerarDadosFinanceirosDoAluno, dadosParaRenderizarAProvaRealizadaPeloAluno, CursosEmQueOAlunoEstaMatriculado, MateriasDeUmCurso
# Create your views here.


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


@login_required(login_url="/")
def Dashboard(request):
    userAuth = request.user

    context = {
        'user': userAuth,
        'urlCardGerenciarAlunos': '/card-gerenciar-alunos',
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
        'urlCardVisualizarDadosDoAluno': '/card-visualizar-dados-do-aluno',
        'urlCardVisualizarDadosDoAluno': '/card-visualizar-dados-do-aluno',
        'urlCardEditarDadosPessoaisDeUmAluno': '/card-editar-dados-pessoais-de-um-aluno',
    }
    return render(request, 'cardGerenciarAlunos.html', context)


@login_required(login_url="/")
def CardVisualizarDadosDoAluno(request):
    idDoAluno = request.GET['id']
    aluno = Aluno.objects.get(id=idDoAluno)
    dadosBoletimDeDesempenho = gerarDadosBoletimDeDesempenhoDeUmAluno(aluno)
    dadosFinanceirosDoAluno = gerarDadosFinanceirosDoAluno(aluno)

    provasRealizadasPeloAluno = ProvaRealizadaPeloAluno.objects.filter(
        aluno_id=aluno.id).all()
    provasQueOAlunoPodeFazer = []
    for provaRealizada in provasRealizadasPeloAluno:
        provasQueOAlunoPodeFazer.append(provaRealizada.prova)

    context = {
        'aluno': aluno,
        'dadosBoletimDeDesempenho': dadosBoletimDeDesempenho,
        'dadosFinanceirosDoAluno': dadosFinanceirosDoAluno,
        'provasQueOAlunoPodeFazer': provasQueOAlunoPodeFazer,
        'urlCardProvaAdministrativo': "/card-prova-administrativo",
    }
    return render(request, 'cardVisualizarDadosDoAluno.html', context)


# finalizar essa parte. falta fazer a requisição ajax com os parametros necessários para chegar nessa view
# ao clicar em uma prova, exibir o card desta prova no container principal com a opção de voltar
@login_required(login_url="/")
def CardProvaAdministrativo(request):
    idDaProva = request.GET['idDaProva']
    prova = Prova.objects.get(id=idDaProva)
    questoes = Questao.objects.filter(prova=prova)
    idDoAluno = request.GET['idDoAluno']
    aluno = Aluno.objects.get(id=idDoAluno)

    materia = Materia.objects.get(id=prova.materia.id)

    dados = dadosParaRenderizarAProvaRealizadaPeloAluno(prova, questoes, aluno)
    provaRealizadaPeloAluno = dados['provaRealizadaPeloAluno']
    questoesDaProvaRealizadaPeloAluno = dados['questoesDaProvaRealizadaPeloAluno']

    context = {'prova': prova,
               'questoes': questoes,
               'materia': materia,
               'provaRealizadaPeloAluno': provaRealizadaPeloAluno,
               'questoesDaProvaRealizadaPeloAluno': questoesDaProvaRealizadaPeloAluno,
               'urlCardVisualizarDadosDoAluno': "/card-visualizar-dados-do-aluno",
               'aluno': aluno,
               }
    return render(request, 'cardProvaAdministrativo.html', context)


@login_required(login_url="/")
def CardEditarDadosPessoaisDeUmAluno(request):
    idDoAluno = request.GET['id']
    aluno = Aluno.objects.get(id=idDoAluno)

    boletinsDasProvasOQualOAlunoReprovou = BoletimDeDesempenhoDoAluno.objects.filter(
        aluno=aluno, aprovado=False)
    if len(boletinsDasProvasOQualOAlunoReprovou) == 0:
        boletinsDasProvasOQualOAlunoReprovou = None
        provasRealizadasOQualOAlunoReprovou = None
    else:
        provasRealizadasOQualOAlunoReprovou = []
        for boletin in boletinsDasProvasOQualOAlunoReprovou:
            provasRealizadasOQualOAlunoReprovou.append(boletin.provaRealizada)

    context = {
        'aluno': aluno,
        'urlSalvarEdicaoEmUmAluno': '/salvar-dados-pessoais-de-um-aluno',
        'urlCardGerenciarAlunos': '/card-gerenciar-alunos',
        'urlPermitirRefazerAProva': '/permitir-refazer-uma-prova',
        'provasRealizadasOQualOAlunoReprovou': provasRealizadasOQualOAlunoReprovou,
    }
    return render(request, 'cardEditarDadosPessoaisDeUmAluno.html', context)


@login_required(login_url="/")
def SalvarDadosPessoaisDeUmAluno(request):
    idDoAluno = request.POST['id']
    aluno = Aluno.objects.get(id=idDoAluno)
    dadosAlunoSerializado = json.loads(request.POST['dadosAlunoSerializado'])

    for dado in dadosAlunoSerializado:
        if dado['name'] == 'nome':
            aluno.nome = dado['value']
        elif dado['name'] == 'cpf':
            aluno.cpf = int(dado['value'])
        elif dado['name'] == 'rg':
            aluno.rg = int(dado['value'])
        elif dado['name'] == 'email':
            aluno.email = dado['value']
        elif dado['name'] == 'endereco':
            aluno.endereco = dado['value']
        elif dado['name'] == 'sexo':
            aluno.sexo = dado['value']

    aluno.save()

    return JsonResponse(json.dumps(aluno.nome, indent=4, cls=CustomEncoder), safe=False)


@login_required(login_url="/")
def PermitirQueOAlunoRefacaUmaProva(request):
    idProvaRealizada = request.POST['id']
    provaRealizada = ProvaRealizadaPeloAluno.objects.get(id=idProvaRealizada)
    BoletimDeDesempenhoDoAluno.objects.filter(
        provaRealizada=provaRealizada).delete()
    provaRealizada.finalizouAProva = False
    provaRealizada.save()
    return JsonResponse(json.dumps(provaRealizada.prova.nome, indent=4, cls=CustomEncoder), safe=False)


@login_required(login_url="/")
def ExcluirAluno(request):
    id = request.POST['id']
    aluno = Aluno.objects.get(id=id)
    user = User.objects.get(id=aluno.user.id)
    aluno.delete()
    user.delete()
