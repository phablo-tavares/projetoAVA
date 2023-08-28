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

//
//Scripts relacionados ao gerenciamento de alunos//
//
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

function limparCamposFormularioDeCadastroDeAlunos() {
  $("#nome").val("");
  $("#cpf").val("");
  $("#rg").val("");
  $("#email").val("");
  $("#endereco").val("");
  $("#nomeDeUsuario").val("");
  $("#senha").val("");
}
//prettier-ignore
function cadastrarAluno(urlCadastrarAluno, token,urlCardGerenciarAlunos) {
  let dadosAlunoSerializado = JSON.stringify($("#cadastrarAluno").serializeArray());

  Swal.fire({
    title: "Confirmar o cadastro de um novo aluno? ",
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: urlCadastrarAluno,
        type: "post",
        data: {
          'dadosAlunoSerializado': dadosAlunoSerializado,
        },
        dataType: "json",
        headers: { "X-CSRFToken": token },
        success: async function (data) {
          nomeAlunoCriado = JSON.parse(data);
          await Swal.fire(`${nomeAlunoCriado} cadastrado no sistema!`, "", "success");
          exibirCardGerenciarAlunos(urlCardGerenciarAlunos, token);
        },
        error: function(data){
          Swal.fire(`${data.responseJSON['error']}`, "", "error");
        }
      });
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

//
// scripts relacionados ao gerenciamento de matérias
//

function exibirCardGerenciarMaterias(url, token) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, 1);
}
function exibirCardCriarUmaNovaMateria(url, token) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, 1);
}
function exibirCardEditarDadosDeUmaMateria(url, token, idMateria) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, idMateria);
}
function exibirCardMateriaisDeUmaMateria(url, token, idMateria) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, idMateria);
}
function exibirCardCadastrarProva(url, token, idMateria) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, idMateria);
}
function exibirCardVisualizarProva(url, token, idMateria) {
  inserirCardNaPaginaPrincipalAdministrativo(url, token, idMateria);
}
function voltarParaOGerenciamentoDeMaterias(url, token) {
  Swal.fire({
    title: "Tem certeza que deseja voltar? Dados não salvos serão perdidos",
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      exibirCardGerenciarMaterias(url, token);
    }
  });
}
function voltarParaOGerenciamentoDeMateriasSemPedidoDeConfirmacao(url, token) {
  exibirCardGerenciarMaterias(url, token);
}

//prettier-ignore
function salvarNovaMateria(urlSalvarMateria, token, urlCardGerenciarMaterias) {
  let dadosMateriaSerializado = $("#dadosParaCriacaoDeUmaNovaMateria").serializeArray();
  dadosMateriaSerializado.push({
    "name":"cursosParaCadastrarNaMateria",
    "value":[]
  });
  $(".form-check-input:checked").each(function(){
    dadosMateriaSerializado[1]['value'].push($(this).val());
  });
  dadosMateriaSerializado = JSON.stringify(dadosMateriaSerializado);
  console.log(dadosMateriaSerializado);
  
  Swal.fire({
    title: "Confirmar a criação de uma nova matéria?",
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: urlSalvarMateria,
        type: "post",
        data: {
          'dadosMateriaSerializado': dadosMateriaSerializado,
        },
        dataType: "json",
        headers: { "X-CSRFToken": token },
        success: async function (data) {
          nomeMateriaCriada = JSON.parse(data);
          await Swal.fire(`Matéria ${nomeMateriaCriada} criada com sucesso!`, "", "success");
          exibirCardGerenciarMaterias(urlCardGerenciarMaterias, token)
        },
      });
    }
  });
}

