import discord
from discord.ext import commands
from keep_alive import keep_alive
from mcstatus import MinecraftServer
import os
from discord.ext.commands import has_permissions, MissingPermissions


bot = commands.Bot(command_prefix='!')

status = "Online"

@bot.event
async def on_ready():
  print('Ready!')
  (print('I am running on ' + bot.user.name))
  await bot.change_presence(activity=discord.Game(name="hello i am watching you"))

@bot.command(description="Shows bot latency")
async def ping(ctx):
  await ctx.send(f"Pong! {format(round(bot.latency, 1))}")
    

@bot.command(description="Kicks a user")
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member , *, reason = None):
  if ctx.message.author.guild_permissions.kick_members:
    if reason == None:
      reason=f'Kicked by {ctx.author}'
    embed = discord.Embed(title=f"Kicked user {member}", description=f"Reason: {reason}", color = 0xFFFFF)
    await member.kick(reason=reason)
    await ctx.send(embed=embed)
  else:
    await ctx.channel.send('Insufficent Permissions!')

@bot.command(description="Banishes a user")
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member , *, reason = None):
    if reason == None:
      reason=f'Banned by {ctx.author}'
    embed = discord.Embed(title=f"Banned user {member}", description=f"Reason: {reason}", color = 0xFFFFF)
    await member.ban(reason=reason)
    await ctx.send(embed=embed)
  
@bot.command(description="Mutes a user")
@has_permissions(manage_messages=True)
async def mute(self, ctx, member : discord.Member, *, reason = None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
      mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages = False)
    await member.add_roles(mutedRole)

    embed = discord.Embed(title=f"\n\nSucess!",description=f" Muted {member.mention} for {reason}.", color=0xFFFFF)

    author = ctx.message.author
    pfp = author.avatar_url

    embed.set_author(name=author, icon_url=pfp)
    await ctx.send(embed=embed)

@bot.command(description="Displays some info about a user")

async def profile(ctx, member : discord.Member = None):
  if member == None:
    member = ctx.author
  embed = discord.Embed(title=f"Profile of user {member}", description="", color=0xFFFFF)
  embed.add_field(name="User ID", value=member.id, inline=True)
  embed.add_field(name="Date Joined", value=member.joined_at, inline=True)
  await ctx.send(embed=embed)

@bot.command(description="Mass delete messages!")
@has_permissions(manage_messages=True)
async def purge(ctx, amount = 1):
    if amount > 100:
      await ctx.message.delete()
      await ctx.channel.send('You cannot purge more than 100 messages!', delete_after=3)
      return
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(description=f"Purged {amount} message(s)", color=0xFFFFF)
    await ctx.send(embed=embed, delete_after=3)

@bot.command(description="Say Hi!")
async def hello(ctx):
  await ctx.message.delete()
  await ctx.channel.send("Hello! I'm happy to be here. :)")

@bot.command(description='Displays info about the minecraft server!')
async def mcinfo(ctx):
  embed = discord.Embed(title='AzaleaMC Server Info', color=0xFFFFF)
  embed.add_field(name="IP", value="play.azaleamc.org", inline=True)
  embed.add_field(name="Status", value=status, inline=True)
  await ctx.send(embed=embed)

@bot.command(description="Warns the user mentioned")
@has_permissions(manage_messages=True)
async def warn(ctx, member : discord.Member , *, reason=None):
    if reason == None:
      reason=f'Warned by {ctx.author}'
    await member.send(f"You have been warned for: {reason}")
    embed = discord.Embed(title=f"Warned {member} for reason: {reason}", color=0xFFFFF)
    await ctx.send(embed=embed)

@bot.command(description="Shows MC Server Status")
async def status(ctx):
  server = MinecraftServer.lookup("184.95.34.74:25636")

  status = server.status()
  embed = discord.Embed(title="Server Status", color=0xFFFFF)
  embed.add_field(name="Players Online", value=f"{status.players.online}", inline=False)
  embed.add_field(name="Latency (if 0 down for maintenance)", value = round(status.latency, 1),inline=False)

  await ctx.send(embed=embed)


@bot.command(description="Sets the status")
@has_permissions(ban_members=True)
async def setstatus(ctx, str):
  status = str
  ctx.send("Sucessfully set status!")
keep_alive()
token = os.environ['TOKEN']
bot.run(token)