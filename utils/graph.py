from datetime import datetime, timedelta, timezone

import requests


def get_meetings(token, users, start_time=None, end_time=None):
    if start_time is None:
        start_time = datetime.now().astimezone(timezone(timedelta(hours=9)))

    if end_time is None:
        end_time = start_time + timedelta(days=7)  # default to one week of meetings

    start_time = start_time.isoformat()
    end_time = end_time.isoformat()

    url = "https://graph.microsoft.com/v1.0/me/calendar/getSchedule"
    body = {
        "schedules": users,
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
    parsed_schedule = []
    for value in meetings["value"]:
        for item in value["scheduleItems"]:
            parsed_schedule.append(
                {"start": item["start"]["dateTime"], "end": item["end"]["dateTime"], "schedule_id": value["scheduleId"]}
            )
    return parsed_schedule
