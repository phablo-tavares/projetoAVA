from django.urls import include, path

from ava_administrativo.views import Dashboard, CardGerenciarAlunos, ExcluirAluno, CardVisualizarDadosDoAluno, CardProvaAdministrativo, CardEditarDadosPessoaisDeUmAluno, SalvarDadosPessoaisDeUmAluno, PermitirQueOAlunoRefacaUmaProva

urlpatterns = [
    path('ava_administrativo',  Dashboard),
    path('card-gerenciar-alunos',  CardGerenciarAlunos),
    path('card-visualizar-dados-do-aluno',  CardVisualizarDadosDoAluno),
    path('card-prova-administrativo',  CardProvaAdministrativo),

    path('excluir-aluno',  ExcluirAluno),

    path('card-editar-dados-pessoais-de-um-aluno',
         CardEditarDadosPessoaisDeUmAluno),
    path('salvar-dados-pessoais-de-um-aluno', SalvarDadosPessoaisDeUmAluno),
    path('permitir-refazer-uma-prova', PermitirQueOAlunoRefacaUmaProva),
]
