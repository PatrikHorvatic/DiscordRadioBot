import os
import discord
import subprocess
import sys
import time
import random
import asyncio
from podaci import Podaci
from threading import Thread
from datetime import datetime
from discord.ext import commands
from discord import FFmpegPCMAudio
from prettytable import PrettyTable
from keep_alive import keep_alive

from pjesma import Pjesma
from dadjoke import Dadjoke
from deezer import Deezer


def zapisiLog(sadrzaj):
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(dt_string + " " + sadrzaj + "\n")


def installPy():
    while True:
        try:
            print(
                f"Instalacija PyNaCl počinje....{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "PyNaCl"])
        except:
            print("Greška kod instalacije PyNaCl-a")
            zapisiLog(
                f"Greška kod instalacije PyNaCl...{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )
        time.sleep(1800)


podaci = Podaci()
klijent = commands.Bot(command_prefix=podaci.PREFIX)
klijent.remove_command('help')

songs = asyncio.Queue()
play_next_song = asyncio.Event()


#-----------------------------PLAYER--------------------------------------------
@klijent.command(aliases=["sviraj", "pusti", "rokni", "namaži"])
async def radio(poruka, stanica):
    if not poruka.author.voice:
        return await poruka.send("Nisi u voice kanalu.")
    else:
        kanal = poruka.message.author.voice.channel
        global radioStanica
        radioStanica = stanica.upper()

        global uKanalu
        uKanalu = None

        if stanica.upper() in podaci.STANICE:
            try:
                podaci.player = await kanal.connect()
                podaci.player.play(FFmpegPCMAudio(
                    podaci.STANICE[radioStanica]))
                print(f"RadioBot pozvan na kanal: {kanal}")

                podaci.radioStanica = stanica.upper()
                print(podaci.radioStanica)
                await poruka.send(f"Sviram {radioStanica}")
                await poruka.send(file=discord.File("GIF/vibecat.gif"))

                zapisiLog(
                    f"RadioBot pozvan na kanal: {kanal} i svira {podaci.radioStanica}"
                )

                uKanalu = True

            except discord.errors.ClientException as ex:
                podaci.player.play(FFmpegPCMAudio(
                    podaci.STANICE[radioStanica]))
                print(f"RadioBot pozvan na kanal: {kanal}")
                await poruka.send(f"Sviram {radioStanica}")
                await poruka.send(file=discord.File("GIF/vibecat.gif"))
                print(ex)
            except discord.ext.commands.errors.CommandInvokeError:
                installPy()
                time.sleep(5)
                podaci.player = await kanal.connect()
                podaci.player.play(FFmpegPCMAudio(
                    podaci.STANICE[radioStanica]))
                print(f"RadioBot pozvan na kanal: {kanal}")

                podaci.radioStanica = stanica.upper()
                print(podaci.radioStanica)
                await poruka.send(f"Sviram {radioStanica}")
                await poruka.send(file=discord.File("GIF/vibecat.gif"))

                zapisiLog(
                    f"RadioBot pozvan na kanal: {kanal} i svira {podaci.radioStanica}"
                )

                uKanalu = True

        else:
            for i in podaci.STANICE.keys():
                print(i)
                podaci.RadioStanica = i
                #print(podaci.radioStanica)

                if radioStanica in i:
                    try:
                        podaci.player = await kanal.connect()
                        podaci.player.play(FFmpegPCMAudio(podaci.STANICE[i]))

                        print(f"RadioBot pozvan na kanal: {kanal}")
                        await poruka.send(f"Sviram {i}")
                        await poruka.send(file=discord.File("GIF/vibecat.gif"))
                        zapisiLog(
                            f"RadioBot pozvan na kanal: {kanal} i svira {i}")
                        print(podaci.RadioStanica)
                    except discord.ext.commands.errors.CommandInvokeError:
                        installPy()
                        time.sleep(5)
                        podaci.player = await kanal.connect()
                        podaci.player.play(
                            FFmpegPCMAudio(podaci.STANICE[radioStanica]))
                        print(f"RadioBot pozvan na kanal: {kanal}")

                        podaci.radioStanica = stanica.upper()
                        print(podaci.radioStanica)
                        await poruka.send(f"Sviram {radioStanica}")
                        await poruka.send(file=discord.File("GIF/vibecat.gif"))

                        zapisiLog(
                            f"RadioBot pozvan na kanal: {kanal} i svira {podaci.radioStanica}"
                        )

                        uKanalu = True
                    break


@klijent.command(aliases=["denina"])
async def promjeni(poruka, stanica):
    podaci.player.stop()
    podaci.radioStanica = stanica.upper()

    if stanica in podaci.STANICE:
        try:
            podaci.player.play(FFmpegPCMAudio(podaci.STANICE[stanica]))
            zapisiLog(f"Stanica promjenjena na {stanica}")
            #await poruka.send(file=discord.File("vibecat.gif"))

        except:
            await poruka.send("Greška prilikom puštanja radija. Malo sam glup."
                              )
            #await podaci.player.disconnect()

    else:
        for i in podaci.STANICE.keys():
            if stanica.upper() in i:
                try:
                    podaci.player.play(FFmpegPCMAudio(podaci.STANICE[i]))
                    podaci.radioStanica = i
                    print(podaci.radioStanica)
                    #await poruka.send(file=discord.File("vibecat.gif"))
                    break

                except:
                    await poruka.send(
                        "Greška prilikom puštanja radija. Malo sam glup.")
                    #await podaci.player.disconnect()
                    break


@klijent.command(aliases=["PJESMA"])
async def pjesma(poruka):
    aktivnaStanica = podaci.radioStanica
    print(aktivnaStanica)
    stanica = podaci.STANICE[aktivnaStanica]
    trenutna = Pjesma(stanica)
    await poruka.send(f"Trenutna pjesma:  {trenutna.dohvatiPjesmu()}")
    zapisiLog("Pokušaj dohvata imena pjesme.")


@klijent.command(aliases=["stani"])
async def pauza(poruka):
    podaci.player.pause()


@klijent.command()
async def nastavi(poruka):
    podaci.player.resume()


@klijent.command()
async def gasi(poruka):
    podaci.player.stop()


@klijent.command(aliases=["mrš"])
async def izađi(poruka):
    await podaci.player.disconnect()
    await poruka.send(file=discord.File("GIF/dissapear.gif"))
    zapisiLog("RadioBot izbačen iz kanala.")


@klijent.command()
async def dalima(poruka, stanica):
    if stanica.upper() in podaci.STANICE:
        await poruka.send(f"Imam {stanica}")

    else:
        nadena = False
        listaNadenih = []
        for i in podaci.STANICE.keys():
            if stanica.upper() in i:
                nadena = True
                listaNadenih.append(i)

        if nadena == True:
            await poruka.send("Imam sljedeće stanice: ")
            await poruka.send(listaNadenih)
        else:
            await poruka.send("Nemam stanicu ovog ili sličnog imena.")
            await poruka.send(file=discord.File("GIF/sorry.gif"))


#----------------DRUGE KOMANDE-----------------------------------


@klijent.command(
    aliases=["komande", "naredbe", "popisnaredbi", "pomoc", "help"],
    pass_context=True)
async def pomoć(poruka):
    gnjezdo = discord.Embed(colour=discord.Colour.orange())
    gnjezdo.set_author(name="Pomoć")
    gnjezdo.add_field(name=f"{podaci.PREFIX}stanice",
                      value="ispiši popis svih stanica",
                      inline=False)
    gnjezdo.add_field(
        name=f"{podaci.PREFIX}radio (sviraj, pusti, rokni, namaži)",
        value="poziva radio u voice channel, potrebno dodati radio s popisa",
        inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}pauza (stani)",
                      value="Pauzira radio",
                      inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}nastavi",
                      value="Nastavlja sviranje radija",
                      inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}gasi",
                      value="Zaustavnja radio",
                      inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}izađi (mrš)",
                      value="Bot izlazi iz voice kanala",
                      inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}promjeni (denina)",
                      value="Mijenja radio stanicu",
                      inline=False)
    gnjezdo.add_field(
        name=f"{podaci.PREFIX}dalima",
        value=
        "Ispisuje listu stanica ili stanicu iz liste. Ako stanica ne postoji, javlja da je nema, logično.",
        inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}ping",
                      value="Pong! Prikazuje delay sviranja",
                      inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}bok",
                      value="Šalje bok",
                      inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}kekw",
                      value="Šalje sliku Risitas i KEKW!",
                      inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}autor",
                      value="Ispisuje autora bota",
                      inline=False)
    gnjezdo.add_field(name=f"{podaci.PREFIX}verzija",
                      value="Ispisuje verziju bota",
                      inline=False)
    await poruka.send(embed=gnjezdo)


