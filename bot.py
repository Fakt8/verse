import discord
import pyowm
import asyncio
import os
import random
from discord.ext import commands
from discord import Embed

PREFIX = '!'

client = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )
# .say

@client.event 
async def on_ready():
	print( 'BOT connected' )
	await client.change_presence( status = discord.Status.online, activity = discord.Game( 'VERSE' ) )

@client.command()
async def say(ctx, *, arg):
    author = ctx.message.author
    await ctx.send( f'{arg}')

@client.command()
@commands.has_permissions( administrator = True) 
async def saya(ctx, *, arg):
    await ctx.message.delete()
    author = ctx.message.author
    await ctx.send( f'{arg}')

# Мут

@client.command()
@commands.has_permissions( administrator = True) 
async def mute(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        mute_role = discord.utils.get(member.guild.roles, id = 692237120244547584) #Айди роли
        channel_log = client.get_channel(690826853140660275) #Айди канала логов

        await member.add_roles( mute_role )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0xfa0105 )) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0xfa0105 ))  

# Kick
@client.command()
@commands.has_permissions( administrator = True) 
async def kick(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        channel_log = client.get_channel(670260939249156096) #Айди канала логов

        await member.kick( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0xfa0105 ))
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был исключен.\n:book: По причине: {reason}**', color=0xfa0105 )) 


# Ban
@client.command()
@commands.has_permissions( administrator = True) 
async def ban(ctx,member: discord.Member = None, reason = None): 

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif reason is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:
        
        channel_log = client.get_channel(690826853140660275) #Айди канала логов

        await member.ban( reason = reason )
        await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0xfa0105 ))
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1) 
        await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователь {member.mention} был заблокирован.\n:book: По причине: {reason}**', color=0xfa0105 )) 


# Clear chat
@client.command()
@commands.has_permissions( administrator = True)
async def clear(ctx,amount : int):
    
    channel_log = client.get_channel(690826853140660275) #Айди канала логов

    await ctx.channel.purge( limit = amount )
    await ctx.send(embed = discord.Embed(description = f'**:heavy_check_mark: Удалено {amount} сообщений.**', color=0xc9761d))
    await asyncio.sleep(5)
    await ctx.channel.purge(limit=1)
    await channel_log.send(embed = discord.Embed(description = f'**:wastebasket:  Удалено {amount} сообщений.**', color=0xc9761d))


# Help
@client.command()
@commands.has_permissions( administrator = True )
async def helpa( ctx ):
	await ctx.message.delete() # - удаляет команду
	emb = discord.Embed( title = 'Навигация по командам <3' )
	emb.add_field( name = 'Очистка', value = 'Команда для очистки чата, пример искользования ```.clear 2```' )
	emb.add_field( name = f'{PREFIX}Бан', value = 'Команда для бана участника на сервере, пример использования ```.ban @user <причина>```' )
	emb.add_field( name = f'{PREFIX}Кик', value = 'Команда с помощью которой можно выгнать участника с сервера, пример использования ```.kick @user```' )
	emb.add_field( name = f'{PREFIX}Помощь', value = 'Помощь по командам сервера' )
	await ctx.send( embed = emb )

# Error
@kick.error 
async def kick_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, стоп, стоп, стоп! У вас недостаточно прав для использования данной команды!**', color=0xd4bd18))


#---
@ban.error 
async def ban_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, стоп, стоп, стоп! У вас недостаточно прав для использования данной команды!**', color=0xd4bd18)) 


#---
@clear.error 
async def clear_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, стоп, стоп, стоп! У вас недостаточно прав для использования данной команды!**', color=0xd4bd18))

    if isinstance( error, commands.MissingRequiredArgument  ): 
        await ctx.send(embed = discord.Embed(description = f'**:grey_exclamation: {ctx.author.name},обязательно укажите количевство сообщений.**', color=0xc9761d)) 

#---

@mute.error 
async def mute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, стоп, стоп, стоп! У вас недостаточно прав для использования данной команды!**', color=0xc0ac0d))       


# Работа с несуществующими командами

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound ):
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1) 
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name}, ошибочка... такой команды нет на сервере.**', color=0xc56202))
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1) 

#info

