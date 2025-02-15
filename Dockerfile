FROM python:3.11-slim

WORKDIR /app

# Upgrade pip and install dependencies with increased timeout
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --default-timeout=100 \
    streamlit==1.31.0 \
    pandas==2.1.3 \
    plotly==5.18.0 \
    numpy==1.26.2

# Copy only necessary files
COPY app/ ./app/
COPY data/ ./data/

EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app/frontend/main.py", "--server.address", "0.0.0.0", "--server.port", "8501"]