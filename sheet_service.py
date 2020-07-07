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

def batch_update_google_sheet(service, spreadsheet_id, rows):
    major_dim = "COLUMNS"
    start_row_num = 12
    end_row_num = start_row_num + len(rows[0])
    obj_1_range = f'D{start_row_num}:Q{end_row_num}'
    obj_2_range = f'AG{start_row_num}:AT{end_row_num}'
    obj_3_range = f'BJ{start_row_num}:BP{end_row_num}'
    obj_4_range = f'CF{start_row_num}:CL{end_row_num}'
    obj_5_range = f'DB{start_row_num}:DG{end_row_num}'
    obj_6_range = f'DW{start_row_num}:EC{end_row_num}'

    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {
            "majorDimension": major_dim,
            "range": obj_1_range,
            "values": rows[0:13]
            },
            {
            "majorDimension": major_dim,
            "range": obj_2_range,
            "values": rows[14:27]
            },
            {
            "majorDimension": major_dim,
            "range": obj_3_range,
            "values": rows[28:34]
            },
            {
            "majorDimension": major_dim,
            "range": obj_4_range,
            "values": rows[35:41]
            },
            {
            "majorDimension": major_dim,
            "range": obj_5_range,
            "values": rows[42:47]
            },
            {
            "majorDimension": major_dim,
            "range": obj_6_range,
            "values": rows[48:54]
            }
        ]
    }
    request = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    response = request.execute()
    return response
