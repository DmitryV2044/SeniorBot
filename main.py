import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

import buttons

load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN')
config = {
    'token': bot_token,
    'prefix': '/',
}


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or(config['prefix']), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(buttons.CustomRoleView())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')


bot = PersistentViewBot()


@bot.command(name="roles_message")
@commands.has_role('admin')
async def button(ctx: commands.Context):
    view = buttons.CustomRoleView()
    await ctx.message.delete()
    await ctx.send("**Дайте себе роль!**"
                   "\nНажмите кнопку роли, которую хотите добавить!"
                   "\nНажмите еще раз, чтобы удалить эту роль!"
                   "\nРоли:", view=view)


@bot.command(name='kick_test')
@commands.has_role("admin")
async def kick(ctx: commands.Context, user: discord.User, *arg, reason='Причина не указана'):
    await ctx.guild.kick(user)
    await ctx.send(f'Пользователь {user.name} был кикнут (?)')


@bot.command(name='guild')
async def get_guild(ctx: commands.Context):
    print("123")
    await ctx.send(f'guild id: {ctx.guild.id}')


@bot.command(name="gg")
async def test2(ctx):
    await ctx.send('ХАХАХАХА, ты написал gg, а на самом деле это test2.\nХотя, ну, test2, ладно.')


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user):
    print("1323")
    if str(reaction.emoji) == '👉':
        print("111")


@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    print(f"raw reaction {payload.guild_id}")


bot.run(config['token'])
