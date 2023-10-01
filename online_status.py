import requests
from datetime import datetime, timedelta

api_url = "https://sef.podkolzin.consulting/api/users/lastSeen?offset="

def load_user_data(offset):
    try:
        response = requests.get(api_url + str(offset))
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API request failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

localizations = {
    "Just now": {
        "en": "Just now",
        "fr": "À l'instant",
        "uk": "Щойно",
        "de": "Gerade eben",
    },
    "Less than a minute ago": {
        "en": "Less than a minute ago",
        "fr": "Il y a moins d'une minute",
        "uk": "Менше хвилини тому",
        "de": "Vor weniger als einer Minute",
    },
    "Couple of minutes ago": {
        "en": "Couple of minutes ago",
        "fr": "Il y a quelques minutes",
        "uk": "Пару хвилин тому",
        "de": "Vor ein paar Minuten",
    },
    "An hour ago": {
        "en": "An hour ago",
        "fr": "Il y y a une heure",
        "uk": "Годину тому",
        "de": "Vor einer Stunde",
    },
    "Today": {
        "en": "Today",
        "fr": "Aujourd'hui",
        "uk": "Сьогодні",
        "de": "Heute",
    },
    "Yesterday": {
        "en": "Yesterday",
        "fr": "Hier",
        "uk": "Вчора",
        "de": "Gestern",
    },
    "This week": {
        "en": "This week",
        "fr": "Cette semaine",
        "uk": "Цього тижня",
        "de": "Diese Woche",
    },
    "Long time ago": {
        "en": "Long time ago",
        "fr": "Il y a longtemps",
        "uk": "Давно",
        "de": "Vor langer Zeit",
    },
}

def format_last_seen(last_seen, language="uk"):
    if last_seen == "Online":
        return "Online"
    elif last_seen in localizations:
        return localize(last_seen, language)
    else:
        try:
            last_seen_date = last_seen.split('.')[0]
            last_seen_datetime = datetime.fromisoformat(last_seen_date)
        except ValueError:
            return "Invalid Date/Time Format"

        now = datetime.now()
        time_since_last_seen = now - last_seen_datetime

        if time_since_last_seen < timedelta(seconds=30):
            return localizations["Just now"][language]
        elif timedelta(seconds=30) <= time_since_last_seen < timedelta(minutes=1):
            return localizations["Less than a minute ago"][language]
        elif timedelta(minutes=1) <= time_since_last_seen < timedelta(minutes=59):
            return localizations["Couple of minutes ago"][language]
        elif timedelta(minutes=60) <= time_since_last_seen < timedelta(minutes=119):
            return localizations["An hour ago"][language]
        elif timedelta(hours=2) <= time_since_last_seen < timedelta(days=1) - timedelta(
            hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond
        ):
            return localizations["Today"][language]
        elif (now.date() - last_seen_datetime.date()) <= timedelta(days=1):
            return localizations["Yesterday"][language]
        elif time_since_last_seen < timedelta(days=7):
            return localizations["This week"][language]
        else:
            return localizations["Long time ago"][language]

def localize(last_seen, language="uk"):
    return localizations[last_seen].get(language, "Localization not found")

def process_user_data(user_data, user_set, language="uk"):
    for user in user_data.get("data", []):
        user_id = user.get("userId")

        if user_id and user_id not in user_set:
            last_seen_date = user.get("lastSeenDate")
            formatted_last_seen = "Online" if user.get("isOnline") else format_last_seen(last_seen_date, language)

            user_name = user.get("nickname")

            user_set.add(user_id)
            print(f"User {len(user_set)}: {user_name} was|is online {formatted_last_seen}.")

def show_users(language="uk", total_users=217):
    offset = 0
    user_set = set()

    while offset < total_users:
        user_data = load_user_data(offset)
        if not user_data:
            continue

        process_user_data(user_data, user_set, language)
        offset += 1

if __name__ == "__main__":
    show_users()

    formatted_message = format_last_seen("Just now", language="uk")
    print(formatted_message)

    formatted_message = format_last_seen("Less than a minute ago", language="uk")
    print(formatted_message)

    formatted_message = format_last_seen("Couple of minutes ago", language="uk")
    print(formatted_message)

    formatted_message = format_last_seen("An hour ago", language="uk")
    print(formatted_message)

    formatted_message = format_last_seen("Today", language="uk")
    print(formatted_message)

    formatted_message = format_last_seen("Yesterday", language="uk")
    print(formatted_message)

    formatted_message = format_last_seen("This week", language="uk")
    print(formatted_message)

    formatted_message = format_last_seen("Long time ago", language="uk")
    print(formatted_message)
