from datetime import date
import hashlib


def get_event_weather(city: str, event_date: date) -> dict | None:
    """Retourne une météo fictive pour les concerts dans les 15 jours à venir."""
    today = date.today()
    days_until = (event_date - today).days
    if days_until < 0 or days_until > 15:
        return None

    seed = f"{city.lower()}-{event_date.isoformat()}"
    digest = hashlib.sha256(seed.encode()).hexdigest()
    value = int(digest[:8], 16)

    weather_types = [
        {"label": "Ensoleillé", "icon": "☀️", "description": "Ciel dégagé et ambiance estivale."},
        {"label": "Nuageux", "icon": "☁️", "description": "Quelques nuages, mais la météo reste agréable."},
        {"label": "Orageux", "icon": "⛈️", "description": "Rafales et averses possibles, prévoyez un imperméable."},
        {"label": "Pluvieux", "icon": "🌧️", "description": "Pluie légère à modérée, pensez à un parapluie."},
        {"label": "Doux", "icon": "🌤️", "description": "Temps tempéré avec une belle lumière de fin de journée."},
    ]

    weather = weather_types[value % len(weather_types)]
    temperature = 12 + (value % 15)
    chance = 30 + (value % 61)

    return {
        "city": city,
        "date": event_date.strftime("%d/%m/%Y"),
        "temperature": f"{temperature}°C",
        "chance": f"{chance}% de précipitations",
        **weather,
    }
