import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('DISCORD_TOKEN')
config = {
    'token': bot_token,
    'prefix': '/',
}
custom_roles = {'Python', 'C#', 'C++', 'Blender', 'Unreal Engine', 'Unity', 'Godot'}

default_button_style = discord.ButtonStyle.blurple


class CustomRoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.custom_role_buttons = []
        for role in custom_roles:
            self.custom_role_buttons.append(
                discord.ui.Button(style=default_button_style,label=role,custom_id=role))

        for btn in self.custom_role_buttons:
            btn.callback = add_role_callback
            self.add_item(btn)


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or(config['prefix']), intents=intents)

    async def setup_hook(self) -> None:
        self.add_view(CustomRoleView())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')


bot = PersistentViewBot()


@bot.command(name="roles_message")
@commands.has_role('admin')
async def button(ctx: commands.Context):
    view = CustomRoleView()
    await ctx.message.delete()
    await ctx.send("Выдай себе роль что бы показать, с чем ты умеешь работать: ", view=view)


async def add_role_callback(interaction: discord.Interaction):
    # await interaction.response.edit_message(
    #     content="Выдай себе роль что бы показать, с чем ты умеешь работать: ",
    #     view=CustomRoleView())
    user = interaction.user
    role_name = interaction.data['custom_id']
    role = discord.utils.get(interaction.guild.roles, name=role_name)
    if role is None:
        role = await interaction.guild.create_role(
            name=role_name, colour=discord.Colour.teal(),
            mentionable=False, reason='auto created custom role')
        print('none')

    message = ""
    if role in user.roles:
        await user.remove_roles(role, reason='auto custom role removal')
        message = f'Убрана роль: {role_name}!'
    else:
        await user.add_roles(role, reason='auto custom role adding')
        message = f'Добавлена роль: {role_name}!'
    await interaction.response.send_message(content=message, ephemeral=True)


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
    print("123")
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
