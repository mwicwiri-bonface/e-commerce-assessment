# E-Commerce Backend

This is an e-commerce backend built using Django Rest Framework (DRF) with JWT authentication os
used in development is fedora. 

## Technologies Used

- Django
- Django Rest Framework (DRF)
- JWT Authentication
- Other dependencies (specified in requirements.txt)

## Project Structure

The project is structured as follows:

- `e-commerce-assessment/`: Django project root directory.
  - `accounts/`: Auth model and logic.
  - `core/`: Django project settings directory.
    - `settings/`: Contains settings files.
      - `base.py`: Base settings.
      - `development.py`: Development settings.
      - `production.py`: Production settings.
  - `static-files/`: Static files directory.
  - `templates/`: HTML templates directory.
  - `media/`: Media files directory (e.g., user-uploaded images).
  - `manage.py`: Django project management script.

## Setup Instructions

1. Clone the repository:

    ```bash
    git clone https://github.com/mwicwiri-bonface/e-commerce-assessment.git
    ```

2. Navigate to the project directory:

    ```bash
    cd e-commerce-assessment
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Update the .env file:

    - Create a new `.env` file in the project root directory.
    - Add the following environment variables:

      ```dotenv
      DEBUG=True
      SECRET_KEY=your-secret-key
      ```

      Replace `your-secret-key` with your actual secret key.

5. Apply migrations:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser (admin) account:

    ```bash
    python manage.py createsuperuser
    ```

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

8. Access the website at `http://127.0.0.1:8000/`.

## Deployment

For deployment to production:

1. Update the .env file:

    - Modify the `.env` file to include PostgreSQL database configuration for production:

      ```dotenv
      DEBUG=False
      SECRET_KEY=your-secret-key

      POSTGRES_DB_NAME=db_name
      POSTGRES_DB_USER=postgres
      POSTGRES_DB_PASSWORD=password
      POSTGRES_DB_HOST=127.0.0.1
      POSTGRES_DB_PORT=5432
      ```

      Replace `db_name`, `postgres`, `password`, `127.0.0.1`, and `5432` with the appropriate values for your PostgreSQL database.

2. Collect static files:

    ```bash
    python manage.py collectstatic
    ```

3. Configure your production server (e.g., Gunicorn, Nginx).
4. Set up environment variables (e.g., `SECRET_KEY`, `POSTGRES_DB_NAME`, `POSTGRES_DB_USER`, `POSTGRES_DB_PASSWORD`, `POSTGRES_DB_HOST`, `POSTGRES_DB_PORT`).
5. Deploy your application to your chosen hosting provider (e.g., Heroku, AWS, DigitalOcean).

## Contributors

- [Bonface Mwicwiri](https://github.com/mwicwiri-bonface)

## License

This project is licensed under the [MIT License](LICENSE).
