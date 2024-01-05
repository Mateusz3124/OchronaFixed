FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=Jon15SgqPwkdaw1HKwwps1
ENV MYSQL_DATABASE=bank
ENV MYSQL_USER=mati
ENV MYSQL_PASSWORD=Jon15SgqPwkdaw1HKwwps1

# Copy SQL scripts to initialize the database
COPY init.sql /docker-entrypoint-initdb.d

# Expose the MySQL port
EXPOSE 3306

# Start MySQL service
CMD ["mysqld"]

