from discord.ext import commands
from replit import db
import dns.query
import weblinks
import discord
import os
import time
import datetime
import psutil
import asyncio
import pymongo
import json
import sys


#Config
prefix = "?"
token = os.environ["DISCORD_TOKEN"]
client = commands.Bot(
  command_prefix=prefix, 
  intents=discord.Intents.all()
)
client.remove_command("help")

username = os.environ["DB_USERNAME"]
password = os.environ["DB_PASSWORD"]
database = f"mongodb+srv://{username}:{password}@cluster0.buvu1.mongodb.net/database?retryWrites=true&w=majority"
database = pymongo.MongoClient(database)

commands = {
  "help" : {
    "name" : "help",
    "description" : "View the help menu.",
    "perms" : 0,
    "usage" : "{Command}",
    "permName" : "User"
  },

  "calc" : {
    "name" : "calc",
    "description" : "Calculate a mathmatical expression.",
    "perms" : 7,
    "usage" : "[Expression]",
    "permName" : "Owner"
  },

  "plot" : {
    "name" : "plot",
    "description" : "View statisitics of a CBP plot.",
    "perms" : 0,
    "usage" : "[PlotID]",
    "permName" : "User"
  },

  "botstats" : {
    "name" : "botstats",
    "description" : "View the statistics for the bot.",
    "perms" : 0,
    "usage" : "",
    "permName" : "User"
  },

  "restart" : {
    "name" : "restart",
    "description" : "Restart the bot.",
    "perms" : 5,
    "usage" : "",
    "permName" : "DEVELOPER"
  },

  "updateguidelines" : {
    "name" : "updateguidelines",
    "description" : "Update the guidelines in <#835886069517647903> channel.",
    "perms" : 6,
    "usage" : "",
    "permName" : "ADMIN"
  },

  "stats" : {
    "name" : "stats",
    "description" : "View suggestion stats of a user.",
    "perms" : 0,
    "usage" : "[UserID]",
    "permName" : "User"
  }

}

#Bot Code
async def permsCalc(ctx):
  global perm
  global permInt

  for role in reversed(ctx.author.roles):
    role = role.id

    if role == 781542046778785862:
      permInt = 7
      perm = "OWNER"
      return()

    if role == 786292786088902676:
      permInt = 6
      perm = "ADMIN"
      return()

    if role == 789481171683115038:
      permInt = 5
      perm = "DEVELOPER"
      return()

    if role == 815939052817612832:
      permInt = 4
      perm = "BUILDER"
      return()
  
    if role == 786292735241486377:
      permInt = 3
      perm = "MODERATOR"
      return()

    if role == 785407257419841538:
      permInt = 2
      perm = "TESTER"
      return()

    if role == 818901245095182337:
      permInt = 1
      perm = "RETIRED STAFF"
      return()

  permInt = 0
  perm = "USER"

@client.command(no_pm=True, name="plot")
async def plot_(ctx, args="0"):
  data = database.discStudiosBot.plotData.find_one({"_id":args})
  if data == None:
    embed = discord.Embed(
      color=0xff0000,
      title="Error!",
      description="Plot was not found."
    )
    await ctx.send(embed=embed)
  else:
    embed = discord.Embed(
      title = f"Plot Infomation ({args})"
    )
    
    name = data["name"]
    owner = data["owner"]
    node = data["node"]
    size = "Basic"
    tags = data["tags"]
    autoClear = data["autoClear"]
    lastActive = data["lastActive"]
    whitelisted = data["whitelisted"]
    playerCount = data["playerCount"]
    currentVotes = data["currentVotes"]
    barrelLoc = data["barrelLoc"]

    icon = data["icon"]
    icon = str(os.environ["ITEM_API"] + icon + ".png")
    embed.add_field(
      name = "Name",
      value = name
    )
    embed.add_field(
      name = "Owner",
      value = owner
    )
    embed.add_field(
      name = "Node",
      value = node
    )
    embed.add_field(
      name = "Plot Size",
      value = size
    )
    embed.add_field(
      name = "Plot Tags",
      value = tags
    )
    embed.add_field(
      name = "Auto Clear Date",
      value = autoClear
    )
    embed.add_field(
      name = "Last Active Date",
      value = lastActive
    )
    embed.add_field(
      name = "Whitelisted",
      value = whitelisted
    )
    embed.add_field(
      name = "Player Count",
      value = playerCount
    )
    embed.add_field(
      name = "Current Votes",
      value = currentVotes
    )
    embed.add_field(
      name = "Barrel Loc",
      value = barrelLoc
    )
    
    embed.set_thumbnail(
      url = icon
    )
    await ctx.send(embed=embed)

