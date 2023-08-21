from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from ava.models import Aluno, Curso, ProvaRealizadaPeloAluno, Prova, Questao, Materia, Material, MateriaDoCurso, BoletimDeDesempenhoDoAluno
from ava.views import CardFinanceiro, CardBoletimDeDesempenho
import json
from django.http import JsonResponse
from ava.util.util import gerarDadosBoletimDeDesempenhoDeUmAluno, gerarDadosFinanceirosDoAluno, dadosParaRenderizarAProvaRealizadaPeloAluno, CursosEmQueOAlunoEstaMatriculado, MateriasDeUmCurso
from django.core.files.storage import FileSystemStorage


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


@login_required(login_url="/")
def Dashboard(request):
    userAuth = request.user

    context = {
        'user': userAuth,
        'urlCardGerenciarAlunos': '/card-gerenciar-alunos',
        'urlCardGerenciarCursos': '/card-gerenciar-cursos',
        'urlCardGerenciarMaterias': '/card-gerenciar-materias',
    }

    return render(request, 'ava_administrativo.html', context)


#############################################
#######  Views relacionadas a alunos  #######
#############################################

@login_required(login_url="/")
def CardGerenciarAlunos(request):

    if Aluno.objects.exists():
        alunos = Aluno.objects.all()
    else:
        alunos = None

    context = {
        'alunos': alunos,
        'urlCardGerenciarAlunos': '/card-gerenciar-alunos',
        'urlExcluirAluno': '/excluir-aluno',
        'urlCardVisualizarDadosDoAluno': '/card-visualizar-dados-do-aluno',
        'urlCardVisualizarDadosDoAluno': '/card-visualizar-dados-do-aluno',
        'urlCardEditarDadosPessoaisDeUmAluno': '/card-editar-dados-pessoais-de-um-aluno',
    }
    return render(request, 'templates relacionados a alunos/cardGerenciarAlunos.html', context)


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
    return render(request, 'templates relacionados a alunos/cardVisualizarDadosDoAluno.html', context)


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
    return render(request, 'templates relacionados a alunos/cardProvaAdministrativo.html', context)


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
    return render(request, 'templates relacionados a alunos/cardEditarDadosPessoaisDeUmAluno.html', context)


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


#############################################
#######  Views relacionadas a cursos  #######
#############################################

@login_required(login_url="/")
def CardGerenciarCursos(request):

    if Curso.objects.exists():
        cursos = Curso.objects.all()
    else:
        cursos = None

    context = {
        'cursos': cursos,
        'urlCriarUmNovoCurso': '/card-criar-novo-curso',
        'urlCardEditarDadosDeUmCurso': '/card-editar-dados-do-curso',
        'urlExcluirCurso': '/excluir-curso',
        'urlCardGerenciarCursos': '/card-gerenciar-cursos',
    }
    return render(request, 'templates relacionados a cursos/cardGerenciarCursos.html', context)


@login_required(login_url="/")
def CardCriarUmNovoCurso(request):
    context = {
        'urlCardGerenciarCursos': '/card-gerenciar-cursos',
        'urlSalvarCurso': '/salvar-curso',
    }
    return render(request, 'templates relacionados a cursos/cardCriarNovoCurso.html', context)


@login_required(login_url="/")
def CardEditarDadosDeUmCurso(request):
    idDoCurso = request.GET['id']
    curso = Curso.objects.get(id=idDoCurso)
    context = {
        'curso': curso,
        'urlCardGerenciarCursos': '/card-gerenciar-cursos',
        'urlSalvarCurso': '/salvar-curso',
    }
    return render(request, 'templates relacionados a cursos/cardEditarDadosDeUmCurso.html', context)


@login_required(login_url="/")
def SalvarCurso(request):
    if 'idDoCurso' in request.POST:
        curso = Curso.objects.get(id=request.POST['idDoCurso'])
    else:
        curso = Curso()

    dadosCursoSerializado = json.loads(request.POST['dadosCursoSerializado'])

    for dado in dadosCursoSerializado:
        if dado['name'] == 'nomeDoCurso':
            curso.nome = dado['value']

    curso.save()

    return JsonResponse(json.dumps(curso.nome, indent=4, cls=CustomEncoder), safe=False)


