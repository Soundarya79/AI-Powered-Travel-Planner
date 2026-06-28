from ai.travel_dna import generate_travel_dna
from ai.hotel_agent import generate_hotels
from ai.itinerary import generate_itinerary


def generate_trip(data):

    travel_dna = generate_travel_dna(data)

    hotels = generate_hotels(data)

    itinerary = generate_itinerary(data)

    return {
        "travel_dna": travel_dna,
        "hotels": hotels,
        "itinerary": itinerary
    }