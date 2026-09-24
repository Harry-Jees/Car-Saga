"""
Authentication Service for Car Saga.
Handles user registration, bcrypt password hashing, and role-based login.
"""

from database.connection import get_connection
from utils.security import hash_password, verify_password
from utils.validators import validate_email, validate_password


class AuthService:
    @staticmethod
    def register_user(full_name, username, email, password, confirm_password):
        # Validate required inputs
        if not full_name or not username or not email or not password or not confirm_password:
            return {"success": False, "message": "All fields are required."}

        full_name = full_name.strip()
        username = username.strip()
        email = email.strip()

        if len(username) < 3:
            return {"success": False, "message": "Username must be at least 3 characters long."}
        if not validate_email(email):
            return {"success": False, "message": "Please enter a valid email address."}
        if not validate_password(password):
            return {"success": False, "message": "Password must be at least 6 characters long."}
        if password != confirm_password:
            return {"success": False, "message": "Passwords do not match."}

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Check for existing username or email
            cursor.execute(
                "SELECT id FROM users WHERE username = %s OR email = %s",
                (username, email),
            )
            if cursor.fetchone():
                return {"success": False, "message": "Username or email is already registered."}

            pw_hash = hash_password(password)
            cursor.execute(
                """
                INSERT INTO users (full_name, username, email, password_hash, role_id, is_active)
                VALUES (%s, %s, %s, %s, 2, 1)
                """,
                (full_name, username, email, pw_hash),
            )
            conn.commit()
            return {"success": True, "message": "Registration successful! You can now log in."}
        except Exception as e:
            conn.rollback()
            return {"success": False, "message": f"Registration failed: {str(e)}"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def login(username, password):
        if not username or not password:
            return {"success": False, "message": "Please enter both username and password."}

        username = username.strip()
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT u.id, u.full_name, u.username, u.email, u.password_hash, u.is_active, r.name AS role_name
                FROM users u
                JOIN roles r ON r.id = u.role_id
                WHERE u.username = %s
                """,
                (username,),
            )
            user = cursor.fetchone()
            if not user:
                return {"success": False, "message": "Invalid username or password."}

            if not user.get("is_active"):
                return {"success": False, "message": "This account is inactive. Please contact admin."}

            if not verify_password(password, user["password_hash"]):
                return {"success": False, "message": "Invalid username or password."}

            return {
                "success": True,
                "message": "Login successful.",
                "user": {
                    "id": user["id"],
                    "full_name": user["full_name"],
                    "username": user["username"],
                    "email": user["email"],
                    "role": user["role_name"],
                },
            }
        except Exception as e:
            return {"success": False, "message": "Unable to connect to database. Please check MySQL."}
        finally:
            cursor.close()
            conn.close()