@login_required(login_url="/")
def ExcluirCurso(request):
    id = request.POST['id']
    Curso.objects.get(id=id).delete()


#############################################
######  Views relacionadas a materias  ######
#############################################
@login_required(login_url="/")
def CardGerenciarMaterias(request):

    if Materia.objects.exists():
        materias = Materia.objects.all()
    else:
        materias = None

    context = {
        'materias': materias,
        'urlCriarUmaNovaMateria': '/card-criar-nova-materia',
        'urlExcluirMateria': '/excluir-materia',
        'urlCardGerenciarMaterias': '/card-gerenciar-materias',
        'urlCardEditarDadosDeUmaMateria': '/card-editar-dados-da-materia',
        'urlMateriaisDeUmaMateria': '/card-materiais-de-uma-materia',
        'urlCardCadastrarProva': '/card-cadastrar-prova',
        'urlCardVisualizarProva': '/card-visualizar-prova',
    }
    return render(request, 'templates relacionados a materias/cardGerenciarMaterias.html', context)


@login_required(login_url="/")
def CardCriarUmaNovaMateria(request):
    if Curso.objects.exists():
        cursos = Curso.objects.all()
    else:
        cursos = None
    context = {
        'cursos': cursos,
        'urlCardGerenciarMaterias': '/card-gerenciar-materias',
        'urlSalvarMateria': '/salvar-materia',
    }
    return render(request, 'templates relacionados a materias/cardCriarUmaNovaMateria.html', context)


@login_required(login_url="/")
def CardEditarDadosDeUmaMateria(request):
    idDaMateria = request.GET['id']
    materia = Materia.objects.get(id=idDaMateria)

    if Curso.objects.exists():
        cursos = Curso.objects.all()
        for curso in cursos:
            if MateriaDoCurso.objects.filter(materia=materia, curso=curso).exists():
                curso.AMateriaEstaPresenteNesteCurso = True
    else:
        cursos = None

    context = {
        'materia': materia,
        'cursos': cursos,
        'urlCardGerenciarMaterias': '/card-gerenciar-materias',
        'urlSalvarMateria': '/salvar-materia',
    }
    return render(request, 'templates relacionados a materias/cardEditarDadosDeUmaMateria.html', context)


@login_required(login_url="/")
def SalvarMateria(request):
    if 'idDaMateria' in request.POST:
        materia = Materia.objects.get(id=request.POST['idDaMateria'])
    else:
        materia = Materia()
        materia.nome = ""
        materia.save()

    dadosMateriaSerializado = json.loads(
        request.POST['dadosMateriaSerializado'])

    for dado in dadosMateriaSerializado:
        if dado['name'] == 'nomeDaMateria':
            materia.nome = dado['value']

        if dado['name'] == 'cursosParaCadastrarNaMateria' and dado['value'] is not []:
            idCursos = dado['value']
            materiasDoCurso = MateriaDoCurso.objects.filter(
                materia_id=materia.id).all()
            for materiaDoCurso in materiasDoCurso:
                tem = False
                for id in idCursos:
                    if int(id) == materiaDoCurso.curso.id:
                        tem = True
                if not tem:
                    materiaDoCurso.delete()

            for id in idCursos:
                if not MateriaDoCurso.objects.filter(materia_id=materia.id, curso_id=int(id)).exists():
                    materiaDoCurso = MateriaDoCurso()
                    materiaDoCurso.materia = materia
                    materiaDoCurso.curso = Curso.objects.get(id=int(id))
                    materiaDoCurso.save()

    materia.save()

    return JsonResponse(json.dumps(materia.nome, indent=4, cls=CustomEncoder), safe=False)


