-- Создаём роль-логин для приложения (без прав по умолчанию)
CREATE ROLE app_user
  LOGIN
  PASSWORD 'app_user_password'
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;

-- Создаём роль с правами (группа ролей)
CREATE ROLE app_role
  NOLOGIN
  NOSUPERUSER
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;

-- Назначаем роль-приложение пользователю
GRANT app_role TO app_user;
