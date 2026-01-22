-- Создаём БД для приложения
CREATE DATABASE app_db
  OWNER postgres
  ENCODING UTF8
  LC_COLLATE 'C'
  LC_CTYPE 'C'
  TEMPLATE template0;

-- Даём права на подключение к БД
GRANT CONNECT ON DATABASE app_db TO app_role;

-- Даём права на использование БД (подключение + временные таблицы)
GRANT USAGE ON SCHEMA public TO app_role;
GRANT CREATE ON SCHEMA public TO app_role;

-- Права на все таблицы/последовательности/функции в public (будущие тоже)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_role;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_role;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO app_role;

-- Автоматически для новых объектов
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO app_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO app_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO app_role;
