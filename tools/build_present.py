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
    return f'<div class="device {cls}"><img src="../assets/app/{name}.webp" alt="" width="620" height="1342"></div>'

def phone(name):
    return f'<div class="sphone">{device(name)}</div>'

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
          <p class="lead">Свое приложение холдинга: что уже работает и куда идем — согласование, подпись ЭЦП, новые заявления, веб-портал.</p>
        </div>
      </div>
      <div class="fan" aria-hidden="true">
        {device('salary')}
        {device('vacation')}
        {device('home')}
      </div>''', 'band hero'))

# 2. О продукте
S.append(slide('about', 'О продукте', f'''<h2>Кабинет сотрудника</h2>
      <p class="intro">Мобильное приложение Ular для iOS и Android. Данные из 1С — зарплата, отпуск, пропуск, справки — у сотрудника в телефоне.</p>
      <div class="cards c3">
        {card('globe', 'Для всех', 'Без входа: новости компаний, калькулятор зарплаты и налогов, производственный календарь')}
        {card('user', 'Для сотрудников', 'Вход по ИИН: зарплата, отпуск, пропуск, скидки, заявления и справки')}
        {card('users', 'HR и администраторы', 'Данные по организации, пользователи и доступ, коды доступа сотрудникам')}
      </div>
      <p class="note">Свой продукт: бренд холдинга, наши серверы и доработки под наши процессы.</p>''', kick='О продукте'))

# 3. Зачем
qa = [('Сколько дней отпуска у меня осталось?', 'Остаток и история отпусков'),
      ('Сколько начислили и что удержали?', 'Начисления и удержания по месяцам'),
      ('Нужна справка с места работы', 'Заказ в приложении, готовый PDF на бланке'),
      ('Как оформить отпуск?', 'Заявление в пару касаний, статус в приложении'),
      ('Какие новости и скидки для сотрудников?', 'Лента новостей и скидки партнеров')]
rows = ''.join(f'<div class="qa-row"><span class="q">{q}</span><span class="arrow">{ico("route")}</span><span class="a">{a}</span></div>' for q, a in qa)
S.append(slide('why', 'Зачем', f'''<h2>Вопросы в кадры — ответы в телефоне</h2>
      <div class="qa"><div class="qa-head"><span>Сотрудник спрашивает</span><span></span><span>Приложение отвечает</span></div>{rows}</div>''', kick='Зачем'))

# 4. Сравнение
cmp = [('Бренд', 'Бренд поставщика', 'Бренд холдинга'),
       ('Доработки', 'По плану поставщика', 'Под наши процессы, когда нужно'),
       ('Где данные', 'Облако поставщика', 'Серверы холдинга'),
       ('Оплата', 'Подписка за каждого сотрудника', 'Своя разработка, без подписки'),
       ('Возможности холдинга', 'Типовой набор', 'Пропуск, скидки, калькулятор, новости')]
rows = ''.join(f'<div class="cmp-row"><span class="k">{k}</span><span class="o">{o}</span><span class="u">{ico("check")}{u}</span></div>' for k, o, u in cmp)
S.append(slide('compare', 'Сравнение', f'''<h2>Свой кабинет и платный сервис</h2>
      <div class="cmp"><div class="cmp-head"><span></span><span>Платный кабинет сотрудника</span><span>Кабинет сотрудника</span></div>{rows}</div>''', kick='Сравнение'))

# 5. Раздел
S.append(slide('part1', 'Что уже работает', '''<p class="num">01</p>
      <h2 class="big">Что уже работает</h2>
      <p class="lead">Приложение для iOS и Android, сервер на 1С и инструменты администратора</p>''', 'band divider'))

def split(sid, title, kick, h, points, ph):
    pts = ''.join(f'<li><span class="ci">{ico(i)}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, t, d in points)
    return slide(sid, title, f'''<div class="split"><div><h2>{h}</h2><ul class="points">{pts}</ul></div>{phone(ph)}</div>''', kick=kick)

# 6-10. Возможности с экранами
S.append(split('nologin', 'Без входа', 'Без входа', 'Полезно с первой минуты', [
    ('news', 'Новости холдинга', 'Посты с картинками от компаний холдинга'),
    ('calc', 'Калькулятор налогов РК', 'ИП и ТОО, прямой и обратный расчет'),
    ('cal', 'Производственный календарь', 'Праздники и переносы')], 'news'))
S.append(split('home', 'Главный экран', 'После входа по ИИН', 'Все важное на главном экране', [
    ('sun', 'Стаж, отпуск, зарплата', 'Видно сразу при открытии'),
    ('user', 'Профиль', 'Личные и рабочие данные'),
    ('users', 'Для всех компаний холдинга', 'Один вход по ИИН, где бы вы ни работали')], 'home'))
S.append(split('salary', 'Зарплата и отпуск', 'Зарплата и отпуск', 'Без вопросов в бухгалтерию и кадры', [
    ('wallet', 'Расчетный листок', 'Начисления и удержания по месяцам, можно скачать PDF'),
    ('db', 'Данные из 1С:ЗУП', 'Берутся в момент открытия — без копий и расхождений'),
    ('cal', 'Остаток отпуска', 'Сколько дней осталось и вся история отпусков')], 'salary'))
S.append(split('pass', 'Пропуск и скидки', 'Пропуск и скидки', 'Пропуск и скидки всегда с собой', [
    ('id', 'Электронный пропуск', 'Фото, организация, должность, номер и срок действия'),
    ('tag', 'Скидки у партнеров', 'Магазины и сервисы по категориям, экран на кассе'),
    ('user', 'Профиль', 'Свое фото для пропуска и профиля')], 'pass'))
S.append(slide('requests', 'Заявления и справки', f'''<h2>Заявления и справки — из приложения</h2>
      <div class="cards c3 steps3">
        {card('file', 'Подайте', 'Заявление на отпуск или заказ справки в пару касаний')}
        {card('route', 'Следите за статусом', 'На согласовании, согласовано или отклонено с причиной')}
        {card('x', 'Передумали?', 'Отмените, пока заявление не оформлено')}
      </div>
      <div class="cards c3">
        {card('file', 'Справка с места работы', 'Обычная или с указанием зарплаты')}
        {card('shield', 'Официальный бланк', 'С номером, печатью и подписью')}
        {card('download', 'Готовый PDF в телефоне', 'Скачайте или отправьте туда, где нужна справка')}
      </div>''', kick='Заявления и справки'))

# 11. Экраны
figs = ''.join(f'<figure>{device(n)}<figcaption>{c}</figcaption></figure>' for n, c in
               (('home', 'Главная'), ('salary', 'Зарплата'), ('vacation', 'Отпуск'), ('pass', 'Пропуск'), ('profile', 'Профиль'),
                ('news', 'Новости'), ('notifications', 'Уведомления'), ('calculator', 'Калькулятор'), ('calendar', 'Календарь')))
S.append(slide('screens', 'Экраны', f'''<h2>Как это выглядит</h2>
      <div class="strip" tabindex="0" aria-label="Экраны приложения">{figs}</div>''', kick='Экраны'))

# 12. Как устроено
S.append(slide('arch', 'Как устроено', f'''<h2>Приложение, сервер и 1С:ЗУП</h2>
      <div class="flow3">
        <div class="node">{ico('phone')}<b>Приложение Ular</b><p>iOS и Android. Вход по ИИН, на телефоне хранится только ключ доступа</p></div>
        <span class="link"></span>
        <div class="node main">{ico('server')}<b>Кабинет сотрудника</b><p>Сервер на 1С: единый вход и проверки. Сам ведет калькулятор, календарь, новости и скидки</p></div>
        <span class="link"></span>
        <div class="node">{ico('db')}<b>1С:ЗУП организаций</b><p>Зарплата, отпуска, сотрудники — в базе каждой организации</p></div>
      </div>
      <div class="cards c2">
        {card('route', 'Одна точка входа для холдинга', 'Сервер сам направляет запрос в базу ЗУП нужной организации')}
        {card('swap', 'Гибкие подключения', 'Новая организация подключается настройкой, без доработки приложения')}
      </div>''', kick='Как устроено'))

# 13. Безопасность
S.append(slide('security', 'Безопасность', f'''<h2>Доступ под контролем</h2>
      <div class="cards c3">
        {card('key', 'Код доступа от кадров', 'Зарегистрироваться можно только с личным кодом из отдела кадров')}
        {card('face', 'Код и биометрия', 'Повторный вход по короткому коду, Face ID или отпечатку')}
        {card('lock', 'Короткие сессии', 'Ключ доступа живет недолго и обновляется сам')}
        {card('users', 'Уволенные отключаются', 'Доступ закрывается автоматически, без участия администратора')}
        {card('log', 'Журнал безопасности', 'Неверные пароли и попытки подбора фиксируются')}
        {card('shield', 'Данные в 1С холдинга', 'Ничего не хранится у сторонних сервисов')}
      </div>''', kick='Безопасность'))

# 14. HR и администраторы
S.append(slide('admin', 'Для HR и администраторов', f'''<h2>Инструменты, которые уже есть</h2>
      <div class="cards c3">
        {card('users', 'Сотрудники и отпуска', 'Данные по организации, кадровые документы, структура холдинга')}
        {card('monitor', 'Панель администратора', 'Видно ровно то, что видит сотрудник в приложении')}
        {card('key', 'Коды доступа', 'Выдача и перевыпуск кодов для регистрации и восстановления пароля')}
        {card('server', 'Подключения к ЗУП', 'Общие для организации и отдельные для сотрудника')}
        {card('megaphone', 'Новости и партнеры', 'Публикация новостей, уведомлений и скидок для сотрудников')}
        {card('download', 'Установка', 'Памятка с QR-кодами приложения для новых сотрудников')}
      </div>''', kick='Для HR и администраторов'))

# 15. Раздел
S.append(slide('part2', 'Что планируется', '''<p class="num">02</p>
      <h2 class="big">Что планируется</h2>
      <p class="lead">Согласование в телефоне, подпись ЭЦП, новые виды заявлений, роли и веб-портал</p>''', 'band divider'))

# 16. Согласование
steps = [('Заявление', 'создает сотрудник'), ('Согласование', 'руководители'), ('Кадры', 'проверка и оформление'), ('Директор', 'подписывает ЭЦП')]
st = ''.join(f'<li><span class="sn">{i}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(steps, 1))
S.append(slide('approval', 'Согласование', f'''<h2>Согласование заявлений и документов</h2>
      <ol class="chain">{st}</ol>
      <div class="cards c3">
        {card('phone', 'В телефоне — дополнительно', 'Руководитель может согласовать в приложении, основное место согласования остается в 1С:Документообороте')}
        {card('x', 'Отказ с причиной', 'Причина обязательна и приходит сотруднику')}
        {card('swap', 'Замещение', 'На время отпуска руководителя согласует заместитель')}
      </div>''', kick='В плане'))

# 17. ЭЦП
S.append(slide('esign', 'Подпись ЭЦП', f'''<h2>Подпись ЭЦП — у документа официальная сила</h2>
      <p class="intro">Приказы и кадровые документы подписываются электронной цифровой подписью в 1С:Документообороте. Подписанный документ имеет юридическую силу — без бумаги и визитов в кадры.</p>
      <div class="cards c3">
        {card('key', 'Каждый своим ключом', 'Участники маршрута и директор подписывают своей ЭЦП')}
        {card('shield', 'Подпись проверяема', 'Кто и когда подписал, хранится вместе с документом')}
        {card('phone', 'eGov Mobile', 'Рассматриваем подпись итоговых документов в телефоне')}
      </div>''', kick='В плане'))

# 18. Роли и веб-портал
S.append(slide('roles', 'Роли и веб-портал', f'''<h2>Роли и веб-портал</h2>
      <div class="cards c3">
        {card('megaphone', 'Маркетолог', 'Новости и посты с картинками, партнеры и скидки')}
        {card('users', 'Кадры', 'Заявления и справки сотрудников, отчеты')}
        {card('monitor', 'Администратор', 'Пользователи и пароли, подключения к ЗУП, журнал безопасности')}
        {card('route', 'Руководитель подразделения', 'Согласует заявления своего подразделения')}
        {card('file', 'Делопроизводитель', 'Регистрационный номер документов')}
        {card('key', 'Директор', 'Подписывает документы организации')}
      </div>
      <p class="note">Один вход по ИИН и паролю — набор разделов зависит от роли.</p>''', kick='В плане'))

# 19. Маршрут
S.append(slide('route-slide', 'Маршрут развития', '''<h2>Маршрут развития</h2>
      <div id="route" class="route"></div>''', 'route-slide'))

# 20. Как начать
S.append(slide('start-using', 'Как начать', f'''<h2>Регистрация за пару минут</h2>
      <ol class="chain c3">
        <li><span class="sn">1</span><b>Получите код доступа</b><p>В отделе кадров, на памятке вместе с QR-кодами</p></li>
        <li><span class="sn">2</span><b>Установите Ular</b><p>Из App Store или Google Play по QR-коду</p></li>
        <li><span class="sn">3</span><b>Введите ИИН и код</b><p>Придумайте пароль, дальше вход по коду или Face ID</p></li>
      </ol>
      <div class="cards c2">
        {card('key', 'Забыли пароль?', 'Восстановите его тем же кодом доступа, звонить в кадры не нужно')}
        {card('x', 'Потеряли код?', 'Отдел кадров выдаст новый, старый перестанет действовать')}
      </div>''', kick='Как начать'))

# 21. Финал
S.append(slide('end', 'Скачать', f'''<div class="finale-grid">
        <div class="finale-text">
          <h2 class="big">Меньше вопросов в кадры. Меньше бумаги.</h2>
          <p class="lead">Сотрудник сам видит свои данные, кадры настраивают процессы у себя, документы подписываются ЭЦП.</p>
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
    {btn('theme', 'Светлая или темная тема (T)', '<circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v2.5M12 19.5V22M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8 6 18M18 6l1.8-1.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>')}
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
