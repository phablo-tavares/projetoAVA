from django.contrib import admin
from .models import Aluno, Curso, Materia, MateriaDoCurso, Matricula

# Register your models here.
admin.site.register(Aluno)
admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(MateriaDoCurso)
admin.site.register(Matricula)
