from project1 import greet


def test_greet_returns_custom_message():
    assert greet("World") == "Hello, World!"
