import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import List, Any
from itertools import zip_longest

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
pickle_file = os.path.join(os.path.dirname(__file__), 'token.pickle')
credentials_file = os.path.join(os.path.dirname(__file__), 'credentials.json')


def create_sheets_client():
    """ Login to Google API with either previously saved refresh token
    or run a new authorization flow from credentials. """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_file, 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service


def read_values_from_sheet(spreadsheet_id, ranges) -> List[Any]:
    """ Make a request to Sheets API and return response values """
    service = create_sheets_client()
    request = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=ranges)
    response = request.execute()
    value_ranges = response.get('valueRanges', [])
    return value_ranges


def read_config_dicts_from_sheet(spreadsheet_id, layout):
    """ Read provided addresses from Sheets API and return name-value pairs in a dict """
    config_dicts = list()
    field_names = list()
    ranges = list()
    for field_name, field_cell_address in layout.cell_addresses.items():
        field_names.append(field_name)
        ranges.append('!'.join((layout.sheet_name, field_cell_address)))  # get address like "Sheet!A1"
    value_ranges = read_values_from_sheet(spreadsheet_id=spreadsheet_id, ranges=ranges)
    # Calculate length of the longest row
    table_width = max(len(value_range.get('values', [[]])[0]) for value_range in value_ranges)
    for i in range(table_width):
        config_dict = dict()
        for field_name, value_range in zip(field_names, value_ranges):
            try:
                config_dict[field_name] = value_range['values'][0][i]
            except (KeyError, IndexError, ValueError):
                config_dict[field_name] = None
        config_dicts.append(config_dict)
    return config_dicts
