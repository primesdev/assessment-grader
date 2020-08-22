from pprint import pprint
from sheet_service import batch_update_objective_rubric, create_new_sheet, get_sheet_range, push_csv_to_gsheet, update_google_sheet
from google_service import get_google_sheet_service
import numpy as np
import json

# Load Properties from JSON file.
with open('properties.json') as assessment_ranges_sheet:
      properties_dic = json.load(assessment_ranges_sheet)
SURVEY_MONKEY_SPREADSHEET_RANGE = properties_dic["survey_monkey_spreadsheet_range"]
SCORE_SHEET_RESPONSE_RANGE = properties_dic["score_sheet_response_range"]
SCORE_SHEET_OBJECTIVE_RANGE = properties_dic["score_sheet_objective_range"]
MENTEE_OBJECTIVE_SCORE_SHEET_RANGE = properties_dic["mentee_objective_score_sheet_range"]
CSV_FILE_PATH = properties_dic["csv_file_path"]
SCORE_SHEET_TEMPLATE_ID = properties_dic["score_sheet_template_id"]
MENTEE_OBJECTIVE_SCORE_SHEET_ID = properties_dic["mentee_objective_scoresheet_id"]

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
    mentee_names = [i[1] for i in survey]
    updated_rows = update_google_sheet(service, SCORE_SHEET_TEMPLATE_ID, SCORE_SHEET_RESPONSE_RANGE, survey)

    # get updated values from the rows
    objective_score_rows = get_sheet_range(service, SCORE_SHEET_TEMPLATE_ID, SCORE_SHEET_OBJECTIVE_RANGE)

    # copy A259-AU255 every other row starting with row[1]
    cohort_score_list = objective_score_rows[1::2]
    cohort_mentee_names = mentee_names[:len(cohort_score_list[0])]

    # TODO Convert to row range update, will need to seperate them out
    objective_update_rows = batch_update_objective_rubric(service, cohort_mentee_names, MENTEE_OBJECTIVE_SCORE_SHEET_ID, cohort_score_list)
    


if __name__ == '__main__':
    main()