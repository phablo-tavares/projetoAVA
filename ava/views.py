from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso, Material, Prova, Questao, ProvaRealizadaPeloAluno, QuestaoDaProvaRealizadaPeloAluno, BoletimDeDesempenhoDoAluno, Parcela
from ava.util.util import CursosEmQueOAlunoEstaMatriculado, editarQuestaoRealizadaAnteriormente, criarQuestaoRealizadaESalvarNaProvaRealizada, MateriasDeUmCurso, gerarDadosBoletimDeDesempenhoDeUmAluno, gerarDadosFinanceirosDoAluno, dadosParaRenderizarAProvaRealizadaPeloAluno
from django.core.files.storage import FileSystemStorage
import json
from django.db.models import Sum
from datetime import date
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse

# Create your views here.


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


@login_required(login_url="/")
def Dashboard(request):
    # OBTEM O USUÁRIO DA INSTANCIA
    userAuth = request.user

    # BUSCA INFORMAÇÕES DO USUÁRIO
    aluno = Aluno.objects.get(user=userAuth)

    data_atual = timezone.now().date()
    if Parcela.objects.filter(aluno=aluno, dataDeVencimento__gt=data_atual).exists():
        aluno.possuiParcelaVencida = True

    context = {
        'aluno': aluno,
        'urlBoletimDeDesempenho': "/card-boletim-de-desempenho",
        'urlCursosMatriculados': "/card-cursos-matriculados",
        'urlFinanceiro': "/card-financeiro",
        'urlEditarDadosPessoaisDoAluno': "/card-editar-dados-pessoais",
    }

    return render(request, 'ava.html', context)


@login_required(login_url="/")
def CardCursosMatriculados(request):
    aluno = Aluno.objects.get(user=request.user)
    cursosMatriculados = CursosEmQueOAlunoEstaMatriculado(aluno=aluno)
    if cursosMatriculados == []:
        cursosMatriculados = None
    urlMateriasDoCurso = "/card-materias-do-curso"

    context = {'aluno': aluno, 'cursosMatriculados': cursosMatriculados,
               'urlMateriasDoCurso': urlMateriasDoCurso}
    return render(request, 'cardCursosMatriculados.html', context)


@login_required(login_url="/")
def CardMateriasDoCurso(request):
    idCurso = request.GET['id']
    curso = Curso.objects.get(id=idCurso)
    materiasDoCurso = MateriasDeUmCurso(curso)
    if materiasDoCurso == []:
        materiasDoCurso = None

    urlMateriaisDaMateria = "/card-materiais-da-materia"
    urlCursosMatriculados = "/card-cursos-matriculados"

    context = {'curso': curso, 'materiasDoCurso': materiasDoCurso,
               'urlMateriaisDaMateria': urlMateriaisDaMateria, 'urlCursosMatriculados': urlCursosMatriculados}
    return render(request, 'cardMateriasDoCurso.html', context)


@login_required(login_url="/")
def CardMateriaisDaMateria(request):
    idDaMateria = request.GET['id']
    materia = Materia.objects.get(id=idDaMateria)

    materiais = Material.objects.filter(materia_id=idDaMateria)

    urlMateriasDoCurso = "/card-materias-do-curso"
    urlProvas = "/card-prova"

    try:
        prova = Prova.objects.get(materia=materia)
    except:
        prova = None

    aluno = Aluno.objects.get(user=request.user)
    try:
        provaRealizadaPeloAluno = ProvaRealizadaPeloAluno.objects.get(
            aluno_id=aluno.id, prova_id=prova.id)
        alunoJaFinalizouAProva = provaRealizadaPeloAluno.finalizouAProva
    except:
        alunoJaFinalizouAProva = False

    if prova is not None:
        existeQuestaoCadastradaNaProva = Questao.objects.filter(
            prova_id=prova.id).exists()

    context = {'materia': materia, 'materiais': materiais, 'prova': prova, 'urlMateriasDoCurso': urlMateriasDoCurso, 'urlProvas': urlProvas,
               'alunoJaFinalizouAProva': alunoJaFinalizouAProva, 'existeQuestaoCadastradaNaProva': existeQuestaoCadastradaNaProva}
    return render(request, 'cardMateriaisDaMateria.html', context)


@login_required(login_url="/")
def CardProva(request):
    idDaProva = request.GET['id']
    prova = Prova.objects.get(id=idDaProva)
    questoes = Questao.objects.filter(prova=prova)
    aluno = Aluno.objects.get(user=request.user)

    materia = Materia.objects.get(id=prova.materia.id)

    dados = dadosParaRenderizarAProvaRealizadaPeloAluno(prova, questoes, aluno)
    provaRealizadaPeloAluno = dados['provaRealizadaPeloAluno']
    questoesDaProvaRealizadaPeloAluno = dados['questoesDaProvaRealizadaPeloAluno']

    context = {'prova': prova,
               'questoes': questoes,
               'materia': materia,
               'provaRealizadaPeloAluno': provaRealizadaPeloAluno,
               'questoesDaProvaRealizadaPeloAluno': questoesDaProvaRealizadaPeloAluno,
               'urlMateriaisDaMateria': "/card-materiais-da-materia",
               'urlBoletimDeDesempenho': "/card-boletim-de-desempenho",
               }
    return render(request, 'cardProva.html', context)


