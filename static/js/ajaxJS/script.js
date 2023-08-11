$(document).ready(function () {
  let url = "/card-cursos-matriculados";
  let token = $("#token").val();
  exibirCardDosCursos(url, token, "");
});

function ToggleInformacoesAluno() {
  $("#informacoesAluno").toggle();
}

function registrarCursoAtual(cursoId) {
  cursoId = Number(cursoId);
  $("#idCursoAtual").val(cursoId);
}

function insertDataInsideTag(tagSelector, content) {
  $(tagSelector).html(content);
}
//prettier-ignore
function inserirCardNaPaginaPricipal(url,token,id){
  id = Number(id)
  $.ajax({
    url: url,
    type: "get",
    data: { 'id': id },
    headers: { "X-CSRFToken": token },
    success: function (data) {
      insertDataInsideTag("#card-container-pagina-principal",data);
    },
  });
}

function exibirCardDosCursos(url, token, idAluno) {
  inserirCardNaPaginaPricipal(url, token, idAluno);
}
function ExibirCardDasMateriasDoCurso(url, token, idCurso) {
  inserirCardNaPaginaPricipal(url, token, idCurso);
}
function exibirCardDosMateriaisDaMateria(url, token, idMateria) {
  inserirCardNaPaginaPricipal(url, token, idMateria);
}
function ExibirCardDaProva(url, token, idProva) {
  inserirCardNaPaginaPricipal(url, token, idProva);
}

function exibirCardBoletimDeDesempenhoDoAluno(url, token) {
  if ($("#informacoesAluno").css("display") === "none") ToggleInformacoesAluno();
  $("#alertaPagamentoVencido").hide();
  inserirCardNaPaginaPricipal(url, token, "");
}
function exibirCardFinanceiroDoAluno(url, token) {
  if ($("#informacoesAluno").css("display") === "none") ToggleInformacoesAluno();
  $("#alertaPagamentoVencido").hide();
  inserirCardNaPaginaPricipal(url, token, "");
}
function exibirCardEditarDadosPessoaisDoDoAluno(url, token) {
  if ($("#informacoesAluno").css("display") === "none") ToggleInformacoesAluno();
  $("#alertaPagamentoVencido").hide();
  inserirCardNaPaginaPricipal(url, token, "");
}

function voltarDaMateriaParaOCursoAtual(url, token) {
  let idDoAluno = $("#alunoId").val();
  exibirCardDosCursos(url, token, idDoAluno);
}

function voltarDoMaterialParaAMateriaAtual(url, token) {
  let idDoCurso = $("#idCursoAtual").val();
  ExibirCardDasMateriasDoCurso(url, token, idDoCurso);
}

//prettier-ignore
async function salvarProvaRealizada(idDaProva, token, finalizouAProva) {
  let url = "/enviar-prova";
  let provaSerializada = JSON.stringify($("#prova").serializeArray());

  $.ajax({
    url: url,
    type: "post",
    data: {
      'idDaProva': idDaProva,
      'provaSerializada': provaSerializada,
      'finalizouAProva': finalizouAProva,
    },
    dataType: "json",
    headers: { "X-CSRFToken": token },
  });
}

//prettier-ignore
function salvarEdicaoAluno(url, token) {
  let dadosAlunoSerializado = JSON.stringify($("#dadosPessoaisDoAluno").serializeArray());

  $.ajax({
    url: url,
    type: "post",
    data: {
      'dadosAlunoSerializado': dadosAlunoSerializado,
    },
    dataType: "json",
    headers: { "X-CSRFToken": token },
    success: function(data){
      nomeAtualizado = JSON.parse(data)
      $(".nomeAluno").html(nomeAtualizado)
      $("#cardHeaderEditarDados").html(`Editar Dados Pessoais - ${nomeAtualizado}`)
      Swal.fire("Dados Editados com sucesso", "", "success");
    }
  });

  
}

function SwallfirefinalizarProva(idDaProva, token, finalizouAProva, urlBoletimDeDesempenho) {
  Swal.fire({
    title: "Tem certeza que deseja finalizar a prova? Operação Irreversivel",
    showDenyButton: true,
    confirmButtonText: "Finalizar",
    denyButtonText: `Continuar Fazendo a prova`,
  }).then(async (result) => {
    if (result.isConfirmed) {
      await Swal.fire("Prova Enviada!", "", "success");
      await salvarProvaRealizada(idDaProva, token, finalizouAProva);
      ToggleInformacoesAluno();
      exibirCardBoletimDeDesempenhoDoAluno(urlBoletimDeDesempenho, token);
    }
  });
}
