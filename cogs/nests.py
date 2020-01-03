# Author : Hillari Denny
# ~1/1/2020

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
prefix = os.getenv('prefix')


# Don't need this anymore, but leaving it for now.
# def search_dict(pkmn):
#     """ Search through our dictionary and return the results"""
#     results = None
#     if pkmn.lower() in pkmn_dict:
#         results = pkmn_dict[pkmn.lower()]
#     return results


def build_nest_dict():
    """ Helper for nest commands & functions.
    Uses the Google Sheets API to build a dictionary from current nests."""
    print("Creating a new dictionary")
    values = main()  # FIXME restructure so we aren't using main to get sheet values
    for row in values:
        if row is not None:
            key = ''.join(row[0:1]).lower()  # Storing as lower case so we can ignoring cases when searching
            value = list((row[1:]))
            if key and value:
                pkmn_dict[key] = value
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

    # @commands.command()
    # async def printsheet(self, ctx):
    #     """For testing purposes. Depends on the A1 notation used in main() """
    #     values = main()
    #     if not values:
    #         msg = "No data found"
    #     else:
    #         for row in values:
    #             msg = values
    #             # Print columns A and E, which correspond to indices 0 and 4.
    #             # print('%s, %s' % (row[0], row[4]))
    #             # print(row[0], " - ", row[1])
    #     await ctx.send(msg)

    # @commands.has_role(ctx.message, nestlead)
    @commands.command()
    async def buildnest(self, ctx):
        """Creates a data structure to hold all the sheet values.
         Intended use of this function is for Staff to create a dictionary
         all at once after all nests have been found. """

        # Would be good to make try/except, but what kind of exception to catch?? KeyError & ...?
        if build_nest_dict():
            await ctx.channel.send("Nest database built successfully.")
        else:
            await ctx.channel.send("Build failed.")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """
        Hillari Denny and Kris Carroll

        Listener will scan every message in specified channel for the prefix
        Once it finds the prefix, we search the dictionary and report results back to channel
        NOTE: You *must* have run !buildnest in order for this function to work"""

        spamchan = 646622175016779801  # TODO don't hardcode this. Maybe put in list to check.
        if ctx.channel.id == spamchan:
            if ctx.content.startswith('$'):  # Only process messages appropriately prefixed
                search = ctx.content.split()  # Grab up to first whitespace, split, pass to dict
                pkmn = search[0][1:]
                try:
                    results = pkmn_dict[pkmn.lower()]
                    msg = "Found the following nest(s) for " + pkmn.capitalize() + ":\n"
                    for result in results:
                        (lat, long) = result.split(',')
                        msg += "> {}, {}\n".format(lat, long)
                    await ctx.channel.send(msg)
                except KeyError:
                    results = None  # Set results to None so we can inform user why the search failed
                    # TODO add checks for when a user misspells/enters something that is not a pokemon
                    if pkmn not in nesting_pkmn_list:
                        await ctx.channel.send("Sorry, " + pkmn.capitalize() + " does not nest.")
                    if pkmn in nesting_pkmn_list and results is None:
                        await ctx.channel.send("Sorry, we haven't found any nests for " + pkmn.capitalize() + " yet.")


if __name__ == '__main__':
    main()


def setup(bot):
    bot.add_cog(Nests(bot))
