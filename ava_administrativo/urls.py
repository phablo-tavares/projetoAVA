from django.urls import include, path

from ava_administrativo.views import Dashboard, CardGerenciarAlunos, ExcluirAluno, CardVisualizarDadosDoAluno

urlpatterns = [
    path('ava_administrativo',  Dashboard),
    path('card-gerenciar-alunos',  CardGerenciarAlunos),
    path('card-visualizar-dados-do-aluno',  CardVisualizarDadosDoAluno),

    path('excluir-aluno',  ExcluirAluno),
]
