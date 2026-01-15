import argparse
import hashlib
import os


def hash_password(password, salt=None, iterations=100_000):
    if salt is None:
        salt = os.urandom(16)
    if isinstance(salt, str):
        salt = bytes.fromhex(salt)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return salt.hex(), digest.hex(), iterations


def verify_password(password, salt_hex, digest_hex, iterations=100_000):
    _, new_digest, _ = hash_password(password, salt_hex, iterations)
    return new_digest == digest_hex


def main():
    parser = argparse.ArgumentParser(description="Security utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    hash_parser = subparsers.add_parser("hash", help="Hash a password")
    hash_parser.add_argument("--password", required=True)
    hash_parser.add_argument("--iterations", type=int, default=100_000)

    verify_parser = subparsers.add_parser("verify", help="Verify a password")
    verify_parser.add_argument("--password", required=True)
    verify_parser.add_argument("--hash", required=True)
    verify_parser.add_argument("--salt", required=True)
    verify_parser.add_argument("--iterations", type=int, default=100_000)

    args = parser.parse_args()

    if args.command == "hash":
        salt, digest, iterations = hash_password(args.password, iterations=args.iterations)
        print(f"salt={salt}")
        print(f"hash={digest}")
        print(f"iterations={iterations}")
        return 0

    if args.command == "verify":
        ok = verify_password(args.password, args.salt, args.hash, args.iterations)
        print("verified" if ok else "invalid")
        return 0 if ok else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
