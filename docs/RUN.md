# Starting

We currently use docker-compose to run our scripts in an orderly fashion.

# Setting environment variables

This application requires the use of a Zerodha KiteConnect API key and a brokerage account with Zerodha. To set these environment variables, you must

1. Make a copy of the `.env.template` file in the root directory, and rename it to .env.
2. Set the values in `.env` accordingly.


# Running the Application

To build and run all the containers, you can use the command `docker-compose up` to start the containers.