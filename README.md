# Flask Pokémon API

This repository contains a Flask-based RESTful API for managing Pokémon data. With this API, users can register, login, and perform various operations related to Pokémon, such as retrieving information about specific Pokémon, registering new Pokémon, and managing user accounts.

## Features:

- **User Authentication:** Users can register and login securely using email and password authentication.
- **Token-based Authentication:** JWT (JSON Web Tokens) are used for secure authentication and authorization of users.
- **Pokémon Management:** Users can retrieve information about Pokémon, including their abilities, types, and images. They can also register new Pokémon to the database.
- **User Management:** Admin functionality is included for managing user accounts.

## Technologies Used:

- **Flask:** A lightweight web application framework for Python.
- **Flask-JWT-Extended:** Extension for Flask that adds JWT support to applications.
- **Flask-SQLAlchemy:** Flask extension for working with SQLAlchemy, a popular SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Marshmallow:** A Python library for object serialization and deserialization.
- **SQLite:** A lightweight relational database management system used for storing Pokémon and user data.

## Usage:

1. Clone the repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`.
3. Set up a virtual environment (recommended).
4. Run the Flask application using `python app.py`.
5. Access the API endpoints using a tool like Postman or by making HTTP requests.

Feel free to contribute to this project by submitting pull requests or reporting issues!
