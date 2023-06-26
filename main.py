import functions
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = "-", caseInsensitive = True, intents = intents)

@bot.event
async def on_ready():
    print("Entramos como {0.user}".format(bot))

# evento para atribuir cargo ao novo membro
@bot.event
async def on_member_join(member):
    # ID
    idServidor = 1117572776098803762
    idBoasVindas = 1117581401785643038
    idPretendente = 1117573586669010964

    # comandos para sempre que um novo membro entrar, ele ter acesso só a sala de autenticação
    guild = member.guild
    role = guild.get_role(idBoasVindas)
    # comandos para sempre que um novo membro entrar, mandar uma mensagem automatica
    chamadaEmail = bot.get_channel(idBoasVindas)
    mensagem = await chamadaEmail.send(f"Bem vindo(a), {member.mention}! Informe seu e-mail institucional para ter acesso ao servidor.")
    # comandos atribuir cargo de pretendente
    servidor = bot.get_guild(idServidor)
    global cargoPretendente
    cargoPretendente = servidor.get_role(idPretendente)
    await member.add_roles(cargoPretendente)
    print(f"O cargo {cargoPretendente.name} foi atribuído a {member.name}.")

# evento para receber os emails e verificar se existe no arquivo csv
@bot.event
async def on_message(message):
    idBoasVindas = 1117581401785643038
    if message.author != bot.user:
        if '@' in message.content and message.channel.id == idBoasVindas:
            mailDestinatario = message.content
            if mailDestinatario in functions.verifEmail():
                member = message.author
                retorno = f"Um código foi enviado para o seu e-mail,{member.mention}."
                await message.channel.send(retorno)
            else:
                retorno = "Não foi encontrado o e-mail institucional. Crie e volte aqui."
                await message.channel.send(retorno)
                await asyncio.sleep(5)
                await functions.banir(message.author)
            print(mailDestinatario)

            # envio do email
            cod = functions.envioEmail(mailDestinatario)

            # banir após 5min
            codeEnviado = await bot.wait_for("message")
            if codeEnviado.content == cod:
                # remover cargo de pretendente e atribuir o novo
                member = message.author
                cargo = functions.cargoAluPro(mailDestinatario)
                cargoAtribuido = discord.utils.get(message.guild.roles, name = cargo)
                await message.author.remove_roles(cargoPretendente)
                await message.author.add_roles(cargoAtribuido)
                await (functions.nomeUsuario(mailDestinatario, member))
                await message.channel.send(f"Como vai, {member.mention}?! Agora você faz parte do cargo {cargo}. Aproveite o servidor!")
                return exit

            else:
                await asyncio.sleep(300)
                await message.channel.send("Hmm... O código não parece certo. Que tal tentar novamente?")
                await functions.banir(message.author)

    aguardo = await bot.wait_for("message")
    idChatGpt = 1122688706394984539
    if aguardo.author == bot.user:
        return
    if aguardo.channel.id == idChatGpt:
        member = aguardo.author
        pergunta = aguardo.content
        resposta = functions.perguntaGPT(pergunta)
        await aguardo.channel.send(f"{member.mention}: {resposta}")

    await bot.process_commands(message)

bot.run('MTExNzUyNTAyOTQ1OTA4MzM0NQ.GXAlPH.n0PFq4BCJtoLCtseJ-ACnfwFPkTNcZUuX_Dt_Y')