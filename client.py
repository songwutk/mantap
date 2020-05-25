from important import *
from module import *
from setup_args import *
from list_def import *

# Login Client
listAppType = ['DESKTOPWIN', 'DESKTOPMAC', 'IOSIPAD', 'CHROMEOS']
try:
    print ('Pesan Sistem : *Klien Masuk.')
    client = None
    if args.apptype:
        tokenPath = Path('authToken.txt')
        if tokenPath.exists():
            tokenFile = tokenPath.open('r')
        else:
            tokenFile = tokenPath.open('w+')
        savedAuthToken = tokenFile.read().strip()
        authToken = savedAuthToken if savedAuthToken and not args.token else args.token
        idOrToken = authToken if authToken else print("# Tidak ada token terbaca, silahkan scan qr dibawah.")
        try:
            client = LINE(idOrToken, appType=args.apptype, systemName=args.systemname, channelId=args.channelid, showQr=args.showqr)
            tokenFile.close()
            tokenFile = tokenPath.open('w+')
            tokenFile.write(client.authToken)
            tokenFile.close()
        except TalkException as talk_error:
            if args.traceback: traceback.print_tb(talk_error.__traceback__)
            sys.exit('(+) Error : %s' % talk_error.reason.replace('_', ' '))
        except Exception as error:
            if args.traceback: traceback.print_tb(error.__traceback__)
            sys.exit('(+) Error : %s' % str(error))
    else:
        for appType in listAppType:
            tokenPath = Path('authToken.txt')
            if tokenPath.exists():
                tokenFile = tokenPath.open('r')
            else:
                tokenFile = tokenPath.open('w+')
            savedAuthToken = tokenFile.read().strip()
            authToken = savedAuthToken if savedAuthToken and not args.token else args.token
            idOrToken = authToken if authToken else print("# Tidak ada token terbaca, silahkan scan qr dibawah.")
            try:
                client = LINE(idOrToken, appType=appType, systemName=args.systemname, channelId=args.channelid, showQr=args.showqr)
                tokenFile.close()
                tokenFile = tokenPath.open('w+')
                tokenFile.write(client.authToken)
                tokenFile.close()
                break
            except TalkException as talk_error:
                print ('(+) Error : %s' % talk_error.reason.replace('_', ' '))
                if args.traceback: traceback.print_tb(talk_error.__traceback__)
                if talk_error.code == 1:
                    continue
                sys.exit(1)
            except Exception as error:
                print ('(+) Error : %s' % str(error))
                if args.traceback: traceback.print_tb(error.__traceback__)
                sys.exit(1)
except Exception as error:
    print ('Pesan Sistem : Error : %s' % str(error))
    if args.traceback: traceback.print_tb(error.__traceback__)
    sys.exit(1)

if client:
    print ('\nPenting: Auth Token -> %s' % client.authToken)
    print ('Penting: Timeline Token -> %s' % client.tl.channelAccessToken)
    print ('\nPesan Sistem : *Berhasil Masuk.')
else:
    sys.exit('Pesan Sistem : *Gagal Masuk.')

myMid = client.profile.mid
admin = "uac8e3eaf1eb2a55770bf10c3b2357c33"
programStart = time.time()
oepoll = OEPoll(client)
tmp_text = []

settings = livejson.File('setting.json', True, False, 4)

bool_dict = {
    True: ['Yes', 'Aktif', 'Sukses', 'Open', 'On'],
    False: ['No', 'Tidak Aktif', 'Gagal', 'Close', 'Off']
}

#DEFFTEMPLATE
def sendTemplate(to, data):
    xyz = LiffChatContext(to)
    xyzz = LiffContext(chat=xyz)
    view = LiffViewRequest('1602687308-GXq4Vvk9', xyzz)
    token = client.liff.issueLiffView(view)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))

def helpmessage():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = ''
    helpMessage ="╭─「 Umum 」─── " + "\n" + \
                    "│ Prefix : " + key + "\n" + \
                    "│ " + key + "Me" + "\n" + \
                    "│ " + key + "Pembuat" + "\n" + \
                    "╰────────────" + "\n" + \
                    "╭─「 Media 」─" + "\n" + \
                    "│ " + key + "Antonim (kata)" + "\n" + \
                    "│ " + key + "Cat facts" + "\n" + \
                    "│ " + key + "Countryinfo (nama_negara)" + "\n" + \
                    "│ " + key + "Daily nasa" + "\n" + \
                    "│ " + key + "Harrypotter" + "\n" + \
                    "│ " + key + "Ipcheck (ip)" + "\n" + \
                    "│ " + key + "Kbbi (kata)" + "\n" + \
                    "│ " + key + "Meanslike (kata)" + "\n" + \
                    "│ " + key + "Number (nomor)" + "\n" + \
                    "│ " + key + "Random Date" + "\n" + \
                    "│ " + key + "Random Quote" + "\n" + \
                    "│ " + key + "Random Year" + "\n" + \
                    "│ " + key + "Superhero" + "\n" + \
                    "│ " + key + "Surah (nomor)" + "\n" + \
                    "│ " + key + "Twitter (username)" + "\n" + \
                    "│ " + key + "Urbandict (kata)" + "\n" + \
                    "│ " + key + "Wikipedia" + "\n" + \
                    "╰────────────"
    return helpMessage

