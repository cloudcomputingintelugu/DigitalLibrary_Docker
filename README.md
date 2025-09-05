#******************************************************************************************
#                           Dockerfile 1 (MySQL)
#******************************************************************************************

FROM mysql/mysql-server:5.7
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_USER=root
EXPOSE 3306
COPY database.sql /docker-entrypoint-initdb.d/database.sql

#--------------------------# Build image. network and creat the container
touch database/Dockerfile
vim database/Dockerfile

docker network create ccit-net
docker build -t dbimage database/
docker run -d --name cont-db -p 3306:3306 --network ccit-net dbimage
#--------------------------


#******************************************************************************************
#                           Dockerfile 2 (Auth service)
#******************************************************************************************

FROM python:3.11-slim
WORKDIR /app

# copy app code
COPY requirements.txt .

# install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run flask app
CMD ["python", "auth_service.py"]

#--------------------------
touch auth_service/Dockerfile
vim auth_service/Dockerfile

docker build -t authimage auth_service/
docker run -d --name auth_service --network ccit-net  -p 5001:5001 authimage
#--------------------------


#******************************************************************************************
#                           Dockerfile 3 (Books service)
#******************************************************************************************

FROM python:3.11-slim
WORKDIR /app

# copy app code
COPY requirements.txt .

# install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run flask app
CMD ["python", "book_service.py"]

#--------------------------
touch book_service/Dockerfile
vim book_service/Dockerfile

docker build -t bookimage book_service/
docker run -d --name book_service --network ccit-net  -p 5002:5002 bookimage
#--------------------------

#******************************************************************************************
#                           Dockerfile 4 (Borrow service)
#******************************************************************************************

FROM python:3.11-slim
WORKDIR /app

# copy app code
COPY requirements.txt .

# install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run flask app
CMD ["python", "borrow_service.py"]

#--------------------------
touch borrow_service/Dockerfile
vim borrow_service/Dockerfile

docker build -t borrowimage borrow_service/
docker run -d --name borrow_service --network ccit-net  -p 5003:5003 borrowimage
#--------------------------

#******************************************************************************************
#                           Dockerfile 5 (Gateway service)
#******************************************************************************************

FROM python:3.11-slim
WORKDIR /app

# copy app code
COPY requirements.txt .

# install requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# run flask app
CMD ["python", "app.py"]

#--------------------------
vim gateway/app.py    

AUTH_URL = "http://auth_service:5001"
BOOK_URL = "http://book_service:5002"
BORROW_URL = "http://borrow_service:5003"

touch gateway/Dockerfile
vim gateway/Dockerfile

docker build -t gatewayimage gateway/
docker run -d --name gateway --network ccit-net  -p 5000:5000 gatewayimage
#--------------------------
