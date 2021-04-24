from discord.ext import commands
import weblinks
import discord
import os
import time
import datetime
import psutil

#Config
prefix = "s!"
token = os.environ["DISCORD_TOKEN"]
client = commands.Bot(
  command_prefix=prefix, 
  intents=discord.Intents.all()
)
client.remove_command("help")

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
    "perms" : 4,
    "usage" : "[Expression]",
    "permName" : "Owner"
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
      permInt = 4
      perm = "OWNER"
      return()

    if role == 786292786088902676:
      permInt = 3
      perm = "ADMIN"
      return()

    if role == 789481171683115038:
      permInt = 2
      perm = "DEVELOPER"
      return()

    if role == 834432135350845471:
      permInt = 1
      perm = "SUGGESTION MODERATOR"
      return()

  permInt = 0
  perm = "USER"

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

  if 835165724452192307 in ctx.raw_mentions:
    await ctx.channel.send(f"{ctx.author.mention}, My prefix is: {prefix}")

@client.command(no_pm=True, name="calc")
async def calc_(ctx, *, args="0*0"):
  x = eval(args)
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
  embed.add_field(name="• Users", value={ctx.guild.member_count})
  embed.add_field(name="• Channels", value={len(ctx.guild.channels)}, inline=False)
  embed.add_field(name="• API Latency", value=f"{ping}ms", inline=False)
  embed.set_footer(text=f"Requested by {ctx.author}")
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
  embed.set_image(
    url=f"https://mc-heads.net/body/{member.name}"
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
  embed.set_image(
    url=f"https://mc-heads.net/body/{member.name}"
  )

  channel = client.get_channel(815913578666131486)
  await channel.send(embed=embed)

#Run Bot
client.run(token)
