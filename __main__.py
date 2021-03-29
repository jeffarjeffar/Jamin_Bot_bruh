import discord
import os
from discord.ext import commands

from Chess_Bot.cogs.Misc import *
from Chess_Bot.cogs.Engine import *
from Chess_Bot.cogs.Viewing import *
from Chess_Bot.cogs.Mooderation import *
from Chess_Bot.cogs.Development import *
from Chess_Bot.cogs.Help import *
from Chess_Bot.cogs.Timer import *
from Chess_Bot.cogs.Topgg import *

import Chess_Bot.cogs.Data as data
import Chess_Bot.cogs.Utility as util

import logging
import traceback

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='debug.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

async def get_prefix(bot, message):
	if message.guild == None:
		return ['$', f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']
	return [data.data_manager.get_prefix(message.guild.id), f'<@{bot.user.id}> ', f'<@!{bot.user.id}> ']

bot = commands.Bot(command_prefix=get_prefix, help_command=None)

bot.add_cog(Engine(bot))
bot.add_cog(Misc(bot))
bot.add_cog(Viewing(bot))
bot.add_cog(Mooderation(bot))
bot.add_cog(Development(bot))
bot.add_cog(Help(bot))
bot.add_cog(Timer(bot))
bot.add_cog(Topgg(bot))

'''
@bot.event
async def on_error(error, *args, **kwargs):
	print('error found')
	print(error, type(error))
	error_channel = bot.get_channel(799761964401819679)
	await error_channel.send(f'Error: {str(error)}\nArgs: {args}\nkwargs: {kwargs}')
'''
@bot.event
async def on_command_error(ctx, exc):
	if type(exc) == commands.errors.BotMissingPermissions:
		await ctx.send(f'Chess Bot is missing permissions.\nThe missing permissions are: {" ".join(exc.missing_perms)}')
	elif type(exc) == commands.errors.MissingRequiredArgument:
		await ctx.send(f'Missing required argument.\nPlease enter a value for: {exc.param}')
	elif type(exc) == commands.errors.ArgumentParsingError:
		await ctx.send(f'There was an error parsing your argument')
	elif type(exc) == commands.errors.TooManyArguments:
		await ctx.send(f'Bruh what why are there so many arguments?')
	elif type(exc) == commands.errors.CommandOnCooldown:
		await ctx.send(f'You are on cooldown. Try again in {util.pretty_time(exc.retry_after)}')
	elif type(exc) == commands.errors.CommandNotFound:
		await ctx.send('Command not found.')
	else:
		print('Command error found')
		
		# get data from exception
		etype = type(exc)
		trace = exc.__traceback__

		# 'traceback' is the stdlib module, `import traceback`.
		lines = traceback.format_exception(etype, exc, trace)

		# format_exception returns a list with line breaks embedded in the lines, so let's just stitch the elements together
		traceback_text = ''.join(lines)
		
		print(traceback_text)
		
		await ctx.send('Uh oh. Something went wrong.')
		
		error_channel = bot.get_channel(799761964401819679)
		await error_channel.send(f'Command Error:\n```\n{traceback_text}\n```')

token = os.environ.get('BOT_TOKEN')

# token = input('Token? ')

bot.run(token)
