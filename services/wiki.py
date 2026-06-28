import wikipediaapi

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="VoyageAI/1.0"
)


def get_destination_info(destination):
    page = wiki.page(destination)

    if not page.exists():
        return ""

    return page.summary[:3000]


def get_place_description(place):
    """
    Returns a short description for a place.
    """

    page = wiki.page(place)

    if not page.exists():
        return "No description available."

    summary = page.summary.strip()

    if not summary:
        return "No description available."

    sentences = summary.split(". ")

    return ". ".join(sentences[:2]) + "."