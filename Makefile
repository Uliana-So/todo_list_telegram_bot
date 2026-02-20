all:	up

up:
	docker-compose up --build

down:
	docker-compose down -v

stop:
	docker-compose stop

rm:
	docker-compose rm -s -v -f
	docker volume rm srcs_postgresql
	docker volume rm srcs_media
	docker volume rm srcs_static

clean:	rm

fclean:	stop clean

.PHONY:	all up down stop rm clean fclean