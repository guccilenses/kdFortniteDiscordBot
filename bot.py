import discord
import requests
import math
from keys import GITHUB_DISCORD_TOKEN, GITHUB_FORTNITE_API_KEY

client = discord.Client()

# Constant
DISCORD_TOKEN = GITHUB_DISCORD_TOKEN
FORTNITE_API_KEY = GITHUB_FORTNITE_API_KEY

LIST = ['Verified']
VERIFIED = 4

# Return the current season squad K/D of the fortnite player
def get_ratio(username):
    try:
        print(username)
        link = 'https://api.fortnitetracker.com/v1/profile/pc/' + username
        response = requests.get(link, headers={'TRN-Api-Key': FORTNITE_API_KEY})
        if response.status_code == 200:
            collection = response.json()
            if 'error' in collection:
                return "-1"
            else:
                ratio = collection['stats']['curr_p9']['kd']['value']
                return ratio
            print("Invalid username")
            return "-1"
        else:
            print("Error parsing data.")
            return "-2"
    except KeyError:
        print("Error finding data. KeyError was returned.")
        return "-3"

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # The command !patch return a link with the lastest patch note
    if message.content.startswith('!patch'):
        await client.send_message(message.channel, 'Last patch notes: https://www.epicgames.com/fortnite/en/news')
    # The command !help explains the one function
    if message.content.startswith('!help'):
        await client.send_message(message.channel, 'Type \'!verify\'. That\'s it.')
    # The command !verify return attribute a rank according to the K/D of the user
    if message.content.startswith("!verify"):
        for list in LIST:
            roles = discord.utils.get(message.server.roles, name=list)
        username = '{0.author.display_name}'.format(message)
        ratio = float(get_ratio(username))
        msgVerified = str(VERIFIED)
        print(ratio)
        print("-")
        if ratio == -1.0:
            msg = "Your IGN and Discord name must be the same.".format(message)
            await client.send_message(message.channel, msg)
        elif ratio == -2.0:
            msg = "Looks like Fortnite Tracker servers are down. Please try again later!".format(message)
            await client.send_message(message.channel, msg)
        elif ratio == -3.0:
            msg = "Data not found. Do you have games played in squad mode this season?".format(message)
            await client.send_message(message.channel, msg)
        elif ratio > 0 and ratio < VERIFIED:
            role = discord.utils.get(message.server.roles, name=LIST[0])
            msg = ("{0.author.mention} doesn't have a " + msgVerified + " K/D").format(message) + "."
            await client.send_message(message.channel, msg)
        elif ratio >= VERIFIED:
            role = discord.utils.get(message.server.roles, name=LIST[0])
            msg = ("{0.author.mention} has over a " + msgVerified + " K/D. " + role.name).format(message) + "!"
            await client.send_message(message.channel, msg)
            await client.add_roles(message.author, role) 
            
@client.event
async def on_ready():
    print("-")
    print('Logged in as: ' + client.user.name)
    print('With Client User ID: ' + client.user.id)
    print("-")

client.run(DISCORD_TOKEN)
