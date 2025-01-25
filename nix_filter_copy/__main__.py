import asyncio
import sys

from aiohttp import ClientSession


def get_store_path_hash(store_path: str) -> str:
    return store_path.removeprefix("/nix/store/").split("-")[0]


async def is_missing_store_path(session: ClientSession, store_path: str) -> bool:
    async with session.head(f"https://cache.nixos.org/{get_store_path_hash(store_path)}.narinfo") as response:
        return response.status != 200  # noqa: PLR2004


async def async_main() -> None:
    store_paths = list(map(str.strip, sys.stdin.readlines()))

    async with ClientSession() as session:
        store_path_is_missing = await asyncio.gather(
            *map(
                lambda store_path: is_missing_store_path(session, store_path),
                store_paths,
            )
        )

    for store_path, is_missing in zip(store_paths, store_path_is_missing):
        if is_missing:
            print(store_path)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
