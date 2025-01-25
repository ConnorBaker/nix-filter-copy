import sys
from http.client import HTTPSConnection


def get_store_path_hash(store_path: str) -> str:
    return store_path.removeprefix("/nix/store/").split("-")[0]


def is_store_path_available(connection: HTTPSConnection, store_path: str) -> bool:
    connection.request("HEAD", f"/{get_store_path_hash(store_path)}.narinfo")
    response = connection.getresponse()
    _ = response.read()
    return response.status == 200  # noqa: PLR2004


def main() -> None:
    connection = HTTPSConnection("cache.nixos.org")
    connection.connect()
    # Read the lines from stdin
    for store_path in map(str.strip, sys.stdin.readlines()):
        if not is_store_path_available(connection, store_path):
            print(store_path)
    connection.close()


if __name__ == "__main__":
    main()
