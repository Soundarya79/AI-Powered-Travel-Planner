from pathlib import Path
from services.wiki import get_destination_info

PROMPT_FOLDER = Path("prompts")


def load_prompt(filename):
    with open(PROMPT_FOLDER / filename, "r", encoding="utf-8") as file:
        return file.read()


def build_travel_dna_prompt(data):

    prompt = load_prompt("travel_dna.txt")

    prompt = prompt.replace("{source}", data["source"])
    prompt = prompt.replace("{destination}", data["destination"])
    prompt = prompt.replace("{days}", str(data["days"]))
    prompt = prompt.replace("{budget}", str(data["budget"]))
    prompt = prompt.replace("{travelers}", str(data["travelers"]))
    prompt = prompt.replace("{experience}", data["experience"])
    prompt = prompt.replace("{trip_type}", data["trip_type"])
    prompt = prompt.replace("{mood}", data["mood"])
    prompt = prompt.replace("{interests}", ", ".join(data["interests"]))
    prompt = prompt.replace("{pace}", data.get("pace", "Balanced"))
    prompt = prompt.replace("{start_date}", data.get("start_date", ""))

    return prompt


def build_itinerary_prompt(data):

    prompt = load_prompt("itinerary.txt")

    destination_info = get_destination_info(data["destination"])

    prompt = prompt.replace("{destination_info}", destination_info)
    prompt = prompt.replace("{source}", data["source"])
    prompt = prompt.replace("{destination}", data["destination"])
    prompt = prompt.replace("{days}", str(data["days"]))
    prompt = prompt.replace("{budget}", str(data["budget"]))
    prompt = prompt.replace("{travelers}", str(data["travelers"]))
    prompt = prompt.replace("{experience}", data["experience"])
    prompt = prompt.replace("{trip_type}", data["trip_type"])
    prompt = prompt.replace("{mood}", data["mood"])
    prompt = prompt.replace("{interests}", ", ".join(data["interests"]))

    return prompt
