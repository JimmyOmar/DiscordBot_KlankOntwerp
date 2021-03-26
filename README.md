#
# **Interactief Discord Klankwereld**

### Project Makerskills 2C

_Mick Broer &amp; Jimmy van der Heijden_

**Voorwoord**

In dit project zullen wij een poging doen tot het ontwerpen van een interactieve bot voor het instant messaging platform Discord. Voorheen was het plan om een bot te maken die in staat was om de stem van de gebruiker te kopiëren, maar na verdere tests zijn wij er achter gekomen dat dit toch niet haalbaar is voor ons (op dit moment).

Het programmeerwerk is gedaan in Python waarbij de bot wordt aangeroepen in Discord.

Je kan het eindresultaat hier bekijken: [https://youtu.be/KSu6qIBJ8QQ](https://youtu.be/KSu6qIBJ8QQ)


**MoSCoW**

Must: Discord Interactie via OSC.

Should: Synthese toepassen vanuit Discord.

Could: Bot stand-alone maken.

Would: Voice cloning.


**Discord functionaliteit**

Hieronder zullen wij het creeëren en functioneren van de bot binnen Discord uitleggen.

Daar komt bij kijken:
- Registreren
- Deelname aan een server
- Verbinding maken met Discord

Wat je nodig zult hebben:
- Python
- Text editor
- Discord account


**Discord package installeren**
Voordat we beginnen moeten de Discord package voor python installeren met het command:


#### Linux/macOS
python3 -m pip install -U discord.py


#### Windows
py -3 -m pip install -U discord.py


**Registreren**
Om te beginnen moeten we naar het Discord&#39;s Developer Portal. Voor toegang heb je een al bestaand Discord account nodig of moet je er één aanmaken.

[https://discord.com/developers/docs/intro](https://discord.com/developers/docs/intro)

Ga naar de application tab en maak een nieuwe applicatie aan.

![image1](https://user-images.githubusercontent.com/65659487/112617538-62f3a180-8e25-11eb-9662-37d027189fa1.png)

Voer een naam in en je zal gebracht worden naar de tab &#39;General information&#39;.

Top, we hebben nu een applicatie aangemaakt. Alleen wilt dat nog niet zeggen dat de bot ook al is aangemaakt.

Ga na het tabje &#39;Bot&#39; en klik op &#39;Add Bot&#39;.

![image2](https://user-images.githubusercontent.com/65659487/112617628-7e5eac80-8e25-11eb-93fa-0661cf28569c.png)

Zodra je hebt bevestigd dat je de bot aan je applicatie wilt toevoegen, zie je de nieuwe bot-gebruiker in het portaal.

De bot neemt vanzelf de naam aan die je aan de applicatie hebt gegeven. Dit kan je makkelijk veranderen door de username van de bot te veranderen.


**Deelname aan server**
Een bot kan geen uitnodigingen accepteren zoals een normale gebruiker dat wel kan. In plaats daarvan voeg je je bot toe met behulp van het OAuth2-protocol.

![image3](https://user-images.githubusercontent.com/65659487/112617659-87e81480-8e25-11eb-916f-9675c99f0597.png)

Ga naar de OAuth2 pagina. Op deze pagina zie je de OAuth2 URL generator.

Deze generator maakt een autorisatie-link aan voor het activeren en deactiveren van verschillende bot-functies.

In dit geval wil je de botgebruiker toegang verlenen tot Discord API&#39;s met behulp van de OAuth2-credentials. Om dit te doen scroll je naar beneden en selecteer je &#39;bot&#39; onder de &#39;SCOPES&#39; opties en &#39;Administrator&#39; onder de &#39;BOT PERMISSIONS&#39; opties.

![image4](https://user-images.githubusercontent.com/65659487/112617680-8f0f2280-8e25-11eb-9fb4-a0478005b831.png)

Nu heeft Discord de autorisatie-URL van je app gegenereerd met de geselecteerde machtigingen.

Selecteer &#39;Copy&#39; naast de URL die voor je is gegenereerd, plak deze in je browser en selecteer de server/guild waaraan je bot moet deelnemen.

Open de Discord applicatie en je zult zien dat de bot heeft deelgenomen aan je server.


**Verbinding maken met Discord**
Er zal in dit verslag niet te diep ingegaan worden op de programmeertaal Python zelf meer eerder op de geschreven functies: wat ze doen en hoe ze te gebruiken etc.

Nu dat de bot zich bevindt in de gewenste server moeten we de bot &#39;online&#39; krijgen. Met discord.py doe je dit door een instantie van Client in een text-editor te maken:

import discord

from discord.ext import commands

client = discord.Bot(command\_prefix - &#39;.&#39;)

@client.event async def on\_ready():

print(&#39;Bot is ready.&#39;&#39;)

client.run(TOKEN)

We hebben nog één ding nodig voordat we het bestand opslaan.

Je moet &#39;TOKEN&#39; vervangen door jouw bot-token. Die kan je krijgen door terug te gaan naar de Bot-pagina op de Developer Portal en op Copy te klikken onder de TOKEN-sectie.

Houd je token privé. Wanneer anderen toegang tot de token krijgen zullen zij de mogelijkheid hebben om andere scripts te koppelen aan je bot. Mocht dit gebeuren kan je een nieuwe maken door op Regenerate te klikken. Dit zal de oude token ongeldig maken.

![image5](https://user-images.githubusercontent.com/65659487/112617696-946c6d00-8e25-11eb-9548-2111fc01c638.png)
 
Nu heb je een Client aangemaakt en een on\_ready () event geïmplementeerd. Dit event zal een melding in de console-log geven wanneer de Client een verbinding tot stand heeft gebracht met Discord en het klaar is met het voorbereiden van de gegevens die Discord heeft verzonden, zoals inlogstatus, gilde en kanaal data en meer.

Sla de het tekstbestand op als &#39;bot.py&#39;. Open het bestand met Python of een ander programma waarmee je Python taal kunt draaien.

Open Discord, je zult zien dat de bot nu online is!


**Discord Bot interactie met externe programma&#39;s**
Voor de interactie met andere programma&#39;s gebruiken we Open Sound Control. Om met OSC te werken in Python, moet je eerst via pip een library installeren:

$ pip install python-osc

Bovenaan in ons bot.py bestand importeren we deze library:

from pythonosc import udp\_client

Vervolgens geven we deze client een aantal initialisatie waardes. Deze kunnen aangepast worden wanneer je bot.py aanroept in de terminal, door middel van &#39;--port&#39; of &#39;--ip&#39;.

parser = argparse.ArgumentParser()

parser.add\_argument(&quot;--ip&quot;, default=&quot;127.0.0.1&quot;,

help=&quot;The ip of the OSC server&quot;)

parser.add\_argument(&quot;--port&quot;, type=int, default=5005,

help=&quot;The port the OSC server is listening on&quot;)

args = parser.parse\_args()

client2 = udp\_client.SimpleUDPClient(args.ip, args.port)

Belangrijk is hier dat je de udp\_client een andere naam geeft dan de Discord client. Wij hebben gekozen voor &#39;client2&#39;.

Vervolgens moeten we een functie schrijven die commands uit Discord kan lezen en vervolgens een OSC message kan sturen naar de gewenste port:

@client.command()

async def rate(ctx, \*, oscMessage):

client2.send\_message(&quot;/rate&quot;, oscMessage)

await ctx.send(oscMessage)

Bij het bovenstaande voorbeeld zie je dat we eerst de Discord client laten weten dat we bezig zijn met een command. Vervolgens definiëren we de functie, we noemen hem in dit geval rate. We geven haar wat argumenten, en sturen het _&#39;oscMessage&#39;_ argument direct via OSC door naar port 5005 en dan specifiek naar &#39;/rate&#39;.

&#39;await&#39; stuurt diezelfde _&#39;oscMessage&#39;_ ook weer terug naar de gebruiker, zodat die enige feedback krijgt dat zijn opdracht aankomt. Vervolgens kun je de bot weer runnen:

python bot.py

Je kunt nu elk programma dat OSC kan ontvangen aansturen door middel van Discord commands. Wij hebben ervoor gekozen dit te doen in SuperCollider:

OSCdef(\rateOSC, {

arg msg, time, addr, port;

~def.set(\rate, msg[1].asFloat);

msg[1].postln;

}, &#39;/rate&#39;, recvPort:5005);

Veel plezier met OSC en Discord ;)


#### Bronnen:
Lucas (2020.) _Python: Making a Discord Bot (Rewrite / v1.x)_

Geraadpleegd van:

[https://youtube.com/playlist?list=PLW3GfRiBCHOhfVoiDZpSz8SM\_HybXRPzZ](https://youtube.com/playlist?list=PLW3GfRiBCHOhfVoiDZpSz8SM_HybXRPzZ)

Alex Ronquillo _How to Make a Discord Bot in Python_

Geraadpleegd:

[https://realpython.com/how-to-make-a-discord-bot-python/#creating-a-discord-account](https://realpython.com/how-to-make-a-discord-bot-python/#creating-a-discord-account)

Eli Fieldsteel _Week 10: OSC - MUS 499C Fall 2019 - Audio Coding with SuperCollider_

[https://youtu.be/R0ulauoGCvI](https://youtu.be/R0ulauoGCvI)

python-osc 1.7.4

[https://pypi.org/project/python-osc/](https://pypi.org/project/python-osc/)
