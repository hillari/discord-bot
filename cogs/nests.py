
# re __future__ statement:
# https://docs.python.org/2/library/__future__.html
from __future__ import print_function
##
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
##
from discord.ext import commands


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
# TODO get these vars
SAMPLE_SPREADSHEET_ID = '1NWXK11Lu3iBUdgR20ZYh0A4geMz-8UyM1zO9prZr350'
SAMPLE_RANGE_NAME = 'Current Nests!A3:B8'


class Nests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def printsheet(self, ctx):
        values = main()
        if not values:
            msg = "No data found"
        else:
            for row in values:
                msg = values
                # Print columns A and E, which correspond to indices 0 and 4.
                # print('%s, %s' % (row[0], row[4]))
                print(row[0], " - ", row[1])
        await ctx.send(msg)


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Pokemon, Nests:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            # print('%s, %s' % (row[0], row[4]))
            print(row[0], " - ", row[1])
    return values


if __name__ == '__main__':
    main()


def setup(bot):
    bot.add_cog(Nests(bot))
