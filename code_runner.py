import discord
import requests


# TODO: добваить возможность взаимодействовать с input()
class CodeRunner:

    @staticmethod
    def run_code(code: str, show_code_on_error: bool = False) -> str:
        url = "https://codex-api.herokuapp.com/"

        payload = {
            "code": code,
            "language": 'py',
            "input": '',
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.request("POST", url, data=payload, headers=headers).json()
        print(response)
        if response['success']:
            return response['output']
        else:
            if show_code_on_error:
                return response['error'] + '\n**Code:**\n' + code
            else:
                return response['error']

    class PythonRunnerModal(discord.ui.Modal, title='Python runner'):

        def __init__(self, show_code: bool):
            super().__init__()
            self.show_code = show_code

        answer = discord.ui.TextInput(label='Напишите свой код здесь:',
                                      style=discord.TextStyle.paragraph,
                                      placeholder='На данный момент пользовтаельский ввод(input()) не доступен, '
                                      'учитывайте это при написании программы!')

        async def on_submit(self, interaction: discord.Interaction) -> None:
            if self.show_code:
                embed_description = f"**Code:** " \
                                    f"\n{self.answer.value}" \
                                    f"\n**Console output**" \
                                    f"\n{CodeRunner.run_code(self.answer.value)}"
            else:
                embed_description = f"**Console output**" \
                                    f"\n{CodeRunner.run_code(self.answer.value, True)}"

            embed = discord.Embed(title=self.title,
                                  description=embed_description,
                                  colour=discord.Colour.teal())

            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
