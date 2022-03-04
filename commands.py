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
      points = db['ids'].get(player)
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


async def gamble(ctx, arg, arg2):
  player = str(ctx.message.author)
  if arg.lower() == "create":
    if arg != None and arg2 != None:
      if db['bets'].get(player) >= int(arg2):
        await create(ctx, arg, arg2, player)

  elif arg.lower() in db['bets']:
    if arg2 != None:
      pass
      


async def create(ctx, arg, arg2, player):
  length = len(db['bets'])
  while length in db['bets']:
    length += 1
  db['bets'].update({length: [arg, arg2, player]})