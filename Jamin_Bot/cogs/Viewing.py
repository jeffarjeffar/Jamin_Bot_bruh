import discord
from discord.ext import commands
from PIL import Image

from cogs.Utility import *

def get_image(person, end):
    game_file = f'data/output-{person}.txt'
    F = open(game_file)
    game = F.readlines()
    F.close()

    result = Image.open('images/blank_board.png')
    result = result.resize((400, 400))

    for i in range(end - 14, end + 2, 2):
        print(i, ": ", game[i])
        for j in range(1, 25, 3):
            square = 'images/'
            if game[i][j:j+2] == '  ':
                square += 'blank'
            else:
                square += game[i][j:j+2]
            x = (i + 14 - end)//2
            y = (j - 1)//3
            if (x + y) % 2:
                square += '-light.png'
            else:
                square += '-dark.png'
            
            square_img = Image.open(square)
            square_img = square_img.resize((50, 50), Image.ANTIALIAS)

            x *= 50
            y *= 50
            
            if colors[person] == 1:
                result.paste(square_img, (y, x, y + 50, x + 50))
            else:
                result.paste(square_img, (350 - y, 350 - x, 400 - y, 400 - x))
    
    result.save(f'data/image-{person}.png')

class Viewing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def view(self, ctx, *user):
        '''
        Views your current game
        '''

        person = -1
        if len(user) == 1:
            person = int(user[0][3:-1])
        else:
            person = ctx.author.id

        if not person in games.keys():
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return

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
        f.write('60\n')
        if colors[person] == 0:
            f.write('white\n')
        else:
            f.write('black\n')
        f.write('quit\nquit\n')
        f.close()
        stdout, stderr, status = await run(f'.\\a < {file_in} > {file_out}')
        #await ctx.send(f'stdout: {stdout}\nstderr: {stderr}\n{status}')
        await output_move(ctx, person)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.default)
    async def fen(self, ctx, *user):
        '''
        Sends current game in FEN format
        '''

        person = -1
        if len(user) == 1:
            person = int(user[0][3:-1])
        else:
            person = ctx.author.id

        if not person in games.keys():
            if len(user) == 1:
                await ctx.send(f'{user[0]} does not have a game in progress')
            else:
                await ctx.send('You do not have a game in progress')
            return

        person = ctx.author.id
        file_in = f'data/input-{person}.txt'
        file_out = f'data/output-{person}.txt'
        if not file_in[5:] in os.listdir('data'):
            f = open(file_in, 'x')
            f.close()
        if not file_out[5:] in os.listdir('data'):
            f = open(file_out, 'x')
            f.close()

        f = open(file_in, 'w')
        f.write('fen\n')
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
        f.write('quit\n')
        f.close()
        await run(f'.\\a < {file_in} > {file_out}')
        f = open(file_out)
        out = f.readlines()
        f.close()

        await ctx.send(out[-2])