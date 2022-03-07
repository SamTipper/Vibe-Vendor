import discord
from discord.ext import commands
from replit import db


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

db['bets'] = {}


async def points(ctx, arg):
  if arg == None:
    player = str(ctx.message.author)
    if player in db['ids']:
      points = await get_points(player)
      await ctx.send(f"You have {points} Vibe Points!")
      
  elif arg.lower() == "all":
    embed = discord.Embed(
      title = '**Vibe Points**',
      description = '--------',
      colour = discord.Colour.green()
    )
    
    for name, points in db['ids'].items():
      embed.add_field(name=f'{name}', value=f"{points}", inline=False)
      
    await ctx.send(embed=embed)


async def bet(ctx, arg, arg2):
  player = str(ctx.message.author)
  if arg.lower() == "create":
    if arg != None and arg2 != None:
      if db['bets'].get(player) >= int(arg2):
        await create(ctx, arg, arg2, player)

  elif arg.lower() in db['bets']:
    if arg2 != None and arg2.isdigit():
      points = await get_points(player)
      if points >= arg2:
        points -= arg2
        db['bets'].update({player: points})
        await ctx.send(f"You have bet on {arg} with {arg2} Vibe Points!")

  elif arg == None and arg2 == None:
    pass



async def create(ctx, arg, arg2, player):
  points = await get_points(player)
  if int(points) >= int(arg2):
    length = len(db['bets'])
    while length in db['bets']:
      length += 1
    db['bets'].update({length: [arg, arg2, player]})
    await ctx.send(f"Bet created, its ID is: {length}")


async def get_points(player):
  points = db['ids'].get(player)
  return points
  
