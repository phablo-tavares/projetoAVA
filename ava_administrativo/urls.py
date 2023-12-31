from django.urls import include, path


from ava_administrativo.views import Dashboard, CardGerenciarAlunos, CardGerenciarCursos, ExcluirAluno, CardVisualizarDadosDoAluno, CardProvaAdministrativo, CardEditarDadosPessoaisDeUmAluno, SalvarDadosPessoaisDeUmAluno, PermitirQueOAlunoRefacaUmaProva, CardCriarUmNovoCurso, SalvarCurso, ExcluirCurso, CardEditarDadosDeUmCurso, CardGerenciarMaterias, CardCriarUmaNovaMateria, SalvarMateria, ExcluirMateria, CardEditarDadosDeUmaMateria, CardMateriaisDeUmaMateria, ExcluirMaterial, SalvarMaterial, CardCadastrarProva, CriarProva, cardVisualizarProva, ExcluirProva, CardFinanceiroAdministrativo, EnviarParcela, AlterarStatusDePagamentoParaPago, AlterarValorDaParcela, AlterarDataDeVencimento, CadastrarAluno, CardGerenciarNotificacoes, ExcluirNotificacaoAluno, CardCriarUmaNovaNotificacao, SalvarNotificacao, CardEditarNotificacao, AlterarCurso

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
    path('cadastrar-aluno',  CadastrarAluno),


    path('card-gerenciar-cursos',  CardGerenciarCursos),
    path('card-criar-novo-curso',  CardCriarUmNovoCurso),
    path('card-editar-dados-do-curso',  CardEditarDadosDeUmCurso),
    path('salvar-curso',  SalvarCurso),
    path('excluir-curso',  ExcluirCurso),

    path('card-gerenciar-materias',  CardGerenciarMaterias),
    path('card-criar-nova-materia',  CardCriarUmaNovaMateria),
    path('card-editar-dados-da-materia',  CardEditarDadosDeUmaMateria),
    path('salvar-materia',  SalvarMateria),
    path('card-materiais-de-uma-materia',  CardMateriaisDeUmaMateria),
    path('card-cadastrar-prova',  CardCadastrarProva),
    path('criar-prova',  CriarProva),
    path('excluir-materia',  ExcluirMateria),
    path('excluir-material',  ExcluirMaterial),
    path('excluir-prova',  ExcluirProva),
    path('salvar-material',  SalvarMaterial),
    path('card-visualizar-prova',  cardVisualizarProva),

    path('card-financeiro-administrativo',  CardFinanceiroAdministrativo),
    path('enviar-parcela',  EnviarParcela),
    path('alterar-status-de-pagamento-para-pago',
         AlterarStatusDePagamentoParaPago),
    path('alterar-valor-da-parcela', AlterarValorDaParcela),
    path('alterar-data-de-vencimento', AlterarDataDeVencimento),

    path('card-gerenciar-notificacoes', CardGerenciarNotificacoes),
    path('card-criar-nova-notificacao', CardCriarUmaNovaNotificacao),
    path('card-editar-notificacao', CardEditarNotificacao),
    path('salvar-notificacao', SalvarNotificacao),
    path('excluir-notificacao',  ExcluirNotificacaoAluno),

    path('alterar-curso',  AlterarCurso),
]
