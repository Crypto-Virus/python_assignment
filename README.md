# G123 Python Assignment Solution

This repository contains solutions for G123 Python backend position assignment.

**Note: This expects that docker is installed and running on your machine**


## Installation
Open up a terminal and use git to clone repository locally onto your machine

```bash
git clone https://github.com/Crypto-Virus/python_assignment.git
```

## Running the API service and database

Change directory to **python_assignment** which you have just cloned
```bash
cd python_assignment
```

Build and run docker container with the below command

```bash
docker-compose up
```

### Task 1
Since we are using sqlite database. The `get_raw_data.py` script must be executed from within the container shell. This is because it needs direct access to the file.

**Note: An alternative to this is to create new API endpoint to write to database so when don't have to execute command from within container shell**

To execute command in container we can use `docker exec -it <container name> <command>`

First open up a new terminal and type the below to access shell of running docker container
```bash
docker exec -it python-assignment-app-1 bash
```
Add Alphaadvantage API_KEY to environment variable
```bash
export API_KEY=<your-key-goes-here>
```

Execute `get_raw_data.py`
```bash
python get_raw_data.py
```

### Task2

Open up a new terminal and execute curl commands to test API service
```bash
curl -X GET 'http://localhost:5000/api/financial_data?start_date=2023-01-01&end_date=2023-01-14&symbol=IBM&limit=3&page=2'

```
```bash
curl -X GET 'http://localhost:5000/api/statistics?start_date=2023-01-01&end_date=2023-01-31&symbol=IBM'

```

## Libraries
This solution uses the following libraries:
- FastAPI: It is a great libraries for building API services and I have used it before. It was also listed in job description.
- SQLAlchemy: ORM for dealing with databases.
- Alembic: Handles migrations.
- Uvicorn: Runs FastAPI server.


## Database choice: SQLite
SQLite was used as database choice because it is simple and easy to use for projects and doesn't require starting and running another service. However, in production, I would suggest using another database such as PostgreSQL.

## Storing and Managing API key
Environment variable is used to store API key instead of hardcoding it into code. This makes it easier to manage and update the keys without modifying the code. You can set the environment variables in the deployment environment, and the code can read them at runtime

A secrets management tool can securely store and manage sensitive data, including API keys. Some popular tools are HashiCorp Vault, AWS Secrets Manager, and Google Cloud Secret Manager. These tools provide access controls, audit logs, and encryption to protect the secrets.

## Migrations
Alembic library is used to handle migrations. Simply, when model is added or updated in `financial/models.py`, run the below command to autogenerate migration file which is stored in `alembic` directory.

```bash
alembic revision -m "New model added"
```

Then apply migration by running
```bash
alembic upgrade head
```

