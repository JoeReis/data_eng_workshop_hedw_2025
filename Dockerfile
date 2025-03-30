# Use Python 3.12 as base image
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies and PostgreSQL
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    postgresql-client \
    wget \
    python3-distutils \
    python3-dev \
    python3-setuptools \
    unzip \
    vim \
    nano \
    less \
    netcat \
    libc6 \
    && rm -rf /var/lib/apt/lists/*

# Initialize PostgreSQL database
USER postgres
RUN /etc/init.d/postgresql start && \
    psql --command "CREATE USER root WITH SUPERUSER PASSWORD 'root';" && \
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" && \
    createdb -O docker docker && \
    createdb -O root root && \
    /etc/init.d/postgresql stop

# Configure PostgreSQL authentication
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/13/main/pg_hba.conf && \
    echo "listen_addresses='*'" >> /etc/postgresql/13/main/postgresql.conf

USER root

# Add PostgreSQL environment variables
ENV PGUSER=root \
    PGPASSWORD=root \
    PGDATABASE=root

# Install development tools
RUN pip install --no-cache-dir \
    black \
    flake8 \
    pylint \
    ipython

# Install DuckDB CLI
RUN if [ "$(uname -m)" = "aarch64" ]; then \
    wget https://github.com/duckdb/duckdb/releases/download/v1.2.1/duckdb_cli-linux-aarch64.zip && \
    unzip duckdb_cli-linux-aarch64.zip && \
    rm duckdb_cli-linux-aarch64.zip; \
    else \
    wget https://github.com/duckdb/duckdb/releases/download/v1.2.1/duckdb_cli-linux-amd64.zip && \
    unzip duckdb_cli-linux-amd64.zip && \
    rm duckdb_cli-linux-amd64.zip; \
    fi && \
    mv duckdb /usr/local/bin/ && \
    chmod +x /usr/local/bin/duckdb

# Add aliases for convenience
RUN echo 'alias duck="duckdb"\n\
    alias pg="psql"' >> /root/.bashrc

# Install Python packages and DuckDB CLI
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create DuckDB CLI alias
RUN echo 'alias duck="python3 -c \"import duckdb; duckdb.shell()\""' >> /root/.bashrc

# Create startup script
RUN echo '#!/bin/bash\n\
    \n\
    # Function to check if a port is available\n\
    check_port() {\n\
    nc -z localhost $1\n\
    return $?\n\
    }\n\
    \n\
    # Function to wait for a service\n\
    wait_for_service() {\n\
    local port=$1\n\
    local service=$2\n\
    local retries=60\n\
    while ! check_port $port; do\n\
    echo "Waiting for $service to be ready..."\n\
    retries=$((retries-1))\n\
    if [ $retries -eq 0 ]; then\n\
    echo "$service failed to start"\n\
    return 1\n\
    fi\n\
    sleep 2\n\
    done\n\
    echo "$service is ready!"\n\
    return 0\n\
    }\n\
    \n\
    echo "Starting PostgreSQL..."\n\
    service postgresql start\n\
    wait_for_service 5432 "PostgreSQL"\n\
    \n\
    echo "Starting Streamlit..."\n\
    if [ -f "/workspace/app.py" ]; then\n\
    streamlit run /workspace/app.py --server.address=0.0.0.0 &\n\
    else\n\
    echo "Welcome to the Data Stack!" > /app/app.py\n\
    streamlit run /app/app.py --server.address=0.0.0.0 &\n\
    fi\n\
    wait_for_service 8501 "Streamlit"\n\
    \n\
    echo "All services are running!"\n\
    echo "======================"\n\
    echo "Access your services at:"\n\
    echo "PostgreSQL: localhost:5432 (User: root, Password: root)"\n\
    echo "DuckDB: Use '\''duck'\'' command in terminal"\n\
    echo "Streamlit: localhost:8501"\n\
    echo "======================"\n\
    \n\
    # Monitor service logs\n\
    tail -f \\\n\
    /root/.streamlit/logs/*.log \\\n\
    2>/dev/null\n\
    ' > /start.sh \
    && chmod +x /start.sh

# Expose ports
EXPOSE 5432
EXPOSE 8501

# Set working directory
WORKDIR /app

# Command to run on container start
CMD ["/start.sh"]