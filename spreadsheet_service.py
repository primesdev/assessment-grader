from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

def copy_spreadsheet(service, orig_spreadsheet_id, orig_sheet_id, new_spreadsheet_id):
    body = {
        "destinationSpreadsheetId": new_spreadsheet_id
    }
    request = service.spreadsheets().sheets().copyTo(spreadsheetId=orig_spreadsheet_id, sheetId=orig_sheet_id, body=body)
    response = request.execute()
    if not response:
        print("no response for sheet update request")
        return

    return response

def get_spreadsheet_properties(service, spreadsheet_id):
    request = service.spreadsheets().get(spreadsheetId=spreadsheet_id)
    response = request.execute()
    if not response:
        print('No data found.')
        return
    else:  
        return response
  
def get_spreadsheet_range(service, spreadsheet_id, range):
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
      spreadsheet_id ([string]): Id of spreadsheet to update
      range_to_update ([string]): Google Sheets notation string for the range of cells to update
      rows ([array]): Array of rows to insert
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

  request = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, includeValuesInResponse=True, body=value_range_body)
  response = request.execute()
  if not response:
      print("no response for sheet update request")
      return
  
  return response

def batch_update_objective_rubric(service, mentee_names, spreadsheet_id, rows):
    major_dim = "COLUMNS"
    start_row_num = 12
    row_length = len(rows[0])
    end_row_num = start_row_num + row_length
    mentee_column_range = f'A{start_row_num}:A{end_row_num}'
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
                "range": mentee_column_range,
                "values": [mentee_names]
            },
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


def create_new_spreadsheet(service, name):
  spreadsheet_body = {
    "properties": {
      "title": name
    }
  }

  request = service.spreadsheets().create(body=spreadsheet_body)
  response = request.execute()
  return response

def push_csv_to_gsheet(service, csv_path, spreadsheet_id, sheet_id):
  """Pushes a csv file to google sheets api.

  Args:
      service ([Google resource]): [resource for accessing sheets api]
      csv_path ([string]): [filepath for csv file to be uploaded]
      spreadsheet_id ([string]): [id of spreadsheet to upload file]
      sheet_id ([string]): [id for which worksheet to upload data]

  Returns:
      [Google Spreadsheet]: [Spreadsheet includes id, sheets]
  """  
  API = service
  with open(csv_path, 'r') as csv_file:
      csvContents = csv_file.read()
  body = {
      'requests': [{
          'pasteData': {
              "coordinate": {
                  "sheetId": sheet_id,
                  "rowIndex": "0",  # adapt this if you need different positioning
                  "columnIndex": "0", # adapt this if you need different positioning
              },
              "data": csvContents,
              "type": 'PASTE_NORMAL',
              "delimiter": ',',
          }
      }]
  }
  request = API.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
  response = request.execute()
  return response
