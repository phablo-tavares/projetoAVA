
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso,Questao,QuestaoDaProvaRealizadaPeloAluno


def CursosEmQueOAlunoEstaMatriculado(aluno):
    matriculasDoAluno = Matricula.objects.filter(aluno=aluno).prefetch_related(
        'aluno_id').prefetch_related('curso_id').values()

    cursosMatriculados = []
    for matricula in matriculasDoAluno:
        cursosMatriculados.append(
            Curso.objects.get(id=matricula['curso_id']))

    return cursosMatriculados

def editarQuestaoRealizadaAnteriormente(respostaDeQuestao, questaoRealizada):
    alternativaEscolhida = int(respostaDeQuestao['value'])
    questaoRealizada.alternativaEscolhida = alternativaEscolhida

    if questaoRealizada.alternativaEscolhida == questaoRealizada.questaoCorrespondente.alternativaCorreta:
        questaoRealizada.acertouAQuestao == True
    else:
        questaoRealizada.acertouAQuestao == False

    questaoRealizada.save()


def criarQuestaoRealizadaESalvarNaProvaRealizada(respostaDeQuestao, provaRealizada):
    questaoRealizada = QuestaoDaProvaRealizadaPeloAluno()
    questaoRealizada.provaRealizada = provaRealizada

    alternativaEscolhida = int(respostaDeQuestao['value'])
    questaoRealizada.alternativaEscolhida = alternativaEscolhida

    idQuestaoCorrespondente = int(respostaDeQuestao['name'][27:])
    questaoCorrespondente = Questao.objects.get(
        id=idQuestaoCorrespondente)
    questaoRealizada.questaoCorrespondente = questaoCorrespondente

    if questaoRealizada.alternativaEscolhida == questaoCorrespondente.alternativaCorreta:
        questaoRealizada.acertouAQuestao == True
    else:
        questaoRealizada.acertouAQuestao == False

    questaoRealizada.save()
