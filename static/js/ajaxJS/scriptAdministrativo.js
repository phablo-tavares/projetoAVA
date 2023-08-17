$(document).ready(function () {
  let url = "/card-gerenciar-alunos";
  let token = $("#token").val();
  exibirCardGerenciarAlunos(url, token);
});
function insertDataInsideTag(tagSelector, content) {
  $(tagSelector).html(content);
}

//
//Scripts relacionados ao gerenciamento de alunos//
//

//prettier-ignore
function inserirCardNaPaginaPrincipalAdministrativo(url, token, id) {
  id = Number(id);
  $.ajax({
    url: url,
    type: "get",
    data: { id: id },
    headers: { "X-CSRFToken": token },
    success: function (data) {
      insertDataInsideTag("#card-container-administrativo-pagina-principal", data);
    },
  });
}

function exibirCardGerenciarAlunos(url, token) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, 1);
}
function visualizarDadosDoAluno(url, token, idDoAluno) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, idDoAluno);
}

//prettier-ignore
function exibirCardProvaAdministrativo(url, token, idDoAluno, idDaProva) {
  idDoAluno = Number(idDoAluno);
  idDaProva = Number(idDaProva);
  $.ajax({
    url: url,
    type: "get",
    data: {
        'idDoAluno': idDoAluno,
        'idDaProva': idDaProva,
    },
    headers: { "X-CSRFToken": token },
    success: function (data) {
      insertDataInsideTag("#card-container-administrativo-pagina-principal", data);
    },
  });
}

function exibirCardEditarDadosPessoaisDeUmAluno(url, token, idAluno) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, idAluno);
}
//prettier-ignore
function salvarEdicaoDeUmAluno(url, token,idAluno) {
  let dadosAlunoSerializado = JSON.stringify($("#dadosPessoaisDoAlunoAdministrativo").serializeArray());

  $.ajax({
    url: url,
    type: "post",
    data: {
      'id': idAluno,
      'dadosAlunoSerializado': dadosAlunoSerializado,
    },
    dataType: "json",
    headers: { "X-CSRFToken": token },
    success: function (data) {
      nomeAtualizado = JSON.parse(data);
      console.log(nomeAtualizado)
      Swal.fire("Dados Editados com sucesso", "", "success");
    },
  });
}

//prettier-ignote
function permitirQueUmAlunoRefacaUmaProva(url, token, id) {
  Swal.fire({
    title: "Tem certeza que deseja autorizar que o aluno refaça a prova?",
    showDenyButton: true,
    confirmButtonText: "Sim",
    denyButtonText: `Não`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      id = Number(id);
      $.ajax({
        url: url,
        type: "post",
        data: { id: id },
        headers: { "X-CSRFToken": token },
        success: function (data) {
          nomeAtualizado = JSON.parse(data);
          console.log(nomeAtualizado);
          $(`#botaoPermitirQueOAlunoRefacaAProva${id}`).remove();
          if ($("#containerBotoesPermitirRefazerProva button").length === 0) {
            $("#provasRealizadasOQualOAlunoReprovou").remove();
          }
        },
      });
    }
  });
}

async function deletarRegistro(url, token, id) {
  id = Number(id);
  $.ajax({
    url: url,
    type: "post",
    data: { id: id },
    headers: { "X-CSRFToken": token },
  });
}
function excluirAluno(urlExcluirAluno, token, idAluno, urlCardGerenciarAlunos) {
  Swal.fire({
    title: "Tem certeza que deseja excluir o aluno? Operação Irreversivel",
    showDenyButton: true,
    confirmButtonText: "Sim",
    denyButtonText: `Não`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      await deletarRegistro(urlExcluirAluno, token, idAluno);
      await Swal.fire("Aluno excluido do sistema!", "", "success");
      exibirCardGerenciarAlunos(urlCardGerenciarAlunos, token);
    }
  });
}

//
//scripts relacionados ao gerenciamento de cursos
//
function exibirCardGerenciarCursos(url, token) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, 1);
}
function exibirCardCriarUmNovoCurso(url, token) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, 1);
}
function exibirCardEditarDadosDeUmCurso(url, token, idCurso) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, idCurso);
}
function voltarParaOGerenciamentoDeCursos(url, token) {
  Swal.fire({
    title: "Tem certeza que deseja voltar? Dados não salvos serão perdidos",
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      exibirCardGerenciarCursos(url, token);
    }
  });
}

//prettier-ignore
function salvarNovoCurso(urlSalvarCurso, token, urlCardGerenciarCursos) {
  let dadosCursoSerializado = JSON.stringify($("#dadosParaCriacaoDeUmNovoCurso").serializeArray());

  Swal.fire({
    title: "Confirmar a criação de um novo curso?",
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: urlSalvarCurso,
        type: "post",
        data: {
          'dadosCursoSerializado': dadosCursoSerializado,
        },
        dataType: "json",
        headers: { "X-CSRFToken": token },
        success: async function (data) {
          nomeCursoCriado = JSON.parse(data);
          await Swal.fire(`Curso ${nomeCursoCriado} criado com sucesso!`, "", "success");
          exibirCardGerenciarCursos(urlCardGerenciarCursos, token);
        },
      });
    }
  });
}

//prettier-ignore
function salvarEdicaoNoCurso(urlSalvarCurso, token, idDoCurso, urlCardGerenciarCursos) {
  let dadosCursoSerializado = JSON.stringify($("#dadosParaEdicaoDoCurso").serializeArray());
  idDoCurso = Number(idDoCurso);

  Swal.fire({
    title: "Confirmar a edição do curso?",
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: urlSalvarCurso,
        type: "post",
        data: {
          'dadosCursoSerializado': dadosCursoSerializado,
          'idDoCurso': idDoCurso,
        },
        dataType: "json",
        headers: { "X-CSRFToken": token },
        success: async function (data) {
          nomeCursoCriado = JSON.parse(data);
          await Swal.fire(`Curso ${nomeCursoCriado} editado com sucesso!`, "", "success");
          exibirCardGerenciarCursos(urlCardGerenciarCursos, token);
        },
      });
    }
  });
}

function excluirUmCurso(urlExcluirCurso, token, idCurso, urlCardGerenciarCursos) {
  Swal.fire({
    title: "Tem certeza que deseja excluir o curso? Operação Irreversivel!!",
    showDenyButton: true,
    confirmButtonText: "Sim",
    denyButtonText: `Não`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      await deletarRegistro(urlExcluirCurso, token, idCurso);
      await Swal.fire("Curso excluido do sistema!", "", "success");
      exibirCardGerenciarCursos(urlCardGerenciarCursos, token);
    }
  });
}
