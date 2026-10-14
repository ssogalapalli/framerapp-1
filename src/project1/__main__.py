import sys

mobile_main = None


def main() -> int:
    global mobile_main

    if len(sys.argv) > 1 and sys.argv[1] in {"--demo", "-d"}:
        from .app import greet

        name = input("What is your name? ")
        print(greet(name))
        return 0

    if len(sys.argv) > 1 and sys.argv[1] in {"--mobile", "-m"}:
        if mobile_main is None:
            from .gui_app import main as gui_main

            mobile_main = gui_main
        mobile_main()
        return 0

    from .web_app import main as web_main

    web_main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
