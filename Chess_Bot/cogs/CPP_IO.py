import os
import discord

from cogs.Utility import *


def prepare_input(person, move=''):
    file_in = f'data/input-{person}.txt'
    file_out = f'data/output-{person}.txt'
    if not file_in[5:] in os.listdir('data'):
        f = open(file_in, 'x')
        f.close()
    if not file_out[5:] in os.listdir('data'):
        f = open(file_out, 'x')
        f.close()

    f = open(file_in, 'w')
    f.write('play\n')
    if len(games[person]) == 0:
        f.write('no\n')
    else:
        f.write('yes2\n')
        game_str = ''
        for i in range(len(games[person])):
            if i % 2 == 0:
                game_str += str(i//2+1) + '. '
            game_str += str(games[person][i]) + ' '
        game_str += '*'
        f.write(game_str + '\n')
    f.write(f'{time_control[person]}\n')
    if colors[person] == 0:
        f.write('white\n')
    else:
        f.write('black\n')
    f.write(move + '\nquit\nquit\n')
    f.close()

    return file_in, file_out



async def output_move(ctx, person, client):
    user = await ctx.message.guild.fetch_member(person)
    
    f = open(f'data/output-{person}.txt')
    out = f.readlines()
    f.close()
    
    wb = ['Black', 'White']
    embed = discord.Embed(title= f'{user}\'s game', description=f'{wb[colors[user.id]]} to move', color=0x5ef29c)
    embed.set_footer(text = f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)
            
    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('COMPUTER PLAYED'):
            embed.add_field(name='Computer moved', value=out[i][16:])
            break
        
    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('-----'):
            get_image(person, i - 1)
                    
            temp_channel = client.get_channel(806967405414187019)
            image_msg = await temp_channel.send(file = discord.File(f'data/image-{person}.png'))
            
            image_url = image_msg.attachments[0].url
            
            embed.set_image(url = image_url)
            
            await ctx.message.reply(embed=embed)
            break
        
    for i in range(len(out) - 1, 0, -1):
        if out[i].startswith('GAME: '):
            game_str = out[i][6:-1].split(' ')
            games[person].clear()
            for i in game_str:
                if i == '' or i == '\n':
                    continue
                games[person].append(int(i))
            push_games()
            return


async def log(person, client):
    f = open(f'data/output-{person}.txt')
    out = f.readlines()
    f.close()
    log_channel = client.get_channel(798277701210341459)
    msg = f'<{person}>\n```\n'
    for i in range(len(out)):
        msg += out[i] + '\n'
        if i % 10 == 0:
            msg += '```'
            await log_channel.send(msg)
            msg = '```'
    msg += '```'
    await log_channel.send(msg)