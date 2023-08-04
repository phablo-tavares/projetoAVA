from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso, Material, Prova, Questao, ProvaRealizadaPeloAluno, QuestaoDaProvaRealizadaPeloAluno, BoletimDeDesempenhoDoAluno
from myProject.util import CursosEmQueOAlunoEstaMatriculado, editarQuestaoRealizadaAnteriormente, criarQuestaoRealizadaESalvarNaProvaRealizada
from django.core.files.storage import FileSystemStorage
import json
from django.db.models import Sum

# Create your views here.


def Dashboard(request):
    # OBTEM O USUÁRIO DA INSTANCIA
    userAuth = request.user

    # BUSCA O ID DO USUÁRIO DA INSTANCIA
    # idAuthUser = User.objects.filter(username=userAuth).values()
    # idAuthUser = idAuthUser[0]['id']

    # BUSCA INFORMAÇÕES DO USUÁRIO
    aluno = Aluno.objects.get(user=userAuth)

    context = {
        'aluno': aluno,
    }
    return render(request, 'ava.html', context)


def CardCursosMatriculados(request):
    idDoAluno = request.GET['id']
    aluno = Aluno.objects.get(user=request.user)
    cursosMatriculados = CursosEmQueOAlunoEstaMatriculado(aluno=aluno)
    urlMateriasDoCurso = "/card-materias-do-curso"

    context = {'aluno': aluno, 'cursosMatriculados': cursosMatriculados,
               'urlMateriasDoCurso': urlMateriasDoCurso}
    return render(request, 'cardCursosMatriculados.html', context)


def CardMateriasDoCurso(request):
    idCurso = request.GET['id']
    curso = Curso.objects.get(id=idCurso)

    idDasMateriasDoCurso = MateriaDoCurso.objects.filter(curso=curso).prefetch_related(
        'materia_id').values()

    materiasDoCurso = []
    for idMateria in idDasMateriasDoCurso:
        materiasDoCurso.append(
            Materia.objects.get(id=idMateria['materia_id']))

    urlMateriaisDaMateria = "/card-materiais-da-materia"
    urlCursosMatriculados = "/card-cursos-matriculados"

    context = {'curso': curso, 'materiasDoCurso': materiasDoCurso,
               'urlMateriaisDaMateria': urlMateriaisDaMateria, 'urlCursosMatriculados': urlCursosMatriculados}
    return render(request, 'cardMateriasDoCurso.html', context)


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


def CardProva(request):
    idDaProva = request.GET['id']
    prova = Prova.objects.get(id=idDaProva)
    questoes = Questao.objects.filter(prova=prova)

    materia = Materia.objects.get(id=prova.materia.id)

    urlMateriaisDaMateria = "/card-materiais-da-materia"

    aluno = Aluno.objects.get(user=request.user)
    try:
        provaRealizadaPeloAluno = ProvaRealizadaPeloAluno.objects.get(
            aluno_id=aluno.id, prova_id=prova.id)
        try:
            questoesDaProvaRealizadaPeloAluno = QuestaoDaProvaRealizadaPeloAluno.objects.filter(
                provaRealizada=provaRealizadaPeloAluno)
        except:
            questoesDaProvaRealizadaPeloAluno = None
    except:
        provaRealizadaPeloAluno = None
        questoesDaProvaRealizadaPeloAluno = None

    if questoesDaProvaRealizadaPeloAluno is not None:
        for questaoDaProvaRealizadaPeloAluno in questoesDaProvaRealizadaPeloAluno:
            for questao in questoes:
                if questaoDaProvaRealizadaPeloAluno.questaoCorrespondente == questao:
                    if questaoDaProvaRealizadaPeloAluno.alternativaEscolhida == 1:
                        questao.alternativa1foiSelecionada = True
                    elif questaoDaProvaRealizadaPeloAluno.alternativaEscolhida == 2:
                        questao.alternativa2foiSelecionada = True
                    elif questaoDaProvaRealizadaPeloAluno.alternativaEscolhida == 3:
                        questao.alternativa3foiSelecionada = True
                    elif questaoDaProvaRealizadaPeloAluno.alternativaEscolhida == 4:
                        questao.alternativa4foiSelecionada = True

    context = {'prova': prova, 'questoes': questoes, 'materia': materia, 'urlMateriaisDaMateria': urlMateriaisDaMateria,
               'provaRealizadaPeloAluno': provaRealizadaPeloAluno, 'questoesDaProvaRealizadaPeloAluno': questoesDaProvaRealizadaPeloAluno}
    return render(request, 'cardProva.html', context)


def EnviarProva(request):
    aluno = Aluno.objects.get(user=request.user)

    idDaProva = int(request.POST['idDaProva'])
    prova = Prova.objects.get(id=idDaProva)

    if request.POST['finalizouAProva'] == 'true':
        finalizouAProva = True
    else:
        finalizouAProva = False

    if ProvaRealizadaPeloAluno.objects.filter(
            aluno_id=aluno.id, prova_id=idDaProva).exists():
        provaRealizada = ProvaRealizadaPeloAluno.objects.get(
            aluno=aluno, prova=prova)
        provaRealizada.aluno = aluno
        provaRealizada.prova = prova
        provaRealizada.finalizouAProva = finalizouAProva
        provaRealizada.save()
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
            aluno=aluno, materia=prova.materia, prova=prova)

    return redirect('/')


# finalizar essa parte
def gerarBoletimDeDesempenho(aluno, materia, prova):
    boletimDeDesempenhoDoAluno = BoletimDeDesempenhoDoAluno()

    boletimDeDesempenhoDoAluno.aluno = aluno

    boletimDeDesempenhoDoAluno.materia = materia

    provaRealizadaDestamateria = ProvaRealizadaPeloAluno.objects.get(
        prova=prova, aluno=aluno)
    filtroQuestoesRealizadas = QuestaoDaProvaRealizadaPeloAluno.objects.filter(
        provaRealizada=provaRealizadaDestamateria)
    quantidadeDeAcertosDoAluno = filtroQuestoesRealizadas.aggregate(
        Sum('acertouAQuestao'))
    quantidadeDeQuestoesNaProva = Questao.objects.filter(prova=prova).count()
    notaFinal = float(quantidadeDeQuestoesNaProva/quantidadeDeAcertosDoAluno)
