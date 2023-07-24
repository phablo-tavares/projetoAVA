// prettier-ignore
function ExibirCardDasMateriasDoCurso(url, token, idDoCurso) {
  let idCurso = Number(idDoCurso);
  $.ajax({
    url: url,
    type: "post",
    data: { 'idDoCurso': idCurso },
    headers: { "X-CSRFToken": token },
    success: function (data) {
      $("#card-container-pagina-principal").html(data);
    },
  });
}

// prettier-ignore
function exibirCardDosCursosNaPaginaPrincipal(token) {
  let alunoId = $('#alunoId').val();
  $.ajax({
    url: "/card-cursos-matriculados",
    type: "get",
    data: { 'alunoId': alunoId },
    headers: { "X-CSRFToken": token },
    success: function (data) {
      $("#card-container-pagina-principal").html(data);
    },
  });
}

// prettier-ignore
$(document).ready(function () {
  let token = $('#token').val();
  let alunoId = $('#alunoId').val();
});
