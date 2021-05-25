# Lemons.Market Application

API for creating stock orders

Small scale API to support an image sharing application.

API requirements:
  /orders/ endpoint, primarily requestable through Post request, using those fields (snake_case or CamelCase open to you):

    i. isin (String, 12 chars (this identifies a stock))
    ii. limit_price (Float, always >0)
    iii. side (Enum: buy | sell, case sensitive tolerant)
    iv. valid_until (Integer, Unix UTC Timestamp)
    v. quantity (Integer, always >0)

## User Manual

Clone repository (assumes that docker-compose is installed)
```bash
git clone https://github.com/FranciscoNMora/LemonsMarket.git
```

Move to folder
```bash
cd LemonsMarket
```

Create .env file from sample. You can modify the env variables if you want.
```bash
cp .env.sample .env
```

Built and deploy containers (assume that docker-compose is installed):
```bash
docker-compose up -d --build
```


## API Documentation
The documentation of the API is available in the following URLs. The API can be tested here:

-http://127.0.0.1:8000/doc/swagger/ : SwaggerUI documentation

To create orders using the API, it is necessary for the DB to have some Stocks stored (the order is associated to a Stock).
Stocks can be created using the admin interface (/admin/), accessing using your superuser credentials, or using the
/stock/ API (also available in Swagger)