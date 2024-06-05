Sure, here is an updated `README.md` reflecting the new structure of the project:

```markdown
# Flask Pokémon API

This repository contains a Flask-based RESTful API for managing Pokémon data. With this API, users can register, log in, and perform various operations related to Pokémon, such as retrieving information about specific Pokémon, registering new Pokémon, and managing user accounts.

## Features

- **User Authentication:**
  - Secure user registration and login using email and password.
  - JWT (JSON Web Tokens) for authentication and authorization.

- **Pokémon Management:**
  - Retrieve information about Pokémon, including abilities, types, and images.
  - Admin users can register new Pokémon, edit their ratings, and delete Pokémon from the database.

- **User Management:**
  - Admin functionality for managing user accounts, including viewing all users.

- **Token Management:**
  - Secure token handling, including token revocation and blocking.

## Technologies Used

- **Flask:** A lightweight web application framework for Python.
- **Flask-JWT-Extended:** Extension for Flask that adds JWT support to applications.
- **Flask-SQLAlchemy:** Flask extension for working with SQLAlchemy, a popular SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Marshmallow:** A Python library for object serialization and deserialization.
- **SQLite:** A lightweight relational database management system used for storing Pokémon and user data.

## Project Structure

```
flask_pokemon_api/
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── jwt_callbacks.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── pokemon.py
├── config.py
├── run.py
├── .venv/
└── README.md
```

## Setup Instructions

### Prerequisites

Ensure you have Python and pip installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/pokemon-api.git
   cd pokemon-api
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```bash
   flask db upgrade
   ```

### Running the Application

1. **Run the Flask application:**
   ```bash
   python run.py
   ```

2. **Access the API:**
   Open your browser or API testing tool (e.g., Postman) and navigate to `http://127.0.0.1:5000`.

## API Endpoints

### User Endpoints

- **Register:**
  - `POST /register`
  - Request Body: `{ "name": "your_name", "email": "your_email", "password": "your_password" }`

- **Login:**
  - `POST /login`
  - Request Body: `{ "email": "your_email", "password": "your_password" }`
  - returns access_token

- **Change Password:**
  - `POST /change-password`
  - Request Body: `{ "current_password": "your_current_password", "new_password": "your_new_password" }`
  - requests access_token

- **Logout:**
  - `DELETE /logout`
  - requests access_token
### Pokémon Endpoints

- **Get All Pokémon:**
  - `GET /get-all-pokemon`

- **Get Pokémon by ID:**
  - `GET /pokemon/<int:pokemon_id>`

- **Search Pokémon():**
  - `GET /search`
  - Query Parameter: `pokemon_name`

- **Add Pokémon (Admin only):**
  - `POST /add/<string:pokemon_name>`

- **Edit Pokémon (Admin only):**
  - `POST /edit-pokemon/<int:pokemon_id>`
  - Query Parameter: `rating`

- **Delete Pokémon (Admin only):**
  - `GET or POST /delete/<int:pokemon_id>`

### Admin Endpoints

- **Get All Users (Admin only):**
  - `GET /get-all-users`

### Miscellaneous Endpoints

- **Who Am I:**
  - `GET /who-am-i`

## Contribution

Contributions are welcome! Feel free to submit pull requests or report issues.