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
      await ctx.send(f"You have {points} VBC!")
      
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
  if arg == None:
    embed = discord.Embed(
      title = '**Bet Board**',
      description = '--------',
      colour = discord.Colour.green()
    )
    
    for id, info in db['bets'].items():
      name = info[0]
      wager = info[1]
      initiator = info[2]
      embed.add_field(name=f'{id}', value=f"{name} \n {wager} VBC \n Bet by: {initiator}", inline=False)
    await ctx.send(embed=embed)

  elif arg.lower() in db['bets']:
    bet = db['bets'].get(arg)
    if arg2 != None and arg2.isdigit():
      points = await get_points(player)
      arg2 = int(arg2)
      if points >= arg2:
        points -= arg2
        bet[1] += arg2
        db['ids'].update({player: points})
        db['bets'].update({player: points})
        await ctx.send(f"You have bet on {arg} with {arg2} VBC!")
  
  elif arg.lower() != None:
    if arg2 != None:
      points = db['ids'].get(player)
      if int(points) >= int(arg2):
        await create(ctx, arg, arg2, player)


async def create(ctx, arg, arg2, player):
  points = await get_points(player)
  if int(points) >= int(arg2):
    length = len(db['bets'])
    while length in db['bets']:
      length += 1
    points -= int(arg2)
    db['ids'].update({player: points})
    db['bets'].update({length: [arg, arg2, player]})
    await ctx.send(f"Bet created, its ID is: {length}")


async def get_points(player):
  points = db['ids'].get(player)
  return points
  