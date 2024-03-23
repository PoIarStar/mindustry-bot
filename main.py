from disnake.ext import commands
from os import listdir
from configparser import ConfigParser

import disnake


config = ConfigParser()
config.read('config.ini')


bot = commands.Bot(command_prefix=disnake.ext.commands.when_mentioned,
                   test_guilds=[1135140239808143370],
                   command_sync_flags=commands.CommandSyncFlags(),
                   intents=disnake.Intents.all())

for name in listdir('cogs'):
    if name.endswith('.py'):
        bot.load_extension(f'cogs.{name[:-3]}')

bot.run(config['bot']['token'])
