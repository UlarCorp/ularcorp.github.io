// Кабинет сотрудника: интерактивный маршрут из assets/roadmap.json и листание сайта как презентации.
(function () {
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.classList.add("js");

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  var NS = "http://www.w3.org/2000/svg";
  function svg(tag, attrs) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  var STATUS = { done: "У сотрудников", next: "Следующее обновление", plan: "В плане" };

  function plural(n, one, few, many) {
    var a = n % 10, b = n % 100;
    if (a === 1 && b !== 11) return one;
    if (a >= 2 && a <= 4 && (b < 12 || b > 14)) return few;
    return many;
  }

  // Число растет от 0 до значения, когда маршрут появляется на экране
  function countUp(node, to) {
    if (reduce) { node.textContent = to; return; }
    var t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / 1200);
      node.textContent = Math.round(to * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  // ---------- Маршрут ----------
  function buildRoute(host, data) {
    var ms = data.milestones;
    var done = ms.filter(function (m) { return m.status === "done"; });
    var next = ms.filter(function (m) { return m.status === "next"; });
    var itemsDone = done.reduce(function (n, m) { return n + m.items.length; }, 0);
    var itemsNext = next.reduce(function (n, m) { return n + m.items.length; }, 0);

    var stats = el("div", "route-stats");
    [[done.length, "из " + ms.length + " этапов пройдено"],
     [itemsDone, plural(itemsDone, "возможность", "возможности", "возможностей") + " уже у сотрудников"],
     [itemsNext, "выйдет в следующем обновлении"]].forEach(function (s) {
      var d = el("div", "stat");
      var b = el("b", null, "0");
      b.dataset.to = s[0];
      d.appendChild(b);
      d.appendChild(el("span", null, s[1]));
      stats.appendChild(d);
    });
    host.appendChild(stats);

    // Дорога: волна через все остановки
    var W = 1200, H = 260, padX = 70, n = ms.length;
    var pts = ms.map(function (m, i) {
      return { x: padX + i * (W - 2 * padX) / (n - 1), y: i % 2 ? 172 : 98 };
    });
    var d = "M " + pts[0].x + " " + pts[0].y;
    for (var i = 1; i < n; i++) {
      var a = pts[i - 1], b2 = pts[i], cx = (b2.x - a.x) / 2;
      d += " C " + (a.x + cx) + " " + a.y + ", " + (b2.x - cx) + " " + b2.y + ", " + b2.x + " " + b2.y;
    }

    var scroll = el("div", "route-scroll");
    var s = svg("svg", { viewBox: "0 0 " + W + " " + H, class: "route-svg", role: "img",
      "aria-label": "Маршрут развития: пройдено " + done.length + " этапов из " + ms.length });
    var defs = svg("defs", {});
    var grad = svg("linearGradient", { id: "rg", x1: "0", x2: "1", y1: "0", y2: "0" });
    grad.appendChild(svg("stop", { offset: "0", "stop-color": "#FFCE64" }));
    grad.appendChild(svg("stop", { offset: ".55", "stop-color": "#FF7A2F" }));
    grad.appendChild(svg("stop", { offset: "1", "stop-color": "#FF4600" }));
    defs.appendChild(grad);
    var sh = svg("filter", { id: "rs", x: "-10%", y: "-30%", width: "120%", height: "160%" });
    sh.appendChild(svg("feDropShadow", { dx: "0", dy: "8", stdDeviation: "8", "flood-color": "#FF4600", "flood-opacity": ".28" }));
    defs.appendChild(sh);
    s.appendChild(defs);

    s.appendChild(svg("path", { d: d, class: "road-bed" }));
    s.appendChild(svg("path", { d: d, class: "road-future" }));
    var passed = svg("path", { d: d, class: "road-passed", stroke: "url(#rg)", filter: "url(#rs)" });
    s.appendChild(passed);

    var here = svg("g", { class: "here-marker" });
    here.appendChild(svg("circle", { r: "22", class: "pulse" }));
    here.appendChild(svg("circle", { r: "9", class: "core" }));
    // Плашка «Мы здесь» справа снизу: дорога в этом месте уходит вверх, подпись ее не перекрывает
    var tag = svg("g", { class: "here-tag", transform: "translate(18 22)" });
    here.tag = tag;
    tag.appendChild(svg("rect", { x: "0", y: "0", width: "92", height: "28", rx: "14" }));
    var hereLabel = svg("text", { x: "46", y: "19", class: "here-label", "text-anchor": "middle" });
    hereLabel.textContent = "Мы здесь";
    tag.appendChild(hereLabel);
    here.appendChild(tag);

    var nodes = svg("g", {});
    ms.forEach(function (m, i) {
      var g = svg("g", { class: "node " + m.status, transform: "translate(" + pts[i].x + " " + pts[i].y + ")",
        tabindex: "0", role: "button", "aria-label": m.version + ", " + (m.approx ? "ориентировочно " : "") + m.date + ": " + m.title });
      var ahead = m.status !== "done";
      if (m.status === "next") g.appendChild(svg("circle", { r: "16", class: "halo" }));
      g.appendChild(svg("circle", { r: ahead ? "19" : "16", class: "ring" }));
      if (ahead) {
        // Впереди: в кружке - сколько возможностей войдет в релиз
        var num = svg("text", { y: "5", class: "node-count", "text-anchor": "middle" });
        num.textContent = m.items.length;
        g.appendChild(num);
      } else {
        g.appendChild(svg("circle", { r: "8", class: "dot" }));
      }
      var up = i % 2 === 0;
      var t1 = svg("text", { y: up ? -34 : 44, class: "node-ver", "text-anchor": "middle" });
      t1.textContent = m.version;
      var t2 = svg("text", { y: up ? -52 : 62, class: "node-date", "text-anchor": "middle" });
      t2.textContent = (m.approx ? "≈ " : "") + m.date;
      g.appendChild(t2); g.appendChild(t1);
      if (m.short) {
        var t3 = svg("text", { y: up ? -70 : 80, class: "node-short", "text-anchor": "middle" });
        if (up) { t3.setAttribute("y", -34); t1.setAttribute("y", -52); t2.setAttribute("y", -70); }
        t3.textContent = m.short;
        g.appendChild(t3);
      }
      g.addEventListener("click", function () { select(i, true); });
      g.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); e.stopPropagation(); select(i, true); }
      });
      nodes.appendChild(g);
    });
    s.appendChild(nodes);
    s.appendChild(here);
    scroll.appendChild(s);

    // Карта и описание выбранной остановки - одна панель, уголок указывает на остановку
    var panel = el("div", "route-panel");
    var card = el("div", "route-card");
    panel.appendChild(scroll);
    panel.appendChild(card);
    host.appendChild(panel);

    var tools = el("div", "route-tools");
    var pdf = el("button", "tool", "Скачать PDF");
    pdf.type = "button";
    pdf.addEventListener("click", function () { window.print(); });
    var csv = el("button", "tool", "Скачать для Excel");
    csv.type = "button";
    csv.addEventListener("click", function () { downloadCsv(data); });
    tools.appendChild(pdf); tools.appendChild(csv);
    tools.appendChild(el("span", "updated", "Обновлено " + data.updated));
    host.appendChild(tools);

    // Полный список - для печати и для отдельной страницы
    var all = el("div", "route-all");
    ms.forEach(function (m) {
      var sec = el("section", "ms " + m.status);
      var h = el("h3", null, m.version + " · " + m.title);
      sec.appendChild(h);
      sec.appendChild(el("p", "ms-meta", (m.approx ? m.date + ", ориентировочно" : m.date) + " — " + STATUS[m.status]));
      var ul = el("ul", null);
      m.items.forEach(function (p) {
        var li = el("li", null);
        li.appendChild(el("b", null, p[0]));
        li.appendChild(el("span", null, p[1]));
        ul.appendChild(li);
      });
      sec.appendChild(ul);
      all.appendChild(sec);
    });
    host.appendChild(all);

    var nodeEls = nodes.children;
    function pointTo(i) {
      var r = nodeEls[i].querySelector(".ring").getBoundingClientRect(), pr = panel.getBoundingClientRect();
      panel.style.setProperty("--caret", Math.round(r.left + r.width / 2 - pr.left) + "px");
    }
    window.addEventListener("resize", function () { if (selected >= 0) pointTo(selected); });
    scroll.addEventListener("scroll", function () { if (selected >= 0) pointTo(selected); });
    var selected = -1;
    function select(i, user) {
      if (i === selected) return;
      selected = i;
      Array.prototype.forEach.call(nodeEls, function (g, k) { g.classList.toggle("sel", k === i); });
      var m = ms[i];
      var inner = el("div", "card-inner " + m.status);
      var head = el("div", "card-head");
      head.appendChild(el("span", "chip " + m.status, STATUS[m.status]));
      head.appendChild(el("span", "card-date", m.approx ? m.date + ", ориентировочно" : m.date));
      inner.appendChild(head);
      inner.appendChild(el("h3", null, m.version + " — " + m.title));
      var ul = el("ul", null);
      m.items.forEach(function (p, k) {
        var li = el("li", null);
        li.style.setProperty("--k", k);
        li.appendChild(el("i", "ico"));
        var t = el("p", null);
        t.appendChild(el("b", null, p[0]));
        t.appendChild(document.createTextNode(" — " + p[1]));
        li.appendChild(t);
        ul.appendChild(li);
      });
      inner.appendChild(ul);
      card.replaceChildren(inner);
      pointTo(i);
      if (user && scroll.scrollWidth > scroll.clientWidth) {
        var x = pts[i].x / W * scroll.scrollWidth - scroll.clientWidth / 2;
        scroll.scrollTo({ left: x, behavior: reduce ? "auto" : "smooth" });
      }
    }

    // Где на дороге «мы здесь»: между последней пройденной и следующей остановкой
    var lastDone = ms.map(function (m) { return m.status; }).lastIndexOf("done");
    var total, target;
    function lengthAt(pt) {
      var best = 0, bestD = 1e9;
      for (var L = 0; L <= total; L += 4) {
        var p = passed.getPointAtLength(L), dd = (p.x - pt.x) * (p.x - pt.x) + (p.y - pt.y) * (p.y - pt.y);
        if (dd < bestD) { bestD = dd; best = L; }
      }
      return best;
    }
    function measure() {
      total = passed.getTotalLength();
      var a = lengthAt(pts[lastDone]);
      var b = lastDone + 1 < n ? lengthAt(pts[lastDone + 1]) : a;
      target = a + (b - a) * 0.42;
      // Плашка - с той стороны, где дорога не проходит: на спуске сверху справа, на подъеме снизу справа
      var down = lastDone + 1 < n && pts[lastDone + 1].y > pts[lastDone].y;
      here.tag.setAttribute("transform", down ? "translate(16 -46)" : "translate(18 22)");
      passed.style.strokeDasharray = total;
    }
    function place(L) {
      passed.style.strokeDashoffset = total - L;
      var p = passed.getPointAtLength(L);
      here.setAttribute("transform", "translate(" + p.x + " " + p.y + ")");
    }

    var played = false;
    function play() {
      if (played) return;
      played = true;
      measure();
      stats.querySelectorAll("b").forEach(function (b) { countUp(b, +b.dataset.to); });
      if (reduce) { place(target); return; }
      var t0 = null;
      function step(t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / 2200);
        place(target * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    measure(); place(0);
    select(Math.min(lastDone + 1, n - 1), false);
    return { play: play };
  }

  function downloadCsv(data) {
    var rows = [["Этап", "Когда", "Статус", "Возможность", "Что это"]];
    data.milestones.forEach(function (m) {
      m.items.forEach(function (p) { rows.push([m.version + " — " + m.title, m.approx ? m.date + " (ориентировочно)" : m.date, STATUS[m.status], p[0], p[1]]); });
    });
    var text = "﻿" + rows.map(function (r) {
      return r.map(function (c) { return '"' + String(c).replace(/"/g, '""') + '"'; }).join(";");
    }).join("\r\n");
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type: "text/csv;charset=utf-8" }));
    a.download = "Кабинет сотрудника - дорожная карта " + data.updated + ".csv";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  }

  // ---------- Сборка ----------
  var routeHost = document.getElementById("route");
  var route = null;
  var ready = routeHost ? fetch("assets/roadmap.json", { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) { route = buildRoute(routeHost, data); })
    .catch(function () { routeHost.appendChild(el("p", "updated", "Не удалось загрузить дорожную карту. Обновите страницу.")); })
    : Promise.resolve();

  // Глубина: веер телефонов слегка поворачивается за курсором
  var fan = document.querySelector(".fan");
  if (fan && !reduce && window.matchMedia("(pointer: fine)").matches) {
    document.addEventListener("mousemove", function (e) {
      var x = e.clientX / window.innerWidth - 0.5, y = e.clientY / window.innerHeight - 0.5;
      fan.style.transform = "perspective(1200px) rotateY(" + (x * 10) + "deg) rotateX(" + (-y * 6) + "deg)";
    });
  }

  var isDeck = document.body.classList.contains("deck-page");
  ready.then(function () {
    if (!isDeck) {
      if (route) {
        var obs = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { route.play(); obs.disconnect(); } }, { threshold: 0.3 });
        obs.observe(routeHost.querySelector(".route-svg") || routeHost);
      }
      return;
    }

    var slides = Array.prototype.slice.call(document.querySelectorAll(".slide"));
    var count = document.getElementById("count");
    var top = document.querySelector(".fixed-top");
    var bar = document.getElementById("progress");
    var current = 0;

    function show(i) {
      current = Math.max(0, Math.min(slides.length - 1, i));
      count.textContent = (current + 1) + " / " + slides.length;
      document.getElementById("prev").disabled = current === 0;
      document.getElementById("next").disabled = current === slides.length - 1;
      if (top) top.classList.toggle("on-band", slides[current].classList.contains("band"));
      if (bar) bar.style.transform = "scaleX(" + ((current + 1) / slides.length) + ")";
    }
    function go(i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      slides[i].scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
      show(i);
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-active");
        show(slides.indexOf(e.target));
        history.replaceState(null, "", "#" + e.target.id);
        if (route && e.target.contains(routeHost)) route.play();
      });
    }, { threshold: 0.5 });
    slides.forEach(function (s) { io.observe(s); });

    document.getElementById("prev").addEventListener("click", function () { go(current - 1); });
    document.getElementById("next").addEventListener("click", function () { go(current + 1); });
    document.getElementById("full").addEventListener("click", toggleFull);
    function toggleFull() {
      if (document.fullscreenElement) { document.exitFullscreen(); return; }
      var p = document.documentElement.requestFullscreen && document.documentElement.requestFullscreen();
      if (p && p.catch) p.catch(function () {});
    }

    document.addEventListener("keydown", function (e) {
      var t = e.target;
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(t.tagName))) {
        if (e.key === " " || e.key === "Enter") return;
      }
      if (t && t.classList && (t.classList.contains("strip") || t.classList.contains("route-scroll")) &&
          (e.key === "ArrowLeft" || e.key === "ArrowRight")) return;
      var k = e.key;
      if (k === "ArrowRight" || k === "PageDown" || (k === " " && !e.shiftKey)) { e.preventDefault(); go(current + 1); }
      else if (k === "ArrowLeft" || k === "PageUp" || (k === " " && e.shiftKey)) { e.preventDefault(); go(current - 1); }
      else if (k === "Home") { e.preventDefault(); go(0); }
      else if (k === "End") { e.preventDefault(); go(slides.length - 1); }
      else if (k === "f" || k === "F" || k === "а" || k === "А") { toggleFull(); }
    });

    var start = location.hash ? slides.findIndex(function (s) { return "#" + s.id === location.hash; }) : 0;
    if (start > 0) slides[start].scrollIntoView({ block: "start" });
    show(Math.max(start, 0));
  });
})();
