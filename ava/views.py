from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso, Material, Prova,Questao,ProvaRealizadaPeloAluno,QuestaoDaProvaRealizadaPeloAluno
from myProject.util import CursosEmQueOAlunoEstaMatriculado
from django.core.files.storage import FileSystemStorage

# Create your views here.


def Dashboard(request):
    # OBTEM O USUÁRIO DA INSTANCIA
    userAuth = request.user

    # BUSCA O ID DO USUÁRIO DA INSTANCIA
    # idAuthUser = User.objects.filter(username=userAuth).values()
    # idAuthUser = idAuthUser[0]['id']

    # BUSCA INFORMAÇÕES DO USUÁRIO
    aluno = Aluno.objects.get(user=userAuth)

    return render(request, 'ava.html',
                  {
                      'aluno': aluno,
                  })


def CardCursosMatriculados(request):
    idDoAluno = request.GET['id']
    aluno = Aluno.objects.get(id=idDoAluno)
    cursosMatriculados = CursosEmQueOAlunoEstaMatriculado(aluno=aluno)
    urlMateriasDoCurso = "/card-materias-do-curso"
    return render(request, 'cardCursosMatriculados.html', {'aluno':aluno,'cursosMatriculados': cursosMatriculados,'urlMateriasDoCurso':urlMateriasDoCurso})


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

    return render(request, 'cardMateriasDoCurso.html', {'curso': curso, 'materiasDoCurso': materiasDoCurso,'urlMateriaisDaMateria':urlMateriaisDaMateria,'urlCursosMatriculados':urlCursosMatriculados})


def CardMateriaisDaMateria(request):
    idDaMateria = request.GET['id']
    materia = Materia.objects.get(id=idDaMateria)
    try:
        prova = Prova.objects.get(materia=materia)
    except:
        prova = None
    materiais = Material.objects.filter(materia_id=idDaMateria)
    urlMateriasDoCurso = "/card-materias-do-curso"
    urlProvas = "/card-prova"

    aluno = Aluno.objects.get(user=request.user)
    alunoJaFinalizouAProva = False
    if ProvaRealizadaPeloAluno.objects.filter(aluno_id=aluno.id , prova_id=prova.id).exists():
        provaRealizadaPeloAluno = ProvaRealizadaPeloAluno.objects.get(aluno_id = aluno.id, prova_id=prova.id)
        alunoJaFinalizouAProva = provaRealizadaPeloAluno.finalizouAProva
            

    return render(request, 'cardMateriaisDaMateria.html', {'materia': materia, 'materiais': materiais, 'prova': prova,'urlMateriasDoCurso':urlMateriasDoCurso,'urlProvas':urlProvas,'alunoJaFinalizouAProva':alunoJaFinalizouAProva})


def CardProva(request):
    idDaProva = request.GET['id']
    prova = Prova.objects.get(id=idDaProva)
    questoes = Questao.objects.filter(prova=prova)

    materia = Materia.objects.get(id=prova.materia.id)
    
    urlMateriaisDaMateria = "/card-materiais-da-materia"

    #finaliar a logica abaixo amanhã
    aluno = Aluno.objects.get(user=request.user)
    try:
        provaRealizadaPeloAluno = ProvaRealizadaPeloAluno.objects.get(aluno_id = aluno.id, prova_id=prova.id)
    except:
        provaRealizadaPeloAluno = None


    return render(request,'cardProva.html',{'prova':prova,'questoes':questoes,'materia':materia,'urlMateriaisDaMateria':urlMateriaisDaMateria,'provaRealizadaPeloAluno':provaRealizadaPeloAluno})


def EnviarProva(request):
    idDoAluno = int(request.POST['idDoAluno'])
    aluno = Aluno.objects.get(id=idDoAluno)

    idDaProva = int(request.POST['idDaProva'])
    prova = Prova.objects.get(id=idDaProva)

    provaSerializada = request.POST['provaSerializada']
    
    if request.POST['finalizouAProva'] == 'true':
        finalizouAProva = True
    else:
        finalizouAProva = False

    if ProvaRealizadaPeloAluno.objects.filter(aluno_id=idDoAluno , prova_id=idDaProva).exists():
        ProvaRealizadaPeloAluno.objects.get(aluno = aluno).delete()
    provaRealizada = ProvaRealizadaPeloAluno()
    provaRealizada.aluno = aluno
    provaRealizada.prova = prova
    provaRealizada.finalizouAProva = finalizouAProva

    provaRealizada.save()

    k=0
    alternativaEscolhidaEmCadaQuestao = []
    for i in range(0,len(provaSerializada),31):
        j=i+30
        alternativaEscolhidaEmCadaQuestao.append(provaSerializada[i:j])

        questaoRealizada = QuestaoDaProvaRealizadaPeloAluno()
        questaoRealizada.provaRealizada = provaRealizada

        alternativaEscolhida = int(alternativaEscolhidaEmCadaQuestao[k][-1])
        questaoRealizada.alternativaEscolhida = alternativaEscolhida

        idQuestaoCorrespondente = int(alternativaEscolhidaEmCadaQuestao[k][-3])
        questaoCorrespondente = Questao.objects.get(id = idQuestaoCorrespondente)
        questaoRealizada.questaoCorrespondente = questaoCorrespondente

        if questaoRealizada.alternativaEscolhida == questaoCorrespondente.alternativaCorreta:
            questaoRealizada.acertouAQuestao = True
        
        questaoRealizada.save()
        k+=1

    return redirect('/')


