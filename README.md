### Installation prerequisites
1. Docker, docker-compose

### Installation
```
cp .env.template .env
```
```
docker-compose build
```
```
docker-compose up -d
```
```
docker-compose exec hyper python manage.py migrate
```