def executeCmd(msg, text, txt, cmd, msg_id, receiver, sender, to, setKey):

    # // Bot Logouted His Device
    if cmd == '@logout device':
      client.sendReplyMessage(msg_id, to, '* Program di-berhentikan.')
      sys.exit('##----- PROGRAM STOPPED -----##')

    # // Bot Send His Creator Contact
    if cmd == "pembuat":
        client.sendContact(to,"uac8e3eaf1eb2a55770bf10c3b2357c33")

    # // Checking Speed of Bot Send an Message
    elif cmd == 'speed':
        start = time.time()
        client.sendReplyMessage(msg_id, to, 'Mengautentikasi...')
        elapse = time.time() - start
        client.sendReplyMessage(msg_id, to, 'Kecepatan Mengirim Pesan %s Detik' % str(elapse))
    
    # // Runtime when Program Started
    elif cmd == "runtime":
        timeNow = time.time()
        runtime = timeNow - programStart
        runtime = timeChange(runtime)
        client.sendReplyMessage(msg_id, to, "Bot telah bekerja selama {}".format(str(runtime)))

    # // Restart the Program
    elif cmd == 'relogin':
        client.sendReplyMessage(msg_id, to, 'Berhasil Mengulangi Program!')
        settings['restartPoint'] = to
        restartProgram()
    
    # // Bot Send His Menu
    if cmd == "menu":
            helpMessage = helpmessage()
            mids = "uac8e3eaf1eb2a55770bf10c3b2357c33"
            mantap={
                'type': 'text',
                'text': '{}'.format(str(helpMessage)),
                'sentBy': {
                    'label': 'Reighpuy',
                    'iconUrl' : "https://pbs.twimg.com/profile_images/1164752786992484354/PyFcqmzG_400x400.jpg",
                    'linkUrl' : 'https://line.me/ti/p/~yapuy'
                }
            }
            sendTemplate(to, mantap)

    # // Bot Send Profile Of Sender
    if cmd == "me":
        paramz = client.getContact(sender)
        isi = "╭───「 Profile Info 」"
        isi += "\n│"
        isi += "\n│ • y'mid : " + paramz.mid
        isi += "\n│ • y'name : " + paramz.displayName
        isi += "\n│ • y'bio : " + paramz.statusMessage
        isi += "\n│"
        isi += "\n╰────────────"
        client.sendReplyMessage(msg_id,to, isi)

                   # // MEDIA STARTING // #

    # KBBI
    elif cmd.startswith("kbbi "):
      try:
        judul = removeCmd(text)
        data = KBBI(judul)
        hasil = "╭──[ KBBI ]"
        hasil += "\n├ Judul : " +str(judul)
        hasil += "\n╰──────────"
        hasil += '\n\n-> Hasil : \n'+str(data.__str__(contoh=False))
        client.sendReplyMessage(msg_id, to, str(hasil))
      except Exception as error:
          client.sendReplyMessage(msg_id, to, "#Perintah Gagal, kata {} Tidak ditemukan".format(judul))
          logError(error)

    # MEANS LIKE
    elif cmd.startswith("meanslike "):
      try:
         proses = msg.text.split(" ")
         urutan = msg.text.replace(proses[0] + " ","")
         r = requests.get("https://api.datamuse.com/words?ml={}".format(str(urutan)))
         data = r.text
         data = json.loads(data)
         ret_ = "1) : {}".format(str(data[0]["word"]))
         ret_ += "\n2) : {}".format(str(data[1]["word"]))
         ret_ += "\n3) : {}".format(str(data[2]["word"]))
         ret_ += "\n4) : {}".format(str(data[3]["word"]))
         ret_ += "\n5) : {}".format(str(data[4]["word"]))
         client.sendReplyMessage(msg_id, to, str(ret_))
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : {} Tidak ditemukan.".format(urutan))

    # WIKIPEDIA
    elif cmd.startswith('wikipedia'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        res = '╭───「 Wikipedia 」'
        res += '\n├'
        res += '\n├ Language : ID'
        res += '\n├ Usage : '
        res += '\n│ • {key}Wikipedia Summary (query)'
        res += '\n│ • {key}Wikipedia Article (countrycode)'
        res += '\n│ • {key}Wikipedia Medialist (query)'
        res += '\n│ • {key}Wikipedia Related (query)'
        res += '\n│ • {key}Wikipedia Randomsum'
        res += '\n├'
        res += '\n╰───「 Reighpuy @HelloWorld 」'
        if cmd == 'wikipedia':
            client.sendReplyMessage(msg_id, to, parsingRes(res).format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('article '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get("https://id.wikipedia.org/api/rest_v1/data/recommendation/article/creation/translation/{}".format(str(texts)))
            data = req.text
            data = json.loads(data)
            isi = "╭───[ Wikipedia Lang Article ]"
            isi += "\n├"
            isi += "\n├ 1) {}".format(str(data["items"][0]["title"]))
            isi += "\n├ 2) {}".format(str(data["items"][1]["title"]))
            isi += "\n├ 3) {}".format(str(data["items"][2]["title"]))
            isi += "\n├ 4) {}".format(str(data["items"][3]["title"]))
            isi += "\n├ 5) {}".format(str(data["items"][4]["title"]))
            isi += "\n├ 6) {}".format(str(data["items"][5]["title"]))
            isi += "\n├ 7) {}".format(str(data["items"][6]["title"]))
            isi += "\n├ 8) {}".format(str(data["items"][7]["title"]))
            isi += "\n├ 9) {}".format(str(data["items"][8]["title"]))
            isi += "\n├ 10) {}".format(str(data["items"][9]["title"]))
            isi += "\n├ 11) {}".format(str(data["items"][10]["title"]))
            isi += "\n├ 12) {}".format(str(data["items"][11]["title"]))
            isi += "\n├ 13) {}".format(str(data["items"][12]["title"]))
            isi += "\n├ 14) {}".format(str(data["items"][13]["title"]))
            isi += "\n├ 15) {}".format(str(data["items"][14]["title"]))
            isi += "\n├ 16) {}".format(str(data["items"][15]["title"]))
            isi += "\n├ 17) {}".format(str(data["items"][16]["title"]))
            isi += "\n├ 18) {}".format(str(data["items"][17]["title"]))
            isi += "\n├ 19) {}".format(str(data["items"][18]["title"]))
            isi += "\n├ 20) {}".format(str(data["items"][19]["title"]))
            isi += "\n├ 21) {}".format(str(data["items"][20]["title"]))
            isi += "\n├ 22) {}".format(str(data["items"][21]["title"]))
            isi += "\n├ 23) {}".format(str(data["items"][22]["title"]))
            isi += "\n├ 24) {}".format(str(data["items"][23]["title"]))
            isi += "\n├"
            isi += "\n╰───[ Ended ]"
            client.sendReplyMessage(msg_id, to, isi)
          except:client.sendReplyMessage(msg_id, to, "# Perintah Gagal, Kode negara {} Tidak ditemukan.".format(texts))
        elif texttl.startswith('summary '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get("https://id.wikipedia.org/api/rest_v1/page/summary/{}?redirect=false".format(str(texts)))
            data = req.text
            data = json.loads(data)
            isi = "╭───[ Wikipedia Summary ]"
            isi += "\n├"
            isi += "\n├ Title : {}".format(str(data["title"]))
            isi += "\n├ Wikibas_item : {}".format(str(data["wikibase_item"]))
            isi += "\n├ Lang : {}".format(str(data["lang"]))
            isi += "\n├ Description : {}".format(str(data["description"]))
            isi += "\n├"
            isi += "\n╰───[ Ended ]"
            isi += "\n├ Full Desc : {}".format(str(data["extract"]))
            client.sendReplyMessage(msg_id, to, isi)
          except:client.sendReplyMessage(msg_id, to, "# Perintah Gagal, {} Tidak ditemukan.".format(texts))
        elif texttl.startswith('medialist '):
          try:
            texts = textt[10:]
            textsl = texts.lower()
            req = requests.get("https://id.wikipedia.org/api/rest_v1/page/media-list/{}?redirect=false".format(str(texts)))
            data = req.text
            data = json.loads(data)
            isi = "╭───[ Wikipedia Medialist ]"
            isi += "\n├"
            isi += "\n├ Type : {}".format(str(data["items"][0]["type"]))
            isi += "\n├ Title : {}".format(str(data["items"][0]["title"]))
            isi += "\n├ Caption : {}".format(str(data["items"][0]["caption"]["text"]))
            isi += "\n├"
            isi += "\n╰───[ Ended ]"
            client.sendReplyMessage(msg_id, to, isi)
          except:client.sendReplyMessage(msg_id, to, "# Perintah Gagal, {} Tidak ditemukan.".format(texts))
        elif texttl.startswith('related '):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get("https://id.wikipedia.org/api/rest_v1/page/related/{}".format(str(texts)))
            data = req.text
            data = json.loads(data)
            isi = "╭───[ Wikipedia Related ]"
            isi += "\n├"
            isi += "\n├ 1) {}".format(str(data["pages"][0]["title"]))
            isi += "\n├ 2) {}".format(str(data["pages"][1]["title"]))
            isi += "\n├ 3) {}".format(str(data["pages"][2]["title"]))
            isi += "\n├ 4) {}".format(str(data["pages"][3]["title"]))
            isi += "\n├ 5) {}".format(str(data["pages"][4]["title"]))
            isi += "\n├"
            isi += "\n╰───[ Ended ]"
            client.sendReplyMessage(msg_id, to, isi)
          except:client.sendReplyMessage(msg_id, to, "# Perintah Gagal, {} Tidak ditemukan.".format(texts))
        elif texttl.startswith('randomsum'):
          try:
            req = requests.get("https://id.wikipedia.org/api/rest_v1/page/random/summary")
            data = req.text
            data = json.loads(data)
            isi = "╭───[ Wikipedia Random Summary ]"
            isi += "\n├"
            isi += "\n├ Title : {}".format(str(data["title"]))
            isi += "\n├ Wikibase_item : {}".format(str(data["wikibase_item"]))
            isi += "\n├ PageId : {}".format(str(data["pageid"]))
            isi += "\n├ Language : {}".format(str(data["lang"]))
            isi += "\n├ Description : {}".format(str(data["description"]))
            isi += "\n├"
            isi += "\n╰───[ Ended ]"
            isi += "\nFull Desc : {}".format(str(data["extract"]))
            client.sendReplyMessage(msg_id, to, isi)
          except:client.sendReplyMessage(msg_id, to, "# Perintah Gagal.".format(texts))

    # HARRYPOTTER
    elif cmd.startswith('harrypotter'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        res = '╭───「 Harrypotter 」'
        res += '\n├'
        res += '\n├ Usage : '
        res += '\n│ • {key}Harrypotter Profile (name)'
        res += '\n│ • {key}Harrypotter Charlist'
        res += '\n├'
        res += '\n╰───「 Ended 」'
        if cmd == 'harrypotter':
            client.sendReplyMessage(msg_id, to, parsingRes(res).format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith("profile "):
          try:
            texts = textt[8:]
            textsl = texts.lower()
            req = requests.get("https://www.potterapi.com/v1/characters/?key=$2a$10$cO8xUVqBD2LPqRb6sF.Z1uGpDQ0Xv.L.quEnQh6USoxdyjP7v7g/e&name={}".format(str(texts)))
            data = req.text
            data = json.loads(data)
            isi = "╭──「 HarryPotter - Character 」"
            isi += "\n├ "
            isi += "\n├ Name : {}".format(str(data[0]["name"]))
            isi += "\n├ ID : {}".format(str(data[0]["_id"]))
            isi += "\n├ House : {}".format(str(data[0]["house"]))
            isi += "\n├ School : {}".format(str(data[0]["school"]))
            isi += "\n├ Blood Status : {}".format(str(data[0]["bloodStatus"]))
            isi += "\n├ Species : {}".format(str(data[0]["species"]))
            isi += "\n├"
            isi += "\n╰───「 Ended 」"
            mantap={
                'type': 'text',
                'text': '{}'.format(str(isi)),
                'sentBy': {
                    'label': 'Harry Potter Characters',
                    'iconUrl' : "https://2.bp.blogspot.com/-DlE53qq9NtA/VlKJORbZbfI/AAAAAAAAFl8/1Ypt2CW4iRQ/s1600/Harry%2BPotter%2Band%2Bsorcerer%2527s%2Bstone.jpg",
                    'linkUrl' : 'http://line.me/ti/p/~yapuy'
                }
            }
            sendTemplate(to, mantap)
          except:client.sendReplyMessage(msg_id,to, "Nama {} Tidak ditemukan.".format(str(texts)))
        elif texttl.startswith("charlist"):
            client.sendReplyMessage(msg_id,to, "https://github.com/reighpuy/harry_potter_api/blob/master/characters.txt")
    # SUPERHERO
    elif cmd.startswith('superhero'):
      try:
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        param1 = sender
        client.findAndAddContactsByMid(param1)
        res = '╭───「 Superhero 」'
        res += '\n├'
        res += '\n├ Max Number of Hero : 731'
        res += '\n├ Usage : '
        res += '\n│ • {key}Superhero List'
        res += '\n│ • {key}Superhero Search (name)'
        res += '\n│ • {key}Superhero Num (no)'
        res += '\n│ • {key}Superhero Powerstats (no)'
        res += '\n│ • {key}Superhero Bio (no)'
        res += '\n│ • {key}Superhero Appearance (no)'
        res += '\n│ • {key}Superhero Work (no)'
        res += '\n│ • {key}Superhero Connections (no)'
        res += '\n│ • {key}Superhero Image (no)'
        res += '\n├'
        res += '\n╰───「 Reighpuy @HelloWorld 」'
        if cmd == 'superhero':
            client.sendReplyMessage(msg_id, to, parsingRes(res).format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('list'):
            client.sendReplyMessage(msg_id,to, "https://github.com/reighpuy/super_hero/blob/master/daftar_super_hero")
        elif texttl.startswith('num '):
            texts = textt[4:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/259395488445252/{}".format(texts))
            data = r.text
            data = json.loads(data)
            client.sendReplyMessage(msg_id, to, data["name"])
        elif texttl.startswith('powerstats '):
            texts = textt[11:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/259395488445252/{}/powerstats".format(texts))
            data = r.text
            data = json.loads(data)
            isi = "ID : {}".format(str(data["id"]))
            isi += "\nName : {}".format(str(data["name"]))
            isi += "\nIntelligence : {}".format(str(data["intelligence"]))
            isi += "\nStrength : {}".format(str(data["strength"]))
            isi += "\nSpeed : {}".format(str(data["speed"]))
            isi += "\nDurability : {}".format(str(data["durability"]))
            isi += "\nPower : {}".format(str(data["power"]))
            isi += "\nCombat : {}".format(str(data["combat"]))
            client.sendReplyMessage(msg_id, to, isi)
        elif texttl.startswith('bio '):
            texts = textt[4:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/259395488445252/{}/biography".format(texts))
            data = r.text
            data = json.loads(data)
            isi = "ID : {}".format(str(data["id"]))
            isi += "\nName : {}".format(str(data["name"]))
            isi += "\nFull name : {}".format(str(data["full-name"]))
            isi += "\nAlter egos : {}".format(str(data["alter-egos"]))
            isi += "\nPlace of birth : {}".format(str(data["place-of-birth"]))
            isi += "\nFirst appearance : {}".format(str(data["first-appearance"]))
            isi += "\nPublisher : {}".format(str(data["publisher"]))
            isi += "\nAlignment : {}".format(str(data["alignment"]))
            client.sendReplyMessage(msg_id, to, isi)
        elif texttl.startswith('appearance '):
            texts = textt[11:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/259395488445252/{}/appearance".format(texts))
            data = r.text
            data = json.loads(data)
            isi = "ID : {}".format(str(data["id"]))
            isi += "\nName : {}".format(str(data["name"]))
            isi += "\nGender : {}".format(str(data["gender"]))
            isi += "\nRace : {}".format(str(data["race"]))
            isi += "\nHeight : {}".format(str(data["height"][1]))
            isi += "\nWeight : {}".format(str(data["weight"][1]))
            isi += "\nEye-color : {}".format(str(data["eye-color"]))
            isi += "\nHair-color : {}".format(str(data["hair-color"]))
            client.sendReplyMessage(msg_id, to, isi)
        elif texttl.startswith('work '):
            texts = textt[5:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/259395488445252/{}/work".format(texts))
            data = r.text
            data = json.loads(data)
            isi = "ID : {}".format(str(data["id"]))
            isi += "\nName : {}".format(str(data["name"]))
            isi += "\nOccupation : {}".format(str(data["occupation"]))
            isi += "\nBase : {}".format(str(data["base"]))
            client.sendReplyMessage(msg_id, to, isi)
        elif texttl.startswith('connections '):
            texts = textt[12:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/259395488445252/{}/connections".format(texts))
            data = r.text
            data = json.loads(data)
            isi = "ID : {}".format(str(data["id"]))
            isi += "\nName : {}".format(str(data["name"]))
            isi += "\nGroup affiliation : {}".format(str(data["group-affiliation"]))
            isi += "\nRelatives : {}".format(str(data["relatives"]))
            client.sendReplyMessage(msg_id, to, isi)
        elif texttl.startswith('image '):
            texts = textt[6:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/259395488445252/{}/image".format(texts))
            data = r.text
            data = json.loads(data)
            client.sendImageWithURL(to, data["url"])
        elif texttl.startswith("search "):
            texts = textt[7:]
            textsl = texts.lower()
            r = requests.get("https://www.superheroapi.com/api.php/259395488445252/search/{}".format(texts))
            data = r.text
            data = json.loads(data)
            isi = "╭───[ Superhero Info ]"
            isi += "\n├"
            isi += "\n├ Nama : {}".format(data["results-for"])
            isi += "\n├ ID : {}".format(data["results"][0]["id"])
            isi += "\n├"
            isi += "\n├ -> Power stats : "
            isi += "\n├ Intelligence : {}".format(data["results"][0]["powerstats"]["intelligence"])
            isi += "\n├ Strength : {}".format(data["results"][0]["powerstats"]["strength"])
            isi += "\n├ Speed : {}".format(data["results"][0]["powerstats"]["speed"])
            isi += "\n├ Durability : {}".format(data["results"][0]["powerstats"]["durability"])
            isi += "\n├ Power : {}".format(data["results"][0]["powerstats"]["power"])
            isi += "\n├ Combat : {}".format(data["results"][0]["powerstats"]["combat"])
            isi += "\n├"
            isi += "\n├ -> Biography : "
            isi += "\n├ Full Name : {}".format(data["results"][0]["biography"]["full-name"])
            isi += "\n├ Alter egos : {}".format(data["results"][0]["biography"]["alter-egos"])
            isi += "\n├ Place of-birth : {}".format(data["results"][0]["biography"]["place-of-birth"])
            isi += "\n├ First appearance : {}".format(data["results"][0]["biography"]["first-appearance"])
            isi += "\n├ Publisher : {}".format(data["results"][0]["biography"]["publisher"])
            isi += "\n├ Alignment : {}".format(data["results"][0]["biography"]["alignment"])
            isi += "\n├"
            isi += "\n├ -> Appearance : "
            isi += "\n├ Gender : {}".format(data["results"][0]["appearance"]["gender"])
            isi += "\n├ Race : {}".format(data["results"][0]["appearance"]["race"])
            isi += "\n├ Height : {}".format(data["results"][0]["appearance"]["height"][1])
            isi += "\n├ Weight : {}".format(data["results"][0]["appearance"]["weight"][1])
            isi += "\n├ Eye color : {}".format(data["results"][0]["appearance"]["eye-color"])
            isi += "\n├ Hair color : {}".format(data["results"][0]["appearance"]["hair-color"])
            isi += "\n├"
            isi += "\n├ -> Work : "
            isi += "\n├ Occupation : {}".format(data["results"][0]["work"]["occupation"])
            isi += "\n├ Base : {}".format(data["results"][0]["work"]["base"])
            isi += "\n├"
            isi += "\n├ -> Connections : "
            isi += "\n├ Group affiliation : {}".format(data["results"][0]["connections"]["group-affiliation"])
            isi += "\n├"
            isi += "\n╰───[ Reighpuy @HelloWorld ]"
            client.sendReplyMessage(msg_id,to, isi)
      except:client.sendReplyMessage(msg_id,to, "# Gagal memuat perintah, Superehero {} Tidak ditemukan.".format(texts))

    # get Country
    elif cmd.startswith("countryinfo "):
      try:
            proses = msg.text.split(" ")
            urutan = msg.text.replace(proses[0] + " ","")
            r = requests.get("http://countryapi.gear.host/v1/Country/getCountries?pName={}".format(str(urutan)))
            data = r.text
            data = json.loads(data)
            isi = "Name : {}".format(str(data["Response"][0]["Name"]))
            isi += "\nAlpha 2 Code : {}".format(str(data["Response"][0]["Alpha2Code"]))
            isi += "\nAlpha 3 Code : {}".format(str(data["Response"][0]["Alpha3Code"]))
            isi += "\nNative Name : {}".format(str(data["Response"][0]["NativeName"]))
            isi += "\nRegion : {}".format(str(data["Response"][0]["Region"]))
            isi += "\nSub Region : {}".format(str(data["Response"][0]["SubRegion"]))
            mantap={
                'type': 'text',
                'text': '{}'.format(str(isi)),
                'sentBy': {
                    'label': '{}'.format(str(data["Response"][0]["Name"])),
                    'iconUrl' : "{}".format(str(data["Response"][0]["FlagPng"])),
                    'linkUrl' : 'https://line.me/ti/p/~yapuy'
                }
            }
            sendTemplate(to, mantap)
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : {} Tidak ditemukan.".format(urutan))

    # Urban dict
    elif cmd.startswith("urbandict "):
      try:
          proses = msg.text.split(" ")
          urutan = msg.text.replace(proses[0] + " ","")
          r = requests.get("http://urbanscraper.herokuapp.com/search/{}".format(str(urutan)))
          data = r.text
          data = json.loads(data)
          ret_ = "Term : {}".format(str(data[0]["term"]))
          ret_ += "\nDefinisi : {}".format(str(data[0]["definition"]))
          ret_ += "\nContoh : {}".format(str(data[0]["example"]))
          ret_ += "\nAlamat : {}".format(str(data[0]["url"]))
          client.sendReplyMessage(msg_id,to, ret_)
      except:
          client.sendReplyMessage(msg_id, to,"#Perintah Gagal : {} Tidak ditemukan.".format(urutan))

    # ANTONYM
    elif cmd.startswith("antonim "):
      try:
            proses = msg.text.split(" ")
            urutan = msg.text.replace(proses[0] + " ","")
            r = requests.get("https://api.datamuse.com/words?rel_ant={}".format(str(urutan)))
            data = r.text
            data = json.loads(data)
            ret_ = "[ Antonim dari kata : {} ]".format(urutan)
            ret_ += "\n\n- {}".format(str(data[0]["word"]))
            client.sendReplyMessage(msg_id, to, str(ret_))
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : {} Tidak ditemukan.".format(urutan))

    # SURAH AL'QURAN
    elif cmd.startswith("surah "):
      try:
        proses = msg.text.split(" ")
        urutan = msg.text.replace(proses[0] + " ","")
        r = requests.get("https://api.banghasan.com/quran/format/json/surat/{}".format(str(urutan)))
        data = r.text
        data = json.loads(data)
        ret_ = "╭──[ Info Surah ]"
        ret_ += "\n├\n├ Nomor Surah : {}".format(str(data["hasil"][0]["nomor"]))
        ret_ += "\n├ Nama Surah : {}".format(str(data["hasil"][0]["nama"]))
        ret_ += "\n├ Arti Surah : {}".format(str(data["hasil"][0]["arti"]))
        ret_ += "\n├ Asma : {}".format(str(data["hasil"][0]["asma"]))
        ret_ += "\n├ Start : {}".format(str(data["hasil"][0]["start"]))
        ret_ += "\n├ Ayat : {}".format(str(data["hasil"][0]["ayat"]))
        ret_ += "\n├ Tipe : {}".format(str(data["hasil"][0]["type"]))
        ret_ += "\n├ Urut : {}".format(str(data["hasil"][0]["urut"]))
        ret_ += "\n├ Rukuk : {}".format(str(data["hasil"][0]["rukuk"]))
        ret_ += "\n├\n╰──[ Reighpuy @HelloWorld ]"
        ret_ += "\n\nKeterangan : \n{}".format(str(data["hasil"][0]["keterangan"]))
        client.sendReplyMessage(msg_id, to, str(ret_))
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : {} Tidak ditemukan.".format(urutan))

    # RANDOM NASA
    elif cmd == 'daily nasa':
        r = requests.get("https://api.nasa.gov/planetary/apod?api_key=plx64zHKoYUg03rYVT8FqmJrwy3xcKsUaW7GsfHr")
        data = r.text
        data = json.loads(data)
        isi = "╭──[ NASA ]"
        isi += "\n├\n├ Judul : {}".format(str(data["title"]))
        isi += "\n├ Media Tipe : {}".format(str(data["media_type"]))
        isi += "\n├ Tanggal : {}".format(str(data["date"]))
        isi += "\n├ Penjelasan : {}".format(str(data["explanation"]))
        isi += "\n├\n╰──[ Reighpuy @HelloWorld ]"
        mantap={
            'type': 'text',
            'text': '{}'.format(str(isi)),
            'sentBy': {
                'label': 'NASA',
                'iconUrl' : "{}".format(str(data["url"])),
                'linkUrl' : '{}'.format(str(data["hdurl"]))
            }
        }
        sendTemplate(to, mantap)

    # IP CHECK
    elif cmd.startswith("ipcheck "):
      try:
         proses = msg.text.split(" ")
         urutan = msg.text.replace(proses[0] + " ","")
         r = requests.get("http://apitrojans.herokuapp.com/checkip?ip={}".format(str(urutan)))
         data = r.text
         data = json.loads(data)
         ret_ = "╭──[ Ip Check ]"
         ret_ += "\n├ IP : {}".format(str(data["result"]["ip"]))
         ret_ += "\n├ Desimal : {}".format(str(data["result"]["decimal"]))
         ret_ += "\n├ Hostname : {}".format(str(data["result"]["hostname"]))
         ret_ += "\n├ ASN : {}".format(str(data["result"]["asn"]))
         ret_ += "\n├ ISP : {}".format(str(data["result"]["isp"]))
         ret_ += "\n├ Organisasi : {}".format(str(data["result"]["organization"]))
         ret_ += "\n├ Tipe : {}".format(str(data["result"]["type"]))
         ret_ += "\n├ Benua : {}".format(str(data["result"]["continent"]))
         ret_ += "\n├ Negara : {}".format(str(data["result"]["country"]))
         ret_ += "\n├ Wilayah : {}".format(str(data["result"]["region"]))
         ret_ += "\n├ Kota : {}".format(str(data["result"]["city"]))
         ret_ += "\n╰──[ Reighpuy @HelloWorld ]"
         client.sendReplyMessage(msg_id, to, str(ret_))
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : {} Tidak ditemukan.".format(urutan))

    elif cmd.startswith("random quote"):
        r = requests.get("http://apitrojans.herokuapp.com/quotes")
        data = r.text
        data = json.loads(data)
        client.sendReplyMessage(msg_id,to, data["result"]["quotes"])

    # TWITTER
    elif cmd.startswith("twitter "):
      try:
         proses = msg.text.split(" ")
         urutan = msg.text.replace(proses[0] + " ","")
         r = requests.get("http://apitrojans.herokuapp.com/twitter?user={}".format(str(urutan)))
         data = r.text
         data = json.loads(data)
         ret_ = "╭──[ Twitter - User Info ]"
         ret_ += "\n├ Nama : {}".format(str(data["result"]["nama"]))
         ret_ += "\n├ Id : {}".format(str(data["result"]["id"]))
         ret_ += "\n├ Tweet : {}".format(str(data["result"]["tweet"]))
         ret_ += "\n├ Mengikuti : {}".format(str(data["result"]["following"]))
         ret_ += "\n├ Pengikut : {}".format(str(data["result"]["followers"]))
         ret_ += "\n├ Bio : {}".format(str(data["result"]["bio"]))
         ret_ += "\n├ Avatar : {}".format(str(data["result"]["picture"]))
         ret_ += "\n╰──[ Reighpuy @HelloWorld ]"
         client.sendReplyMessage(msg_id, to, str(ret_))
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : {} Tidak ditemukan.".format(urutan))

    # CAT FACTS
    elif cmd == 'cat facts':
        r = requests.get("https://cat-fact.herokuapp.com/facts")
        data = r.text
        data = json.loads(data)
        yup = data["all"]
        random_index = randint(0, len(yup)-1)
        yup2 = yup[random_index]['text']
        client.sendReplyMessage(msg_id, to, yup2)

    # Random Number Story
    elif cmd.startswith("number "):
      try:
         proses = msg.text.split(" ")
         urutan = msg.text.replace(proses[0] + " ","")
         r = requests.get("http://numbersapi.com/{}?json".format(str(urutan)))
         data = r.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id, to, data["text"])
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : Anda Bau!")
    # RANDOM DATE
    elif cmd == 'random date':
      try:
         r = requests.get("http://numbersapi.com/random/date?json")
         data = r.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id,to, data["text"])
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : Anda Bau!")
    # RANDOM YEARS
    elif cmd == 'random year':
      try:
         r = requests.get("http://numbersapi.com/random/year?json")
         data = r.text
         data = json.loads(data)
         client.sendReplyMessage(msg_id,to, data["text"])
      except:client.sendReplyMessage(msg_id, to,"#Perintah Gagal : Anda Bau!")

                   # // MEDIA ENDED // #

    # // SETTINGS // #
    elif cmd.startswith('error'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        cond = textt.split(' ')
        res = '╭───「 Error 」'
        res += '\n│ Usage : '
        res += '\n│ • {key}Error'
        res += '\n│ • {key}Error Logs'
        res += '\n│ • {key}Error Reset'
        res += '\n│ • {key}Error Detail <errid>'
        res += '\n╰───────────'
        if cmd == 'error':
            client.sendReplyMessage(msg_id, to, parsingRes(res).format_map(SafeDict(key=setKey.title())))
        elif cond[0].lower() == 'logs':
            try:
                filee = open('errorLog.txt', 'r')
            except FileNotFoundError:
                return client.sendReplyMessage(msg_id, to, 'Tidak ditemukan Error.')
            errors = [err.strip() for err in filee.readlines()]
            filee.close()
            if not errors: return client.sendReplyMessage(msg_id, to, 'Tidak ditemukan Error.')
            res = '╭───「 Error Logs 」'
            res += '\n├ List :'
            parsed_len = len(errors)//200+1
            no = 0
            for point in range(parsed_len):
                for error in errors[point*200:(point+1)*200]:
                    if not error: continue
                    no += 1
                    res += '\n│ %i. %s' % (no, error)
                    if error == errors[-1]:
                        res += '\n╰──────────'
                if res:
                    if res.startswith('\n'): res = res[1:]
                    client.sendReplyMessage(msg_id, to, res)
                res = ''
        elif cond[0].lower() == 'reset':
            filee = open('errorLog.txt', 'w')
            filee.write('')
            filee.close()
            shutil.rmtree('tmp/errors/', ignore_errors=True)
            os.system('mkdir tmp/errors')
            client.sendReplyMessage(msg_id, to, 'Success reset error logs')
        elif cond[0].lower() == 'detail':
            if len(cond) < 2:
                return client.sendReplyMessage(msg_id, to, parsingRes(res).format_map(SafeDict(key=setKey.title())))
            errid = cond[1]
            if os.path.exists('tmp/errors/%s.txt' % errid):
                with open('tmp/errors/%s.txt' % errid, 'r') as f:
                    client.sendReplyMessage(msg_id, to, f.read())
            else:
                return client.sendReplyMessage(msg_id, to, 'Failed display details error, errorid not valid')
        else:
            client.sendReplyMessage(msg_id, to, parsingRes(res).format_map(SafeDict(key=setKey.title())))

    elif txt.startswith('setkey'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        res = '╭───「 Setting Key 」'
        res += '\n│ Status : ' + bool_dict[settings['setKey']['status']][1]
        res += '\n│ Key : ' + settings['setKey']['key'].title()
        res += '\n│ Usage : '
        res += '\n│ • Setkey'
        res += '\n│ • Setkey <on/off>'
        res += '\n│ • Setkey <key>'
        res += '\n╰──────────'
        if txt == 'setkey':
            client.sendReplyMessage(msg_id, to, parsingRes(res))
        elif texttl == 'on':
            if settings['setKey']['status']:
                client.sendReplyMessage(msg_id, to, 'Gagal mengaktifkan setkey, setkey sudah aktif')
            else:
                settings['setKey']['status'] = True
                client.sendReplyMessage(msg_id, to, 'Berhasil mengaktifkan Setkey.')
        elif texttl == 'off':
            if not settings['setKey']['status']:
                client.sendReplyMessage(msg_id, to, 'Gagal menonaktifkan setkey, setkey sudah dinonaktifkan')
            else:
                settings['setKey']['status'] = False
                client.sendReplyMessage(msg_id, to, 'Berhasil menonaktifkan Setkey.')
        else:
            settings['setKey']['key'] = texttl
            client.sendReplyMessage(msg_id, to, 'Sukses ubah set kunci ke (%s)' % textt)

def executeOp(op):
    try:
        #print ('Program Operasi : ( %i ) %s' % (op.type, OpType._VALUES_TO_NAMES[op.type].replace('_', ' ')))
        if op.type == 13:
            if settings['autoJoin']['status'] and myMid in op.param3:
                client.acceptGroupInvitation(op.param1)
                if settings['autoJoin']['reply']:
                    if '@!' not in settings['autoJoin']['message']:
                        client.sendMessage(op.param1, settings['autoJoin']['message'])
                    else:
                        client.sendMentionV2(op.param1, settings['autoJoin']['message'], [op.param2])
        if op.type == 26 or op.type == 25:
            msg      = op.message
            text     = str(msg.text)
            msg_id   = msg.id
            receiver = msg.to
            sender   = msg._from
            to       = sender if not msg.toType and sender != myMid else receiver
            txt      = text.lower()
            cmd      = command(text)
            setKey   = settings['setKey']['key'] if settings['setKey']['status'] else ''
            if text in tmp_text:
                return tmp_text.remove(text)
            if msg.contentType == 0: # Content type is text
                if '/ti/g/' in text and settings['autoJoin']['ticket']:
                    regex = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                    links = regex.findall(text)
                    tickets = []
                    gids = client.getGroupIdsJoined()
                    for link in links:
                        if link not in tickets:
                            tickets.append(link)
                    for ticket in tickets:
                        try:
                            group = client.findGroupByTicket(ticket)
                        except:
                            continue
                        if group.id in gids:
                            client.sendReplyMessage(msg_id, to, 'Sudah di Grup ' + group.name)
                            continue
                        client.acceptGroupInvitationByTicket(group.id, ticket)
                        if settings['autoJoin']['reply']:
                            if '@!' not in settings['autoJoin']['message']:
                                client.sendReplyMessage(msg_id, to, settings['autoJoin']['message'])
                            else:
                                client.sendMentionV2(to, settings['autoJoin']['message'], [sender])
                        client.sendReplyMessage(msg_id, to, 'Sukses Gabung Grup ' + group.name)
                try:
                    executeCmd(msg, text, txt, cmd, msg_id, receiver, sender, to, setKey)
                except TalkException as talk_error:
                    logError(talk_error)
                    if talk_error.code in [7, 8, 20]:
                        sys.exit(1)
                    client.sendReplyMessage(msg_id, to, '#Perintah Gagal : ' + str(talk_error))
                except Exception as error:
                    logError(error)
                    client.sendReplyMessage(msg_id, to, '#Perintah Gagal : ' + str(error))
        elif op.type == 25 or op.type == 25:
            msg      = op.message
            text     = str(msg.text)
            msg_id   = msg.id
            receiver = msg.to
            sender   = msg._from
            to       = sender if not msg.toType and sender != myMid else receiver
            txt      = text.lower()
            if msg.contentType == 0: # Content type is text
                if '/ti/g/' in text and settings['autoJoin']['ticket']:
                    regex = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
                    links = regex.findall(text)
                    tickets = []
                    gids = client.getGroupIdsJoined()
                    for link in links:
                        if link not in tickets:
                            tickets.append(link)
                    for ticket in tickets:
                        try:
                            group = client.findGroupByTicket(ticket)
                        except:
                            continue
                        if group.id in gids:
                            client.sendReplyMessage(msg_id, to, 'I\'m aleady on group ' + group.name)
                            continue
                        client.acceptGroupInvitationByTicket(group.id, ticket)
                        if settings['autoJoin']['reply']:
                            if '@!' not in settings['autoJoin']['message']:
                                client.sendReplyMessage(msg_id, to, settings['autoJoin']['message'])
                            else:
                                client.sendMentionV2(to, settings['autoJoin']['message'], [sender])
                        client.sendReplyMessage(msg_id, to, 'Success join to group ' + group.name)
    except TalkException as talk_error:
        logError(talk_error)
        if talk_error.code in [7, 8, 20]:
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit('Pesan SIstem : *KEYBOARD INTERRUPT.')
    except Exception as error:
        logError(error)

def runningProgram():
    while True:
        try:
            ops = oepoll.singleTrace(count=50)
        except TalkException as talk_error:
            logError(talk_error)
            if talk_error.code in [7, 8, 20]:
                sys.exit(1)
            continue
        except KeyboardInterrupt:
            sys.exit('Pesan SIstem : *KEYBOARD INTERRUPT.')
        except Exception as error:
            logError(error)
            continue
        if ops:
            for op in ops:
                executeOp(op)
                oepoll.setRevision(op.revision)

if __name__ == '__main__':
    print ('Pesan SIstem : *MENJALANKAN PROGRAM.\n#################################')
    runningProgram()
