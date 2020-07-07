from pprint import pprint
from sheet_service import get_sheet_range, update_google_sheet, batch_update_google_sheet
from google_service import get_google_sheet_service
from upload_google_sheet import find_sheet_id_by_name, push_csv_to_gsheet
from create_new_sheet import create_new_sheet
import numpy as np

# Survey ids and ranges for template sheets.
CSV_FILE_PATH = "resources/test/SurveyMonkey Data - Jeremy Test.csv"
SURVEY_MONKEY_SPREADSHEET_ID = '1GFt9XSIfjykkpWqiaLRamSZC8ad-8DNW02i9jGKy_IM'
SURVEY_MONKEY_SPREADSHEET_RANGE = 'J1:EN1000'
SCORE_SHEET_TEMPLATE_ID = '1EBmFujKhO84_DEZye3-kPag_-G2pWU5pUec_8YbAp3Q'#'1coMbBVBZn8PLlXwXIQGHY3HYoitzSxhxrR7huEnu3Fk'
SCORE_SHEET_RESPONSE_RANGE = 'Sheet1!B1:EN1000'
SCORE_SHEET_OBJECTIVE_RANGE = 'B259:AU368'
MENTEE_OBJECTIVE_SCORE_SHEET_ID = '1GbX4ja3mPaAzbqI3STzzSWwCbdX-WOYf33i9y2F2zzA'
MENTEE_OBJECTIVE_SCORE_SHEET_RANGE = 'Cohort!D12:Q53'
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    service = get_google_sheet_service()

    # create new sheet
    new_sheet = create_new_sheet(service, "Survey Monkey CSV Data")
    new_sheet_spreadsheet_id = new_sheet['spreadsheetId']
    first_worksheet = new_sheet['sheets'][0]
    # copy csv into new sheet
    push_csv_to_gsheet(service, CSV_FILE_PATH, 
      spreadsheet_id= new_sheet_spreadsheet_id,
      sheet_id= first_worksheet['properties']['sheetId'])
    
    # get survey
    survey = get_sheet_range(service, new_sheet_spreadsheet_id, SURVEY_MONKEY_SPREADSHEET_RANGE)
    # print('Name, Major:')
    for row in survey:
    # Print rows
      pprint('%s,' % (row))
    
    # skip first two rows in upload
    survey = survey[2:]
    updated_rows = update_google_sheet(service, SCORE_SHEET_TEMPLATE_ID, SCORE_SHEET_RESPONSE_RANGE, survey)

    # get updated values from the rows
    objective_score_rows = get_sheet_range(service, SCORE_SHEET_TEMPLATE_ID, SCORE_SHEET_OBJECTIVE_RANGE)

    # copy A259-AU255 every other row starting with row[1]
    cohort_score_list = objective_score_rows[1::2]

    # TODO Convert to row range update, will need to seperate them out
    objective_update_rows = batch_update_google_sheet(service, MENTEE_OBJECTIVE_SCORE_SHEET_ID, cohort_score_list)
    



if __name__ == '__main__':
    main()