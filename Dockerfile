# Use official Python image
FROM python:3.9-slim

# Install Tesseract OCR
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose port (Streamlit default port is 8501)
EXPOSE 8501

# Start Streamlit app
CMD ["streamlit", "run", "oi_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
