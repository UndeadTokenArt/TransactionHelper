from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the necessary scopes for the Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

# Load the credentials from a JSON file (you can also set the credentials as environment variables)
credentials = service_account.Credentials.from_service_account_file(
    'service-account.json')

# Create a Drive API client
drive_service = build('drive', 'v3', credentials=credentials)

# Define the metadata for the new spreadsheet
spreadsheet_metadata = {
    'name': 'My Spreadsheet',
    'sheets': [{
        'properties': {
            'title': 'Sheet 1'
        }
    }]
}

# Create the new spreadsheet
created_spreadsheet = drive_service.spreadsheets().create(body=spreadsheet_metadata).execute()

# Get the ID of the newly created spreadsheet
spreadsheet_id = created_spreadsheet['spreadsheetId']

# Define the data to be written to the spreadsheet
data = [['Name', 'Email'], ['John', 'john@example.com'], ['Jane', 'jane@example.com']]

# Define the range where the data should be written
range_name = 'Sheet1!A1:B3'

# Define the request to write the data to the spreadsheet
request = drive_service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id,
    range=range_name,
    valueInputOption='USER_ENTERED',
    body={'values': data}).execute()

# Print the response
print(request)
