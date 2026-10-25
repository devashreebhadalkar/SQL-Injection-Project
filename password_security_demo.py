import hashlib
import secrets


def hash_password(password, salt):
    password_bytes = password.encode("utf-8")
    salt_bytes = salt.encode("utf-8")

    return hashlib.pbkdf2_hmac(
        "sha256",
        password_bytes,
        salt_bytes,
        600_000
    ).hex()


def main():
    password = input("Enter a sample password: ")

    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    print("\nPassword security demonstration")
    print("Original password: [not displayed]")
    print("Generated salt:", salt)
    print("Password hash:", password_hash)

    entered_password = input("\nRe-enter the password to verify: ")

    entered_hash = hash_password(entered_password, salt)

    if secrets.compare_digest(password_hash, entered_hash):
        print("\nPassword verification successful!")
    else:
        print("\nPassword verification failed!")


if __name__ == "__main__":
    main()