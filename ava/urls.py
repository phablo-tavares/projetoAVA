from django.urls import include, path
from ava.views import Dashboard, CardMateriasDoCurso, CardCursosMatriculados, CardMateriaisDaMateria, CardProva, EnviarProva, CardBoletimDeDesempenho, CardFinanceiro, CardEditarDadosPessoais, SalvarDadosPessoaisAluno
urlpatterns = [
    path('ava',  Dashboard),
    path('card-cursos-matriculados', CardCursosMatriculados),
    path('card-materias-do-curso', CardMateriasDoCurso),
    path('card-materiais-da-materia', CardMateriaisDaMateria),
    path('card-prova', CardProva),
    path('enviar-prova', EnviarProva),

    path('card-boletim-de-desempenho', CardBoletimDeDesempenho),
    path('card-financeiro', CardFinanceiro),

    path('card-editar-dados-pessoais', CardEditarDadosPessoais),
    path('salvar-dados-pessoais-aluno', SalvarDadosPessoaisAluno),


]
