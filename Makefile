.PHONY: up down logs simulate clean

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

simulate:
	docker compose run --rm simulator

clean:
	docker compose down -v
