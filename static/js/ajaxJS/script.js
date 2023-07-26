function insertDataInsideTag(tagSelector, conteudo) {
  $(tagSelector).html(conteudo);
}

function registrarCursoAtual(cursoId) {
  cursoId = Number(cursoId);
  $("#idCursoAtual").val(cursoId);
}

// prettier-ignore
function exibirCardDosCursos() {
  let url = "/card-cursos-matriculados"
  let alunoId = $('#alunoId').val();
  let token = $('#token').val();
  $.ajax({
    url: url,
    type: "get",
    data: { 'alunoId': alunoId },
    headers: { "X-CSRFToken": token },
    success: function (data) {
      insertDataInsideTag("#card-container-pagina-principal",data);
    },
  });
}

// prettier-ignore
function ExibirCardDasMateriasDoCurso(url, token) {
  let idCurso = $("#idCursoAtual").val(); //implementei desta maneira para que ao voltar do card dos materiais para o card das matérias de um curso, seja possível saber qual curso foi acessado, já que a relação entre cursos e matérias é many to many
  $.ajax({
    url: url,
    type: "get",
    data: { 'idDoCurso': idCurso },
    headers: { "X-CSRFToken": token },
    success: function (data) {
      insertDataInsideTag("#card-container-pagina-principal",data);
    },
  });
}

// prettier-ignore
function exibirCardDosMateriaisDaMateria(url, token, idMateria) {
  let idDaMateria = Number(idMateria);
  $.ajax({
    url: url,
    type: "get",
    data: { 'idDaMateria': idDaMateria },
    headers: { "X-CSRFToken": token },
    success: function (data) {
      insertDataInsideTag("#card-container-pagina-principal",data);
    },
  });
}

$(document).ready(function () {
  exibirCardDosCursos();
});
