from disnake.ext import commands, tasks

import disnake
from cogs.core import game
from json import loads


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update.start()

    @commands.slash_command()
    async def base(self, inter):
        player = game.User(inter.author.id)
        emb = player.buildings.display()
        emb.add_field('Ресурсы', str(player.resources), inline=False)
        await inter.response.send_message(embed=emb)

    @commands.slash_command()
    async def buildings_shop(self, inter):
        with open('cogs/core/buildings.json', encoding='utf8') as f:
            buildings = loads(f.read())
        emb = disnake.Embed(title='Покупка построек')
        for i in buildings:
            emb.add_field(name=i, value='\n'.join(buildings[i]), inline=False)
        await inter.response.send_message(embed=emb)

    @commands.slash_command()
    async def building_info(self, inter, building):
        with open('cogs/core/buildings.json', encoding='utf8') as f:
            buildings = loads(f.read())
            emb = disnake.Embed(title=building)
            if building in buildings['Ядра']:
                emb.add_field('Стоимость', buildings['Ядра'][building]['cost'], inline=False)
                emb.add_field('Описание', buildings['Ядра'][building]['desc'], inline=False)
                emb.add_field('Вместимость', buildings['Ядра'][building]['vol'], inline=False)
            elif building in buildings['Буры']:
                emb.add_field('Стоимость', buildings['Буры'][building]['cost'], inline=False)
                emb.add_field('Описание', buildings['Буры'][building]['desc'], inline=False)
                emb.add_field('Добыча', str(eval(f"game.{buildings['Буры'][building]['class']}().mining")),
                              inline=False)
            elif building in buildings['Турели']:
                emb.add_field('Стоимость', buildings['Турели'][building]['cost'], inline=False)
                emb.add_field('Описание', buildings['Турели'][building]['desc'], inline=False)
            elif building in buildings['Стены']:
                emb.add_field('Стоимость', buildings['Стены'][building]['cost'], inline=False)
                emb.add_field('Описание', buildings['Стены'][building]['desc'], inline=False)
            else:
                emb = disnake.Embed(title='Ошибка',
                                    description='Такой постройки не существует. Проверьте правильность написания')
        await inter.response.send_message(embed=emb)

    @commands.slash_command()
    async def buy(self, inter, building, count: int = 1):
        with open('cogs/core/buildings.json', encoding='utf8') as f:
            buildings = loads(f.read())
            for i in buildings:
                try:
                    new = buildings[i][building]['class']
                    break
                except KeyError:
                    pass
            try:
                new = eval(f'game.{new}()')
                user = game.User(inter.author.id)
                if count > 0:
                    if user.resources >= new.cost * count:
                        user.resources -= new.cost * count
                        for i in range(count):
                            user.buildings.append(new)
                        await inter.response.send_message('Покупка успешна')
                    else:
                        await inter.response.send_message('У вас недостаточно ресурсов')
                else:
                    while user.resources >= new.cost:
                        user.resources -= new.cost
                        user.buildings.append(new)
                    await inter.response.send_message('Покупка успешна')
            except UnboundLocalError:
                await inter.response.send_message('Такой постройки не существует. Проверьте правильность написания')

    @commands.slash_command()
    async def attack(self, inter, player: disnake.Member):
        attacker = game.User(inter.author.id)
        defender = game.User(player.id)
        await inter.response.send_message(f'Вы напали на игрока {player.nick}. Ожидание результата')
        game.fight(attacker, defender)

    @tasks.loop(hours=1)
    async def update(self):
        with open('cogs/core/players.json') as f:
            players = loads(f.read())
            for i in players:
                player = game.User(i)
                player.update()


def setup(bot):
    bot.add_cog(Game(bot))
