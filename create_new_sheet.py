from googleapiclient import discovery

def create_new_sheet(service, name):
  spreadsheet_body = {
    "properties": {
      "title": name
    }
  }

  request = service.spreadsheets().create(body=spreadsheet_body)
  response = request.execute()
  return response

