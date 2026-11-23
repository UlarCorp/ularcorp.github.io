// Дорожная карта строится из assets/roadmap.json: чтобы обновить страницу, достаточно поправить данные.
(function () {
  var board = document.getElementById("board");
  var legend = document.getElementById("legend");

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function render(data) {
    var head = el("div", "row cols");
    head.appendChild(el("div", null, "Направление"));
    data.stages.forEach(function (s) { head.appendChild(el("div", null, s.name)); });
    board.appendChild(head);

    data.rows.forEach(function (r) {
      var row = el("div", "row");
      var dir = el("div", "dir", r.dir);
      dir.appendChild(el("small", null, r.hint));
      row.appendChild(dir);
      data.stages.forEach(function (s) {
        var items = r[s.id] || [];
        var cell = el("div", "cell " + s.id + (items.length ? "" : " is-empty"));
        cell.appendChild(el("span", "cap", s.name));
        if (!items.length) cell.appendChild(el("span", "empty", "–"));
        items.forEach(function (pair) {
          var it = el("div", "item " + s.id);
          it.appendChild(el("i", "mark " + s.id));
          it.appendChild(el("b", null, pair[0]));
          it.appendChild(el("span", null, pair[1]));
          cell.appendChild(it);
        });
        row.appendChild(cell);
      });
      board.appendChild(row);
    });

    data.stages.forEach(function (s) {
      var count = data.rows.reduce(function (n, r) { return n + (r[s.id] || []).length; }, 0);
      var b = el("button", "stage");
      b.type = "button";
      b.setAttribute("aria-pressed", "false");
      b.appendChild(el("span", "mark " + s.id));
      b.appendChild(el("span", null, s.name));
      b.appendChild(el("span", "n", String(count)));
      b.addEventListener("click", function () {
        var on = board.dataset.focus === s.id;
        if (on) delete board.dataset.focus; else board.dataset.focus = s.id;
        Array.prototype.forEach.call(legend.children, function (x) {
          x.setAttribute("aria-pressed", String(!on && x === b));
        });
      });
      legend.appendChild(b);
    });

    document.getElementById("updated").textContent = "Обновлено " + data.updated;
  }

  fetch("assets/roadmap.json", { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(render)
    .catch(function () {
      board.appendChild(el("div", "row", "Не удалось загрузить дорожную карту. Обновите страницу."));
    });
})();
