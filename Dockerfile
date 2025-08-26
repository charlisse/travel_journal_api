# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose Flask default port
EXPOSE 5000

# Run the app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
