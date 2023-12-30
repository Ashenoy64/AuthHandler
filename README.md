# AuthHandler

AuthHandler is a Python module designed to handle user authentication and session management functionalities within applications. It offers a set of methods and functionalities to facilitate  user authentication and session control.

## Purpose

This module aims to simplify the setup process for user authentication in prototypes or simple projects. By encapsulating authentication and session management functionalities, AuthHandler enables rapid integration of login systems into various projects, saving development time and effort.

## Features

- **User Registration:** Register new users, ensuring uniqueness for usernames and emails.
- **User Login:** Authenticate users by validating their credentials (email/username and password).
- **Session Management:** Generate, validate, and manage user sessions using JWT tokens.
- **Password Hashing:** Securely hash and verify passwords using bcrypt for enhanced security.
- **Token Handling:** Decode and verify JWT tokens for session validation and logout functionality.

## Installation

To use the AuthHandler module, follow these steps:

1. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    This will install the necessary dependencies for the module.

2. Include the `AuthHandler` module in your project:

    ```python
    from Auth import Auth  # Import the Auth module
    ```

## Usage

### Initialization:

```python
# Initialize AuthHandler
auth = Auth()
```

### User Registration:

```python
# Register a new user
result = auth.registerUser('username', 'email@example.com', 'password')
```

### User Login:

```python
# Login with email
login_result = auth.loginUserEmail('email@example.com', 'password')

# Login with username
login_result = auth.loginUserName('username', 'password')
```

### Session Management:

```python
# Verify and decode a token
token = 'your_token_here'
verification_result = auth.verifyToken(token)

# Logout a session
logout_result = auth.logoutSession(token)
```

## License

This project is licensed under the [MIT License](LICENSE).


