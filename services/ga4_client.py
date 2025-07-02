from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange, Metric, RunReportRequest
)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


async def get_session_count(access_token: str, property_id: str):

    credentials = Credentials(
        token=access_token,
        refresh_token=None,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=None,
        client_secret=None,
        scopes=["https://www.googleapis.com/auth/analytics.readonly"]
    )


    client = BetaAnalyticsDataClient(credentials=credentials)


    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[],
        metrics=[Metric(name="sessions")],
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")]
    )

    response = client.run_report(request)
    

    if response.rows:
        return {
            "metric": "sessions_last_30_days",
            "value": response.rows[0].metric_values[0].value
        }
    else:
        return {
            "metric": "sessions_last_30_days",
            "value": "0"
        }
