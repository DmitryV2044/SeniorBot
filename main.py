import os
from discord.ext import commands
from dotenv import load_dotenv
from code_runner import *
import views

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
        self.add_view(views.CustomRoleView())

    async def on_ready(self):
        await self.tree.sync()
        print(f'Logged in as {self.user} (ID: {self.user.id})')


bot = PersistentViewBot()


@bot.tree.command(name="roles_message", description="Создать сообщение с кнопками для выбора роли")
@commands.has_role('admin')
async def send_roles_message(interaction: discord.Interaction):
    view = views.CustomRoleView()
    await interaction.response.send_message(
        content="**Дайте себе роль!**"
        "\nНажмите кнопку роли, которую хотите добавить!"
        "\nНажмите еще раз, чтобы удалить эту роль!"
        "\nРоли:", view=view)


@bot.tree.command(name='guild', description="Вывести guild id сервера")
async def get_guild(interaction:  discord.Interaction):
    await interaction.response.send_message(f'guild id: {interaction.guild.id}', ephemeral=True)


@bot.tree.command(name='run', description='Открывает окно для выполнения кода на Python')
async def run_py(interaction: discord.Interaction, show_code: bool = False):
    await interaction.response.send_modal(CodeRunner.PythonRunnerModal(show_code))


bot.run(config['token'])
