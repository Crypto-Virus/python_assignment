# Use the official Python image as a parent image
FROM python:3.9

#Set the current working directory to /code.
WORKDIR /code

# Copy the file with the requirements to the /code directory.
COPY requirements.txt requirements.txt

# Install the package dependencies in the requirements file.
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the ./financial directory inside the /code directory.
COPY ./financial /code/app

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]