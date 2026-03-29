version: '3'

services:
  db:
    image: mariadb:10.6
    restart: always
    environment:
      - MYSQL_ROOT_PASSWORD=[REDACTED_SECURE_PASSWORD]
      - MYSQL_PASSWORD=[REDACTED_SECURE_PASSWORD]
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
    volumes:
      - nextcloud_db:/var/lib/mysql

  app:
    image: nextcloud:latest
    restart: always
    ports:
      - 8085:80
    depends_on:
      - db
    volumes:
      # 1. Nextcloud is stayin on ssd
      - nextcloud_data:/var/www/html
      # 2.they go to hard drive
      - /mnt/nextcloud_data:/var/www/html/data
    environment:
      - MYSQL_PASSWORD=[REDACTED_SECURE_PASSWORD]
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud
      - MYSQL_HOST=db

volumes:
  nextcloud_db:
  nextcloud_data:
