# -*- coding: utf-8 -*-
"""
Discord sunucu kanal ve rol adı değiştirme (user/self token ile).
Kullanım: !degistir <aranan_kelime> <yeni_kelime>
Token'ı .env dosyasına DISCORD_TOKEN olarak ekleyin (kendi hesabınızın user token'ı).

UYARI: User token kullanımı Discord Kullanım Şartlarına aykırıdır; hesap riski vardır.
      Mümkünse Developer Portal'dan bot oluşturup bot token kullanın.
"""

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
_raw = os.getenv("DISCORD_TOKEN")
TOKEN = (_raw or "").strip().strip('"').strip("'")

# discord.py-self: Intents yok, user hesabı için self_bot=True
bot = commands.Bot(command_prefix="!", self_bot=True)


@bot.event
async def on_ready():
    print(f"{bot.user} olarak giriş yapıldı.")
    print("Komut: !degistir <aranan_kelime> <yeni_kelime>")


@bot.event
async def on_message(message):
    # Self-bot kütüphanesi komutları sadece kendi kullanıcısına işliyor olabilir.
    # !degistir'i burada elle işliyoruz; yetkili herkes kullanabilsin.
    if not message.content.startswith("!degistir ") and message.content != "!degistir":
        await bot.process_commands(message)
        return

    if not message.guild:
        await message.channel.send("Bu komut sadece sunucuda kullanılabilir.")
        return

    # Yetki: Komutu yazan üyede Kanal Yönet + Rol Yönet olmalı (veya komutu botu çalıştıran hesap yazdıysa izin ver)
    if message.author.id == bot.user.id:
        pass  # Kendi hesabımız, yetki kontrolü atla
    else:
        try:
            member = message.guild.get_member(message.author.id)
            if member is None:
                member = getattr(message, "member", None) or message.author
            perms = getattr(member, "guild_permissions", None)
        except Exception:
            perms = None
        if perms is None or not (perms.manage_channels and perms.manage_roles):
            await message.channel.send("Bu komutu kullanmak için **Kanal Yönet** ve **Rol Yönet** yetkileri gerekli.")
            return

    # "!degistir Hermes Rovenia" -> aranan=Hermes, yeni=Rovenia
    parts = message.content.split(None, 2)
    if len(parts) < 3:
        await message.channel.send("Kullanım: `!degistir <aranan_kelime> <yeni_kelime>`")
        return

    aranan, yeni = parts[1], parts[2]
    guild = message.guild
    degisen_kanallar = []
    degisen_roller = []
    hatalar = []

    for channel in guild.channels:
        if aranan not in channel.name:
            continue
        try:
            eski_isim = channel.name
            yeni_isim = channel.name.replace(aranan, yeni)
            await channel.edit(name=yeni_isim)
            degisen_kanallar.append(f"**{eski_isim}** → **{yeni_isim}**")
        except discord.Forbidden:
            hatalar.append(f"Kanal: {channel.name} (yetki yok)")
        except Exception as e:
            hatalar.append(f"Kanal: {channel.name} ({e})")

    for role in guild.roles:
        if role.is_default() or role.is_bot_managed():
            continue
        if aranan not in role.name:
            continue
        try:
            eski_isim = role.name
            yeni_isim = role.name.replace(aranan, yeni)
            await role.edit(name=yeni_isim)
            degisen_roller.append(f"**{eski_isim}** → **{yeni_isim}**")
        except discord.Forbidden:
            hatalar.append(f"Rol: {role.name} (yetki yok)")
        except Exception as e:
            hatalar.append(f"Rol: {role.name} ({e})")

    mesaj = []
    if degisen_kanallar:
        mesaj.append("**Değiştirilen kanallar:**\n" + "\n".join(degisen_kanallar))
    if degisen_roller:
        mesaj.append("**Değiştirilen roller:**\n" + "\n".join(degisen_roller))
    if hatalar:
        mesaj.append("**Hatalar:**\n" + "\n".join(hatalar))

    if not degisen_kanallar and not degisen_roller and not hatalar:
        await message.channel.send(f"'{aranan}' adında veya içeren kanal/rol bulunamadı.")
        return
    if not degisen_kanallar and not degisen_roller:
        await message.channel.send("Hiçbir kanal/rol değiştirilemedi.\n" + "\n".join(hatalar))
        return

    sonuc = "\n\n".join(mesaj)
    if len(sonuc) > 1900:
        sonuc = sonuc[:1900] + "\n...(kesildi)"
    await message.channel.send(sonuc)


def main():
    if not TOKEN or TOKEN.lower() in ("buraya_bot_tokeninizi_yazin", "your_token_here", "buraya_user_tokeninizi_yazin"):
        print("HATA: Geçerli bir token bulunamadı.")
        print("  - .env dosyasında DISCORD_TOKEN=... olarak (user) token'ı yazın.")
        print("  - User token: Discord tarayıcıda F12 → Console'da dokümandaki kodu çalıştırın veya")
        print("    Network → bir istek → Headers → Authorization değerini kopyalayın.")
        return
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("HATA: Discord token geçersiz (401 Unauthorized).")
        print("  - Token'da başta/sonda boşluk veya tırnak olmasın.")
        print("  - User token sık sık geçersiz olur; tarayıcıdan yeni kopyalayın.")


if __name__ == "__main__":
    main()
