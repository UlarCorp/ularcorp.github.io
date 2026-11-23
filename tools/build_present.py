# Собирает present/index.html - презентацию Кабинета сотрудника.
# Запуск из корня сайта:  py tools/build_present.py
# Тексты слайдов правятся здесь; маршрут развития берется из assets/roadmap.json при показе.
import re, hashlib, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOGO = re.search(r'<svg viewBox="0 0 849 220".*?</svg>', (ROOT / 'index.html').read_text(encoding='utf-8'), re.S).group(0)

I = {  # значки (обводка, 24x24)
 'news': '<path d="M4 5h13v14H6a2 2 0 0 1-2-2z"/><path d="M17 9h3v8a2 2 0 0 1-2 2M8 9h5M8 13h5"/>',
 'calc': '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
 'cal': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 'wallet': '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 15h2"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/>',
 'id': '<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M8 17c.8-1.8 2.2-2.6 4-2.6s3.2.8 4 2.6"/>',
 'tag': '<path d="M20 12l-8 8-9-9V3h8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
 'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>',
 'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c1-3.5 3.6-5.5 7-5.5s6 2 7 5.5M16 4.5a3.5 3.5 0 0 1 0 7M18 14.5c2 .7 3.4 2.6 4 5.5"/>',
 'file': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>',
 'shield': '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 'key': '<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/>',
 'log': '<path d="M5 4h14v16H5z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
 'phone': '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
 'server': '<rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 7.5h.01M7 16.5h.01"/>',
 'db': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
 'route': '<circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M8 19h7a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h7"/>',
 'check': '<path d="M5 12l4 4 10-10"/>',
 'x': '<path d="M6 6l12 12M18 6 6 18"/>',
 'swap': '<path d="M7 7h11l-3-3M17 17H6l3 3"/>',
 'monitor': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
 'megaphone': '<path d="M3 11v2a1 1 0 0 0 1 1h2l5 4V6L6 10H4a1 1 0 0 0-1 1zM15 9a3 3 0 0 1 0 6M18 6a7 7 0 0 1 0 12"/>',
 'lock': '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 'face': '<path d="M4 8V6a2 2 0 0 1 2-2h2M16 4h2a2 2 0 0 1 2 2v2M20 16v2a2 2 0 0 1-2 2h-2M8 20H6a2 2 0 0 1-2-2v-2M9 10v1M15 10v1M10 15c1.3.8 2.7.8 4 0M12 9v3"/>',
 'download': '<path d="M12 3v12M7 10l5 5 5-5M5 21h14"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.5 3.8 9s-1.3 6.5-3.8 9c-2.5-2.5-3.8-5.5-3.8-9S9.5 5.5 12 3z"/>',
}
def ico(n):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

def card(i, t, d):
    return f'<div class="card"><span class="ci">{ico(i)}</span><b>{t}</b><p>{d}</p></div>'

def device(name, cls=''):
    return f'<div class="device {cls}"><img src="../assets/app/light/{name}.webp" alt="" width="620" height="1342"></div>'

