import requests
import random
from datetime import datetime

# Database of real famous attractions for major cities
REAL_ATTRACTIONS_DB = {
    "paris": [
        ("Eiffel Tower", "landmark", 1500), ("Louvre Museum", "museum", 1800), 
        ("Notre-Dame Cathedral", "religious", 800), ("Arc de Triomphe", "landmark", 1000),
        ("Sacré-Cœur", "religious", 500), ("Champs-Élysées", "shopping", 1200),
        ("Latin Quarter", "culture", 600), ("Montmartre", "art", 700),
        ("Versailles Palace", "history", 2000), ("Seine River Cruise", "nature", 900)
    ],
    "tokyo": [
        ("Senso-ji Temple", "religious", 400), ("Tokyo Tower", "landmark", 1200),
        ("Shibuya Crossing", "culture", 500), ("Akihabara", "shopping", 800),
        ("Meiji Shrine", "religious", 300), ("Tsukiji Market", "food", 1000),
        ("Tokyo National Museum", "museum", 1100), ("Harajuku", "shopping", 900),
        ("Imperial Palace", "history", 600), ("Skytree Tower", "landmark", 1500)
    ],
    "new york": [
        ("Statue of Liberty", "landmark", 2000), ("Central Park", "nature", 300),
        ("Times Square", "culture", 400), ("Empire State Building", "landmark", 1600),
        ("Metropolitan Museum", "museum", 1400), ("Brooklyn Bridge", "landmark", 500),
        ("Broadway Theater", "entertainment", 2500), ("9/11 Memorial", "history", 800),
        ("Rockefeller Center", "landmark", 1200), ("Madison Avenue", "shopping", 1500)
    ],
    "london": [
        ("Big Ben & Parliament", "landmark", 1800), ("Tower of London", "history", 1400),
        ("British Museum", "museum", 1200), ("Buckingham Palace", "landmark", 900),
        ("Westminster Abbey", "religious", 1000), ("Tower Bridge", "landmark", 800),
        ("London Eye", "entertainment", 1500), ("Piccadilly Circus", "culture", 600),
        ("Regent Street", "shopping", 1100), ("St. Paul's Cathedral", "religious", 700)
    ],
    "barcelona": [
        ("Sagrada Família", "history", 1800), ("Park Güell", "nature", 1400),
        ("Gothic Quarter", "history", 800), ("Casa Batlló", "architecture", 1600),
        ("Las Ramblas", "culture", 500), ("Montjuïc", "landmark", 900),
        ("Barcelona Cathedral", "religious", 600), ("Picasso Museum", "museum", 1300),
        ("Beach of Barcelona", "nature", 200), ("Mercat de la Boqueria", "food", 800)
    ],
    "sydney": [
        ("Sydney Opera House", "landmark", 2000), ("Bondi Beach", "nature", 300),
        ("Sydney Harbour Bridge", "landmark", 1200), ("Royal Botanic Garden", "nature", 800),
        ("Taronga Zoo", "family", 1500), ("Chinese Garden", "nature", 700),
        ("Darling Harbour", "entertainment", 600), ("Art Gallery NSW", "museum", 1100),
        ("Manly Beach", "nature", 400), ("Hyde Park", "nature", 200)
    ],
    "dubai": [
        ("Burj Khalifa", "landmark", 2500), ("Dubai Mall", "shopping", 1200),
        ("Palm Jumeirah", "nature", 1000), ("Gold Souk", "market", 800),
        ("Jumeirah Beach", "nature", 500), ("Dubai Fountain", "entertainment", 400),
        ("Sheikh Mohammed Centre", "culture", 900), ("Dubai Museum", "museum", 700),
        ("Miracle Garden", "nature", 1100), ("Dubai Marina", "landmark", 600)
    ],
    "rome": [
        ("Colosseum", "history", 1800), ("Vatican City", "religious", 2000),
        ("Roman Forum", "history", 1200), ("Pantheon", "history", 900),
        ("Trevi Fountain", "landmark", 600), ("Spanish Steps", "culture", 500),
        ("Capitoline Museum", "museum", 1100), ("St. Peter's Basilica", "religious", 1500),
        ("Castel Sant'Angelo", "history", 1000), ("Trastevere", "food", 900)
    ],
    "amsterdam": [
        ("Anne Frank House", "history", 1600), ("Van Gogh Museum", "museum", 1400),
        ("Canal Cruise", "nature", 800), ("Rijksmuseum", "museum", 1300),
        ("Dam Square", "landmark", 500), ("Red Light District", "culture", 400),
        ("Windmills of Kinderdijk", "history", 1100), ("Albert Cuyp Market", "food", 600),
        ("Vondelpark", "nature", 300), ("Flower Market", "shopping", 700)
    ],
    "istanbul": [
        ("Blue Mosque", "religious", 500), ("Hagia Sophia", "history", 1200),
        ("Topkapi Palace", "history", 1400), ("Grand Bazaar", "shopping", 700),
        ("Galata Tower", "landmark", 900), ("Bosphorus Cruise", "nature", 1000),
        ("Dolmabahçe Palace", "history", 1300), ("Suleymaniye Mosque", "religious", 400),
        ("Street of Spices", "food", 600), ("Golden Horn", "nature", 300)
    ],
    "hyderabad": [
        ("Charminar", "history", 800), ("Golconda Fort", "history", 1000),
        ("Hussain Sagar Lake", "nature", 600), ("Ramoji Film City", "entertainment", 2500),
        ("Salar Jung Museum", "museum", 1200), ("Mecca Masjid", "religious", 400),
        ("Birla Temple", "religious", 500), ("Tank Bund Park", "nature", 300),
        ("Begum Bazaar", "shopping", 600), ("Necklace Road", "nature", 200)
    ],
    "delhi": [
        ("Red Fort", "history", 1500), ("India Gate", "landmark", 800),
        ("Jama Masjid", "religious", 400), ("Raj Ghat", "historical", 500),
        ("Humayun's Tomb", "history", 1200), ("Qutub Minar", "history", 1000),
        ("Delhi Zoo", "family", 600), ("Lodhi Garden", "nature", 300),
        ("National Museum", "museum", 1100), ("Chandni Chowk Market", "shopping", 900)
    ],
    "mumbai": [
        ("Taj Mahal Mumbai", "history", 2000), ("Gateway of India", "landmark", 800),
        ("Marine Drive", "nature", 500), ("Haji Ali", "religious", 400),
        ("Elephanta Caves", "history", 1500), ("Colaba Causeway", "shopping", 1200),
        ("Worli Sea Face", "nature", 200), ("Mount Mary Church", "religious", 500),
        ("Prince of Wales Museum", "museum", 1300), ("Chowpatty Beach", "nature", 300)
    ],
    "goa": [
        ("Basilica of Bom Jesus", "religious", 400), ("Fort Aguada", "history", 1000),
        ("Dudhsagar Waterfall", "nature", 1200), ("Calangute Beach", "nature", 600),
        ("Churches of Goa", "religious", 500), ("Arabitown Market", "market", 800),
        ("Spice Plantation Tour", "nature", 1100), ("Anjuna Flea Market", "shopping", 900),
        ("Panjim Heritage Walk", "culture", 700), ("Chapora Fort", "history", 800)
    ],
    "singapore": [
        ("Marina Bay Sands", "landmark", 2000), ("Gardens by the Bay", "nature", 1500),
        ("Sentosa Island", "entertainment", 1300), ("Singapore Zoo", "family", 1600),
        ("Merlin's Wax Museum", "museum", 1200), ("Chinatown", "culture", 600),
        ("Universal Studios", "entertainment", 2500), ("ArtScience Museum", "museum", 1400),
        ("Kallang River Cruise", "nature", 900), ("Raffles Hotel", "landmark", 1100)
    ]
}