@client.command()
async def info(ctx):
    embed=discord.Embed(title="**Информация про сервер**", description="Сервер ***_VERSE_*** предназначен - для: \n ***общения, развлечения, знакомств, фильмов, игр, музыки и многого многого другого.*** \n Так же есть специальные роли, которые позволяют видеть ***__ограниченные каналы__***, которые ***__ не видят__*** другие участники. \n Пример таких ***__ролей__*** представлен ниже: \n <@&690999231703679048>, \n <@&690998992451928144>, \n <@&691000735869173872>.. \n И ещё пара ***__специальных__*** ролей, о которых вы сможете узнать в канале <#690941012998357034>. \n Вот вам небольшая информация про ***__наш__*** сервер. \n \n **Дополнительную информацию про каналы и их описание вы сможете узнать в: <#690826854470254622>, <#690941062880952341>.**", color=0xbbd3e0 )

    embed.set_footer( text = "Собственность сервера VERSE!", icon_url = client.user.avatar_url )
    #embed.set_author(name="Stishok")
    await ctx.send(embed=embed)

# Вход
@client.event
async def on_member_join(member):
  embed = discord.Embed(title="**Привет! Я очень рад тебя видеть на сервере** ***__VERSE!__***", description="Надеюсь тебе тут понравится! \n Для того чтобы ***__не много__*** ознакомится с сервером, напиши в чат ``Информация``, я тебе автоматически отвечу! \n Ну и не большой совет, прочитай ***<#690826855825145877>*** нашего сервера. \n ***Приятного времяпровождения <3***", color=0xbbd3e0)
  await member.send(embed=embed)





# Helpmee
help_me = ['команды', 'какие команды?']

info_b = ['информация про сервер', 'информация', 'что за сервер?', 'информация?']

oos_s = ['кто администратор?', 'кто основатель?', 'кто создатель?', 'кто администраторы?', 'кто администрация?', 'кто админ?']

partners = ['партнерство?', 'может быть партнёрство?', 'партнёрство?', 'что насчёт партнерства?']

hello = ['hi', 'hello', 'привет', 'ку', 'здарова', 'саламалейкум']

@client.event

async def on_message(message):
	await client.process_commands(message)
	msg = message.content.lower()

	if msg in help_me:
		await message.channel.send('**Чтобы узнать команды, пропиши -** ``.help``')

	if msg in info_b:
		await message.channel.send('**Чтобы ознакомится с сервером, пропиши -** ``.info``')

	if msg in partners:
		await message.channel.send('**По поводу партнёрства, можно обратится в лс к администрации сервера.**')

	if msg in oos_s:
		await message.channel.send('**Администрация данного сервера -** \n <@512971928471076864>, \n <@519558988304482304>, \n <@497155059772293151>.')
		


#embed = discord.Embed(description="Администрация данного сервера -** \n <@512971928471076864>, \n <@519558988304482304>, \n <@497155059772293151>", color=0x02130)
		#await member.send(embed=embed)

# Команды кстом
@client.command()
@commands.has_permissions( administrator = True )

async def priv( ctx ):

	await ctx.message.delete() # - удаляет команду

	emb = discord.Embed( title="**Приветствие!**", description="Привет дорогой друг! \n Рад тебя приветствовать тебя на ***__нашем__*** сервере! \n Думаю, то что много про сервер описывать не нужно \n Ведь вы сами можете осмотреть его. Но всё же я в крации напишу \n **инструктаж по каналам:** \n <#690826854470254622> - и есть инструктаж. \n <#690826855825145877> - правила нашего сервера. \n <#690826857612050502> - публикуются новости сервер. \n <#690941012998357034> - роли которые можно получить. \n <#690941062880952341> - список и описание каналов \n <#690826860598394881> - партнёры нашего сервера. \n \n <#690826861978320946> - публикуются мемы. \n <#690826862628175882> - публикуются фильмы. \n <#690826863328886834> - проводятся розыгрышы. \n <#690826864104701982> - проводятся ивенты. \n <#690826865254072354> - публикуется 18+ контент. \n \n <#690826867577585725> - тут можете заказать музыку \n **Если вы увидили как кто-то из пользователей нарушил** ***__правила__*** **нашего сервера, то вы можете оформить на него** ***репорт***. \n **Команда -** ``!report @User Причина``", color=0x9150b4 )
	await ctx.send( embed = emb )
#await ctx.send(embed=emb, delete_after=10)- удаляет сообщния бота

