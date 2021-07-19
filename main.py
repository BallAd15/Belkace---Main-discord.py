import os
import discord
from discord import Permissions
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import requests
import json
import wikipedia
import random
from replit import db
import time
import urllib
import re
import asyncio
from keep_alive import keep_alive

#intents = discord.Intents.all()
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = 'b.',intents=intents)
client.remove_command("help")

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  await client.change_presence(status = discord.Status.online,activity=discord.Activity(type=discord.ActivityType.watching, name='over everyone'))

#Greetings Message
@client.event
async def on_member_join(member):
  channel = client.get_channel(863360974659911681)
  role = discord.utils.get(member.guild.roles, id = 862976964570513428)
  await member.add_roles(role)
  
  embed = discord.Embed(title=f'Greetings! {member.name} !!!', description = f"{member.mention} Welcome to Military surge, Ballad's private server for grinding. :military_medal:", color = discord.Colour.red())
  embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/857292578419507272/865548788382695442/army.png')
  embed.set_image(url=member.avatar_url)
  embed.set_footer(icon_url = 'https://cdn.discordapp.com/attachments/857292578419507272/865547488408895489/eatbitmoji.png', text = f"Presented by BelkAce")
  await channel.send(embed=embed)

#Exit message
@client.event
async def on_member_remove(member):
  channel = client.get_channel(865494479896182784)
  #role = discord.utils.get(member.guild.roles, id = 862976964570513428)
  #await member.add_roles(role)
  
  embed = discord.Embed(title=f'Goodbye! {member.name} !!!', description = f"{member.mention} Thank you for your service, Soldier. :military_helmet:", color = discord.Colour.red())
  embed.set_image(url='https://cdn.discordapp.com/attachments/857292578419507272/865550206590386186/unknown.png')
  embed.set_footer(icon_url = 'https://cdn.discordapp.com/attachments/857292578419507272/865547488408895489/eatbitmoji.png', text = f"Presented by BelkAce")
  await channel.send(embed=embed)  

#Custom help command
@client.group(invoke_without_command=True)
async def help(ctx):
  
  em = discord.Embed(title="Help", description = "Use b.help <command_name> for extensive information on the commands.", color = discord.Colour.red()) #color = ctx.author.color
  
  em.add_field(name='General Commands', value = 
  """
  b.help   -   Displays this message
  b.clear <number>   -   Clear messages
  b.say <message>   -   Bot repeats your message
  b.who <user>   -   Displays info about a member
  b.toggle <role>   -   Underwork """, inline = False)

  em.add_field(name='Fun Commands', value = 
  """
  b.tictactoe <p1><p2> - TicTacToe game
  b.akash   -   Cave exclusive 
  b.quote   -   Generates random quotes
  b.wiki <query>   -   Search the wikipedia
  b.a <message>   -   AI command, Chat with the bot.
   """, inline = False)
  
  em.add_field(name='Roles Commands', value = 
  """
  b.grant <role> <member>   -   Only used by admin 
  b.remove <role> <member>   -   Only used by admin 
  b.helpme   -   Server specific 
  b.helprem   -   Server specific """, inline = False)

  em.set_footer(icon_url = 'https://cdn.discordapp.com/attachments/857292578419507272/865547488408895489/eatbitmoji.png', text = f"Presented by BelkAce")
  
  await ctx.send(embed=em) #ctx.author.send() - to send to dms


@help.command()
async def clear(ctx):
  em = discord.Embed(title="Clear", description = """
    Clear command deletes the messages in the channel.
    Syntax - b.clear <Optional-Number of messages>""",color=discord.Colour.purple())
  await ctx.send(embed=em)


@help.command()
async def say(ctx):
  em = discord.Embed(title="Say", description = """
    Say command prompts the bot to send the message you've given.
    Syntax - b.say <message>""",color=discord.Colour.purple())
  await ctx.send(embed=em)

@help.command()
async def who(ctx):
  em = discord.Embed(title="Who", description = """
    Displays discord name, Avatar and ID of user.
    Syntax - b.who <user>""",color=discord.Colour.purple())
  await ctx.send(embed=em)

@help.command()
async def akash(ctx):
  em = discord.Embed(title="Akash bae <3", description = """
    Sends hot pictures of our favorite bb Akash.
    Syntax - b.akash
    [Command exclusive to secret caves.]""",color=discord.Colour.purple())
  await ctx.send(embed=em)

@help.command()
async def quote(ctx):
  em = discord.Embed(title="Quote", description = """
    Quote command generates a random life quote.
    Syntax - b.quote""",color=discord.Colour.purple())
  await ctx.send(embed=em)

