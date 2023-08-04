from django.contrib import admin
from .models import Aluno, Curso, Materia, MateriaDoCurso, Matricula, Prova, Material, Questao, ProvaRealizadaPeloAluno, QuestaoDaProvaRealizadaPeloAluno, BoletimDeDesempenhoDoAluno

# Register your models here.
admin.site.register(Aluno)
admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(MateriaDoCurso)
admin.site.register(Matricula)
admin.site.register(Prova)
admin.site.register(Material)
admin.site.register(Questao)
admin.site.register(ProvaRealizadaPeloAluno)
admin.site.register(QuestaoDaProvaRealizadaPeloAluno)
admin.site.register(BoletimDeDesempenhoDoAluno)