function excluirUmaMateria(urlExcluirMateria, token, idMateria, urlCardGerenciarMaterias) {
  Swal.fire({
    title: "Tem certeza que deseja excluir esta matéria? Operação Irreversivel!!",
    showDenyButton: true,
    confirmButtonText: "Sim",
    denyButtonText: `Não`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      await deletarRegistro(urlExcluirMateria, token, idMateria);
      await Swal.fire("Matéria excluida do sistema!", "", "success");
      exibirCardGerenciarMaterias(urlCardGerenciarMaterias, token);
    }
  });
}
function excluirUmMaterial(
  urlExcluirMaterial,
  token,
  idMaterial,
  idMateria,
  urlMateriaisDeUmaMateria
) {
  Swal.fire({
    title: "Tem certeza que deseja excluir esta material? Operação Irreversivel!!",
    showDenyButton: true,
    confirmButtonText: "Sim",
    denyButtonText: `Não`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      await deletarRegistro(urlExcluirMaterial, token, idMaterial);
      await Swal.fire("Matéria excluida do sistema!", "", "success");
      exibirCardMateriaisDeUmaMateria(urlMateriaisDeUmaMateria, token, idMateria);
    }
  });
}

//prettier-ignore
function salvarEdicaoNaMateria(urlSalvarMateria, token, idDaMateria, urlCardGerenciarMaterias) {
  let dadosMateriaSerializado = $("#dadosParaEdicaoDaMateria").serializeArray();
  dadosMateriaSerializado.push({
    "name":"cursosParaCadastrarNaMateria",
    "value":[]
  });
  $(".form-check-input:checked").each(function(){
    dadosMateriaSerializado[1]['value'].push($(this).val());
  });
  dadosMateriaSerializado = JSON.stringify(dadosMateriaSerializado);
  console.log(dadosMateriaSerializado);
  
  Swal.fire({
    title: "Confirmar a edição da materia?",
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: urlSalvarMateria,
        type: "post",
        data: {
          'dadosMateriaSerializado': dadosMateriaSerializado,
          'idDaMateria': idDaMateria,
        },
        dataType: "json",
        headers: { "X-CSRFToken": token },
        success: async function (data) {
          nomeMateriaEditado = JSON.parse(data);
          await Swal.fire(`Matéria ${nomeMateriaEditado} editada com sucesso!`, "", "success");
          exibirCardGerenciarMaterias(urlCardGerenciarMaterias, token);
        },
      });
    }
  });
}

//prettier-ignore
async function enviarMaterial(urlEnviarMateiral, token,idMateria,urlMateriaisDeUmaMateria) {
  let fileInput = document.getElementById("arquivo");
  let file = fileInput.files[0];
  var formData = new FormData();
  formData.append("file", file);
  formData.append("idMateria", idMateria);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", urlEnviarMateiral, true); // Substitua pela URL correta da sua view do Django
  xhr.setRequestHeader("X-CSRFToken", token);
  console.log('teste')
  xhr.onload = function() {
    if (xhr.status === 200) {
      console.log("Anexo enviado com sucesso!");
      exibirCardMateriaisDeUmaMateria(urlMateriaisDeUmaMateria, token, idMateria);
    } else {
      console.error("Erro ao enviar anexo.");
    }
  };
  xhr.send(formData)
}

