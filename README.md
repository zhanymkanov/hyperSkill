### Installation prerequisites
1. Docker, docker-compose

### Installation
1. Setup environ
```
cp .env.template .env
```
2. Build images
```
docker-compose build
```
3. Run the app
```
docker-compose up -d
```
4. Run migrations
```
docker-compose exec hyper python manage.py migrate
```
### Database Population
Script automatically populate DB every 2-5 seconds, so you can comment out `hyper_populate` service if it is not required

### Clickhouse Playground
1. Run clickhouse-client
```
docker-compose exec clickhouse-client clickhouse-client --host clickhouse
```
2. Copy-paste SQL from sql/date_action_users.sql
3. Try any other queries 
