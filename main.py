import asyncio
import discord
from discord import app_commands, Intents, Client, Interaction
from discord.ext import commands
import requests
import random
import json
import re
import os
import sympy

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(name = "greet", description = "Sends a greeting message.")
async def greet(interaction: discord.Interaction):
    await interaction.response.send_message("Hello there!")


@tree.command(name = "math", description = "Evaluates a mathematical expression.")
async def math(interaction: discord.Interaction, expression: str, precision: int = 2):
    try:
        result = sympy.sympify(expression).evalf(precision)
    except sympy.SympifyError:
        await interaction.response.send_message("Invalid expression.")
        return
    re.sub("^(\-?)0\.", r'\1.', "%.4f" % result)
    await interaction.response.send_message(f"The answer is {result}")


@tree.command(name = "roll", description = "Simulates rolling dice e.g 2d6 to roll 2 dice.")
async def roll(interaction: discord.Interaction, dice: str):
    rolls = dice.split("d")
    total = 0
    for i in range(0, int(rolls[0])):
        total += random.randint(1, int(rolls[1]))
    await interaction.response.send_message(f"You rolled a total of {total}.")


@tree.command(name = "dolar", description = "Fetches the current exchange rate of US dollars to Turkish lira.")
async def dolar(interaction: discord.Interaction):
    api_key = "TOKEN"
    url = "https://api.apilayer.com/fixer/latest"
    headers = {"apikey": api_key}
    params = {"base": "USD", "symbols": "USD,TRY"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(f"1 USD = {data['rates']['TRY']} TRY")
    try:
        # Print the exchange rate of USD to TRY
        await interaction.response.send_message(f"1 USD = {data['rates']['TRY']} TRY")
    except KeyError:
        #Print a message if the 'rates' or 'TRY' keys are not found in the response data
        await interaction.response.send_message("Sorry, I could not fetch the current exchange rate.")


@tree.command(name = "euro", description = "Fetches the current exchange rate of euros to Turkish lira.")
async def euro(interaction: discord.Interaction):
    api_key = "TOKEN"
    url = "https://api.apilayer.com/fixer/latest"
    headers = {"apikey": api_key}
    params = {"base": "EUR", "symbols": "EUR,TRY"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(f"1 EUR = {data['rates']['TRY']} TRY")
    try:
        # Print the exchange rate of EUR to TRY
        await interaction.response.send_message(f"1 EUR = {data['rates']['TRY']} TRY")
    except KeyError:
        #Print a message if the 'rates' or 'TRY' keys are not found in the response data
        await interaction.response.send_message("Sorry, I could not fetch the current exchange rate.")


@tree.command(name = "oyun", description = "Sends a message.")
async def oyun(interaction: discord.Interaction):
    await interaction.response.send_message("beni rahat bırakın")


@tree.command(name = "say", description = "Makes the bot say a message.")
async def say(interaction: discord.Interaction, *, message: str):
  # Send the message
  await interaction.response.send_message("Sent", ephemeral=True)
  await interaction.channel.send(message)


@tree.command(name = "joke", description = "Fetches a random joke from the icanhazdadjoke API and sends it to the channel.")
async def joke(interaction: discord.Interaction):
    # Fetch a random joke from the icanhazdadjoke API
    response = requests.get("https://icanhazdadjoke.com/",
                          headers={
                                "Accept": "text/plain",
                                "Content-Type": "text/plain; charset=utf-8"
                          })

    # Replace the special characters with their Unicode escape sequences
    joke = response.text.replace("â", "\u2019")

    # Send the joke to the channel
    await interaction.response.send_message(joke)


@tree.command(name = "quote", description = "Fetches a random quote from the Forismatic API and sends it to the channel.")
async def quote(interaction: discord.Interaction):
    # Fetch a random quote from the Forismatic API
    response = requests.get("http://api.forismatic.com/api/1.0/",
                          params={
                                "method": "getQuote",
                                "format": "text",
                                "lang": "en"
                          })

    # Send the quote to the channel
    await interaction.response.send_message(response.text)


@tree.command(name = "avatar", description = "Sends the avatar of a specified member to the channel.")
async def avatar(interaction: discord.Interaction, member: discord.Member, use_server_avatar: str = "default"):
    # Send the member's avatar to the channel
    if use_server_avatar.lower() == "server" or use_server_avatar.lower() == "true" or use_server_avatar.lower() == "yes":
        # Send the member's server-specific avatar if use_server_avatar is True
        await interaction.response.send_message(member.display_avatar)
    else:
        # Send the member's default avatar if use_server_avatar is False
        await interaction.response.send_message(member.avatar)


@tree.command(name = "sspam", description = "Sends a spam message.")
async def sspam(interaction: discord.Interaction):
    await interaction.response.send_message(
        "s\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\ns"
    )


commands = {}

@tree.command(name = "addcommand", description = "Adds a custom command to the bot.")
async def addcommand(interaction: discord.Interaction, message: str, answer: str):
    # Check if the user has the necessary permissions
    if interaction.channel.permissions_for(interaction.user).manage_messages:
        # Check if the bot has the necessary permissions
        if interaction.channel.permissions_for(interaction.guild.me).manage_messages:
            # Add the message and answer pair to the commands dictionary
            commands[message] = answer
            # Serialize the commands dictionary to a JSON object
            commands_json = json.dumps(commands)
            # Write the JSON object to the commands.txt file
            with open("commands.txt", "w") as f:
                f.write(commands_json)
            await interaction.response.send_message(f"Command '{message}' added successfully!")
    else:
        await interaction.response.send_message("You do not have the necessary permissions to add commands.")

with open("commands.txt", "r") as f:
  commands_json = f.read()
  commands = json.loads(commands_json)


@tree.command(name = "removecommand", description = "Removes a command from the commands dictionary.")
async def removecommand(interaction: discord.Interaction, message: str):
  # Check if the user has the necessary permissions
  if interaction.channel.permissions_for(interaction.user).manage_messages:
    # Check if the bot has the necessary permissions
    if interaction.channel.permissions_for(interaction.guild.me).manage_messages:
      # Check if the message is a key in the commands dictionary
      if message in commands:
        # Remove the message-answer pair from the commands dictionary
        del commands[message]
        # Serialize the updated commands dictionary to a JSON object
        commands_json = json.dumps(commands)
        # Write the JSON object to the commands.txt file
        with open("commands.txt", "w") as f:
          f.write(commands_json)
        await interaction.response.send_message(f"Command '{message}' removed successfully!")
      else:
        await interaction.response.send_message(f"Command '{message}' does not exist.")
  else:
    await interaction.response.send_message("You do not have the necessary permissions to remove commands.")
  

@tree.command(name = "listcommands", description = "Lists all custom commands.")
async def listcommands(interaction: discord.Interaction):
  command_list = "\n".join([f"{message}: {answer}" for message, answer in commands.items()])
  output = f"Commands:\n```\n{command_list}\n```"
  await interaction.response.send_message(output)


@tree.client.event
async def on_message(interaction: discord.Interaction):
  # Check if the message was sent by the bot
  if interaction.author == client.user:
    return

  # Check if the message is a command in the commands dictionary
  if interaction.content in commands:
    # Send the corresponding answer to the Discord channel
    await interaction.channel.send(commands[interaction.content])

try:
    client.run('TOKEN')
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    system("python restarter.py")
    system('kill 1')
#Keep bot always online on replit  
#client.run("TOKEN")
