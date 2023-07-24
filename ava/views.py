from django.shortcuts import render
from django.contrib.auth.models import User
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso
from myProject.util import CursosEmQueOAlunoEstaMatriculado

# Create your views here.


def Dashboard(request):
    # OBTEM O USUÁRIO DA INSTANCIA
    userAuth = request.user

    # BUSCA O ID DO USUÁRIO DA INSTANCIA
    idAuthUser = User.objects.filter(username=userAuth).values()
    idAuthUser = idAuthUser[0]['id']

    # BUSCA INFORMAÇÕES DO USUÁRIO
    aluno = Aluno.objects.get(user=userAuth)
    cursosMatriculados = CursosEmQueOAlunoEstaMatriculado(aluno=aluno)

    return render(request, 'ava.html', {'aluno': aluno, 'cursosMatriculados': cursosMatriculados})


def CardMateriasDoCurso(request):
    idCurso = request.POST['idDoCurso']
    curso = Curso.objects.get(id=idCurso)

    idDasMateriasDoCurso = MateriaDoCurso.objects.filter(curso=curso).prefetch_related(
        'materia_id').values()

    materiasDoCurso = []
    for idMateria in idDasMateriasDoCurso:
        materiasDoCurso.append(
            Materia.objects.get(id=idMateria['materia_id']))

    return render(request, 'cardMateriasDoCurso.html', {'curso': curso, 'materiasDoCurso': materiasDoCurso})


def CardCursosMatriculados(request):
    alunoId = request.GET['alunoId']
    aluno = Aluno.objects.get(id=alunoId)
    cursosMatriculados = CursosEmQueOAlunoEstaMatriculado(aluno=aluno)
    return render(request, 'cardCursosMatriculados.html', {'cursosMatriculados': cursosMatriculados})