function adicioarMaisUmaQuestaoNaProva() {
  let quantidadeDeQuestoes = Number($("#quantidadeDeQuestoesAtual").val());
  quantidadeDeQuestoes++;
  $("#quantidadeDeQuestoesAtual").val(`${quantidadeDeQuestoes}`);

  let questaoParaAdicionarNaProva = `
  <div class="row card card-secondary" id="Questao${quantidadeDeQuestoes}">
  <div class="card-header">
  <div class="d-flex align-items-center justify-content-between">
  <h3 class="card-title">Questão</h3>
        <button
          class="btn btn-sm btn-danger"
          onclick="removerQuestãoDaProva('${quantidadeDeQuestoes}')"
        >
        Excluir Questão
        </button>
      </div>
    </div>
    <div class="card-body">
      <div class="form-group">
        <label for="enunciadoQuestao${quantidadeDeQuestoes}">Enunciado</label>
        <textarea
          type="textarea"
          class="form-control form-control-sm"
          id="enunciadoQuestao${quantidadeDeQuestoes}"
          name="enunciadoQuestao${quantidadeDeQuestoes}"
          placeholder="Digite aqui o enunciado da questão"
          style="max-height: 100px"
        ></textarea>
      </div>
      <div class="form-group">
        <label for="alternativa1Questao${quantidadeDeQuestoes}">Alternativa 1</label>
        <input
          type="text"
          class="form-control form-control-sm"
          id="alternativa1Questao${quantidadeDeQuestoes}"
          name="alternativa1Questao${quantidadeDeQuestoes}"
          placeholder="Digite aqui a alternativa "
        />
      </div>
      <div class="form-group">
        <label for="alternativa2Questao${quantidadeDeQuestoes}">Alternativa 2</label>
        <input
          type="text"
          class="form-control form-control-sm"
          id="alternativa2Questao${quantidadeDeQuestoes}"
          name="alternativa2Questao${quantidadeDeQuestoes}"
          placeholder="Digite aqui a alternativa "
        />
      </div>
      <div class="form-group">
      <label for="alternativa3Questao${quantidadeDeQuestoes}">Alternativa 3</label>
      <input
          type="text"
          class="form-control form-control-sm"
          id="alternativa3Questao${quantidadeDeQuestoes}"
          name="alternativa3Questao${quantidadeDeQuestoes}"
          placeholder="Digite aqui a alternativa "
          />
      </div>
      <div class="form-group">
        <label for="alternativa${quantidadeDeQuestoes}">Alternativa 4</label>
        <input
          type="text"
          class="form-control form-control-sm"
          id="alternativa4Questao${quantidadeDeQuestoes}"
          name="alternativa4Questao${quantidadeDeQuestoes}"
          placeholder="Digite aqui a alternativa "
        />
      </div>
      <div class="form-group">
        <label for="alternativaCorretaQuestao1">Alternativa Correta</label>
        <select
        class="form-control form-control-sm"
          name="alternativaCorretaQuestao${quantidadeDeQuestoes}"
          id="alternativaCorretaQuestao${quantidadeDeQuestoes}"
        >
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
        </select>
        </div>
    </div>
    </div>
  `;
  $("#formProvaParaCadastrarNaMateria").append(questaoParaAdicionarNaProva);
}

function removerQuestãoDaProva(id) {
  $(`#Questao${id}`).remove();
  let quantidadeDeQuestoes = Number($("#quantidadeDeQuestoesAtual").val());
  quantidadeDeQuestoes--;
  $("#quantidadeDeQuestoesAtual").val(`${quantidadeDeQuestoes}`);
}

//prettier-ignore
function criarProva(urlCriarProva, token, idDaMateria,urlCardGerenciarMaterias , nomeDaMateria) {
  let dadosProvaSerializado = $("#formProvaParaCadastrarNaMateria").serializeArray();
  dadosProvaSerializado = JSON.stringify(dadosProvaSerializado);

  Swal.fire({
    title: `Confirmar a criação desta prova na matéria ${nomeDaMateria}`,
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: urlCriarProva,
        type: "post",
        data: {
          'dadosProvaSerializado': dadosProvaSerializado,
          'idDaMateria': idDaMateria,
        },
        dataType: "json",
        headers: { "X-CSRFToken": token },
        success: async function (data) {
          nomeProvaCriada = JSON.parse(data);
          await Swal.fire(`Prova ${nomeProvaCriada} criada com sucesso!`, "", "success");
          exibirCardGerenciarMaterias(urlCardGerenciarMaterias, token);
        },
      });
    }
  });
}

function excluirProva(urlExcluirProva, token, idProva, urlCardGerenciarMaterias) {
  Swal.fire({
    title: "Tem certeza que deseja excluir esta prova? Operação Irreversivel!!",
    showDenyButton: true,
    confirmButtonText: "Sim",
    denyButtonText: `Não`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      await deletarRegistro(urlExcluirProva, token, idProva);
      await Swal.fire("Prova excluida do sistema!", "", "success");
      exibirCardGerenciarMaterias(urlCardGerenciarMaterias, token);
    }
  });
}

//
// scripts relacionados ao financeiro administrativo
//
function exibirCardFinanceiroAdministrativo(urlCardFinanceiroAdministrativo, token) {
  inserirCardNaPaginaPrincipalAdministrativo(urlCardFinanceiroAdministrativo, token, 1);
}

