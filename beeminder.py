"""API client for Beeminder written in Python."""
import requests

# Config

username = ""
auth_token = ""

URL = "https://www.beeminder.com/api/v1/"


class Datapoint:
    """A Datapoint consists of a timestamp and a value, an optional comment, and meta info.

    A Datapoint belongs to a Goal, which has many Datapoints.

    Attributes:
        id          A unique ID, used to identify a datapoint when deleting/editing it.
        timestamp   The unix time (in seconds) of the datapoint.
        daystamp    The date of the datapoint (e.g., "20150831"). Sometimes timestamps
                    are surprising due to goal deadlines, so if you're looking at
                    Beeminder data, you're probably interested in the daystamp.
        value       The value, e.g., how much you weighed on the day indicated by the
                    timestamp.
        comment     An optional comment about the datapoint.
        updated_at  The unix time that this datapoint was entered or last updated.
        requestid   If a datapoint was created via the API and this parameter was
                    included, it will be echoed back.
    """

    id: str
    timestamp: int
    daystamp: str
    value: int
    comment: str
    updated_at: int
    requestid: str


def create_datapoint(goal: str, value: int, comment: str = "") -> requests.Response:
    """Add a new datapoint to user u's goal g — beeminder.com/u/g."""
    url = f"{URL}/users/{username}/goals/{goal}/datapoints.json"
    data = {
        "auth_token": auth_token,
        "value": value,
        "comment": comment,
    }
    return requests.post(url, data)