@login_required(login_url="/")
def CardBoletimDeDesempenho(request):
    aluno = Aluno.objects.get(user=request.user)
    dadosBoletimDeDesempenho = gerarDadosBoletimDeDesempenhoDeUmAluno(aluno)

    context = {
        'dadosBoletimDeDesempenho': dadosBoletimDeDesempenho,
        'aluno': aluno
    }
    return render(request, 'boletimDeDesempenhoDoAluno.html', context)


@login_required(login_url="/")
def CardFinanceiro(request):
    aluno = Aluno.objects.get(user=request.user)
    dadosFinanceirosDoAluno = gerarDadosFinanceirosDoAluno(aluno)

    context = {
        'aluno': aluno,
        'dadosFinanceirosDoAluno': dadosFinanceirosDoAluno,
    }
    return render(request, 'financeiroDoAluno.html', context)


@login_required(login_url="/")
def CardEditarDadosPessoais(request):
    aluno = Aluno.objects.get(user=request.user)

    context = {
        'aluno': aluno,
        'urlSalvarEdicao': '/salvar-dados-pessoais-aluno'
    }
    return render(request, 'cardEditarDadosPessoais.html', context)


@login_required(login_url="/")
def SalvarDadosPessoaisAluno(request):
    aluno = Aluno.objects.get(user=request.user)
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
def EnviarProva(request):
    aluno = Aluno.objects.get(user=request.user)

    idDaProva = int(request.POST['idDaProva'])
    prova = Prova.objects.get(id=idDaProva)

    if request.POST['finalizouAProva'] == 'true':
        finalizouAProva = True
    else:
        finalizouAProva = False

    aux = ProvaRealizadaPeloAluno.objects
    if aux.filter(aluno_id=aluno.id, prova_id=idDaProva).exists():
        provaRealizada = aux.get(aluno=aluno, prova=prova)
    else:
        provaRealizada = ProvaRealizadaPeloAluno()

    provaRealizada.aluno = aluno
    provaRealizada.prova = prova
    provaRealizada.finalizouAProva = finalizouAProva
    provaRealizada.save()

    provaSerializada = json.loads(request.POST['provaSerializada'])

    if not QuestaoDaProvaRealizadaPeloAluno.objects.filter(provaRealizada=provaRealizada).exists():
        for respostaDeQuestao in provaSerializada:
            criarQuestaoRealizadaESalvarNaProvaRealizada(
                respostaDeQuestao, provaRealizada)

    else:
        questoesRealizadas = QuestaoDaProvaRealizadaPeloAluno.objects.filter(
            provaRealizada=provaRealizada).all()

        for respostaDeQuestao in provaSerializada:
            questaoJaRespondidaAnteriormente = False

            for questaoRealizada in questoesRealizadas:
                if questaoRealizada.questaoCorrespondente.id == int(respostaDeQuestao['name'][27:]):
                    questaoJaRespondidaAnteriormente = True
                    editarQuestaoRealizadaAnteriormente(
                        respostaDeQuestao, questaoRealizada)

            if questaoJaRespondidaAnteriormente == False:
                criarQuestaoRealizadaESalvarNaProvaRealizada(
                    respostaDeQuestao, provaRealizada)

    if provaRealizada.finalizouAProva:
        gerarBoletimDeDesempenho(
            aluno=aluno, materia=prova.materia, prova=prova, provaRealizada=provaRealizada)

    return redirect('/')


def gerarBoletimDeDesempenho(aluno, materia, prova, provaRealizada):
    boletimDeDesempenhoDoAluno = BoletimDeDesempenhoDoAluno()
    boletimDeDesempenhoDoAluno.aluno = aluno
    boletimDeDesempenhoDoAluno.materia = materia
    boletimDeDesempenhoDoAluno.provaRealizada = provaRealizada

    provaRealizadaDestamateria = ProvaRealizadaPeloAluno.objects.get(
        prova=prova, aluno=aluno)

    quantidadeDeAcertosDoAluno = QuestaoDaProvaRealizadaPeloAluno.objects.filter(
        provaRealizada=provaRealizadaDestamateria, acertouAQuestao=True).count()

    if quantidadeDeAcertosDoAluno != 0:
        quantidadeDeQuestoesNaProva = Questao.objects.filter(
            prova=prova).count()
        notaFinal = float(quantidadeDeAcertosDoAluno /
                          quantidadeDeQuestoesNaProva) * 10
    else:
        notaFinal = 0
    boletimDeDesempenhoDoAluno.nota = notaFinal

    if notaFinal >= 6:
        boletimDeDesempenhoDoAluno.aprovado = True
    else:
        boletimDeDesempenhoDoAluno.aprovado = False

    boletimDeDesempenhoDoAluno.save()