function enviarParcela(urlEnviarParcela, token, urlCardFinanceiroAdministrativo) {
  let fileInput = document.getElementById("arquivo");
  let file = fileInput.files[0];
  var formData = new FormData();
  formData.append("file", file);

  idAluno = $("#aluno").val();
  idCurso = $("#curso").val();
  valorDaParcela = $("#valorDaParcela").val();
  dataDeVencimento = $("#dataDeVencimento").val();
  pagamentoRealizado = $("#pagamentoRealizado").val();

  formData.append("idAluno", idAluno);
  formData.append("idCurso", idCurso);
  formData.append("valorDaParcela", valorDaParcela);
  formData.append("dataDeVencimento", dataDeVencimento);
  formData.append("pagamentoRealizado", pagamentoRealizado);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", urlEnviarParcela, true); // Substitua pela URL correta da sua view do Django
  xhr.setRequestHeader("X-CSRFToken", token);
  xhr.onload = function () {
    if (xhr.status === 200) {
      exibirCardFinanceiroAdministrativo(urlCardFinanceiroAdministrativo, token);
    } else {
      console.error("Erro ao enviar anexo.");
    }
  };
  xhr.send(formData);
}

//prettier-ignore
async function alterarStatus(urlAlterarStatusDePagamentoParaPago, token , idParcela) {
  $.ajax({
    url: urlAlterarStatusDePagamentoParaPago,
    type: "post",
    data: {
      'idParcela': idParcela,
    },
    dataType: "json",
    headers: { "X-CSRFToken": token },
  });
}
function alterarStatusDePagamentoParaPago(
  urlAlterarStatusDePagamentoParaPago,
  token,
  idParcela,
  atrasadoParaPago
) {
  Swal.fire({
    title: "Alterar o status de pagamento para Pago?",
    showDenyButton: true,
    confirmButtonText: "Sim",
    denyButtonText: `Não`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      await alterarStatus(urlAlterarStatusDePagamentoParaPago, token, idParcela);
      Swal.fire("Status Alterado!", "", "success");
      $(`#statusPagamentoParcela${idParcela}`).html(
        '<span class="badge badge-success">Pago</span>'
      );
      let qtdParcelasAtrasadas = Number($("#qtdParcelasAtrasadas").text());
      let qtdParcelasPendentes = Number($("#qtdParcelasPendentes").text());
      let qtdParcelasPagas = Number($("#qtdParcelasPagas").text());
      if (atrasadoParaPago) qtdParcelasAtrasadas--;
      qtdParcelasPendentes--;
      qtdParcelasPagas++;
      $("#qtdParcelasAtrasadas").html(`${qtdParcelasAtrasadas}`);
      $("#qtdParcelasPendentes").html(`${qtdParcelasPendentes}`);
      $("#qtdParcelasPagas").html(`${qtdParcelasPagas}`);
    }
  });
}

//prettier-ignore
async function ajaxAlterarValorParcela(urlAlterarValorDaParcela, token, idParcela,valorDaParcela){
  $.ajax({
    url: urlAlterarValorDaParcela,
    type: "post",
    data: {
      'idParcela': idParcela,
      'valorDaParcela': valorDaParcela,
    },
    dataType: "json",
    headers: { "X-CSRFToken": token },
  });
}
async function alterarValorDaParcela(urlAlterarValorDaParcela, token, idParcela) {
  const { value: valorDaParcela } = await Swal.fire({
    title: "Entre o novo valor da parcela",
    input: "number",
    inputLabel: "Valor",
    showCancelButton: true,
    inputValidator: (value) => {
      if (!value) {
        return "Nenhum valor informado!";
      } else {
        partes = value.split(".");
        if (partes.length === 2 && partes[1].length > 2) {
          return "O valor deve ter no maximo 2 casas decimais!";
        }
      }
    },
  });
  if (valorDaParcela) {
    await ajaxAlterarValorParcela(urlAlterarValorDaParcela, token, idParcela, valorDaParcela);
    Swal.fire("Valor Alterado!", "", "success");
    $(`#valorDaParcela${idParcela}`).html(`R$${valorDaParcela}`);
  }
}