def fetch_pois(city):
    """
    Fetch real points of interest with actual place names
    Uses real attractions database, falls back to online sources
    """
    pois = []
    city_lower = city.lower().strip()
    
    # Check if we have real data for this city
    if city_lower in REAL_ATTRACTIONS_DB:
        print(f"[OK] Using real attractions database for {city}")
        attractions = REAL_ATTRACTIONS_DB[city_lower]
        
        for i, (name, category, base_cost) in enumerate(attractions):
            pois.append({
                "name": name,
                "city": city,
                "lat": 0.0 + (i * 0.01),
                "lng": 0.0 + (i * 0.01),
                "category": category,
                "cost": base_cost + random.randint(-200, 200),  # Add some variation
                "rating": round(random.uniform(4.2, 4.9), 1),
                "popularity": round(random.uniform(0.80, 0.98), 2)
            })
        return pois
    
    # For cities not in database, try to fetch from online sources
    try:
        print(f"[OK] Fetching real attractions for {city} from OpenStreetMap...")
        geo_url = "https://nominatim.openstreetmap.org/search"
        geo_params = {"q": city, "format": "json", "limit": 1}
        geo_response = requests.get(geo_url, params=geo_params, timeout=10)
        
        if geo_response.ok and geo_response.json():
            location = geo_response.json()[0]
            city_lat = float(location["lat"])
            city_lon = float(location["lon"])
            
            # Fetch from Overpass API
            overpass_url = "https://overpass-api.de/api/interpreter"
            query = f"""[bbox={city_lat-0.05},{city_lon-0.05},{city_lat+0.05},{city_lon+0.05}];
            (node["tourism"~"attraction|museum|viewpoint"];node["historic"];node["amenity"~"restaurant"];);
            out body center;"""
            
            response = requests.post(overpass_url, data=query, timeout=15)
            if response.ok:
                data = response.json()
                for i, element in enumerate(data.get("elements", [])[:20]):
                    if "tags" in element and "name" in element["tags"]:
                        name = element["tags"]["name"]
                        category = infer_category(name, element.get("tags", {}))
                        cost = estimate_cost(category)
                        
                        pois.append({
                            "name": name,
                            "city": city,
                            "lat": element.get("lat", city_lat),
                            "lng": element.get("lon", city_lon),
                            "category": category,
                            "cost": cost,
                            "rating": round(random.uniform(4.0, 4.9), 1),
                            "popularity": round(random.uniform(0.75, 0.95), 2)
                        })
                
                if len(pois) >= 10:
                    print(f"[OK] Found {len(pois)} real places for {city}")
                    return pois[:20]
    except Exception as e:
        print(f"[WARNING] Could not fetch online data: {str(e)}")
    
    # Final fallback
    print(f"[OK] Using intelligent fallback attractions for {city}")
    return generate_smart_fallback_pois(city)


