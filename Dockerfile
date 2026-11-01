FROM postgres:16

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=appdb

# Optional: scripts in this folder run automatically on first startup
# COPY ./init/ /docker-entrypoint-initdb.d/

EXPOSE 5432