import pathlib
import pygit2


def main():
    here = pathlib.Path(__file__).parent
    pygit2.clone_repository(
        "https://github.com/MaxHalford/openbikes-data",
        here / "openbikes-data.git",
    )


if __name__ == "__main__":
    main()
