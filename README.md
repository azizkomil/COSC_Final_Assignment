ar API - Flask Backend
Overview
This is a simple Flask API that allows you to interact with a PostgreSQL database to manage car records. You can perform CRUD (Create, Read, Update, Delete) operations on car data such as retrieving, adding, and deleting cars from the database.

The API exposes the following endpoints:

GET /cars – Retrieve all cars.

GET /cars/<int:car_id> – Retrieve a specific car by ID.

POST /cars – Add a new car to the database.

DELETE /cars/<int:car_id> – Delete a car by ID.


final_project/ backend -> app.py frontend -> Static frontend files (hosted in S3)

1. Set up EC2 Instance:
Configure the security group to allow traffic on ports: 80, 22, 443, 5432, 8000, and all traffic. Set up RDS PostgreSQL:

Make sure the RDS instance allows all traffic from the EC2 instance (public access). SSH into EC2:

2.  ```Run: ssh -i "C:\your_key_2_ec2.pem" ubuntu@<EC2_Public_IP>```
3.  Install dependencies:

```
sudo apt update
sudo apt install python3 python3-pip postgresql-client -y
```
4. psql -h end point -U user -d database

5.create database 
```CREATE TABLE tbl_azizbek_data (
    id SERIAL PRIMARY KEY,
    model VARCHAR(255),
    brand VARCHAR(255),
    price_usd DECIMAL(10, 2),
    year_released INT
);
```

6. 6.Create Project Directory and Flask Application: Create the project directory and Python file:
mkdir final
cd final
touch app.py

7.Install Python Dependencies: Install python3-venv (if not already installed)

```
cd final
sudo apt update
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```
8. Instal these
   ```
    pip3 install --upgrade pip
    pip3 install flask psycopg2-binary
    ```
9.Run the server:
```
cd final
python app.py
``` 