@client.command(no_pm=True, name="updateguidelines")
async def updateguidelines_(ctx):
  f = open("guidelines.txt", "r")
  text = f.read()
  text = text.split("***")
  guild = client.get_guild(778299599697215528)
  channel = guild.get_channel(835886069517647903)
  index = 0
  for message in text:
    index += 1
    if index == 2:
      embed = discord.Embed(
        color=0x2C2F33,
        title="Creative Build Plots - Vote Event",
        description="When using @vote on a plot it triggers this event."
      )
      embed.add_field(
        name="Uses",
        value="- Can give rewards for users voting on a plot.\n- It would make plots more interesting and enjoyable.",
        inline=False
      )
      await channel.send(embed=embed, content="\n**Example Suggestion**")
    elif index == 4:
      embed = discord.Embed(
        color=0x2C2F33,
        title="Creative Build Plots - Player Action: Send Message does not work with numbers",
        description="When using Send Message with numbers as arguments, it doesn't work."
      )
      embed.add_field(
        name="Reproduction",
        value="1. Place a player action: Send Message\n2. Put a number in the parameter chest\n3. Run the code",
        inline=False
      )
      embed.add_field(
        name="Expected Result",
        value="The message is sent to the player as text.",
        inline=False
      )
      embed.add_field(
        name="Actual Result",
        value="No message is sent.",
        inline=False
      )
      await channel.send(embed=embed, content="\n**Example Issue**")
    else:
      await channel.send(message)

  f.close()

@client.command(no_pm=True, name="restart")
async def restart_(ctx):
  await ctx.send("Restarting the bot...")
  db["restart"] = [ctx.channel.id]
  db["restartTime"] = int(time.time())
  python = sys.executable
  os.execl(python, python, * sys.argv)

@client.command(no_pm=True, name="calc")
async def calc_(ctx, *, args="0*0"):
  try:
    x = eval(args)
  except Exception as e:
    x = f"An error occured: {e}"

  embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3)
  embed.add_field(name="📥 Input", value=f"```{args}```", inline=False)
  embed.add_field(name="📤 Output", value=f"```{x}```", inline=False)
  embed.set_footer(text=f"Requested by {ctx.author}")
  await ctx.send(embed=embed)

@client.command(no_pm=True, name="botstats")
async def botstats_(ctx):
  embed = discord.Embed(timestamp=(datetime.datetime.now()), color=0xfff9b3, description="**📊 Disc Studios Bot - Statistics**")

  ping = round(((client.latency) * 1000), 1)

  embed.add_field(name="• Ram Usage", value=f"{psutil.virtual_memory().percent}%", inline=False)
  embed.add_field(name="• CPU Usage", value=f"{psutil.cpu_percent()}%", inline=False)
  embed.add_field(name="• Users", value=ctx.guild.member_count)
  embed.add_field(name="• Channels", value=len(ctx.guild.channels), inline=False)
  embed.add_field(name="• API Latency", value=f"{ping}ms", inline=False)
  await ctx.send(embed=embed)

@client.command(no_pm=True, name="help")
async def help_(ctx, *, args="Menu"):
  await permsCalc(ctx)
  if args == "Menu":
    embed = discord.Embed(
      color=0xfff9b3
    )
    embed.set_footer(
      text=f"Your permissions: {perm}"
    )
    for command in commands:
      command = commands[command]

      if permInt >= command["perms"]:
        name = command["name"]
        description = command["description"]
        embed.add_field(
          name=name, 
          value=description,
          inline=False
        )
        embed.set_thumbnail(
          url="https://cdn.discordapp.com/attachments/822792824780095528/835185578030137344/Music_Disc_Chirp_JE1_BE1.png"
        )
    
    await ctx.send(embed=embed)

  else:
    if args in commands:
      command = commands[args]
      name = command["name"]
      description = command["description"]
      permName = command["permName"]
      usage = command["usage"]
      usage = f"{prefix}{name} {usage}"

      embed = discord.Embed(
        title="Command Infomation:",
        color=0xfff9b3
      )
      embed.set_footer(
        text=f"Your permissions: {perm}"
      )
      embed.add_field(
        name="Name", 
        value=f"{name}",
        inline=False
      )
      embed.add_field(
        name="Description", 
        value=f"{description}",
        inline=False
      )
      embed.add_field(
        name="Usage", 
        value=f"{usage}",
        inline=False
      )
      embed.add_field(
        name="Required Permission", 
        value=f"{permName}",
        inline=False
      )
      embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/822792824780095528/835185578030137344/Music_Disc_Chirp_JE1_BE1.png"
      )
      await ctx.send(embed=embed)

    else:
      embed = discord.Embed(
        timestamp=(datetime.datetime.now()), 
        color=0xff0000
      )
      embed.add_field(name="Error:", value=f"This command was not found, commands are listed in {prefix}help")
      await ctx.send(embed=embed)

