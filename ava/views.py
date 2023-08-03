from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso, Material, Prova, Questao, ProvaRealizadaPeloAluno, QuestaoDaProvaRealizadaPeloAluno
from myProject.util import CursosEmQueOAlunoEstaMatriculado
from django.core.files.storage import FileSystemStorage
import json

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

    k = 0
    provaSerializada = json.loads(request.POST['provaSerializada'])
    alternativaEscolhidaEmCadaQuestao = []
    for i in range(0, len(provaSerializada), 31):
        j = i+30
        alternativaEscolhidaEmCadaQuestao.append(provaSerializada[i:j])

        questaoRealizada = QuestaoDaProvaRealizadaPeloAluno()
        questaoRealizada.provaRealizada = provaRealizada

        alternativaEscolhida = int(alternativaEscolhidaEmCadaQuestao[k][-1])
        questaoRealizada.alternativaEscolhida = alternativaEscolhida

        idQuestaoCorrespondente = int(alternativaEscolhidaEmCadaQuestao[k][-3])
        questaoCorrespondente = Questao.objects.get(id=idQuestaoCorrespondente)
        questaoRealizada.questaoCorrespondente = questaoCorrespondente

        if questaoRealizada.alternativaEscolhida == questaoCorrespondente.alternativaCorreta:
            questaoRealizada.acertouAQuestao = True

        questaoRealizada.save()
        k += 1

    if not QuestaoDaProvaRealizadaPeloAluno.objects.filter(provaRealizada=provaRealizada).exists():
        for respostaDeQuestao in provaSerializada:
            questaoRealizada = QuestaoDaProvaRealizadaPeloAluno()
            questaoRealizada.provaRealizada = provaRealizada

            alternativaEscolhida = int(respostaDeQuestao['value'])
            questaoRealizada.alternativaEscolhida = alternativaEscolhida

            idQuestaoCorrespondente = respostaDeQuestao['name'][-1]
            questaoCorrespondente = Questao.objects.get(id=idQuestaoCorrespondente)
            questaoRealizada.questaoCorrespondente = questaoCorrespondente

            if questaoRealizada.alternativaEscolhida == questaoCorrespondente.alternativaCorreta
                questaoRealizada.acertouAQuestao == True

            questaoRealizada.save()
    
    else: #finalizar essa lógica
        for respostaDeQuestao in provaSerializada:
            for questaoRealizada in QuestaoDaProvaRealizadaPeloAluno.objects.get(provaRealizada=provaRealizada):
                if questaoRealizada.que:
                    pass

    return redirect('/')