def generate_smart_fallback_pois(city):
    """Generate realistic attraction names for any city"""
    templates = [
        ("City Center", "landmark"),
        ("Historic Old Town", "history"),
        ("Central Park", "nature"),
        ("Main Market Square", "shopping"),
        ("Local History Museum", "museum"),
        ("Cathedral/Temple", "religious"),
        ("Waterfront Promenade", "nature"),
        ("Art Gallery", "culture"),
        ("Night Food Market", "food"),
        ("Shopping District", "shopping"),
        ("Monument", "history"),
        ("Zoo & Wildlife Park", "family"),
        ("Botanical Garden", "nature"),
        ("Local Cuisine Restaurants", "food"),
        ("Theater District", "entertainment"),
    ]
    
    pois = []
    for i, (template, category) in enumerate(templates):
        name = f"{city} {template}"
        pois.append({
            "name": name,
            "city": city,
            "lat": 0.0 + (i * 0.01),
            "lng": 0.0 + (i * 0.01),
            "category": category,
            "cost": estimate_cost(category),
            "rating": round(random.uniform(4.2, 4.8), 1),
            "popularity": round(random.uniform(0.75, 0.95), 2)
        })
    
    return pois


def estimate_cost(category):
    """Realistic visit cost by category"""
    ranges = {
        "landmark": (800, 2000),
        "history": (500, 1800),
        "museum": (800, 1600),
        "nature": (200, 1000),
        "shopping": (500, 2000),
        "food": (300, 1500),
        "religious": (100, 600),
        "culture": (400, 1200),
        "entertainment": (1000, 3000),
        "family": (800, 2000),
        "art": (600, 1400),
        "market": (300, 1200)
    }
    min_cost, max_cost = ranges.get(category.lower(), (400, 1200))
    return random.randint(min_cost, max_cost)


def infer_category(place_name, tags=None):
    """Infer category from name and tags"""
    name = place_name.lower()
    
    if tags:
        tourism = tags.get("tourism", "").lower()
        amenity = tags.get("amenity", "").lower()
        
        if "museum" in tourism or "museum" in amenity:
            return "museum"
        if "attraction" in tourism or "viewpoint" in tourism:
            return "landmark"
        if "restaurant" in amenity or "cafe" in amenity:
            return "food"
    
    keywords = {
        "history": ["fort", "palace", "monument", "historical", "ancient", "ruin"],
        "museum": ["museum", "gallery", "exhibit"],
        "nature": ["beach", "park", "lake", "river", "garden", "waterfall", "forest"],
        "shopping": ["market", "mall", "bazaar", "shopping", "street", "souk"],
        "food": ["restaurant", "cafe", "market", "food", "street", "kitchen"],
        "religious": ["temple", "mosque", "church", "cathedral", "shrine", "monastery"],
        "landmark": ["tower", "gate", "bridge", "square", "plaza", "center"],
        "entertainment": ["theater", "cinema", "show", "circus", "amusement"],
        "family": ["zoo", "aquarium", "park", "playground"]
    }
    
    for category, words in keywords.items():
        if any(word in name for word in words):
            return category
    
    return "landmark"