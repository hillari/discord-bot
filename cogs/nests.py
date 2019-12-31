
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
# Sheet variables
load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
RANGE_NAME = 'Current Nests!A3:B50'
NEST2 = 'Current Nests!A3:D5'
ALL_CELLS = 'Current Nests'

# Global stuffs
pkmn_dict = {}
nesting_pkmn_list = open("./files/nesting_pokemon.txt").read().splitlines()


def search_dict(pkmn):
    """ Search through our dictionary and return the results"""
    # TODO handle if the dictionary does not exist yet?
    results = None
    if pkmn.lower() in pkmn_dict:
        results = pkmn_dict[pkmn.lower()]
    return results


def build_nest_dict():
    """ Helper for nest commands & functions.
    Uses the Google Sheets API to build a dictionary from current nests. Also acts as a getter"""
    res = not pkmn_dict
    if res:  # Only create if it does not already exist
        print("Creating a new dictionary")
        values = main()
        for row in values:
            if row is not None:
                key = ''.join(row[0:1]).lower()  # Storing as lower case so we can ignoring cases when searching
                value = list((row[1:]))
                if key and value:
                    pkmn_dict[key] = value
    else:
        print("This dict already exists")
    # print(pkmn_dict)
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
    return values

# ---- Beginning of cog class/functions --- #


class Nests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    async def printsheet(self, ctx):
        """For testing purposes. Depends on the A1 notation used in main() """
        values = main()
        if not values:
            msg = "No data found"
        else:
            for row in values:
                msg = values
                # Print columns A and E, which correspond to indices 0 and 4.
                # print('%s, %s' % (row[0], row[4]))
                # print(row[0], " - ", row[1])
        await ctx.send(msg)

    @commands.command()
    async def buildnest(self, ctx):
        """Creates a data structure to hold all the sheet values."""
        build_nest_dict()

    @commands.command()
    async def nest(self, ctx, pkmn):
        """Returns a list of nests. Usage: nest <Abra> """

        # TODO handle if someone entered a pokemon name incorrectly
        # Do something like this
        #
        # if pkmn.lower() in all_pkmn_list:
        #     if pkmn.lower() not in nesting_pkmn_list:
        #         await ctx.send("Sorry, " + pkmn + " does not nest.")
        #         return
        # else:
        #     await ctx.send("Sorry, " + pkmn + " is not a pokemon")
        #     return

        spamchan = 646622175016779801
        if ctx.channel.id == spamchan:
            if pkmn.lower() not in nesting_pkmn_list:
                await ctx.channel.send("Sorry, " + pkmn + " does not nest.")
                return
            build_nest_dict()
            results = search_dict(pkmn)
            if len(results) > 1:
                nests = ' nests\n'
            else:
                nests = ' nest\n'
            print("RESULTS: ", results)
            if results is not None:
                await ctx.send("Found these " + pkmn + nests + '\n'.join(results))
            else:
                await ctx.send("Sorry, can't find any nests for " + pkmn + " right now")


if __name__ == '__main__':
    main()


def setup(bot):
    bot.add_cog(Nests(bot))
