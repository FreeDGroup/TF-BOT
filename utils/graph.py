from datetime import datetime, timedelta

import requests


def get_meetings(token, user_id, start_time=None, end_time=None):
    if start_time is None:
        start_time = datetime.now()

    if end_time is None:
        end_time = start_time + timedelta(days=7)  # default to one week of meetings

    start_time = start_time.isoformat() + "Z"
    end_time = end_time.isoformat() + "Z"

    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/calendarview"
    query_params = {"startdatetime": start_time, "enddatetime": end_time}
    headers = {"Authorization": f"Bearer {token}", "Prefer": 'outlook.timezone="Pacific Standard Time"'}
    response = requests.get(url, params=query_params, headers=headers)
    response.raise_for_status()  # If the request fails, this will raise a HTTPError

    meetings = response.json()
    return meetings["value"]
