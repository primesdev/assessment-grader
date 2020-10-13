from pprint import pprint
from datetime import datetime
from spreadsheet_service import batch_update_objective_rubric, copy_spreadsheet, create_new_spreadsheet, get_spreadsheet_properties, get_spreadsheet_range, push_csv_to_gsheet, update_google_sheet
from sheet_service import duplicate_sheet_func, clear_sheet_keep_formatting
from id_util import get_ids_from_names
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

RUN_TIME_DATE_STRING = str(datetime.now())
RUN_TIME_FILE_NAME = "Survey Monkey CSV Data"  + RUN_TIME_DATE_STRING
SCORE_SHEET_TEMPLATE_NAME = properties_dic["score_sheet_template_name"] + RUN_TIME_DATE_STRING

def upload_objective_range(spreadsheet, ids_dict):
  service = get_google_sheet_service()
  # create new sheet
  # new_file_name = RUN_TIME_FILE_NAME
  # new_sheet = create_new_sheet(service, new_file_name)
  spreadsheet_id = spreadsheet['spreadsheetId']
  first_worksheet = spreadsheet['sheets'][0]
  # duplicate sheet
  second_worksheet = duplicate_sheet_func(service, spreadsheet_id, first_worksheet["properties"]["sheetId"], "Sheet 2")
  # clear all values except for macros
  second_worksheet_id = second_worksheet["spreadsheetId"]
  cleared_second_sheet = clear_sheet_keep_formatting(service, spreadsheet_id, second_worksheet_id)
  # upload id rows and user emails
  id_mapping_rows = list(map(list, ids_dict.items()))
  return update_google_sheet(service, spreadsheet, second_worksheet_id["properties"]["title"], id_mapping_rows)

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    service = get_google_sheet_service()

    # create new sheet
    new_file_name = RUN_TIME_FILE_NAME
    new_spreadsheet = create_new_spreadsheet(service, new_file_name)
    new_spreadsheet_id = new_spreadsheet['spreadsheetId']
    first_worksheet = new_spreadsheet['sheets'][0]
    first_worksheet_id = first_worksheet['properties']['sheetId']
    # copy csv into new sheet
    push_csv_to_gsheet(service, CSV_FILE_PATH, 
      spreadsheet_id= new_spreadsheet_id,
      sheet_id= first_worksheet_id)
    
    # get survey
    survey = get_spreadsheet_range(service, new_spreadsheet_id, SURVEY_MONKEY_SPREADSHEET_RANGE)
    # print('Name, Major:')
    for row in survey:
    # Print rows
      pprint('%s,' % (row))
    
    # skip first two rows in upload
    survey = survey[2:]

    #generate mentee ids and save them to file
    mentee_names = [i[1] for i in survey]
    mentee_ids = get_ids_from_names(mentee_names)
    id_mapping_dict = dict(zip(mentee_ids, mentee_names))

    with open('name_id_mapping_sheet.json', 'w', encoding='utf-8') as id_key_sheet:
      json.dump(id_mapping_dict, id_key_sheet, indent=4, separators=(',', ': '), ensure_ascii=False)

    updated_score_sheet_template = update_google_sheet(service, SCORE_SHEET_TEMPLATE_ID, SCORE_SHEET_RESPONSE_RANGE, survey)
    updated_template_sheet_properties = get_spreadsheet_properties(service, SCORE_SHEET_TEMPLATE_ID)
    first_score_template_sheet_id = updated_template_sheet_properties["sheets"][0]["properties"]["sheetId"]
    # create new template sheet
    scoring_template_sheet = create_new_spreadsheet(service, SCORE_SHEET_TEMPLATE_NAME)

    # copy template to new sheet
    template_duplicate = copy_spreadsheet(service, SCORE_SHEET_TEMPLATE_ID, first_score_template_sheet_id, scoring_template_sheet["spreadsheetId"])

    # get updated values from the rows
    objective_score_rows = get_spreadsheet_range(service, SCORE_SHEET_TEMPLATE_ID, SCORE_SHEET_OBJECTIVE_RANGE)

    # copy A259-AU255 every other row starting with row[1]
    cohort_score_list = objective_score_rows[1::2]
    cohort_mentee_names = mentee_ids[:len(cohort_score_list[0])]

    # TODO Convert to row range update, will need to seperate them out
    objective_update_rows = batch_update_objective_rubric(service, cohort_mentee_names, MENTEE_OBJECTIVE_SCORE_SHEET_ID, cohort_score_list)
    

if __name__ == '__main__':
    main()