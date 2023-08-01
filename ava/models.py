from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Aluno(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    rg = models.CharField(max_length=7)
    email = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    sexo = models.CharField(max_length=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'alunos'


class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'cursos'


class Materia(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'materias'


class MateriaDoCurso(models.Model):
    id = models.AutoField(primary_key=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'Matérias dos cursos'


class Matricula(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'matriculas'




class Material(models.Model):
    id = models.AutoField(primary_key=True)
    nomeDoMaterial = models.CharField(max_length=255)
    anexo = models.FileField(upload_to='anexos')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomeDoMaterial

    class Meta:
        db_table = 'materiais'


class PermissaoRealizarProva(models.Model):
    class Meta:
        permissions = [("podeFazerProvas", "aluno pode realizar a prova")]


class Prova(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    materia = models.OneToOneField(Materia, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'provas'


class Questao(models.Model):
    id = models.AutoField(primary_key=True)
    enunciado = models.CharField(max_length=255)
    alternativa1 = models.CharField(max_length=255)
    alternativa2 = models.CharField(max_length=255)
    alternativa3 = models.CharField(max_length=255)
    alternativa4 = models.CharField(max_length=255)
    alternativaCorreta = models.IntegerField()
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)

    def __str__(self):
        return self.enunciado

    class Meta:
        db_table = 'questoes'


class ProvaRealizadaPeloAluno(models.Model):
    id = models.AutoField(primary_key=True)
    prova = models.ForeignKey(Prova,on_delete=models.DO_NOTHING)
    aluno = models.ForeignKey(Aluno,on_delete=models.DO_NOTHING)
    finalizouAProva = models.BooleanField(default=False)

    def __str__(self):
        return f'prova {self.prova.nome} realizada pelo aluno {self.aluno.nome}'
    
    class Meta:
        db_table = 'provas realizadas pelos alunos'


class QuestaoDaProvaRealizadaPeloAluno(models.Model):
    id = models.AutoField(primary_key=True)
    provaRealizada = models.ForeignKey(ProvaRealizadaPeloAluno,on_delete=models.CASCADE)
    questaoCorrespondente = models.ForeignKey(Questao,on_delete=models.DO_NOTHING)
    alternativaEscolhida = models.IntegerField()
    acertouAQuestao = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        db_table = 'questões das provas realizadas pelos alunos'

