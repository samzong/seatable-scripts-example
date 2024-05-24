# Use a smaller base image
FROM python:3.11-slim as builder

LABEL maintainer="samzong.lu@gmail.com"

WORKDIR /app

# Install Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get remove -y curl && apt-get autoremove -y && \
    ln -s $HOME/.local/bin/poetry /usr/local/bin/poetry

# Copy project files
COPY . .

# Install project dependencies
RUN poetry install --only main --no-cache --no-root


# Start a new stage
FROM python:3.11-slim

# Copy only the necessary files from the previous stage
COPY --from=builder /app .

# Expose port
EXPOSE 5000

# Start the project
CMD ["poetry", "run", "uvicorn", "main:app" ,"--host", "0.0.0.0", "--port", "5000"]
