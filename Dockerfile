# 1. Use an official, lightweight Python runtime as a base image
FROM python:3.11-slim

# 2. Set environment variables to optimize Python inside the container
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk
# PYTHONUNBUFFERED: Forces standard output streams to print instantly (crucial for seeing logs live!)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies if needed (SQLite is built into Python, so we stay lightweight)
# We copy requirements first to leverage Docker's build caching layer
COPY requirements.txt /app/

# 5. Install Python library dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your local application code into the container
COPY . /app/

# 7. Expose port 8000 so the container can accept inbound network requests
EXPOSE 8000

# 8. Command to run the application using python -m uvicorn to guarantee module execution
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]