# userinfo
@client.command()
async def userinfo(ctx, Member: discord.Member = None ):
    if not Member:
        Member = ctx.author
    roles = (role for role in Member.roles )
    emb = discord.Embed(title='Информация о пользователе.{}'.format(Member.name), description=f"Участник зашёл на сервер: {Member.joined_at.strftime('%b %#d, %Y')}\n\n "
                                                                                      f"Имя: {Member.name}\n\n"
                                                                                      f"Никнейм: {Member.nick}\n\n"
                                                                                      f"Статус: {Member.status}\n\n"
                                                                                      f"ID: {Member.id}\n\n"
                                                                                      f"Высшая роль: {Member.top_role}\n\n"
                                                                                      f"Аккаунт создан: {Member.created_at.strftime('%b %#d, %Y')}", 
                                                                                      color=0xff0000, timestamp=ctx.message.created_at)

    emb.set_thumbnail(url= Member.avatar_url)
    emb.set_footer(icon_url= Member.avatar_url)
    emb.set_footer(text='Спросил: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

# Servinfo
@client.command()
async def serverinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    guild = ctx.guild
    embed = discord.Embed(title=f"{guild.name}", description=f"Сервер создали {guild.created_at.strftime('%b %#d, %Y')}\n\n"
                                                             f"Регион {guild.region}\n\nГлава сервера {guild.owner}\n\n"
                                                             f"Людей на сервере {guild.member_count}\n\n",  color=0xff0000,timestamp=ctx.message.created_at)

    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"ID: {guild.id}")

    embed.set_footer(text=f"ID Пользователя: {ctx.author.id}")
    await ctx.send(embed=embed)


# Репорт

@client.command()
async def report(ctx,member: discord.Member = None,*,arg = None):
    channel = client.get_channel(692238649613615134) #Айди канала жалоб

    if member is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

    elif arg is None:

        await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: причину!**'))

    else:

        await ctx.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}**', color=0x0c0c0c))
        await channel.send(embed = discord.Embed(description =f'**:shield: На пользователя {member.mention} была отправлена жалоба.\n:bookmark_tabs: По причине: {arg}\n:bust_in_silhouette: Автор жалобы: {ctx.author.mention}**', color=0x0c0c0c))
        emb.set_footer(icon_url= Member.avatar_url)
        emb.set_footer(text='Подал: {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)


# Мут на время

@client.command()
@commands.has_permissions( administrator = True )
async def tempmute(ctx,amount : int,member: discord.Member = None, reason = None):
    mute_role = discord.utils.get(member.guild.roles, id = 692237120244547584) #Айди роли
    channel_log = client.get_channel(690826853140660275) #Айди канала логов

    await member.add_roles( mute_role )
    await ctx.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c)) 
    await channel_log.send(embed = discord.Embed(description = f'**:shield: Пользователю {member.mention} был ограничен доступ к чатам.\n:book: По причине: {reason}**', color=0x0c0c0c))
    await asyncio.sleep(amount)
    await member.remove_roles( mute_role )   

# Работа с ошибками мута на время

@tempmute.error 
async def tempmute_error(ctx, error):

    if isinstance( error, commands.MissingPermissions ):
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: {ctx.author.name},у вас нет прав для использования данной команды.**', color=0x0c0c0c))

@client.command(aliases = ['count', 'calc', 'вычисли', 'math'])
async def __count(ctx, *, args = None):
    text = ctx.message.content

    if args == None:
        await ctx.send(embed = discord.Embed(description = 'Please, specify expression to evaluate.', color = 0x39d0d6))
    else:
        result = eval(args)
        await ctx.send(embed = discord.Embed(description = f'Evaluation result of `{args}`: \n`{result}`', color = 0x39d0d6))  


# Класс

class Messages:

    def __init__(self, Bot):
        self.Bot = Bot

    async def number_messages(self, member):
        n_messages = 0
        for guild in self.Bot.guilds:
            for channel in guild.text_channels:
                try:
                    async for message in channel.history(limit = None):
                        if message.author == member:
                            n_messages += 1
                except (discord.Forbidden, discord.HTTPException):
                    continue
        return n_messages

# Ранг

@client.command(name = "rang")
async def num_msg(ctx, member: discord.Member = None):
    lvl = 0
    user = ctx.message.author if (member == None) else member
    number = await Messages(Bot).number_messages(user)
    
    if number < 1000:
        lvl = 0

    elif number > 1000:
        lvl = 1

    elif number > 2000:
        lvl = 2

    embed = discord.Embed(description = f"Уровень: {lvl} Опыт: {number}", color=0x0c0c0c)
    await ctx.send(embed = embed)

# Шар

