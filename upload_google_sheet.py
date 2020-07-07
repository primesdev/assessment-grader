from googleapiclient.discovery import build

# convenience routines
def find_sheet_id_by_name(service, spreadsheet_id, sheet_name):
  API = service
  # ugly, but works
  sheets_with_properties = API \
      .spreadsheets() \
      .get(spreadsheetId=spreadsheet_id, fields='sheets.properties') \
      .execute() \
      .get('sheets')

  for sheet in sheets_with_properties:
      if 'title' in sheet['properties'].keys():
          if sheet['properties']['title'] == sheet_name:
              return sheet['properties']['sheetId']


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
