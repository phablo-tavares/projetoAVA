from django.urls import include, path
from ava.views import Dashboard, CardMateriasDoCurso, CardCursosMatriculados, CardMateriaisDaMateria,CardProva,EnviarProva
urlpatterns = [
    path('ava',  Dashboard),
    path('card-cursos-matriculados', CardCursosMatriculados),
    path('card-materias-do-curso', CardMateriasDoCurso),
    path('card-materiais-da-materia', CardMateriaisDaMateria),
    path('card-prova', CardProva),
    path('enviar-prova', EnviarProva),


]