@client.command(aliases = ["8ball"])
async def ver(ctx, *, arg):

    message = ['Ежжии, Джан, переспроси вопросик', 'Канешнааа (нет)', 'Слушай, я врать не буду, но Да', 'Можешь не сомневатся!', 'Думаю не стоит'] 
    s = random.choice( message )
    await ctx.send(embed = discord.Embed(description = f'**:crystal_ball: На заборах написано:** {s}', color=0x7a14a7))
    return

# Работа с ошибками шара

@ver.error 
async def ver_error(ctx, error):

    if isinstance( error, commands.MissingRequiredArgument ): 
        await ctx.send(embed = discord.Embed(description = f'Пожалуйста, укажите сообщение.', color=0x7a14a7))  

# Добавление роли на время

@client.command()
@commands.has_permissions(administrator = True)
async def temp_add_role(ctx, amount : int, member: discord.Member = None, role: discord.Role = None):

    try:

        if member is None:

            await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: пользователя!**'))

        elif role is None:

            await ctx.send(embed = discord.Embed(description = '**:grey_exclamation: Обязательно укажите: роль!**'))

        else:

            await discord.Member.add_roles(member, role)
            await ctx.send(embed = discord.Embed(description = f'**Роль успешна выдана на {amount} секунд!**'))
            await asyncio.sleep(amount)
            await discord.Member.remove_roles(member, role)

    except:
        
        await ctx.send(embed = discord.Embed(description = f'**:exclamation: Не удалось выдать роль.**', color=0x0c0c0c))

# Pogoda
@client.command( pass_context = True )        
async def weather( ctx, arg ):
    owm = pyowm.OWM( 'API key' )

    observation = owm.weather_at_place( arg )
    w = observation.get_weather()
    temperature = w.get_temperature( 'celsius' )[ 'temp' ]
    time = w.get_reference_time(timeformat='date')
    clouds = w.get_clouds() 
    rain = w.get_rain()
    snow = w.get_snow()
    wind = w.get_wind()
    humidity = w.get_humidity()
    pressure = w.get_pressure()
    status =  w.get_status()
    detailed_ststus = w.get_detailed_status() 
    sunrise_time = w.get_sunrise_time('iso') 
    sunset_time = w.get_sunset_time('iso')

    emb = discord.Embed( title = f'Weather in { arg }', colour = discord.Color.blue(), icon_url = ':02d:' )
    emb.set_author( name = ctx.author.name, icon_url = ctx.author.avatar_url )
    emb.set_footer( text = f'{ ctx.message.created_at }' )
    emb.add_field( name = '**Temp**', value = f'{temperature} C' )
    emb.add_field( name = '**Time**', value = time, inline = False )
    emb.add_field( name = '**Clouds**', value = clouds, inline = False )
    emb.add_field( name = '**Rain**', value = rain, inline = False )
    emb.add_field( name = '**Snow**', value = snow, inline = False )
    emb.add_field( name = '**Wind**', value = wind, inline = False )
    emb.add_field( name = '**Humidity**', value = f'{humidity}%', inline = False )
    emb.add_field( name = '**Pressure**', value = pressure, inline = False )
    emb.add_field( name = '**Status**', value = status, inline = False )
    emb.add_field( name = '**Detailed status**', value = detailed_ststus, inline = False )
    emb.add_field( name = '**Sunrise time**', value = sunrise_time, inline = False )
    emb.add_field( name = '**Sunset time**', value = sunset_time, inline = False )

    await ctx.send( embed = emb )

# Helpe
@client.command()
async def help( ctx ):
    await ctx.message.delete() # - удаляет команду
    emb = discord.Embed( title = 'Навигация по командам <3', color=0x309ece )
    emb.add_field( name = 'Умный', value = 'Команда для решения вопроса. Пример - ``!ver Я выйграю 1.000.000?``' )
    emb.add_field( name = 'Репорт', value = 'Команда для того чтобы пожаловаться на пользователя. Пример - ``!report @User Причина``' )
    emb.add_field( name = 'Сказать ботом', value = 'Команда с помощью которой вы сможете написать текст, но он будет написан ботом, пример использования ``!say Текст``' )
    emb.add_field( name = 'Информация', value = 'Так же вы можете узнать небольшую информацию про сервер. Напишите в чат ``Информация`` и бот вам автоматически ответит!' )
    await ctx.send( embed = emb )












# Token
token = os.environ.get('BOT_TOKEN')

bot.run(str(token))

#token = open( 'token.txt', 'r' ).readline()

#client.run( token )