@login_required(login_url="/")
def CardMateriaisDeUmaMateria(request):
    idMateria = request.GET['id']
    materia = Materia.objects.get(id=idMateria)
    if Material.objects.filter(materia_id=idMateria).exists():
        materiais = Material.objects.filter(materia_id=idMateria)
    else:
        materiais = None
    context = {
        'materiais': materiais,
        'materia': materia,
        'urlCardGerenciarMaterias': '/card-gerenciar-materias',
        'urlExcluirMaterial': '/excluir-material',
        'urlMateriaisDeUmaMateria': '/card-materiais-de-uma-materia',
        'urlEnviarMaterial': '/salvar-material',
    }
    return render(request, 'templates relacionados a materias/cardMateriaisDeUmaMateria.html', context)


@login_required(login_url="/")
def SalvarMaterial(request):
    material = request.FILES['file']
    fs1 = FileSystemStorage()
    filename = fs1.save(material.name, material)
    urlMaterial = fs1.url(filename)
    idMateria = int(request.POST['idMateria'])
    materia = Materia.objects.get(id=idMateria)

    material = Material.objects.create(nomeDoMaterial=filename,
                                       anexo=urlMaterial, materia=materia)
    material.save()
    return redirect('/')


@login_required(login_url="/")
def ExcluirMateria(request):
    id = request.POST['id']
    Materia.objects.get(id=id).delete()
    return redirect('/')


@login_required(login_url="/")
def ExcluirMaterial(request):
    id = request.POST['id']
    Material.objects.get(id=id).delete()
    return redirect('/')


@login_required(login_url="/")
def CardCadastrarProva(request):
    id = request.GET['id']
    materia = Materia.objects.get(id=id)

    context = {
        'materia': materia,
        'urlCardGerenciarMaterias': '/card-gerenciar-materias',
        'urlCriarProva': '/criar-prova',
    }

    return render(request, 'templates relacionados a materias/cardCadastrarProva.html', context)


@login_required(login_url="/")
def CriarProva(request):
    dadosProvaSerializado = json.loads(request.POST['dadosProvaSerializado'])
    quantidadeDeQuestoes = int((len(dadosProvaSerializado) - 1)/6)

    questoes = []
    for i in range(quantidadeDeQuestoes):
        questao = Questao()
        questoes.append(questao)

    prova = Prova()
    prova.nome = dadosProvaSerializado[0]['value']
    prova.materia = Materia.objects.get(id=int(request.POST['idDaMateria']))
    prova.save()

    dadosProvaSerializado = dadosProvaSerializado[1:]
    for i in range(quantidadeDeQuestoes):
        inicio = i * 6
        fim = (i + 1) * 6
        dadosQuestao = dadosProvaSerializado[inicio:fim]
        questao = questoes[i]
        questao.enunciado = dadosQuestao[0]['value']
        questao.alternativa1 = dadosQuestao[1]['value']
        questao.alternativa2 = dadosQuestao[2]['value']
        questao.alternativa3 = dadosQuestao[3]['value']
        questao.alternativa4 = dadosQuestao[4]['value']
        questao.alternativaCorreta = int(dadosQuestao[5]['value'])
        questao.prova = prova
        questao.save()

    return JsonResponse(json.dumps(prova.nome, indent=4, cls=CustomEncoder), safe=False)


@login_required(login_url="/")
def cardVisualizarProva(request):
    idDaMateria = request.GET['id']
    materia = Materia.objects.get(id=idDaMateria)
    prova = Prova.objects.get(materia=materia)
    questoes = Questao.objects.filter(prova=prova)

    context = {
        'materia': materia,
        'prova': prova,
        'questoes': questoes,
        'urlCardGerenciarMaterias': '/card-gerenciar-materias',
        'urlExcluirProva': '/excluir-prova',
    }
    return render(request, 'templates relacionados a materias/cardVisualizarProva.html', context)


@login_required(login_url="/")
def ExcluirProva(request):
    id = request.POST['id']
    Prova.objects.get(id=id).delete()
    return redirect('/')
