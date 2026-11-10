FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE skip_trace_cli.py mcp_server.py ./
RUN chmod +x mcp_server.py skip_trace_cli.py

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "mcp_server.py"]
