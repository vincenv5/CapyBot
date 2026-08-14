from urllib.request import urlopen
from json import loads

type JSON = dict
code = "utf-8"
joke_api_link = "https://official-joke-api.appspot.com/"


def _get_joke_from_api() -> JSON:
    """
    This function will access the joke API to get a joke. It will then
    read the HTTP response into a string and return a JSON formatted dictionary
    """
    joke = urlopen(joke_api_link + "/jokes/random")
    joke = joke.read()
    return loads(joke)


def get_full_joke() -> str:
    """
    This function will get the joke from the API and extract the setup
    and punchline from the JSON load. It will return a string with the 
    setup and the punchline formatted.
    """
    joke = _get_joke_from_api()
    setup = joke.get("setup")
    punchline = joke.get("punchline")

    return f"{setup}\n{punchline}"


if __name__ == "__main__":
    joke = get_full_joke()
    print(joke)
    