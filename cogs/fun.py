from disnake.ext import commands

import disnake
import random
from cogs.core import game


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    '''@commands.cooldown(5, 1800)
    @commands.slash_command()
    async def roulette(self, inter, bullets: int = 1):
        if bullets < 1:
            await inter.response.send_message(
                'Хотите гарантий, что не проиграете? Гарантирую, что вы не выиграете!'
            )
            return
        elif bullets > 6:
            await inter.response.send_message('Очень жаль, но револьвер шестизарядный.')
            return
        if role:
            if role[0] in [i.id for i in inter.author.roles]:
                await inter.response.send_message(
                    embed=disnake.Embed(
                        title='Русская рулетка',
                        description='Мёртвым нельзя умирать. Иначе даже Бог вас не воскресит.'))
                return
        if randint(1, 6) > bullets:
            cur.execute(f"SELECT great_unit, emoji, id FROM currencies WHERE name = '{currency}'")
            currency = cur.fetchone()
            if not currency:
                await inter.response.send_message('Название валюты указано неверно')
                return
            unit, emoji, id = currency
            cur.execute(f'SELECT roulette_cnt FROM users WHERE uid = {inter.author.id} AND system = {system}')
            cnt = cur.fetchone()[0]
            prize = round(bullets * unit * cnt)
            cur.execute(
                f'UPDATE users SET currency_{id} = currency_{id} + {prize}'
                f' WHERE uid = {inter.author.id} AND system = {system}'
            )
            cur.execute(f'UPDATE users SET roulette_cnt = roulette_cnt + 0.1 '
                        f'WHERE uid = {inter.author.id} AND system = {system}')
            conn.commit()
            await inter.response.send_message(f'Поздравляю. Вы выиграли {prize}{emoji}')
        else:
            cur.execute(f'UPDATE users SET roulette_cnt = 1 '
                        f'WHERE uid = {inter.author.id} AND system = {system}')
            conn.commit()
            if role:
                await inter.author.add_roles(inter.guild.get_role(role[0]))
            await inter.response.send_message('Вы умерли. Соболезнуем вам и вашим близким')'''

    @commands.slash_command()
    async def random_user(self, inter):
        await inter.response.send_message(random.choice(inter.guild.members))

    @commands.slash_command()
    async def write(self, inter, text: str, channel: disnake.TextChannel):
        if inter.author.id == 817312010000924732 or any(i.id == 1162989988699459604 for i in inter.author.roles):
            await channel.send(text)
        else:
            await inter.response.send_message('У вас нет прав на использование данной команды', ephemeral=True)

    @commands.slash_command()
    async def roll(self, inter, first: int = 0, second: int = 100, step: int = 1):
        await inter.response.send_message(random.randrange(first, second, step))

    @commands.slash_command(name='8ball')
    async def ball(self, inter, event):
        n = random.choice(
            ['бесспорно', 'предрешено', 'никаких сомнений', 'определённо, да', 'можешь быть уверен в этом',
             'мне кажется, да', 'вероятнее всего', 'хорошие перспективы', 'знаки говорят "да"', 'да',
             'пока не ясно, попробуй снова', 'спроси позже', 'лучше не рассказывать', 'сейчас нельзя предсказать',
             'сконцентрируйся и спроси опять', 'даже не думай', 'мой ответ — "нет"', 'по моим данным, нет',
             'перспективы не очень хорошие', 'весьма сомнительно'])
        await inter.response.send_message(f'Что касается события "{event}", {n}')


def setup(bot):
    bot.add_cog(Fun(bot))
