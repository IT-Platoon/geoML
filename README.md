# geoML

Для запуска создайте ``.env`` файл с переменными из ``.env.sample``

Запуск:
```
docker-compose up --build
```

Для следующих команд требуется установленный poetry и используемое виртуальное окружение:
```
poetry shell
```

Запуск линтеров в проекте:
```
make lint
```

Запуск форматтеров в проекте:
```
make format
```

Очистка докер контейнеров в проекте:
```
make docker-clean
```