#radi
@klijent.command(aliases=["lista", "popis"])
async def stanice(poruka):
    tablica = PrettyTable()
    tablica.field_names = [
        "-----------------", "RADIO STANICE", "------------------"
    ]
    redak = []
    i = 0
    for x in podaci.STANICE.keys():
        redak.append(x)
        i += 1
        if i == 3:
            tablica.add_row(redak)
            i = 0
            redak.clear()

    await poruka.send(f"```{tablica}```")


#radi
@klijent.command()
async def ping(poruka):
    await poruka.send(f"PONG! {round(klijent.latency * 1000)} ms")
    await poruka.send(file=discord.File("GIF/ping-pong.gif"))


#radi
@klijent.command()
async def bok(poruka):
    await poruka.send("Bok!")


#radi
@klijent.command()
async def kekw(poruka):
    #channel = klijent.get_channel(poruka.message.author.text.channel)
    await poruka.send(file=discord.File("GIF/kekw.png"))
    await poruka.send("KEKW!")


#radi
@klijent.command()
async def autor(poruka):
    await poruka.send("Moj stvaratelj: Patrik Horvatić.")


@klijent.command(aliases=["VERZIJA"])
async def verzija(poruka):
    await poruka.send("Verzija: 1.69.420")


@klijent.command()
async def dadjoke(poruka):
    joke = Dadjoke()
    fora = joke.dohvatiForu()
    #print(fora)
    await poruka.send(fora)
    broj = random.randint(1, 4)
    if broj == 1:
        datoteka = discord.File("GIF/CAT-PIC/CAT-1.jpg")
    elif broj == 2:
        datoteka = discord.File("GIF/CAT-PIC/CAT-2.jpg")
    elif broj == 3:
        datoteka = discord.File("GIF/CAT-PIC/CAT-3.jpg")
    elif broj == 4:
        datoteka = discord.File("GIF/CAT-PIC/CAT-3.jpg")
    await poruka.send(file=datoteka)