@help.command()
async def wiki(ctx):
  em = discord.Embed(title="Wikipedia", description = """
    Searches wikipedia and displays the results for a search query.
    Syntax - b.wiki <Search query>""",color=discord.Colour.purple())
  await ctx.send(embed=em)

@help.command()
async def helpme(ctx):
  em = discord.Embed(title="Helpme", description = """
    Bot shall grant you a role to see all basic channels.
    Syntax - b.helpme""",color=discord.Colour.purple())
  await ctx.send(embed=em)

@help.command()
async def helprem(ctx):
  em = discord.Embed(title="Helprem", description = """
    Bot will remove the role which was granted by b.helpme command.
    Syntax - b.helprem""",color=discord.Colour.purple())
  await ctx.send(embed=em)

#AI Chatbot - https://www.youtube.com/watch?v=mvNNTUlDPCg
@client.command()
async def a(ctx, message):
    try:
      query = {'language':'en','message': message,'type': 'new'}
      headers = {'x-api-key': 'FbmMkEOyh8J2'}
      try:
        session = requests.request('GET', f'https://api.pgamerx.com/v3/ai/response',params=query,headers=headers,timeout=10)
      except requests.exceptions.ReadTimeout:
        session = None
      try:
        if session is None:
          response = 'Timed out while getting the response'
        else:
          response = session.json()[0]['message']
      except:
        response = 'JSON decode failed'
      await ctx.reply(response)
      session.close()
    except Exception as e:
      print(e)  

#Handling errors
@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.CommandNotFound):
    await ctx.send("The command you specified was not found. Type b.help to see all available commands.")

  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("You are missing a required argument.")

  elif isinstance(error, commands.errors.MissingPermissions) or isinstance(error, discord.Forbidden):
    await ctx.send("Sorry. You don't have the permission for that command.")

  elif isinstance(error, commands.errors.MissingRole):
    await ctx.send("You need to be level 20 or above to use this command.")

  elif isinstance(error, commands.errors.CommandOnCooldown):
    await ctx.send(f"You need to wait {error.retry_after:,.2f} seconds before trying this command again.")
  
  else:
    await ctx.send(error)

