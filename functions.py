import discord
import csv
import random
import smtplib
import email.message
import openai

#função para verificar se o email institucional existe
def verifEmail():
    aluPro = ["alunos.csv", "professores.csv"]
    eInst = []
    for i in aluPro:
        with open(i, "r") as arquivo:
            leitor = csv.reader(arquivo)
            if i == "alunos.csv":
                for i in leitor:
                    eInst.append(i[7])
            elif i == "professores.csv":
                for i in leitor:
                    eInst.append(i[1])
    return eInst

#função para gerar código de 6 dígitos
def codigo():
    codigo = random.randint(100000,999999)
    return str(codigo)

#função para enviar email para o usuário
def envioEmail(mailDestinatario):
    # login do remetente (bot)
    remetente = "bot.metabot@gmail.com"
    senha = "jsqijsvrlgrpljzm"
    # mensagem do email
    code = codigo()
    print(code)
    assunto = "[MetaBot] Código de verificação"
    mensagem = f"{code} é seu código de verificação do servidor Code Crunchers."
    # estrutura do email
    config = email.message.Message()
    config["From"] = remetente
    config["To"] = mailDestinatario
    config["Subject"] = assunto
    # smtp
    config.add_header("Content-Type", "Text/html")
    config.set_payload(mensagem)
    server = smtplib.SMTP("smtp.gmail.com: 587")
    server.starttls()
    server.login(config["From"], senha)
    server.sendmail(config["From"], config["To"], config.as_string().encode("utf-8"))
    return code

#função para atribuir cargo de professor ou aluno
def cargoAluPro(mailDestinatario):
    aluPro = ["alunos.csv", "professores.csv"]
    for i in aluPro:
        with open(i, "r") as arquivo:
            leitor = csv.reader(arquivo)
            if i == "alunos.csv":
                for i in leitor:
                    if i[7] == mailDestinatario:
                        cargo = "aluno"
                        return cargo

            elif i == "professores.csv":
                for i in leitor:
                    if i[1] == mailDestinatario:
                        cargo = "professor"
                        return cargo

#função para acessar nome do usuário
def acessarNomeUsuario(mailDestinatario):
    aluPro = ["alunos.csv", "professores.csv"]
    for i in aluPro:
        with open(i, "r") as arquivo:
            leitor = csv.reader(arquivo)
            if i == "alunos.csv":
                for i in leitor:
                    if i[7] == mailDestinatario:
                        return i[1]

            elif i == "professores.csv":
                for i in leitor:
                    if i[1] == mailDestinatario:
                        return i[0]

# função para atribuir um novo nome de usuário
async def nomeUsuario(mailDestinatario, member):
    usuario = acessarNomeUsuario(mailDestinatario)
    print(f"Nome de usuário modificado para: {usuario}")
    await member.edit(nick = usuario)

# função para realizar banimentos
async def banir(member):
    guild = member.guild
    cargoPretendente = discord.utils.get(guild.roles, name = "pretendente")
    if cargoPretendente in member.roles:
        await member.ban(reason = "Tempor de 5 minutos esgosto para retonar o código de verificação.")

# função para receber as perguntas do usuário e retornar as respostas
def perguntaGPT(pergunta):
    openai.api_key = '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'

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": str(pergunta)}]
    )

    return completion.choices[0].message.content