#------------------------------DOGAĐAJI------------------------------------
@klijent.event
async def on_member_join(member):
    print(f"Bok {member}!")


#pošalji povratnu informaciju kada je bot spreman
@klijent.event
async def on_ready():
    await klijent.change_presence(status=discord.Status.online)
    print("RadioBotHrvatska je spreman!")
    zapisiLog("RadioBot Hrvatska upaljen.")


@klijent.event
async def on_error(poruka):
    await poruka.send("Nepoznata greška.")
    await poruka.send(file=discord.File("GIF/computer-boom.gif"))


async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()


@klijent.command()
async def deezer(poruka, umjetnik):
    if not poruka.author.voice:
        return await poruka.send("Nisi u voice kanalu.")
    else:
        kanal = poruka.message.author.voice.channel

        deezer = Deezer(umjetnik)
        deezer.DohvatiPodatke()
        deezer.SpremiRjecnikPoveznica()

        try:
            podaci.player = await kanal.connect()
            podaci.player.play(FFmpegPCMAudio())
            print(f"RadioBot pozvan na kanal: {kanal}")
        except discord.errors.ClientException as ex:
            podaci.player.play(FFmpegPCMAudio(podaci.STANICE[radioStanica]))
            print(f"RadioBot pozvan na kanal: {kanal}")
            print(ex)


#---------------------------OVO ISPOD NE DIRAJ-----------------------------

#Pokreni botaru
t_instalacija = Thread(target=installPy)
t_instalacija.start()

keep_alive()
klijent.loop.create_task(audio_player_task())
klijent.run(podaci.TOKEN)
