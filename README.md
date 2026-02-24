# Discord Kanal ve Rol İsmi Değiştirme Botu

Sunucunuzdaki **kanal** ve **rol** adlarında geçen bir kelimeyi, girdiğiniz yeni kelimeyle toplu değiştiren Discord botu.

## Kurulum

1. **Python 3.8+** yüklü olsun.

2. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
   **Windows’ta** `pip` tanınmıyorsa:
   ```powershell
   py -m pip install -r requirements.txt
   ```

3. **Token'ı ayarlayın:**
   - `.env` dosyasını açıp `DISCORD_TOKEN=` kısmına kendi bot token'ınızı yazın.

   Örnek `.env`:
   ```
   DISCORD_TOKEN=MTIzNDU2Nzg5MDEyMzQ1Njc4.GaBcDe.FgHiJkLmNoPqRsTuVwXyZ
   ```

4. Botu çalıştırın:
   ```bash
   python bot.py
   ```
   **Windows’ta** `python` tanınmıyorsa: `py bot.py`

## Discord'da Botu Ayarlama

1. [Discord Developer Portal](https://discord.com/developers/applications) → **New Application** → İsim verin.
2. **Bot** sekmesinden **Add Bot** ile bot oluşturun.
3. **Reset Token** ile token alın ve `.env` dosyasına yapıştırın.
4. **OAuth2 → URL Generator**:
   - Scopes: `bot`
   - Bot Permissions: **Manage Channels**, **Manage Roles**
5. Oluşan linkle botu sunucunuza ekleyin. Botun rolü, değiştirilecek kanal/rollerden **yukarıda** olmalıdır.

## Kullanım

Komut:

```
!degistir <aranan_kelime> <yeni_kelime>
```

- **aranan_kelime:** Kanal/rol adında geçen ve değiştirilecek kısım.
- **yeni_kelime:** Yerine yazılacak kelime (birden fazla kelime yazabilirsiniz).

### Örnekler

- Tüm kanal ve rollerde "EskiSunucu" → "YeniSunucu":
  ```
  !degistir EskiSunucu YeniSunucu
  ```

- "2024" → "2025":
  ```
  !degistir 2024 2025
  ```

- Birden fazla kelime:
  ```
  !degistir Eski Isim Yeni Isim
  ```

Bot, sunucudaki **tüm kanalları** (metin, ses, kategoriler) ve **tüm rollerı** (bot rolü ve @everyone hariç) tarar; adında `aranan_kelime` geçenlerin adını `yeni_kelime` ile değiştirir.

## Gereken Yetkiler

- **Kanal Yönet** (Manage Channels)
- **Rol Yönet** (Manage Roles)

Komutu yalnızca bu yetkilere sahip kişiler kullanabilir.

## Notlar

- Token'ı kimseyle paylaşmayın; `.env` dosyasını Git'e eklemeyin.
- Botun sunucudaki rolü, değiştirmek istediğiniz kanalların ve rollerin üzerinde olmalıdır.

