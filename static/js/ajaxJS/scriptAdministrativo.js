$(document).ready(function () {
  let url = "/card-gerenciar-alunos";
  let token = $("#token").val();
  exibirCardGerenciarAlunos(url, token);
});
function insertDataInsideTag(tagSelector, content) {
  $(tagSelector).html(content);
}
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
