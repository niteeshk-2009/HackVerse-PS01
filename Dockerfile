FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose port
EXPOSE 8000

ENV HOST=0.0.0.0
ENV PORT=8000
ENV DATA_MODE=DEMO

CMD ["python", "run.py"]
