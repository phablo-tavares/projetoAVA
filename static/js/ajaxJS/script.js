$(document).ready(function () {
  let url = "/card-cursos-matriculados";
  let idAluno = $("#alunoId").val();
  let token = $("#token").val();
  exibirCardDosCursos(url, token, idAluno);
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

function voltarDaMateriaParaOCursoAtual(url, token) {
  let idDoAluno = $("#alunoId").val();
  exibirCardDosCursos(url, token, idDoAluno);
}

function voltarDoMaterialParaAMateriaAtual(url, token) {
  let idDoCurso = $("#idCursoAtual").val();
  ExibirCardDasMateriasDoCurso(url, token, idDoCurso);
}

//prettier-ignore
function salvarProvaRealizada(idDaProva, token, finalizouAProva) {
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

function SwallfirefinalizarProva(
  idDaProva,
  token,
  finalizouAProva,
  urlMateriaisDaMateria,
  idDaMateria
) {
  Swal.fire({
    title: "Tem certeza que deseja finalizar a prova? Uma vez finalizada não será possível",
    showDenyButton: true,
    confirmButtonText: "Finalizar",
    denyButtonText: `Continuar Fazendo a prova`,
  }).then(async (result) => {
    /* Read more about isConfirmed, isDenied below */
    if (result.isConfirmed) {
      await Swal.fire("Prova Enviada!", "", "success");
      salvarProvaRealizada(idDaProva, token, finalizouAProva);
      ToggleInformacoesAluno();
      exibirCardDosMateriaisDaMateria(urlMateriaisDaMateria, token, idDaMateria);
    }
  });
}
