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
    - Used to orchestrate multiple services, API, Redis, DB

## Setup

### Build

1. Clone the repository locally
2. Navigate to the cloned repositories build folder: `cd vqe/build`
3. Run a docker-compose build: `docker-compose build`

### Running the application

1. Ensure that all steps under [Build](#build) are complete.
2. Run the services via docker-compose: `docker-compose up`
3. Navigate to `/ping` endpoint to test connectivity:
    - http://127.0.0.1:8080/ping
    - http://localhost:8080/ping
