from django.shortcuts import render
from django.contrib.auth.models import User
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso, Material, Prova
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
    urlCursosMatriculados = "/card-cursos-matriculados"
    urlMateriasDoCurso = "/card-materias-do-curso"
    urlMateriaisDaMateria = "/card-materiais-da-materia"

    return render(request, 'ava.html',
                  {
                      'aluno': aluno,
                      'urlCursosMatriculados': urlCursosMatriculados,
                      'urlMateriasDoCurso': urlMateriasDoCurso,
                      'urlMateriaisDaMateria': urlMateriaisDaMateria,
                  })


def CardCursosMatriculados(request):
    alunoId = request.GET['alunoId']
    aluno = Aluno.objects.get(id=alunoId)
    cursosMatriculados = CursosEmQueOAlunoEstaMatriculado(aluno=aluno)
    return render(request, 'cardCursosMatriculados.html', {'cursosMatriculados': cursosMatriculados})


def CardMateriasDoCurso(request):
    idCurso = request.GET['idDoCurso']
    curso = Curso.objects.get(id=idCurso)

    idDasMateriasDoCurso = MateriaDoCurso.objects.filter(curso=curso).prefetch_related(
        'materia_id').values()

    materiasDoCurso = []
    for idMateria in idDasMateriasDoCurso:
        materiasDoCurso.append(
            Materia.objects.get(id=idMateria['materia_id']))

    return render(request, 'cardMateriasDoCurso.html', {'curso': curso, 'materiasDoCurso': materiasDoCurso})


def CardMateriaisDaMateria(request):
    idDaMateria = request.GET['idDaMateria']
    materia = Materia.objects.get(id=idDaMateria)
    materiais = Material.objects.filter(materia_id=idDaMateria)
    prova = Prova.objects.get(materia=materia)

    return render(request, 'cardMateriaisDaMateria.html', {'materia': materia, 'materiais': materiais, 'prova': prova})
