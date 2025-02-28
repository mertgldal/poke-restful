# Flask Pokémon API

This project is a Flask-based RESTful API for managing Pokémon data. It features user authentication, CRUD operations for Pokémon, secure token handling, and admin functionalities.

## Features

### User Authentication
- Secure user registration and login using email and password.
- JWT (JSON Web Tokens) for authentication and authorization.

### Pokémon Management
- Retrieve information about Pokémon, including abilities, types, and images.
- Admin users can register new Pokémon, edit their ratings, and delete Pokémon from the database.

### User Management
- Admin functionality for managing user accounts, including viewing all users.

### Token Management
- Secure token handling, including token revocation and blocking.

## Technologies Used

- **Backend:** Python, Flask, SQLAlchemy
- **Serialization:** Marshmallow
- **Authentication:** Flask-JWT-Extended
- **Database:** SQLite


## API Endpoints

### User Endpoints

- **Register:**
  - `POST /register`
  - Request Body: `{ "name": "your_name", "email": "your_email", "password": "your_password" }`

- **Login:**
  - `POST /login`
  - Request Body: `{ "email": "your_email", "password": "your_password" }`

- **Change Password:**
  - `POST /change-password`
  - Request Body: `{ "current_password": "your_current_password", "new_password": "your_new_password" }`

- **Logout:**
  - `DELETE /logout`

### Pokémon Endpoints

- **Get All Pokémon:**
  - `GET /get-all-pokemon`

- **Get Pokémon by ID:**
  - `GET /pokemon/<int:pokemon_id>`

- **Search Pokémon:**
  - `GET /search`
  - Query Parameter: `pokemon_name`

- **Add Pokémon (Admin only):**
  - `POST /add/<string:pokemon_name>`

- **Edit Pokémon (Admin only):**
  - `POST /edit-pokemon/<int:pokemon_id>`
  - Query Parameter: `rating`

- **Delete Pokémon (Admin only):**
  - `DELETE /delete/<int:pokemon_id>`

### Admin Endpoints

- **Get All Users (Admin only):**
  - `GET /get-all-users`

### Miscellaneous Endpoints

- **Who Am I:**
  - `GET /who-am-i`

## Contribution

Contributions are welcome! Feel free to submit pull requests or report issues.
