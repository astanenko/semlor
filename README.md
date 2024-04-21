# Readme

### Dependencies

Make sure the latest docker and docker-compose programs are installed in the host.
- Docker: https://docs.docker.com/engine/install/
- Docker Compose: https://docs.docker.com/compose/install/

## Running the project

* From the root of the directory execute `docker compose up`. The app uses port `80` of your machine.
* After all the containers are built and started navigate to `http://127.0.0.1` to view the main page of the apphttp://127.0.0.1

## Using the app

* The app features a list of Semlors, with Top 3 highlighted entries on the top and the rest in the grid on the bottom.
* You can view every Semlor on its own page, where you can additionally add ratings and view already added ones.
* The website features dark and light mode, as well as simple mobile friendly design.

## Accessing the admin panel

* If you want to access the admin panel, you'll need to create a superuser first, for that from the root of the project directory run `make createsuperuser` and follow the steps.
* Open `http://127.0.0.1/admin`, enter the credentials of freshly created user and login.

# Running the Tests

* Run `make test`

