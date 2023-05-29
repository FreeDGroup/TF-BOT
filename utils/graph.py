from datetime import datetime, timedelta

import requests


def get_meetings(token, user_id, start_time=None, end_time=None):
    if start_time is None:
        start_time = datetime.now()

    if end_time is None:
        end_time = start_time + timedelta(days=7)  # default to one week of meetings

    start_time = start_time.isoformat()
    end_time = end_time.isoformat()

    url = "https://graph.microsoft.com/v1.0/me/calendar/getSchedule"
    body = {
        "schedules": [user_id],
        "startTime": {"dateTime": start_time, "timeZone": "Asia/Seoul"},
        "endTime": {"dateTime": end_time, "timeZone": "Asia/Seoul"},
        "availabilityViewInterval": 60,
    }
    headers = {"Authorization": f"Bearer {token}", "Prefer": 'outlook.timezone="Asia/Seoul"'}
    with requests.Session() as session:
        response = session.post(url, headers=headers, json=body)
    try:
        response.raise_for_status()  # If the request fails, this will raise a HTTPError
    except requests.exceptions.HTTPError as e:
        return str(e) + "\n" + response.text

    meetings = response.json()
    return [x["scheduleItems"] for x in meetings["value"]]
