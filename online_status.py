import requests
from datetime import datetime, timedelta

api_url = "https://sef.podkolzin.consulting/api/users/lastSeen?offset=0"



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
        "fr": "Il y a une heure",
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
    elif last_seen == "Just now":
        return localizations["Just now"][language]
    elif last_seen == "Less than a minute ago":
        return localizations["Less than a minute ago"][language]
    elif last_seen == "Couple of minutes ago":
        return localizations["Couple of minutes ago"][language]
    elif last_seen == "An hour ago":
        return localizations["An hour ago"][language]
    elif last_seen == "Today":
        return localizations["Today"][language]
    elif last_seen == "Yesterday":
        return localizations["Yesterday"][language]
    elif last_seen == "This week":
        return localizations["This week"][language]
    elif last_seen == "Long time ago":
        return localizations["Long time ago"][language]

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
    elif timedelta(hours=2) <= time_since_last_seen < timedelta(days=1) - timedelta(hours=now.hour,minutes=now.minute,seconds=now.second,microseconds=now.microsecond):
        return localizations["Today"][language]
    elif (now.date() - last_seen_datetime.date()) <= timedelta(days=1):
        return localizations["Yesterday"][language]
    elif time_since_last_seen < timedelta(days=7):
        return localizations["This week"][language]
    else:
        return localizations["Long time ago"][language]



def show_users():
    offset = 0
    user_set = set()
    user_counter = 0
    total_users = 217

    while user_counter < total_users:
        user_data = load_user_data(offset)
        if not user_data:
            break

        for user in user_data["data"]:
            user_id = user["userId"]

            if user_id not in user_set:
                last_seen_date = user.get("lastSeenDate")
                formatted_last_seen = "Online" if user["isOnline"] else format_last_seen(last_seen_date)

                user_name = user.get("nickname")

                user_set.add(user_id)
                user_counter += 1

                print(f"User {user_counter}: {user_name} was|is online {formatted_last_seen}.")

if __name__ == "__main__":
    show_users()