//prettier-ignore
async function ajaxAlterarDataDeVencimento(urlAlterarDataDeVencimento, token, idParcela,dataDeVencimento){
  $.ajax({
    url: urlAlterarDataDeVencimento,
    type: "post",
    data: {
      'idParcela': idParcela,
      'dataDeVencimento': dataDeVencimento,
    },
    dataType: "json",
    headers: { "X-CSRFToken": token },
  });
}
async function alterarDataDeVencimento(
  urlAlterarDataDeVencimento,
  token,
  idParcela,
  urlCardFinanceiroAdministrativo
) {
  const { value: dataDeVencimento } = await Swal.fire({
    title: "Entre a nova data de Vencimento",
    html: `
    <div class="form-group">
      <input
        type="date"
        class="form-control"
        id="dataDeVencimentoNova"
        name="dataDeVencimentoNova"
      />
    </div>
    `,
    focusConfirm: false,
    showCancelButton: true,
    preConfirm: () => {
      return document.getElementById("dataDeVencimentoNova").value;
    },
  });
  if (dataDeVencimento) {
    console.log(dataDeVencimento);
    await ajaxAlterarDataDeVencimento(
      urlAlterarDataDeVencimento,
      token,
      idParcela,
      dataDeVencimento
    );
    await Swal.fire("Data Alterada!", "", "success");
    exibirCardGerenciarAlunos(urlCardFinanceiroAdministrativo, token);
    // valores = dataDeVencimento.split("-");
    // ano = valores[0];
    // mes = valores[1];
    // dia = valores[2];
    // $(`#dataDeVencimento${idParcela}`).html(`${dia}/${mes}/${ano}`);
  }
}

//
// scripts relacionados ao gerenciamento de notificações
//
function exibirCardGerenciarNotificacoes(urlGerenciarNotificacoes, token) {
  inserirCardNaPaginaPrincipalAdministrativo(urlGerenciarNotificacoes, token);
}
function exibirCardCriarUmaNovaNotificacao(urlCardCriarUmaNovaNotificacao, token) {
  inserirCardNaPaginaPrincipalAdministrativo(urlCardCriarUmaNovaNotificacao, token);
}
function exibirCardEditarNotificacao(urlCardEditarNotificacao, token, idAluno) {
  inserirCardNaPaginaPrincipalAdministrativo(urlCardEditarNotificacao, token, idAluno);
}
function exibirNotificacao(notificacao) {
  Swal.fire(`${notificacao}`);
}
//prettier-ignore
function excluirNotificacaoAluno(urlExcluirNotificacaoAluno, token, idAluno, urlCardGerenciarNotificacoes) {
  Swal.fire({
    title: "Tem certeza que deseja excluir a notificação? Operação Irreversível",
    showDenyButton: true,
    confirmButtonText: "Sim",
    denyButtonText: `Não`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      await deletarRegistro(urlExcluirNotificacaoAluno, token, idAluno);
      await Swal.fire("Notificação excluida do sistema!", "", "success");
      exibirCardGerenciarNotificacoes(urlCardGerenciarNotificacoes, token);
    }
  });
}
//prettier-ignore
function salvarNotificacao(urlSalvarNotificacao, token, urlCardGerenciarNotificacoes) {
  let dadosNotificacaoSerializado = $("#formNotificacao").serializeArray();
  dadosNotificacaoSerializado = JSON.stringify(dadosNotificacaoSerializado);
  let idAlunoParaCriarNotificacao = $("#idAlunoParaCriarNotificacao").val()

  Swal.fire({
    title: `Salvar notificação?`,
    showCancelButton: true,
    confirmButtonText: "Sim",
    cancelButtonText: `Não`,
  }).then((result) => {
    if (result.isConfirmed) {
      $.ajax({
        url: urlSalvarNotificacao,
        type: "post",
        data: {
          'dadosNotificacaoSerializado': dadosNotificacaoSerializado,
          'idAlunoParaCriarNotificacao': idAlunoParaCriarNotificacao,
        },
        dataType: "json",
        headers: { "X-CSRFToken": token },
        success: async function (data) {
          nomeAluno = JSON.parse(data);
          await Swal.fire(`Notificação salvada com sucesso!`, "", "success");
          exibirCardGerenciarNotificacoes(urlCardGerenciarNotificacoes, token);
        },
      });
    }
  });
}
