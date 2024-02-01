FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=Jon15SgqPwkdaw1HKwwps1
ENV MYSQL_DATABASE=bank
ENV MYSQL_USER=mati
ENV MYSQL_PASSWORD=Jon15SgqPwkdaw1HKwwps1

COPY init.sql /docker-entrypoint-initdb.d

EXPOSE 3306

CMD ["mysqld"]

