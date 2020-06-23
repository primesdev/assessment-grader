from pprint import pprint
from sheet_service import get_sheet_range, update_google_sheet
from google_service import get_google_sheet_service
import numpy as np

# Survey ids and ranges for template sheets.
SURVEY_MONKEY_SPREADSHEET_ID = '1GFt9XSIfjykkpWqiaLRamSZC8ad-8DNW02i9jGKy_IM'
SURVEY_MONKEY_SPREADSHEET_RANGE = 'J1:EN1000'
SCORE_SHEET_TEMPLATE_ID = '1EBmFujKhO84_DEZye3-kPag_-G2pWU5pUec_8YbAp3Q'#'1coMbBVBZn8PLlXwXIQGHY3HYoitzSxhxrR7huEnu3Fk'
SCORE_SHEET_RESPONSE_RANGE = 'Sheet1!B1:EN1000'
SCORE_SHEET_OBJECTIVE_RANGE = 'A259:AU368'
MENTEE_OBJECTIVE_SCORE_SHEET_ID = '1K66En-MrFQ6c2GL7Anu9050tB8J4PRBG1c-tuMF8M1U'
MENTEE_OBJECTIVE_SCORE_SHEET_RANGE = 'Cohort!D12:Q53'
def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    service = get_google_sheet_service()

    # get survey
    survey = get_sheet_range(service, SURVEY_MONKEY_SPREADSHEET_ID, SURVEY_MONKEY_SPREADSHEET_RANGE)
    # print('Name, Major:')
    for row in survey:
    # Print rows
      pprint('%s,' % (row))
    
    # skip first two rows in upload
    survey = survey[2:]
    updated_rows = update_google_sheet(service, SCORE_SHEET_TEMPLATE_ID, SCORE_SHEET_RESPONSE_RANGE, survey)

    # get updated values from the rows
    objective_score_rows = get_sheet_range(service, SCORE_SHEET_TEMPLATE_ID, SCORE_SHEET_OBJECTIVE_RANGE)

    objective_score_rows_value_array = objective_score_rows[1::2]
    object_value_ndarrays = np.transpose(objective_score_rows_value_array)
    transpose_array = object_value_ndarrays.T.tolist()
    # copy A259-AU255 every other row starting with row[1]
    objective_update_rows = update_google_sheet(service, MENTEE_OBJECTIVE_SCORE_SHEET_ID, MENTEE_OBJECTIVE_SCORE_SHEET_RANGE, transpose_array)

    
    



if __name__ == '__main__':
    main()