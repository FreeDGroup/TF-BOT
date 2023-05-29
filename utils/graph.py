from datetime import datetime, timedelta

import requests


def get_meetings(token, user_id, start_time=None, end_time=None):
    if start_time is None:
        start_time = datetime.now()

    if end_time is None:
        end_time = start_time + timedelta(days=7)  # default to one week of meetings

    start_time = start_time.isoformat()
    end_time = end_time.isoformat()

    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/calendarview"
    query_params = f"?startDateTime={start_time}&endDateTime={end_time}"
    headers = {"Authorization": f"Bearer {token}", "Prefer": 'outlook.timezone="Pacific Standard Time"'}
    response = requests.get(url + query_params, headers=headers)
    try:
        response.raise_for_status()  # If the request fails, this will raise a HTTPError
    except requests.exceptions.HTTPError as e:
        return str(e) + "\n" + response.text

    meetings = response.json()
    return meetings["value"]
