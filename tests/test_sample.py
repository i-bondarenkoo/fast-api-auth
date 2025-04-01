from main import (
    ALGORITHM,
    SECRET_KEY,
    UserInDB,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user,
    verify_password,
    fake_users_db,
)
import jwt


class TestExample:
    def test_verify_password(self):
        assert verify_password(
            "secret", "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
        )
        assert verify_password(
            "qwerty", "$2b$12$wyNPjwzKF13fTPiVLtqGdudfFt9g9zp26SKk8xpM0rkP5cVPq2yc6"
        )

    def test_get_password_hash(self):
        assert isinstance(get_password_hash("test"), str)

    def test_get_user(self):
        user = get_user(fake_users_db, "johndoe")
        assert isinstance(user, UserInDB)

        user = get_user(fake_users_db, "john")
        assert user is None

    def test_create_access_token(self):
        token = create_access_token({"sub": "johndoe"})
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert isinstance(token, str)
        assert isinstance(decoded_token, dict)
        assert decoded_token["sub"] == "johndoe"
        assert "exp" in decoded_token

    def test_authenticate_user(self):
        user = authenticate_user(fake_users_db, "johndoe", "secret")
        assert isinstance(user, UserInDB)
        assert user is not False

        user = authenticate_user(fake_users_db, "johndoe", "qwerty")
        assert user is False

        user = authenticate_user(fake_users_db, "name123", "secret")
        assert user is False

    def test_get_current_user(self):
        token = create_access_token({"sub": "johndoe"})
        user_data = get_current_user(token)
        assert user_data.username == "johndoe"