BACK = '''<i class="slice" style="--z:-11.0px"></i><i class="slice" style="--z:-10.5px"></i><i class="slice" style="--z:-10.0px"></i><i class="slice" style="--z:-9.5px"></i><i class="slice" style="--z:-9.0px"></i><i class="slice" style="--z:-8.5px"></i><i class="slice" style="--z:-8.0px"></i><i class="slice" style="--z:-7.5px"></i><i class="slice" style="--z:-7.0px"></i><i class="slice" style="--z:-6.5px"></i><i class="slice" style="--z:-6.0px"></i><i class="slice" style="--z:-5.5px"></i><i class="slice" style="--z:-5.0px"></i><i class="slice" style="--z:-4.5px"></i><i class="slice" style="--z:-4.0px"></i><i class="slice" style="--z:-3.5px"></i><i class="slice" style="--z:-3.0px"></i><i class="slice" style="--z:-2.5px"></i><i class="slice" style="--z:-2.0px"></i><i class="slice" style="--z:-1.5px"></i><i class="slice" style="--z:-1.0px"></i><i class="slice" style="--z:-0.5px"></i><i class="slice" style="--z:0.0px"></i><i class="slice" style="--z:0.5px"></i><i class="slice" style="--z:1.0px"></i><i class="slice" style="--z:1.5px"></i><i class="slice" style="--z:2.0px"></i><i class="slice" style="--z:2.5px"></i><i class="slice" style="--z:3.0px"></i><i class="slice" style="--z:3.5px"></i><i class="slice" style="--z:4.0px"></i><i class="slice" style="--z:4.5px"></i><i class="slice" style="--z:5.0px"></i><i class="slice" style="--z:5.5px"></i><i class="slice" style="--z:6.0px"></i><i class="slice" style="--z:6.5px"></i><i class="slice" style="--z:7.0px"></i><i class="slice" style="--z:7.5px"></i><i class="slice" style="--z:8.0px"></i><i class="slice" style="--z:8.5px"></i><i class="slice" style="--z:9.0px"></i><i class="slice" style="--z:9.5px"></i><i class="slice" style="--z:10.0px"></i><i class="slice" style="--z:10.5px"></i><i class="slice" style="--z:11.0px"></i><i class="edge el"></i><i class="edge er"></i><i class="edge et"></i><i class="edge eb"></i><div class="device-back" aria-hidden="true"><svg viewBox="0 0 283 220"><path d="M29.8086 177.066C33.7452 177.066 37.3371 179.893 39.753 183.002C46.1115 191.182 62.901 204.238 99.253 217.545C46.9515 217.545 9.14565 211.108 0.314484 185.114C-1.13913 180.835 2.66757 177.066 7.18655 177.066H29.8086ZM69.8587 109.004C83.4162 109.004 94.1327 121.016 97.971 134.019C117.186 188.463 173.441 217.545 173.441 217.545C140.13 217.545 106.184 213.955 77.4821 197.048C54.4154 183.46 29.5887 162.787 21.2532 134.056C17.4759 121.036 28.8384 109.004 42.3958 109.004H69.8587ZM175.006 0C191.834 0 205.317 13.4258 206.041 30.2379C208.97 98.2633 226.685 202.657 282.727 217.545H234.255C202.698 217.545 170.627 209.135 148.651 186.488C109.204 145.836 95.3131 97.632 91.8499 28.0963C91.8501 12.3522 104.614 0.000155662 120.358 0H175.006Z" fill="#FF4600"/></svg><span>Ular</span></div>'''

def phone(name):
    return f'<div class="sphone" data-spin title="Зажмите и покрутите"><div class="spin-body">{device(name)}{BACK}</div></div>'

def slide(sid, title, body, cls='', kick=''):
    k = f'<p class="kick">{kick}</p>' if kick else ''
    return f'''  <section class="pslide {cls}" id="{sid}" data-title="{title}">
    <div class="wrap">
      {k}{body}
    </div>
  </section>
'''

S = []
apple = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M16.4 12.6c0-2.4 2-3.5 2-3.6-1.1-1.6-2.8-1.8-3.4-1.8-1.4-.1-2.8.9-3.5.9s-1.9-.9-3.1-.8c-1.6 0-3 .9-3.8 2.3-1.6 2.8-.4 7 1.2 9.3.8 1.1 1.7 2.4 2.9 2.3 1.2 0 1.6-.7 3-.7s1.8.7 3 .7c1.3 0 2.1-1.1 2.8-2.3.9-1.3 1.3-2.6 1.3-2.6s-2.4-1-2.4-3.7zM14.2 5.6c.6-.8 1.1-1.9 1-3-.9 0-2.1.6-2.7 1.4-.6.7-1.1 1.8-1 2.9 1 .1 2.1-.5 2.7-1.3z"/></svg>'
play = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 3.5v17c0 .4.4.7.8.5l9.7-9-9.7-9c-.4-.2-.8.1-.8.5zm11.6 7.4 2.7-2.5-11-6.2 8.3 8.7zm0 2.2-8.3 8.7 11-6.2-2.7-2.5zm1.1-1.1 3 2.8 2.1-1.2c.7-.4.7-1.4 0-1.8l-2.1-1.2-3 2.8z"/></svg>'

# 1. Титул
S.append(slide('start', 'Кабинет сотрудника', f'''<div class="title-grid">
        <div>
          <p class="kicker">Мобильное приложение Ular</p>
          <h1>Кабинет сотрудника</h1>
        </div>
      </div>
      <div class="fan" aria-hidden="true">
        {device('salary')}
        {device('vacation')}
        {device('home')}
      </div>''', 'band hero'))

exec((ROOT / 'tools' / 'slides_mid.py').read_text(encoding='utf-8'))

