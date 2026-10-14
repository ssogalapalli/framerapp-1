def greet(name: str) -> str:
    """Return a greeting for the provided name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    user_name = input("What is your name? ")
    print(greet(user_name))
