from django import forms
from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Aluno(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11)
    rg = models.CharField(max_length=7)
    email = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    sexo = models.CharField(max_length=1)
    notificacao = models.CharField(max_length=510, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
        return f'cadastro da materia {self.materia.nome} no curso {self.curso.nome}'

    class Meta:
        db_table = 'Matérias dos cursos'


class Matricula(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return f'matricula do aluno {self.aluno.nome} no curso {self.curso.nome}'

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


class Permissioes(models.Model):
    class Meta:
        permissions = [
            ("podeFazerProvas", "aluno pode realizar a prova"),
            ("ehAdministrador", "usuário logado é administrador"),
            ("ehAluno", "usuário logado é aluno"),
        ]


class Prova(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    materia = models.OneToOneField(Materia, on_delete=models.CASCADE)

    def __str__(self):
        return f'nome da prova: {self.nome}. Materia: {self.materia.nome}'

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
        return f'questao de id {self.id} da prova: {self.prova.nome}'

    class Meta:
        db_table = 'questoes'


class ProvaRealizadaPeloAluno(models.Model):
    id = models.AutoField(primary_key=True)
    prova = models.ForeignKey(Prova, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    finalizouAProva = models.BooleanField(default=False)

    def __str__(self):
        return f'prova: {self.prova.nome}, realizada pelo aluno: {self.aluno.nome}'

    class Meta:
        db_table = 'provas realizadas pelos alunos'


class QuestaoDaProvaRealizadaPeloAluno(models.Model):
    id = models.AutoField(primary_key=True)
    provaRealizada = models.ForeignKey(
        ProvaRealizadaPeloAluno, on_delete=models.CASCADE)
    questaoCorrespondente = models.ForeignKey(
        Questao, on_delete=models.DO_NOTHING)
    alternativaEscolhida = models.IntegerField()
    acertouAQuestao = models.BooleanField()

    def __str__(self):
        return f'resposta da questao de id {self.questaoCorrespondente.id}, na prova {self.provaRealizada.prova.nome}, do aluno {self.provaRealizada.aluno.nome}'

    class Meta:
        db_table = 'questões das provas realizadas pelos alunos'


class BoletimDeDesempenhoDoAluno(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    provaRealizada = models.ForeignKey(
        ProvaRealizadaPeloAluno, on_delete=models.CASCADE)
    nota = models.DecimalField(decimal_places=2, max_digits=10)
    aprovado = models.BooleanField()

    def __str__(self):
        return f'boletim de desempenho do aluno {self.aluno.nome} na matéria {self.materia.nome}'

    class Meta:
        db_table = 'boletins de desempenho dos alunos'


class Parcela(models.Model):
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    valorDaParcela = models.DecimalField(decimal_places=2, max_digits=10)
    dataDeVencimento = models.DateField()
    pagamentoRealizado = models.BooleanField()
    boleto = models.FileField(upload_to='boletos')

    def __str__(self):
        return f'parcela do aluno {self.aluno.nome} referente ao curso {self.curso.nome}'

    @property
    def parcelaVencida(self):
        return date.today() > self.dataDeVencimento

    class Meta:
        db_table = 'parcelas dos alunos'
