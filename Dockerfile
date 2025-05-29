FROM python:3.13-slim


ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Entrypoint
CMD ["python", "bot.py"]