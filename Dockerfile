FROM python:3.12-slim

# Install necessary tools and libraries
RUN apt-get update && apt-get install -y \
    sqlite3 libsqlite3-dev && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port and set entrypoint
EXPOSE 8501
CMD ["streamlit", "run", "main.py"]
