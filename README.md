# Jobrouter app

Веб-приложение для подбора вакансий по резюме.

![](./screencast.gif)

Быстрый запуск предсобранного докера:

1. Устанавливаем [докер](https://docs.docker.com/engine/install/)
2. Просим ключи от qdrant SaaS (`QDRANT_URL, QDRANT_KEY`)
3. `docker run --pull always -p 8001:80 -e QDRANT_URL=<url> -e QDRANT_KEY=<key> ghcr.io/trafficsurfer/jobrouter:latest`
4. Подождите, пока прогрузится модель для эмбеддингов

Приложение запущено:
- [http://localhost:8001/app](http://localhost:8001/app) (фронт),
- [http://localhost:8001/docs](http://localhost:8001/docs) (Swagger UI).

Технологии:

- Эмбеддинги: [sbert](https://www.sbert.net/) + [multilingual-e5-large](https://huggingface.co/intfloat/multilingual-e5-large)
- Векторная база данных: [qdrant SaaS](https://qdrant.tech/)
- Вспомогательное хранилище для текстов (обход ограничений qdrant free tier): SQLite
- Бекенд: FastAPI
- Фронтенд: astro + solidjs
- Линтеры: black + ruff + pre-commit

На проекте настрен CI/CD (GitHub Actions) для сборки и публикации сервиса в GitHub container registry.

## Локальный запуск

Клонируем репозиторий:

```sh
git clone https://github.com/trafficsurfer/jobrouter-app.git jobrouter
cd jobrouter
```

Устанавливаем зависимости:

```sh
poetry install
# Или без poetry:
# pip install --no-cache-dir --upgrade -r /app/requirements.txt
```

Собираем фронт:

```sh
cd front
npm ci
npm run build
```

Создаём файл `.env` и кладем в него `QDRANT_URL, QDRANT_KEY`

Запускаем приложение:

```sh
docker-compose up --build
```

## Разработка

Запускаем бек:

```sh
QDRANT_URL=<url> QDRANT_KEY=<key> poetry run uvicorn src.jobrouter_api.main:app --reload
```

Запускаем фронт с HMR:

```sh
cd front
npm run dev
```