@client.command(no_pm=True, name="stats")
async def stats_(ctx, args="0"):
  if args == "0":
    args = str(ctx.author.id)
  
  try:
    data = database.discStudiosBot.suggestionData.find_one({"_id":f"{args}"})
    data = data["data"]
    suggestionsList = data

  except:
    embed = discord.Embed(
      timestamp=(datetime.datetime.now()), 
      color=0xff0000
    )
    embed.add_field(name="Error:", value=f"This user was not found.")
    await ctx.send(embed=embed)
    return

  suggestions = 0
  messages = []
  for suggestion in data:
    try:
      channel = ctx.guild.get_channel(830867541601419264)
      message = await channel.fetch_message(suggestion)
    except:
      try:
        channel = ctx.guild.get_channel(834466482464227378)
        message = await channel.fetch_message(suggestion)
      except:
        suggestionsList.remove(suggestion)
    
    try:
      suggestions += 1
      messages.append(message)

    except:
      message = "0"

  denied = 0
  possible = 0
  dupe = 0
  confirmedbug = 0
  accepted = 0
  patched = 0
  altimpl = 0
  impossible = 0
  notdiscstudios = 0
  general = 0

  totalReactions = []

  for reactions in messages:
    for react in reactions.reactions:
      if f"<:{react.emoji.name}:{react.emoji.id}>" not in totalReactions:
        totalReactions.append(f"<:{react.emoji.name}:{react.emoji.id}>")

      if react.emoji.name == "denied":
        denied += 1

      if react.emoji.name == "possible":
        possible += 1
      
      if react.emoji.name == "dupe":
        dupe += 1

      if react.emoji.name == "confirmedbug":
        confirmedbug += 1

      if react.emoji.name == "accepted":
        accepted += 1

      if react.emoji.name == "patched":
        patched += 1

      if react.emoji.name == "altimpl":
        altimpl += 1

      if react.emoji.name == "impossible":
        impossible += 1

      if react.emoji.name == "notdiscstudios":
        notdiscstudios += 1

      if react.emoji.name == "general":
        general += 1

  finalReactions = ["<:news:834457524886569010>"]
  for reactionImage in totalReactions:
    if reactionImage == "<:denied:809049370821394432>":
      finalReactions.append(f"<:denied:809049370821394432> {denied}")

    if reactionImage == "<:possible:809834594014724138>":
      finalReactions.append(f"<:possible:809834594014724138> {possible}")

    if reactionImage == "<:dupe:809049370912882729>":
      finalReactions.append(f"<:dupe:809049370912882729> {dupe}")

    if reactionImage == "<:confirmedbug:809834670543732748>":
      finalReactions.append(f"<:confirmedbug:809834670543732748> {confirmedbug}")

    if reactionImage == "<:accepted:809049370649427969>":
      finalReactions.append(f"<:accepted:809049370649427969> {accepted}")

    if reactionImage == "<:patched:820676613883691034>":
      finalReactions.append(f"<:patched:820676613883691034> {patched}")

    if reactionImage == "<:altimpl:809834670325628931>":
      finalReactions.append(f"<:altimpl:809834670325628931> {altimpl}")

    if reactionImage == "<:impossible:809834670590132234>":
      finalReactions.append(f"<:impossible:809834670590132234> {impossible}")

    if reactionImage == "<:notdiscstudios:809834965385871371>":
      finalReactions.append(f"<:notdiscstudios:809834965385871371> {notdiscstudios}")

    if reactionImage == "<:general:809049370912882730>":
      finalReactions.append(f"<:general:809049370912882730> {general}")

  finalReactions = "\n".join(finalReactions) 

  database.discStudiosBot.suggestionData.delete_one({"_id":f"{args}"})
  database.discStudiosBot.suggestionData.insert_one({"_id":f"{args}", "data":suggestionsList})

  embed = discord.Embed(
    timestamp=(datetime.datetime.now()), 
    color=0xfff9b3,
    title="Stats:"
  )
  embed.add_field(
    name="Suggestion Stats",
    value=f"Total Suggestions: {suggestions}\nTotal Upvotes: 0\nTotal Downvotes: 0"
  )

  embed.add_field(
    name="Reactions Stats",
    value=finalReactions
  )


  await ctx.send(embed=embed)

