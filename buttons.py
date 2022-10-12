import discord

import roles

default_button_style = discord.ButtonStyle.blurple


class CustomRoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.custom_roles = roles.custom_roles
        self.custom_role_buttons = []

        for role in self.custom_roles:
            self.custom_role_buttons.append(
                discord.ui.Button(style=default_button_style, label=role, custom_id=role))

        for btn in self.custom_role_buttons:
            btn.callback = self.add_role_callback
            self.add_item(btn)

    async def add_role_callback(self, interaction: discord.Interaction):
        # await interaction.response.edit_message(
        #     content="**Дайте себе роль!**"
        #             "\nНажмите кнопку роли, которую хотите добавить!"
        #             "\nНажмите еще раз, чтобы удалить эту роль!"
        #             "\nРоли:",
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