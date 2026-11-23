# Слайды 2-18 презентации: подключается из build_present.py (exec), использует slide/card/ico/phone/device.
def bubble(q, a, k):
    return f'''<div class="chat" style="--k:{k}">
          <div class="bub q">{q}</div>
          <div class="bub a"><span class="who">Кабинет сотрудника</span>{a}</div>
        </div>'''

# 2. О продукте - крупное утверждение по центру и три аудитории
S.append(slide('about', 'О продукте', f'''<h2 class="mega">Ответы на кадровые вопросы — в телефоне сотрудника</h2>
      <div class="trio">
        <div><span class="bigi">{ico('globe')}</span><b>Для всех</b><p>Новости и калькулятор без входа</p></div>
        <div><span class="bigi">{ico('user')}</span><b>Для сотрудников</b><p>Зарплата, отпуск, пропуск, справки</p></div>
        <div><span class="bigi">{ico('users')}</span><b>Для отдела кадров</b><p>Доступ, коды, данные организации</p></div>
      </div>''', 'center'))

# 3. Зачем - переписка
S.append(slide('why', 'Зачем', f'''<h2 class="mega">Вопрос в отдел кадров —<br>ответ в приложении</h2>
      <div class="chats">
        {bubble('Сколько дней отпуска у меня осталось?', '18,5 дня. История отпусков — в разделе «Отпуск»', 0)}
        {bubble('Нужна справка с места работы', 'Заказ в приложении, готовый PDF на бланке', 1)}
        {bubble('Сколько начислили и что удержали?', 'Начисления и удержания по месяцам, листок в PDF', 2)}
      </div>''', 'center'))

# 4. Сравнение - две карточки
S.append(slide('compare', 'Сравнение', f'''<h2 class="mega">Свой кабинет вместо подписки</h2>
      <div class="versus">
        <div class="vs-card dim"><p class="vs-t">Платный сервис</p>
          <ul><li>{ico('x')}Бренд поставщика</li><li>{ico('x')}Доработки по плану поставщика</li><li>{ico('x')}Данные в облаке поставщика</li><li>{ico('x')}Подписка за каждого сотрудника</li></ul></div>
        <div class="vs-card hot"><p class="vs-t">Кабинет сотрудника</p>
          <ul><li>{ico('check')}Бренд холдинга</li><li>{ico('check')}Доработки под наши процессы</li><li>{ico('check')}Данные на серверах холдинга</li><li>{ico('check')}Без подписки</li></ul></div>
      </div>''', 'center'))

# 5. Раздел
S.append(slide('part1', 'Что уже работает', '''<div class="div-fan" aria-hidden="true"><i style="--i:0"></i><i style="--i:1"></i><i style="--i:2"></i><i style="--i:3"></i><i style="--i:4"></i><i style="--i:5"></i><i style="--i:6"></i></div>
      <p class="num">01</p>
      <h2 class="big">Что уже работает</h2>
      <p class="lead">Приложение, учет организаций, инструменты отдела кадров</p>''', 'band divider'))

def split(sid, title, kick, h, points, ph):
    pts = ''.join(f'<li><span class="ci">{ico(i)}</span><div><b>{t}</b><p>{d}</p></div></li>' for i, t, d in points)
    return slide(sid, title, f'''<div class="split"><div><h2>{h}</h2><ul class="points">{pts}</ul></div>{phone(ph)}</div>''')

S.append(split('nologin', 'Без входа', 'Без входа', 'Полезно с первой минуты', [
    ('news', 'Новости компаний', 'Посты с картинками'),
    ('calc', 'Калькулятор налогов РК', 'ИП и ТОО, прямой и обратный расчет'),
    ('cal', 'Производственный календарь', 'Праздники и переносы')], 'news'))
S.append(split('home', 'Главный экран', 'После входа по ИИН', 'Все важное — на главном экране', [
    ('sun', 'Стаж, отпуск, зарплата', 'Видно сразу при открытии'),
    ('user', 'Профиль', 'Личные и рабочие данные'),
    ('users', 'Все компании холдинга', 'Один вход по ИИН')], 'home'))
