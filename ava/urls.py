from django.urls import include, path
from ava.views import Dashboard, CardMateriasDoCurso, CardCursosMatriculados, CardMateriaisDaMateria
urlpatterns = [
    path('ava',  Dashboard),
    path('card-cursos-matriculados',  CardCursosMatriculados),
    path('card-materias-do-curso',  CardMateriasDoCurso),
    path('card-materiais-da-materia',  CardMateriaisDaMateria),


]
