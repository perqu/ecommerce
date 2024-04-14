## Simple Django REST API template with Postgres

Example of implementations a simple Django REST API with Postgress DB, Knox tokens, basic permissions, pagination and throttles.

## Docker-compose configuration

- `app`: Django app - Web server
- `postgres`: RDBMS

## How to run the project

1. Clone the repository
2. Install docker
3. install poetry env
4. convert .envexample to .env and update your data
5. Run `docker compose build`
6. Run `docker compose up`
7. Migrations
8. Open http://0.0.0.0:8888 in your browser to see the Swagger UI