# 19. Маршрут
S.append(slide('route-slide', 'Дорожная карта', '''<h2>Дорожная карта</h2>
      <div id="route" class="route"></div>''', 'route-slide'))

# 20. Как начать
S.append(slide('start-using', 'Как начать', f'''<h2 class="mega">Регистрация за пару минут</h2>
      <ol class="chain g3">
        <li><span class="sn">1</span><b>Получите код доступа</b><p>Выдает отдел кадров</p></li>
        <li><span class="sn">2</span><b>Установите Ular</b><p>App Store или Google Play</p></li>
        <li><span class="sn">3</span><b>Введите ИИН и код</b><p>И придумайте пароль</p></li>
      </ol>
      <div class="cards g2">
        {card('key', 'Забыли пароль?', 'Восстановите его тем же кодом доступа, обращаться в отдел кадров не требуется')}
        {card('x', 'Потеряли код?', 'Отдел кадров выдаст новый код, прежний перестанет действовать')}
      </div>''', 'center'))

# 21. Финал
S.append(slide('end', 'Скачать', f'''<div class="finale-grid">
        <div class="finale-text">
          <h2 class="big">Меньше обращений в отдел кадров. Меньше бумаги.</h2>
          
          <p class="credit">© QazDefense 2026</p>
        </div>
        <div class="qr-cards">
          <a class="qr-card" href="https://apps.apple.com/kz/app/ular/id6813023469" rel="noopener"><img src="../assets/qr-ios.svg" alt="QR-код для App Store" width="160" height="160"><span class="qr-meta">{apple}<b>App Store</b><span>iPhone</span></span></a>
          <a class="qr-card" href="https://play.google.com/store/apps/details?id=com.qazdefense.ular" rel="noopener"><img src="../assets/qr-android.svg" alt="QR-код для Google Play" width="160" height="160"><span class="qr-meta">{play}<b>Google Play</b><span>Android</span></span></a>
        </div>
      </div>''', 'band finale'))

ver = hashlib.md5(((ROOT / 'assets/site.css').read_bytes() + (ROOT / 'assets/deck.js').read_bytes())).hexdigest()[:8]
btn = lambda i, label, path: f'<button type="button" id="{i}" aria-label="{label}"><svg viewBox="0 0 24 24" aria-hidden="true">{path}</svg></button>'
html = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Кабинет сотрудника — презентация</title>
<meta name="description" content="Презентация Кабинета сотрудника: что уже работает и куда идем.">
<meta name="theme-color" content="#FF4600">
<link rel="icon" href="../assets/mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="../assets/site.css?v={ver}">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head>
<body class="present-page">

<header class="ptop">
  <a class="brand" href="../" aria-label="Сайт Кабинета сотрудника">{LOGO}</a>
  <nav class="pager" aria-label="Слайды">
    {btn('first', 'К первому слайду', '<path d="M4 11l8-7 8 7v9a1 1 0 0 1-1 1h-5v-6h-4v6H5a1 1 0 0 1-1-1z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>')}
    {btn('prev', 'Предыдущий слайд', '<path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')}
    <span id="count" aria-live="polite">1 / 1</span>
    {btn('next', 'Следующий слайд', '<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')}
    <span class="sep"></span>
    {btn('theme', 'Светлая или темная тема (T)', '<g class="ic-sun"><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v2.5M12 19.5V22M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8 6 18M18 6l1.8-1.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></g><path class="ic-moon" d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>')}
    {btn('full', 'Во весь экран (F)', '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')}
  </nav>
</header>
<div class="progress" aria-hidden="true"><i id="progress"></i></div>

<main class="stage" id="stage">
{"".join(S)}</main>

<script src="../assets/deck.js?v={ver}"></script>
</body>
</html>
'''
(ROOT / 'present' / 'index.html').write_text(html, encoding='utf-8', newline='\n')
# Та же метка версии для главной и страницы маршрута - браузер не берет старые файлы из кэша
for f in ('index.html', 'roadmap.html'):
    p = ROOT / f
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'assets/site\.css(\?v=\w+)?"', f'assets/site.css?v={ver}"', s)
    s = re.sub(r'assets/deck\.js(\?v=\w+)?"', f'assets/deck.js?v={ver}"', s)
    p.write_text(s, encoding='utf-8', newline='\n')
print('слайдов:', len(S), 'версия:', ver)
