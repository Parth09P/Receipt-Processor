FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Set the working directory to /app
WORKDIR /app

# Copy the contents of the local src directory to /app in the container
COPY ./ /app

RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
