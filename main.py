import discord
from discord.ext import commands, tasks
import os
from replit import db
import commands as c

TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['Channel ID'])


client = c.client


@tasks.loop(minutes = 1)
async def awardpoints():
  channel = client.get_channel(CHANNEL_ID)
  members = channel.members
  for i in members:
    if not i.bot:
      i = str(i)
      if i in db['ids']:
        points = db['ids'].get(i)
        points += 1
        db['ids'].update({i: points})
    
      else:
        db['ids'].update({i: 1})


@client.command()
async def points(ctx, arg=None):
  await c.points(ctx, arg)


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Vibes"))
  print('You have logged in as {0.user}'.format(client))
  awardpoints.start()


try:
  client.run(TOKEN)
except:
  os.system("kill 1")