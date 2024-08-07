# DRF_HW1

            ДЗ 24.1
1. Создан новый Django-проект DRF_HW1, подключены DRF в настройках проекта.
2. Добавлены Приложения Users, Education (модели курс и урок)
3. Для реализации CRUD для курса использован Viewsets, а для урока - Generic-классы
(получение списка, получение одной сущности, создание, изменение и удаление).
Для работы контроллеров описаны простейшие сериализаторы.
4. Реализован эндпоинт для создания, редактирования профиля любого пользователя на основе Generic.

            ДЗ 24.2
1. Для модели курса добавлен в сериализатор поле вывода количества уроков.
   (Поле реализовано с помощью SerializerMethodField())
2. Добавлена новая модель в приложение users: Payment
   (данные в табл payment БД заполнены через фикстуру payment.json)
3. В сериализатор для модели курса добавлено поле вывода уроков.
   (Вывод реализован с помощью сериализатора для связанной модели LessonSerializer)
4. Настроена фильтрация для эндпоинта вывода списка платежей с возможностями:
   (менять порядок сортировки по дате оплаты,
   фильтровать по курсу или уроку,
   фильтровать по способу оплаты)
5. Для профиля пользователя добавлена возможность вывода истории платежей
   (расширен сериализатор UserSerializer полем для вывода списка платежей)

          ДЗ.25.1
1. Настроена в проекте использование JWT-авторизации и закрыт каждый эндпоинт авторизацией.
   (Эндпоинты для авторизации и регистрации доступны для неавторизованных пользователей)
2. Создана группу модераторов с правами работы с любыми уроками и курсами, 
но без возможности их удалять и создавать новые. Заложен функционал такой проверки в контроллеры.
3. Описаны права доступа для объектов таким образом, чтобы пользователи, которые не входят в группу модераторов, 
могли видеть, редактировать и удалять только свои курсы и уроки.
4. Для профиля пользователя введены ограничения: авторизованный пользователь может просматривать любой профиль, 
но редактировать только свой. При этом для просмотра чужого профиля доступна только общая информация, 
в которую не входят: пароль, фамилия, история платежей.

         ДЗ.25.2
1. Для сохранения уроков и курсов реализована дополнительная проверка на отсутствие в материалах 
ссылок на сторонние ресурсы, кроме youtube.com. То есть ссылки на видео можно прикреплять в материалы, 
а ссылки на сторонние образовательные платформы или личные сайты — нельзя.
2. Добавлена модель подписки на обновления курса для пользователя. Реализован эндпоинт для установки 
подписки пользователя и на удаление подписки у пользователя. При выборке данных по курсу пользователь видит инфо
о своих подписках на курс.
3. Реализована пагинацию для вывода всех уроков и курсов.
4. Написаны тесты, которые проверяют корректность работы CRUD уроков и функционал работы подписки на обновления курса.
Результат проверки покрытия тестами сохранен в файле test_coverage.html
5. Написаны тесты на все имеющиеся эндпоинты в проекте.

       ДЗ.26.1
1. Подключен и настроен вывод документации для проекта с помощью библиотеки **drf-yasg** 
2. Подключена возможность оплаты курсов и уроков через https://stripe.com/docs/api.
3. Реализована проверка статуса платежа (оплачен/не оплачен).

       ДЗ.26.2
1. Настроен проект для работы с Celery и с celery-beat
2. 1. Добавлена асинхронная рассылка писем пользователям об обновлении материалов курса
2. 2. Пользователь может обновлять каждый урок курса отдельно (если на курс есть подписка). 
Добавлена проверку на то, что уведомление отправляется только в том случае, 
если курс не обновлялся более четырех часов.
3. С помощью celery-beat реализована фоновая задача, которая будет проверять пользователей 
по дате последнего входа (по полю last_login) и, если пользователь не заходил более месяца, 
блокировать его с помощью флага is_active.

         ДЗ.27.2
1. Оформлен Dockerfile для запуска контейнера с проектом.
2. Оформлен файл docker-compose.yaml для запуска приложения, состоящего из следующих контейнеров:
проект DRF_HW1, БД PostgreSQL, Redis, Celery
3. внесены изменения в файл config/settings.py и .env (образец для заполнения .env.sample)
4. Запуск развернутого приложения на машине с Docker осуществляется командой: 
   `docker-compose up --build`
