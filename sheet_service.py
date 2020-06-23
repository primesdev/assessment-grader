from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

def get_sheet_range(service, spreadsheet_id, range):
  """Get a google sheet by id
  
  Args:
      service ([Resource]): Google resource to access api
      spreadsheet_id ([string]): [spreadsheet id]
      range ([string]): [Google A1 notation string]
  
  Returns:
      [array]: [array object containing the rows in the google sheet]
  """    
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=spreadsheet_id,
                              range=range,
                              ).execute()
  values = result.get('values', [])

  if not values:
      print('No data found.')
      return
  else:  
      return values

def update_google_sheet(service, spreadsheet_id, range_to_update, rows):
  """Update a Google Sheet

  Args:
      service ([Resource]): object for interacting w/Google API
      spreadsheet_id ([string]): [Id of spreadsheet to update]
      range_to_update ([string]): [Google Sheets notation string for the range of cells to update]
      rows ([array]): [Array of rows to insert]
  """  
  # The ID of the spreadsheet to update.
  spreadsheet_id = spreadsheet_id  # TODO: Update placeholder value.

  # The A1 notation of the values to update.
  range_ = range_to_update # TODO: Update placeholder value.

  # How the input data should be interpreted.
  value_input_option = 'USER_ENTERED'  # TODO: Update placeholder value.

  value_range_body = {
    "range": range_to_update,
    "values":rows,
    "majorDimension" : "COLUMNS"
   }

  request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=value_range_body)
  response = request.execute()
  if not response:
      print("no response for sheet update request")
      return
  
  return response