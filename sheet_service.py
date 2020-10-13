from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

def add_google_sheet(service, spreadsheet_id, sheet_name, rows):
    body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                    "title": sheet_name,
                    }
                }
            }
        ]
    }
    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    response = request.execute()
    if not response:
        print("no response for sheet update request")
        return

    return response

def clear_sheet_keep_formatting(service, spreadsheet_id, sheet_id):
    body = {
        "requests": [
            {
                "updateCells": {
                    "range": {
                    "sheetId": sheet_id,
                    },
                    "fields": "userEnteredValue"
                }
            }
        ]
    }
    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    response = request.execute()
    if not response:
        print("no response for sheet update request")
        return

    return response

def duplicate_sheet_func(service, spreadsheet_id, sheet_id, duplicate_sheet_name):
    body = {
            "requests": [
                {
                    "duplicateSheet": {
                        "sourceSheetId": sheet_id,
                        "newSheetName": duplicate_sheet_name
                    }
                }
            ]
        }
    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body)
    response = request.execute()
    if not response:
        print("no response for sheet update request")
        return

    return response