S.append(split('salary', 'Зарплата и отпуск', 'Зарплата и отпуск', 'Без вопросов в бухгалтерию', [
    ('wallet', 'Расчетный листок', 'По месяцам, можно скачать PDF'),
    ('db', 'Данные из учета', 'В момент открытия, без копий'),
    ('cal', 'Остаток отпуска', 'И вся история отпусков')], 'salary'))
S.append(split('pass', 'Пропуск и скидки', 'Пропуск и скидки', 'Пропуск и скидки всегда с собой', [
    ('id', 'Электронный пропуск', 'Фото, должность, номер, срок'),
    ('tag', 'Скидки у партнеров', 'Покажите экран на кассе'),
    ('user', 'Профиль', 'Свое фото для пропуска')], 'pass'))

# 10. Заявления - путь заявления статусами + справка
S.append(slide('requests', 'Заявления и справки', f'''<h2 class="mega">Заявления и справки в приложении</h2>
      <div class="status-line">
        <div class="st"><span class="pill gray">Подано</span><p>Сотрудник подает заявление</p></div>
        <span class="st-link"></span>
        <div class="st"><span class="pill sun">На согласовании</span><p>Руководитель, отдел кадров, директор</p></div>
        <span class="st-link"></span>
        <div class="st"><span class="pill green">Согласовано</span><p>Уведомление сотруднику</p></div>
      </div>
      <div class="trio small">
        <div><span class="bigi">{ico('file')}</span><b>Справка с места работы</b><p>С указанием зарплаты или без</p></div>
        <div><span class="bigi">{ico('shield')}</span><b>Официальный бланк</b><p>Номер, печать, подпись</p></div>
        <div><span class="bigi">{ico('download')}</span><b>Документ в PDF</b><p>Скачать или отправить</p></div>
      </div>''', 'center'))

# 11. Экраны
figs = ''.join(f'<figure>{device(n)}<figcaption>{c}</figcaption></figure>' for n, c in
               (('home', 'Главная'), ('salary', 'Зарплата'), ('vacation', 'Отпуск'), ('pass', 'Пропуск'), ('profile', 'Профиль'),
                ('news', 'Новости'), ('notifications', 'Уведомления'), ('calculator', 'Калькулятор'), ('calendar', 'Календарь')))
S.append(slide('screens', 'Экраны', f'''<h2 class="mega">Как это выглядит</h2>
      <div class="strip" tabindex="0" aria-label="Экраны приложения">{figs}</div>''', 'center'))

# 12. Как устроено - веер подключений к нескольким организациям
orgs = ['Организация 1', 'Организация 2', 'Организация 3', 'Организация 4', 'Новая организация']
paths = ''.join(f'<path class="wire{" new" if i == 4 else ""}" d="M560 260 C 720 260, 760 {70 + i * 95}, 900 {70 + i * 95}"/>' for i in range(5))
org_html = ''.join(f'<div class="org{" new" if i == 4 else ""}" style="top:{70 + i * 95}px">{ico("db")}<b>{o}</b>{"<span>подключается настройкой</span>" if i == 4 else "<span>своя база 1С:ЗУП</span>"}</div>' for i, o in enumerate(orgs))
S.append(slide('arch', 'Как устроено', f'''<h2 class="mega">Один вход — все компании холдинга</h2>
      <div class="hub">
        <svg class="wires" viewBox="0 0 1180 520" preserveAspectRatio="none" aria-hidden="true">
          <path class="wire" d="M250 260 L 400 260"/>{paths}
        </svg>
        <div class="hub-app">{ico('phone')}<b>Ular</b><span>iOS и Android</span></div>
        <div class="hub-core">{ico('server')}<b>Кабинет сотрудника</b><span>Единый вход и проверки,<br>новости, скидки, калькулятор</span></div>
        {org_html}
      </div>''', 'center'))

