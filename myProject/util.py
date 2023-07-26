
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso


def CursosEmQueOAlunoEstaMatriculado(aluno):
    matriculasDoAluno = Matricula.objects.filter(aluno=aluno).prefetch_related(
        'aluno_id').prefetch_related('curso_id').values()

    cursosMatriculados = []
    for matricula in matriculasDoAluno:
        cursosMatriculados.append(
            Curso.objects.get(id=matricula['curso_id']))

    return cursosMatriculados
