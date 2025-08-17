# Vehicle Query Engine (VQE)

## Requirements:
- Create a normalized, scalable database to store & manage vehicle data. We've provided some data to get you started and to populate your database.
- Provide comprehensive APIs to view and search and sort vehicles based on different filters that can be derived from the data.
- We expect you to deliver a minimum of three components:
    - Data storage.
    - Server with a REST or GraphQL endpoint which queries the data storage.
    - Documentation to easily navigate the APIs.
- Usage of third-party platforms (e.g., Meilisearch or Algolia) is not allowed.

## Environment Prerequisites

- Linux distro / Windows Subsystem for Linux (WSL)
    - This application was developed using Ubuntu 24.04 running in WSL
- [docker](https://docs.docker.com/get-started/get-docker/)
    - Version `27.4.0` or greater
    - Used to build and run application
- [docker-compose](https://docs.docker.com/compose/install/)
    - Version `2.31.0` or greater
    - Used to orchestrate multiple services; API, DB

## Setup

### Build

1. Clone the repository locally: `git clone git@github.com:Lupeclan/vqe.git`
2. Navigate to the cloned repositories build folder: `cd vqe/build`
3. Run a docker-compose build: `docker-compose build`

### Running the application

1. Ensure that all steps under [Build](#build) are complete.
2. Run the services via docker-compose: `docker-compose --profile app up`
    - To run with a clean DB (New containers): `docker-compose --profile app up --force-recreate -V`
3. Navigate to `/ping` endpoint to test connectivity:
    - http://127.0.0.1:8080/ping
    - http://localhost:8080/ping

### Interacting with the VQE

1. Navigate to `/` or `/api/v1` to interact with Swagger documentation
    - http://127.0.0.1:8080/
    - http://localhost:8080/api/v1
2. Expand `vehicles` tab to view endpoints
    1. Expand `/vehicles/bikes` to interact with Bikes endpoint
    2. Expand `/vehicles/cars` to interact with Cars endpoint
    3. Expand `/vehicles/spaceships` to interact with Spaceships endpoint
3. Expand `Models` to view API response models
