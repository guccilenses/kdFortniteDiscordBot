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
        await client.send_message(message.channel, 'Latest patch notes: https://www.epicgames.com/fortnite/en/news')
    # The command !help explains the one function
    if message.content.startswith('!help'):
        await client.send_message(message.channel, 'Set your Discord nickname to be exacly the same as your Epic Games account name. Then type \'!verify\'. The bot looks at your squad K/D for the current season, so if you have no games played yet, the bot can not verify you.')
    # The command !verify return attribute a rank according to the K/D of the user
    if message.content.startswith("!verify"):
        for list in LIST:
            roles = discord.utils.get(message.server.roles, name=list)
        username = '{0.author.display_name}'.format(message)
        ratio = float(get_ratio(username))
        msgRatio = str(ratio)
        msgVerified = str(VERIFIED)
        print(ratio)
        print("-")
        if ratio == -1.0:
            msg = "Your Discord name and IGN must be exactly the same. Change your Discord nickname and try again.".format(message)
            await client.send_message(message.channel, msg)
        elif ratio == -2.0:
            msg = "Data not found. Either Fortnite Tracker is down, or your account is not a PC account.".format(message)
            await client.send_message(message.channel, msg)
        elif ratio == -3.0:
            msg = "No stats found for squad mode in the current season. Play some games and try again.".format(message)
            await client.send_message(message.channel, msg)
        elif ratio > 0 and ratio < VERIFIED:
            role = discord.utils.get(message.server.roles, name=LIST[0])
            embed = discord.Embed(colour=discord.Colour(0x45278e), url="https://github.com/af1/kdFortniteDiscordBot",)
            embed.set_author(name="Verify " + message.author.name, icon_url=message.author.avatar_url)
            #embed.set_footer(text="Fortnite Verify Bot", icon_url=client.user.avatar_url)
            embed.add_field(name=message.author.name + " does not have over a " + msgVerified + " K/D.", value="Season 6 Squads K/D: **" + msgRatio + "**", inline=False)
            await client.send_message(message.channel, embed=embed)
        elif ratio >= VERIFIED:
            role = discord.utils.get(message.server.roles, name=LIST[0])
            embed = discord.Embed(colour=discord.Colour(0x45278e), url="https://github.com/af1/kdFortniteDiscordBot",)
            embed.set_author(name="Verify " + message.author.name, icon_url=message.author.avatar_url)
            #embed.set_footer(text="Fortnite Verify Bot", icon_url=client.user.avatar_url)
            embed.add_field(name=message.author.name + " has over a " + msgVerified + " K/D. Verified!", value="Season 6 Squads K/D: **" + msgRatio + "**", inline=False)
            await client.send_message(message.channel, embed=embed)
            await client.add_roles(message.author, role) 
            
@client.event
async def on_ready():
    print("-")
    print('Logged in as: ' + client.user.name)
    print('With Client User ID: ' + client.user.id)
    print("-")

client.run(DISCORD_TOKEN)