# 13. Безопасность - темный слайд
S.append(slide('security', 'Безопасность', f'''<h2 class="mega">Доступ под контролем</h2>
      <div class="glow-row">
        <div>{ico('key')}<b>Код доступа</b><p>Регистрация по личному коду</p></div>
        <div>{ico('face')}<b>Face ID и код</b><p>Быстрый и защищенный вход</p></div>
        <div>{ico('users')}<b>Уволенные</b><p>Доступ закрывается сам</p></div>
        <div>{ico('log')}<b>Журнал</b><p>Попытки подбора видны</p></div>
      </div>''', 'center dark'))

# 14. Для кадров
S.append(slide('admin', 'Для отдела кадров и администраторов', f'''<h2 class="mega">Инструменты для отдела кадров</h2>
      <div class="trio four">
        <div><span class="bigi">{ico('key')}</span><b>Коды доступа</b><p>Выдача и перевыпуск</p></div>
        <div><span class="bigi">{ico('monitor')}</span><b>Глазами сотрудника</b><p>Как в приложении</p></div>
        <div><span class="bigi">{ico('megaphone')}</span><b>Новости и партнеры</b><p>Публикация для сотрудников</p></div>
        <div><span class="bigi">{ico('download')}</span><b>Памятка с QR</b><p>Для новых сотрудников</p></div>
      </div>''', 'center'))

# 15. Раздел
S.append(slide('part2', 'Что планируется', '''<div class="div-fan" aria-hidden="true"><i style="--i:0"></i><i style="--i:1"></i><i style="--i:2"></i><i style="--i:3"></i><i style="--i:4"></i><i style="--i:5"></i><i style="--i:6"></i></div>
      <p class="num">02</p>
      <h2 class="big">Что планируется</h2>
      <p class="lead">Согласование, ЭЦП, новые заявления, веб-портал</p>''', 'band divider'))

# 16. Согласование - 4 шага и 4 карточки ровно под ними
steps = [('Заявление', 'подает сотрудник'), ('Руководители', 'согласование по маршруту'), ('Отдел кадров', 'проверка и оформление'), ('Директор', 'подписание ЭЦП')]
st = ''.join(f'<li><span class="sn">{i}</span><b>{t}</b><p>{d}</p></li>' for i, (t, d) in enumerate(steps, 1))
S.append(slide('approval', 'Согласование', f'''<h2 class="mega">Согласование — в телефоне</h2>
      <ol class="chain g4">{st}</ol>
      <div class="cards g4">
        {card('route', 'Статус в приложении', 'Этап согласования виден сотруднику')}
        {card('phone', 'Дополнительный канал', 'Основное место — 1С:Документооборот')}
        {card('x', 'Отказ с причиной', 'Причина доводится до сотрудника')}
        {card('swap', 'Замещение', 'В отсутствие руководителя — заместитель')}
      </div>''', 'center'))

# 17. ЭЦП - темный слайд с крупным образом
S.append(slide('esign', 'Подпись ЭЦП', f'''<h2 class="mega">У документа — официальная сила</h2>
      <div class="glow-row three">
        <div>{ico('key')}<b>Своим ключом</b><p>Каждый участник маршрута</p></div>
        <div>{ico('check')}<b>Проверяемо</b><p>Кто и когда подписал</p></div>
        <div>{ico('phone')}<b>eGov Mobile</b><p>Рассматриваем</p></div>
      </div>''', 'center dark'))

# 18. Роли и веб-портал
roles = [('megaphone', 'Маркетолог'), ('users', 'Отдел кадров'), ('monitor', 'Администратор'), ('route', 'Руководитель'), ('file', 'Делопроизводитель'), ('key', 'Директор')]
S.append(slide('roles', 'Роли и веб-портал', f'''<h2 class="mega">Каждому — свои разделы</h2>
      <div class="role-chips">{''.join(f'<span style="--k:{k}">{ico(i)}{n}</span>' for k, (i, n) in enumerate(roles))}</div>''', 'center'))
