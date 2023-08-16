
from ava.models import Aluno, Matricula, Curso, Materia, MateriaDoCurso, Questao, ProvaRealizadaPeloAluno, QuestaoDaProvaRealizadaPeloAluno, BoletimDeDesempenhoDoAluno, Parcela


def CursosEmQueOAlunoEstaMatriculado(aluno):
    matriculasDoAluno = Matricula.objects.filter(aluno=aluno).prefetch_related(
        'aluno_id').prefetch_related('curso_id').values()

    cursosMatriculados = []
    for matricula in matriculasDoAluno:
        cursosMatriculados.append(
            Curso.objects.get(id=matricula['curso_id']))

    return cursosMatriculados


def MateriasDeUmCurso(curso):
    idDasMateriasDoCurso = MateriaDoCurso.objects.filter(curso=curso).prefetch_related(
        'materia_id').values()

    materiasDoCurso = []
    for idMateria in idDasMateriasDoCurso:
        materiasDoCurso.append(
            Materia.objects.get(id=idMateria['materia_id']))

    return materiasDoCurso


def editarQuestaoRealizadaAnteriormente(respostaDeQuestao, questaoRealizada):
    alternativaEscolhida = int(respostaDeQuestao['value'])
    questaoRealizada.alternativaEscolhida = alternativaEscolhida

    if questaoRealizada.alternativaEscolhida == questaoRealizada.questaoCorrespondente.alternativaCorreta:
        questaoRealizada.acertouAQuestao = True
    else:
        questaoRealizada.acertouAQuestao = False

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
        questaoRealizada.acertouAQuestao = True
    else:
        questaoRealizada.acertouAQuestao = False

    questaoRealizada.save()


def gerarDadosBoletimDeDesempenhoDeUmAluno(aluno):
    cursosMatriculados = CursosEmQueOAlunoEstaMatriculado(aluno=aluno)

    dadosBoletimDeDesempenho = []
    if cursosMatriculados == []:
        dadosBoletimDeDesempenho = None
    else:
        for curso in cursosMatriculados:
            curso.boletins = []
            materiasDoCurso = MateriasDeUmCurso(curso)
            if materiasDoCurso == []:
                curso.boletins = None
            else:
                for materia in materiasDoCurso:
                    boletinsDoAlunoNestaMateria = BoletimDeDesempenhoDoAluno.objects.filter(
                        aluno=aluno, materia=materia).all()
                    curso.boletins.extend(boletinsDoAlunoNestaMateria)
                if curso.boletins == []:
                    curso.boletins = None
            dadosBoletimDeDesempenho.append(curso)

    return dadosBoletimDeDesempenho


def gerarDadosFinanceirosDoAluno(aluno):
    cursosMatriculados = CursosEmQueOAlunoEstaMatriculado(aluno=aluno)

    dadosFinanceirosDoAluno = []
    if cursosMatriculados == []:
        dadosFinanceirosDoAluno = None
    else:
        for curso in cursosMatriculados:
            curso.parcelas = []
            parcelasDoAlunoNesteCurso = Parcela.objects.filter(
                aluno=aluno, curso=curso).all()
            curso.parcelas.extend(parcelasDoAlunoNesteCurso)
            if curso.parcelas == []:
                curso.parcelas = None
            dadosFinanceirosDoAluno.append(curso)

    return dadosFinanceirosDoAluno


def dadosParaRenderizarAProvaRealizadaPeloAluno(prova, questoes, aluno):
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
    dados = {
        'provaRealizadaPeloAluno': provaRealizadaPeloAluno,
        'questoesDaProvaRealizadaPeloAluno': questoesDaProvaRealizadaPeloAluno,
    }
    return dados