@client.event
async def on_member_join(member):
  embed = discord.Embed(
    timestamp=datetime.datetime.now(), 
    description=f"**<:news:834457524886569010> {member} Joined.**"
  )
  embed.set_thumbnail(
    url=member.avatar_url
  )
  embed.set_footer(
    text=f"User ID: {member.id}"
  )
  time.sleep(1)
  if member.nick != None:
    embed.set_image(
      url=f"https://mc-heads.net/body/{member.nick}"
    )

  channel = client.get_channel(815913578666131486)
  await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
  embed = discord.Embed(
    timestamp=datetime.datetime.now(), 
    description=f"**<:news:834457524886569010> {member} Left.**"
  )
  embed.set_thumbnail(
    url=member.avatar_url
  )
  embed.set_footer(
    text=f"User ID: {member.id}"
  )
  if member.nick != None:
    embed.set_image(
      url=f"https://mc-heads.net/body/{member.nick}"
    )

  channel = client.get_channel(815913578666131486)
  await channel.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
  if payload.channel_id in [815894685679616000, 830867541601419264, 834466482464227378]:
    guild = client.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)

    user = client.get_user(payload.user_id)
    if payload.user_id == msg.author.id:
      await msg.remove_reaction(payload.emoji, user)

@client.event
async def on_ready():
  print(f"Logged in as: {client.user}")
  try:
    value = db["restart"]
    restartTime = db["restartTime"]

  except Exception as e:
    print(e)
    return

  del db["restart"]
  del db["restartTime"]
  restartTime = int(time.time()) - restartTime

  guild = client.get_guild(778299599697215528)
  channel = guild.get_channel(value[0])
  await channel.send(f"Restarted! ({restartTime}s)")

@client.event
async def on_message(ctx):
  if ctx.content.startswith(prefix) == True:
    command = ctx.content.split()
    command = command[0]
    command = command.replace(prefix, "")
    if command in commands:
      await permsCalc(ctx)
      command = commands[command]

      if permInt < command["perms"]:
        embed = discord.Embed(
          timestamp=(datetime.datetime.now()), 
          color=0xff0000
        )
        embed.add_field(
          name="No Permission!", 
          value=f"Sorry, you do not have permission to use this command. Commands that you are able to use are listed in {prefix}help."
        )
        perm = command["permName"]
        embed.set_footer(
          text=f"Required Permission: {perm}"
        )
        await ctx.channel.send(embed=embed)
        return

      await client.process_commands(ctx)
      return 

    else:
      embed = discord.Embed(
        timestamp=(datetime.datetime.now()), 
        color=0xff0000
      )
      embed.add_field(name="Error:", value=f"This command was not found, commands are listed in {prefix}help")
      await ctx.channel.send(embed=embed)
      return 

  if ctx.channel.id == 815894685679616000:
    if ctx.attachments != []:
      await ctx.add_reaction("<:upvote:809849047506616411>")
      await ctx.add_reaction("<:downvote:809849047321280544>")

    else:
      await asyncio.sleep(900)
      try:
        await ctx.delete()

      except:
        return
  
  if ctx.channel.id in [830867541601419264, 834466482464227378]:
    try:
      data = database.discStudiosBot.suggestionData.find_one({"_id":f"{ctx.author.id}"})
      database.discStudiosBot.suggestionData.delete_one({"_id":f"{ctx.author.id}"})
      data = data["data"]

    except:
      data = []

    
    data.append(ctx.id)
    if ctx.channel.id == 830867541601419264:
      await ctx.add_reaction("<:upvote:809849047506616411>")
      await ctx.add_reaction("<:downvote:809849047321280544>")

    database.discStudiosBot.suggestionData.insert_one({"_id":f"{ctx.author.id}", "data":data})

  if 835165724452192307 in ctx.raw_mentions:
    await ctx.channel.send(f"{ctx.author.mention}, My prefix is: {prefix}")

#Run Bot
client.run(token)
