# Autotrain веб-приложение

Проект "autotrain_web" представляет собой веб-приложение, разработанное с использованием фреймворка Django.
Этот интерфейс позволяет пользователям загружать, обучать и управлять моделями машинного обучения в автоматическом режиме.

## Зависимости

Перед запуском проекта, убедитесь, что у вас установлены следующие компоненты:

- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

## Клонирование репозитория

Вы можете клонировать репозиторий проекта "autotrain_web" с помощью следующей команды:

```shell
git clone <URL репозитория>
```

## Запуск проекта

1. Перейдите в папку "autotrain_web" с помощью команды:

   ```shell
   cd autotrain_web
   ```

2. Создайте и запустите контейнеры с помощью docker-compose:

   ```shell
   docker-compose up -d
   ```

   Опция `-d` запускает контейнеры в фоновом режиме.

3. После успешного запуска контейнеров, вы можете открыть веб-браузер и перейти по следующему URL-адресу:

   ```
   http://localhost:8000
   ```

   Теперь вы должны увидеть ваше веб-приложение Django.
   
## Создание нового проекта
- На главной странице отображаются все проекты. Для создания нового проекта перейдите по ссылке
```
http://127.0.0.1:8000/create_project/
```
 или нажмите на кнопку "Создать проект" в верхнем меню.  
- После создания проекта загрузите файлы для обучения модели на странице 
```
http://127.0.0.1:8000/upload_files/
```
Или при нажатии на кнопку "Загрузить файлы" в верхнем меню

- После загрузки файлов вы перейдете на страницу настроек, в которой небоходимо будет загрузить файл классов формата .txt, а также конфигуграционные данные

## Дополнительная информация

- Файл `manage.py` является точкой входа для командной строки Django. Вы можете использовать его для запуска различных команд, связанных с проектом Django.
- Docker-файлы и `docker-compose.yml` в папке "autotrain_web" содержат конфигурацию для создания образа конт

ейнера и настройки сети и сервисов для вашего проекта.
- При необходимости, вы можете настроить порты и другие параметры в файле `docker-compose.yml` в соответствии с вашими потребностями.

## Вклад

Если вы обнаружили ошибки, проблемы или имеете предложения по улучшению проекта "autotrain_web", пожалуйста, создайте соответствующий Issue в репозитории или отправьте Pull Request с вашими изменениями.

## Лицензия

Проект "autotrain_web" лицензирован под [MIT License](LICENSE).
