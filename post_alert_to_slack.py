import textwrap
from datetime import datetime, timedelta, tzinfo
from time import sleep
from typing import Dict, List, Optional

import click
import dateutil.parser
import pytz
import requests
from kawasemi import Kawasemi

SCHEDULE_LINK = 'https://camph.net/schedule/'
WEEKDAY_NAMES = ['月', '火', '水', '木', '金', '土', '日']

class Event:
    start: datetime
    end: datetime
    title: str
    url: Optional[str]

    def __init__(self, *, start: datetime, end: datetime, title: str,
                 url: Optional[str]) -> None:
        self.start = start
        self.end = end
        self.title = title
        self.url = url

    @classmethod
    def from_json(cls, data: Dict[str, Optional[str]]) -> "Event":
        if data["start"] is not None:
            start = dateutil.parser.parse(data["start"])
        else:
            raise KeyError
        if data["end"] is not None:
            end = dateutil.parser.parse(data["end"])
        else:
            raise KeyError
        if data["title"] is not None:
            title = data["title"]
        else:
            raise KeyError
        return cls(start=start, end=end, title=title, url=data["url"])

    def get_start(self, tz: tzinfo) -> str:
        start = self.start.astimezone(tz).time().strftime("%H:%M")
        return start

    def get_end(self, tz: tzinfo) -> str:
        end = self.end.astimezone(tz).time().strftime("%H:%M")
        return end

    def get_day_and_time(self, tz: tzinfo) -> str:
        date = self.start.astimezone(tz).date().strftime("%m/%d")
        day = get_japanese_weekday(self.start.astimezone(tz).weekday())
        return f"{date} ({day}) {self.get_start(tz)}〜{self.get_end(tz)}"

    def get_day_and_time_with_title(self, tz: tzinfo) -> str:
        return f"{self.title} {self.get_day_and_time(tz)}"


def divide_events_by_title(events: List[Event]) -> Dict[str, List[Event]]:
    events_by_title: Dict[str, List[Event]] = {}
    for title in ["open", "make", "online open"]:
        events_by_title[title] = [
            e for e in events if e.title.lower() == title]
        events = [e for e in events if e.title.lower() != title]
    events_by_title["other"] = [e for e in events if e.title.strip() != ""]
    return events_by_title


def download_events(url: str) -> Optional[List[Event]]:
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
        return None
    return [Event.from_json(e) for e in response.json()]


def get_japanese_weekday(day: int) -> str:
    return WEEKDAY_NAMES[day]


def validate_datetime(ctx, param, value) -> Optional[datetime]:
    if value is None:
        return None
    try:
        dt = dateutil.parser.parse(value)
    except ValueError:
        ctx.fail(f"Failed to parse '{value}'")
    return dt  # WARNING: tzinfo might be None


def post_alert_to_slack(url: str, api_key: str, api_secret: str, 
                        access_token: str, access_token_secret: str, 
                        dry_run: bool, timezone: str, now: datetime, week: bool) -> None:
    # ここに通知処理を書く
    pass 
    
    # if dry_run:
    #     for i, message in enumerate(messages):
    #         print(f"#{i + 1}\n{message}")
    #     return
    
    # if len(messages) > 0:
    #     kawasemi = Kawasemi({
    #         "CHANNELS": {
    #             "slack": {
    #                 "_backend": "kawasemi.backends.slack.SlackChannel",
    #                 "url": url,
    #                 "api_key": api_key,
    #                 "api_secret": api_secret,
    #                 "access_token": access_token,
    #                 "access_token_secret": access_token_secret,
    #             }
    #         }
    #     })

        # for message in messages:
        #     kawasemi.send(message)


# COA: CAMPHOR- Open Alert
@click.command(help="CAMPHOR- Open Alert")
@click.option("--url", default="https://cal.camph.net/public/schedule.json",
              envvar="COA_URL", 
              help="URL of a schedule file.")
@click.option("--api-key", type=click.STRING,
              envvar="COA_API_KEY", 
              help="Slack API Key.")
@click.option("--api-secret", type=click.STRING,
              envvar="COA_API_SECRET", 
              help="Slack API Secret.")
@click.option("--access-token", type=click.STRING,
              envvar="COA_ACCESS_TOKEN", 
              help="Slack Access Token.")
@click.option("--access-token-secret", type=click.STRING,
              envvar="COA_ACCESS_TOKEN_SECRET",
              help="Slack Access Token Secret.")
@click.option("--dry-run", "-n", default=False, is_flag=True,
              help="Write messages to stdout.")
@click.option("--timezone", default="Asia/Tokyo",
              help="Time zone used to show time. (default: Asia/Tokyo)")
@click.option("--now", callback=validate_datetime,
              help="Specify current time for debugging. (example: 2017-01-01)")
@click.option("--week", default=False, is_flag=True,
              envvar="COA_WEEK", help="Notify weekly schedule.")
def check_open(door_isopen: bool, url: str, timezone: str):
    events = download_events(url)
    
    tz = pytz.timezone(timezone)
    if now is None:
        now = datetime.now(tz=tz)
    elif now.tzinfo is None:
        now = now.replace(tzinfo=tz)
    
    events = list(filter(
                    lambda e: e.start.astimezone(tz).date()
                    == now.astimezone(tz).date(), events))
    events_by_title = divide_events_by_title(events)
    
    open_events = events_by_title["open"]
    if len(open_events) == 1:
        open_event = open_events[0]
        open_start = open_event.get_start(tz)
        # CAMPHOR- Make あり
        make_events = events_by_title["make"]
        if len(make_events) == 1:
            make_event = make_events[0]
            make_start = make_event.get_start(tz)
        elif len(make_events) > 1:
            raise ValueError("The maximum number of Make events per day"
                                " is one, but found several.")
    elif len(open_events) > 1:
        raise ValueError("The maximum number of Open events per day is"
                            " one, but found several.")
    
    # other_events = events_by_title["other"]
    # if len(other_events) == 1:
    #     other_event = other_events[0]
    #     other_start = other_event.get_start(tz)
    # elif len(other_events) > 1:
    #     raise ValueError("The maximum number of Other events per day"
    #                         " is one, but found several.")
    
    # 開館から3時間経過するまでの間にドアが開いていない場合は10分間隔でSlackに通知
    alert_hour = 3
    alert_interval_minutes = 10 * 60
    delta = timedelta(hours=alert_hour)
    if now <= open_start + delta and not door_isopen:
        post_alert_to_slack()
    sleep(alert_interval_minutes)
    


