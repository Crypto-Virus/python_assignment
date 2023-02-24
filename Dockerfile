# Use the official Python image as a parent image
FROM python:3.9

#Set the current working directory to /code
WORKDIR /code

# Copy the file with the requirements to the /code directory
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy required project files to /code directory
COPY ./get_raw_data.py /code/get_raw_data.py
COPY ./alphavantage /code/alphavantage
COPY ./financial /code/financial

# Expose port 8000 for the application
EXPOSE 5000

# Start the application
CMD ["uvicorn", "financial.main:app", "--host", "0.0.0.0", "--port", "5000"]