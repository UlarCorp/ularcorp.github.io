// Языки сайта: русский (исходный текст страниц), казахский и английский.
// Переводы - в assets/i18n/kk.js и assets/i18n/en.js: ключ - русская строка как на странице, значение - перевод.
// Данные маршрута и изменений переводятся в самих roadmap.json и changes.json (поля "kk" и "en").
(function () {
  var LANGS = [
    { code: "ru", short: "RU", name: "Русский" },
    { code: "kk", short: "KZ", name: "Қазақша" },
    { code: "en", short: "EN", name: "English" }
  ];
  var DICT = window.I18N_DICT || {};
  var root = document.documentElement;
  var known = function (c) { return LANGS.some(function (l) { return l.code === c; }); };

  function pick() {
    var q = null;
    try { q = new URLSearchParams(location.search).get("lang"); } catch (e) {}
    if (q === "kz") q = "kk";
    if (known(q)) { try { localStorage.setItem("lang", q); } catch (e) {} return q; }
    var s = null;
    try { s = localStorage.getItem("lang"); } catch (e) {}
    return known(s) ? s : "ru";
  }
  var lang = pick();
  var missing = {};

  function norm(s) { return s.replace(/\s+/g, " ").trim(); }
  function t(s, vars) {
    var out = s;
    if (lang !== "ru") {
      var d = DICT[lang] || {};
      if (Object.prototype.hasOwnProperty.call(d, s)) out = d[s];
      else missing[s] = true;
    }
    if (vars) out = out.replace(/\{(\w+)\}/g, function (m, k) { return k in vars ? vars[k] : m; });
    return out;
  }
  // Число + слово: в русском три формы, в английском две, в казахском одна
  function plural(n, ru, key) {
    if (lang === "ru") {
      var a = n % 10, b = n % 100;
      return a === 1 && b !== 11 ? ru[0] : a >= 2 && a <= 4 && (b < 12 || b > 14) ? ru[1] : ru[2];
    }
    var f = (DICT[lang] || {})[key];
    if (!f) { missing[key] = true; return ru[2]; }
    return typeof f === "string" ? f : (n === 1 ? f[0] : f[1]);
  }
  // Объект данных на текущем языке: поля из obj[lang] поверх русских
  function loc(obj) {
    var x = lang !== "ru" && obj && obj[lang];
    if (!x) { if (lang !== "ru" && obj) missing["data:" + (obj.version || obj.id || "?")] = true; return obj; }
    var r = {};
    for (var k in obj) r[k] = obj[k];
    for (var k2 in x) r[k2] = x[k2];
    if (obj.items && x.items && obj.items[0] && obj.items[0].length === 3) {
      // в changes.json пункт [тип, название, пояснение], в переводе - [название, пояснение]
      r.items = obj.items.map(function (it, i) { var p = x.items[i] || it.slice(1); return [it[0], p[0], p[1]]; });
    }
    return r;
  }

  // ---------- Перевод страницы: текст, подсказки, заголовок, описание ----------
  var ATTRS = ["title", "aria-label", "alt", "data-title", "content"];
  var textOrig = new WeakMap(), attrOrig = new WeakMap();
  function skip(node) {
    for (var e = node; e; e = e.parentElement) {
      if (e.nodeType === 1 && (e.tagName === "SCRIPT" || e.tagName === "STYLE" || e.hasAttribute("data-i18n-skip"))) return true;
    }
    return false;
  }
  function apply() {
    var w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT), n, list = [];
    while ((n = w.nextNode())) list.push(n);
    list.forEach(function (node) {
      if (!textOrig.has(node)) {
        if (!/[А-Яа-я]/.test(node.nodeValue) || skip(node.parentElement)) return;
        textOrig.set(node, node.nodeValue);
      }
      var ru = textOrig.get(node), key = norm(ru);
      var lead = ru.match(/^\s*/)[0], tail = ru.match(/\s*$/)[0];
      node.nodeValue = lang === "ru" ? ru : lead + t(key) + tail;
    });
    document.querySelectorAll("[title],[aria-label],[alt],[data-title],meta[content]").forEach(function (e) {
      if (skip(e)) return;
      var o = attrOrig.get(e);
      if (!o) {
        o = {};
        ATTRS.forEach(function (a) { var v = e.getAttribute(a); if (v && /[А-Яа-я]/.test(v)) o[a] = v; });
        attrOrig.set(e, o);
      }
      for (var a in o) e.setAttribute(a, lang === "ru" ? o[a] : t(norm(o[a])));
    });
    root.lang = lang;
    fixLinks();
  }
  // Внутренние ссылки несут язык: выбор не теряется, даже если браузер не хранит настройки
  function fixLinks() {
    document.querySelectorAll("a[href]").forEach(function (a) {
      var h = a.getAttribute("href");
      if (/^(https?:|mailto:|#)/.test(h)) return;
      var u = new URL(h, location.href);
      if (lang === "ru") u.searchParams.delete("lang"); else u.searchParams.set("lang", lang);
      a.setAttribute("href", h.split(/[?#]/)[0] + u.search + u.hash);
    });
    try {
      var cur = new URL(location.href);
      if (lang === "ru") cur.searchParams.delete("lang"); else cur.searchParams.set("lang", lang);
      history.replaceState(history.state, "", cur.pathname + cur.search + cur.hash);
    } catch (e) {}
  }

  // ---------- Переключатель языка: кнопка с кодом и меню из трех языков ----------
  var menus = [];
  function short() { return LANGS.filter(function (l) { return l.code === lang; })[0].short; }
  function makeSwitch(host, before, isPager) {
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = isPager ? "lang-btn" : "theme-btn lang-btn";
    btn.setAttribute("aria-haspopup", "menu");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("data-i18n-skip", "");
    var code = document.createElement("span");
    code.className = "lang-code";
    btn.appendChild(code);
    host.insertBefore(btn, before);

    var menu = document.createElement("div");
    menu.className = "lang-menu";
    menu.setAttribute("role", "menu");
    menu.setAttribute("data-i18n-skip", "");
    LANGS.forEach(function (l) {
      var it = document.createElement("button");
      it.type = "button";
      it.setAttribute("role", "menuitemradio");
      it.setAttribute("lang", l.code);
      it.dataset.lang = l.code;
      it.innerHTML = '<span class="lm-code"></span><span class="lm-name"></span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l4 4 10-10" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      it.querySelector(".lm-code").textContent = l.short;
      it.querySelector(".lm-name").textContent = l.name;
      it.addEventListener("click", function () { close(); setLang(l.code); btn.focus(); });
      menu.appendChild(it);
    });
    document.body.appendChild(menu);

    function place() {
      var r = btn.getBoundingClientRect();
      menu.style.top = Math.round(r.bottom + 8) + "px";
      menu.style.right = Math.max(12, Math.round(window.innerWidth - r.right)) + "px";
    }
    function open() {
      menus.forEach(function (m) { if (m !== api) m.close(); });
      place();
      menu.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
      var cur = menu.querySelector('[aria-checked="true"]');
      if (cur) cur.focus({ preventScroll: true });
    }
    function close() {
      menu.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    }
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (menu.classList.contains("open")) close(); else open();
    });
    menu.addEventListener("keydown", function (e) {
      var items = Array.prototype.slice.call(menu.children), k = items.indexOf(document.activeElement);
      if (e.key === "Escape") { e.preventDefault(); close(); btn.focus(); }
      else if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault(); e.stopPropagation();
        items[(k + (e.key === "ArrowDown" ? 1 : items.length - 1)) % items.length].focus();
      }
    });
    menu.addEventListener("click", function (e) { e.stopPropagation(); });
    window.addEventListener("resize", function () { if (menu.classList.contains("open")) place(); });
    window.addEventListener("scroll", function () { if (menu.classList.contains("open")) place(); }, { passive: true });

    var api = {
      close: close,
      sync: function () {
        code.textContent = short();
        btn.setAttribute("aria-label", t("Язык") + ": " + LANGS.filter(function (l) { return l.code === lang; })[0].name);
        Array.prototype.forEach.call(menu.children, function (it) { it.setAttribute("aria-checked", it.dataset.lang === lang ? "true" : "false"); });
      }
    };
    menus.push(api);
    api.sync();
  }
  document.addEventListener("click", function () { menus.forEach(function (m) { m.close(); }); });

  // Смена языка без перезагрузки: страница на мгновение гаснет и проявляется уже на новом языке
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function setLang(code) {
    if (code === lang || !known(code)) return;
    try { localStorage.setItem("lang", code); } catch (e) {}
    function swap() {
      lang = code;
      apply();
      menus.forEach(function (m) { m.sync(); });
      document.dispatchEvent(new CustomEvent("langchange", { detail: { lang: lang } }));
      requestAnimationFrame(function () { root.classList.remove("lang-fade"); });
    }
    if (reduce) { swap(); return; }
    root.classList.add("lang-fade");
    setTimeout(swap, 180);
  }

  window.I18N = {
    get lang() { return lang; },
    t: t, plural: plural, loc: loc, setLang: setLang, refresh: apply, missing: missing, langs: LANGS
  };

  document.querySelectorAll(".nav").forEach(function (nav) { makeSwitch(nav, nav.querySelector(".theme-btn"), false); });
  var pager = document.querySelector(".pager #theme");
  if (pager) makeSwitch(pager.parentNode, pager, true);
  apply();
  root.classList.remove("i18n-wait");
})();