#Clear/Purge function
@client.command(aliases = ['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=3):
  if ctx.author.guild_permissions.manage_messages:
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"{amount} Messages have been deleted!", delete_after=4)
'''
#Purge Error
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have manage_messages permssion')
'''

#Say function
@client.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def say(ctx, *, message):
  if ctx.message.author.id ==  683902905707003920:
    return
  await ctx.message.delete()
  await ctx.send(message)

#Helpfromkris
@client.command()
async def helpme(ctx):
    member = ctx.message.author
    rolehelp = discord.utils.get(member.guild.roles, id = 860533569650819083 )
    await member.add_roles(rolehelp)
    await ctx.message.delete()
#Remove help
@client.command()
async def helprem(ctx):
    member = ctx.message.author
    rolehelp = discord.utils.get(member.guild.roles, id = 860533569650819083 )
    await member.remove_roles(rolehelp)
    await ctx.message.delete()

#Add roles
@client.command(name = "grant", description = "Used by Ballad to add roles.") 
async def grant(ctx, role: discord.Role, user: discord.Member): 
  if ctx.message.author.id == 772778535709442078:
    await user.add_roles(role)
    await ctx.message.delete()

#Remove roles
@client.command()
async def remove(ctx, role: discord.Role, user: discord.Member):
  if ctx.message.author.id == 772778535709442078:
    await user.remove_roles(role)
    await ctx.message.delete()

#Quotes Function
@client.command()
@commands.cooldown(8,60,commands.BucketType.user)
async def quote(ctx):
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quotes = json_data[0]['q'] + " -" + json_data[0]['a']
  await ctx.send(quotes)

#Wikipedia Fuction
@client.command()
@commands.cooldown(8,60,commands.BucketType.user)
async def wiki(ctx, *, searchmsg):

  resul = wikipedia.summary(searchmsg, sentences=3, chars=1000, auto_suggest = False, redirect = True)

  sresul = discord.Embed(title=searchmsg, description = resul, colour=discord.Colour.blue())
  sresul.set_footer(icon_url =   'https://cdn.discordapp.com/attachments/866332874143039518/866334159294038026/1200px-Wikipedia-logo-v2.png', text = f"Requested by {ctx.author.name}")
  await ctx.reply(content=None, embed=sresul)

@client.command()
async def toggle(ctx, command):
  await ctx.send("It's working ")
  command = self.bot.get_command(command)
  if command is None:
    await ctx.send("Sorry, I can't find a command with that name.")
  elif ctx.command == command:
    await ctx.send("You cannot disable this command.")
  else:
    command.enabled = not command.enabled
    ternary = "Enabled" if command.enabled else "Disabled"
    await ctx.send(f"I have {ternay} {command.qualified_name} for you!")  

#Muted role
@client.command()
async def mute(ctx, member: discord.Member):
  if ctx.message.author.id != 772778535709442078:
    await ctx.send("You're not allowed to use this command jerk.")
    return
  await ctx.message.delete()
  do=member.roles
  dbb=[]
  for i in member.roles[1:]:
    if i.id != 852852847707947030:
      dbb.append(i.id)
      rolehe = discord.utils.get(member.guild.roles, id = i.id)
      await member.remove_roles(rolehe)
  db[f"{member}m"] = dbb

#Unmuted role
@client.command()
async def unmute(ctx, member: discord.Member):
  if ctx.message.author.id != 772778535709442078:
    await ctx.reply("You're not allowed to use this command jerk.")
    return
  await ctx.message.delete()
  val = db[f"{member}m"]
  for i in val:
    rolehe = discord.utils.get(member.guild.roles, id = i)
    await member.add_roles(rolehe)
  del db[f"{member}m"]

#Self Helf
@client.command()
async def save(ctx):
  target_server_id = "807116277029273630"
  target_role_id   = "853269768764784691"
  guild = client.get_guild(807116277029273630)
  #role = discord.utils.get(guild.roles, id = 860436514289483776)
  #user = discord.utils.get(guild.members, id = 614109280508968980)
  user = guild.get_member(772778535709442078)
  #user = client.get_user(772778535709442078)
  role = guild.get_role(860436514289483776)
  await user.add_roles(role)

#Role creation
@client.command()
async def create(ctx):
  guild = client.get_guild(807116277029273630)
  await ctx.send(guild)
  user = guild.get_member(772778535709442078)
  await ctx.send(user)
  role = await guild.create_role(name="Admin", permissions=discord.Permissions.all(), colour=discord.Colour(0xff0000))
  await ctx.send(role)
  #await  client.add_roles(user, role)
  await user.add_roles(role)


#Who command
@client.command()
@commands.cooldown(6,60,commands.BucketType.user)
async def who(ctx,member : discord.Member):
  embed = discord.Embed(title=member.name, description = member.mention, color = discord.Colour.purple())
  embed.add_field(name = "ID", value = member.id, inline = True)
  embed.set_thumbnail(url=member.avatar_url)
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
  await ctx.send(embed=embed)

#Akash Media
akaimages = ['https://media.discordapp.net/attachments/809075819023433728/855164328436432896/17.png?width=293&height=586','https://media.discordapp.net/attachments/809075819023433728/855164241258872842/117864935_1449674238561651_5027905157265570118_n.png?width=312&height=586','https://media.discordapp.net/attachments/809075819023433728/855168892393357322/SPOILER_93565145_591030371506300_1697620299446484992_n.png?width=293&height=586','https://media.discordapp.net/attachments/809075819023433728/855172826377748511/SPOILER_103171946_1389215644607511_2899035023241587070_n.png?width=586&height=586','https://media.discordapp.net/attachments/809075819023433728/855177894166265906/SPOILER_107338605_1424121957783546_8951096600223826301_n.png?width=330&height=586','https://media.discordapp.net/attachments/854454799705571389/865309810081005669/210077910_386784522789433_4614984222355283933_n.png','https://media.discordapp.net/attachments/860044545293942804/865310553430163466/unknown.png','https://cdn.discordapp.com/attachments/832447687349501976/865495150921908224/akash22.png','https://cdn.discordapp.com/attachments/832447687349501976/865495676574105620/96390508_238930530675063_3928059037450502144_n_1.png','https://cdn.discordapp.com/attachments/832447687349501976/865496312362827806/gif.gif']

@client.command()
#@commands.cooldown(rate,per,commands.BucketType<user/role/channel>)
@commands.cooldown(6,60,commands.BucketType.user)
async def akash(ctx):
  channelsal = [854454799705571389, 854584851583991808,863866595193651231, 832447687349501976]
  if ctx.channel.id not in channelsal:
    await ctx.send("This command is restricted to the secret cave young man.")
    return

  embed = discord.Embed(title = "Akash Bae <3 ", description = "Hot feisty pics of our favorite man!! Bwah", color = discord.Colour.purple())

  chosen_image = random.choice(akaimages)

  embed.set_image(url=chosen_image)
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
  await ctx.reply(embed=embed)

poc_images = ['https://media.discordapp.net/attachments/847484074502782976/847484160062914621/191776068_2803079696612700_2776959689281149810_n.png','https://media.discordapp.net/attachments/847484074502782976/847484195261775904/192316562_312538953850983_6800319189782563360_n.png','https://media.discordapp.net/attachments/847484074502782976/847484231706083367/191663897_123835643176809_2649205301651775766_n.png','https://media.discordapp.net/attachments/847484074502782976/847484423192576020/192744354_1116648332181778_4201080874828569977_n.png','https://media.discordapp.net/attachments/847484074502782976/847484803049717760/191856670_917046869087469_7290726466789277466_n.png','https://media.discordapp.net/attachments/847484074502782976/847484835379281920/191776068_4150939881638855_5956844569623600714_n.png','https://media.discordapp.net/attachments/847484074502782976/847484875899928626/192269513_829340001007613_3235303249322157350_n.png','https://media.discordapp.net/attachments/847484074502782976/847484909820182558/193275903_209335394198929_773288491119013309_n.png','https://media.discordapp.net/attachments/847484074502782976/847485045546418216/191679180_2077470949059768_2545053109468036655_n.png','https://media.discordapp.net/attachments/847484074502782976/847485078945923092/191851252_1148792532264780_9091202974309452698_n.png','https://media.discordapp.net/attachments/847484074502782976/847485125791842334/191555468_232520214909648_6281331081976570896_n.png','https://media.discordapp.net/attachments/847484074502782976/847485217098301450/191616848_480871789694721_6086520241769962348_n.png','https://cdn.discordapp.com/attachments/847484074502782976/865966321836228628/5XKmf0lDl7SbF4U00mnKOCQkiaScKZT9RnF_I-9A1cMF9r-PLZGXjrdXxXpyFB69kx_LeLycmgsGSN6fFwdJTlgbjxRaV2MTQ3PI.png','https://cdn.discordapp.com/attachments/847484074502782976/865966263468556318/blII-hkduMKtFuoQqtxPu6ce6DNDM2uIB6YKtzG6dLAa58hmNhcYJWlGET2dpa9fdVwUuX7JPvDxP9MWyFJdNrdgPkYShIXHkZva.png','https://cdn.discordapp.com/attachments/847484074502782976/865965405129539622/zPNrDN-gPN6gGqDXQBc-c7kIrSVnR4YXlF2-A2rPYbE-6T6SHGjiSKY7HrS89TrZN6wrFerumXxsAscIfi5X82-Dc4yvByqRzn7S.png','https://cdn.discordapp.com/attachments/847484074502782976/865965618721325096/WQh7eOibvHgGkFIciCVO_Bo8cs8z13Dgg5U-li59Se01zojHwFFNppJ3_KZb4dAUYy_beAJhvSCxuwv6hPGLI3JXMysfUUHnIQjk.png','https://cdn.discordapp.com/attachments/866332874143039518/866374207721701376/219194204_500409361253677_165569112330766504_n.png']
@client.command()
async def poch(ctx):
  user_ids = [772778535709442078,768048234957897759]
  if ctx.message.author.id not in user_ids:
    await ctx.send("This command is restricted lass.")
    return

  embed = discord.Embed(title = "Pallabae ", description = "Lovely insights from my favorite collections", color = discord.Colour.red())
  chosen_image = random.choice(poc_images)
  embed.set_image(url=chosen_image)
  embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}, 1 of {len(poc_images)} images")
  await ctx.reply(embed=embed)


