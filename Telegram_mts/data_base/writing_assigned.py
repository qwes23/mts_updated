import sqlite3 as sq

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def update_values(spreadsheet_id, range_name, value_input_option, values):
    
    creds = '/home/grigory/Local/Work/Telegram_mts/Telegram_mts/data_base/new1.json'
    # pylint: disable=maybe-no-member
    try:

        service = build('sheets', 'v4', credentials=creds)
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Pass: spreadsheet_id,  range_name, value_input_option and  _values
    update_values("1T6cGkIk1CGB7RI27bo9AQobp4dtap2tiFIRIgsPxl0E",
                  "A2:B3", "USER_ENTERED",
                  [
                      ['A', 'B'],
                      ['C', 'D']
                  ])