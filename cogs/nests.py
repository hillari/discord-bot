
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
import os
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = 'Current Nests!A3:B50'
NEST2 = 'Current Nests!A3:D5'
ALL_CELLS = 'Current Nests'


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

    @commands.command()
    async def buildnest(self, ctx):
        build_nest_dict()

    @commands.command()
    async def nest(self, ctx, pkmn):
        nesting_pkmn = nester_list()
        values = main()
        if pkmn.lower() not in (line.lower() for line in nesting_pkmn):
            await ctx.send("Sorry, " + pkmn + " does not nest.")
        for row in values:
            if ''.join(row[0:1]) == pkmn:  # join() takes iterable (ie our row) and returns a string
                print("Found pkmn")
                coords = row[1:2]
                await ctx.send("Found some " + pkmn + " nests!\n" + str(coords).strip('[]'))


def nester_list():
    nesting_pkmn_list = open("./files/nesting_pokemon.txt").read().splitlines()  # splitlines will get rid of newline
    return nesting_pkmn_list


def build_nest_dict():
    """ Helper for nest functions
    Uses the Google Sheets API to build a dictionary from current nests"""
    pkmn_dict = {}
    values = main()
    for row in values:
        if row is not None:
            key = str(row[0:1])
            value = list((row[1:]))
            if key and value:
                pkmn_dict[key] = value
    print(pkmn_dict)
    return pkmn_dict


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
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range=ALL_CELLS).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    # else:
    #     print('Pokemon, Nests:')
    #     for row in values:
    #         # Print columns A and E, which correspond to indices 0 and 4.
    #         # print('%s, %s' % (row[0], row[4]))
    #         print(row[0], " - ", row[1])
    return values


if __name__ == '__main__':
    main()


def setup(bot):
    bot.add_cog(Nests(bot))