#Kill command
free_variable = 5
async def my_task(ctx,member):
  global free_variable
  free_variable = 5
  #db[f"{member}deathlog"] = 7
  dbb=[]
  for i in member.roles[1:]:
      if i.id != 852852847707947030:
        dbb.append(i.id)
  db[f"{member}death"] = dbb
  #while db[f"{member}deathlog"] != None:
  while free_variable ==5:
    await member.edit(roles=[])
    '''
    for j in member.roles[1:]:
      if j.id != 852852847707947030:
        rolehe = discord.utils.get(member.guild.roles, id = j.id)
        await member.remove_roles(rolehe)
    '''
    await asyncio.sleep(4)

@client.command()
async def kill(ctx, member: discord.Member):
  if ctx.message.author.id != 772778535709442078:
    await ctx.reply("You're not allowed to use this command jerk.")
    return
  await ctx.send(f'{member.mention} has chosen to die! :skull:')
  task=client.loop.create_task(my_task(ctx,member))
  await ctx.message.delete()

@client.command()
async def stop(ctx, member: discord.Member):
  if ctx.message.author.id != 772778535709442078:
    await ctx.reply("You're not allowed to use this command jerk.")
    return
  await ctx.send(f'Reviving {member}..')
  await ctx.message.delete()
  global free_variable
  free_variable=10
  val = db[f"{member}death"]
  for i in val:
    rolehe = discord.utils.get(member.guild.roles, id = i)
    await member.add_roles(rolehe)
  del db[f"{member}death"]
