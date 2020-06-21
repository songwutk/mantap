from important import *
from module import *
from setup_args import *
from list_def import *

# Login Client
listAppType = ['DESKTOPWIN', 'DESKTOPMAC', 'IOSIPAD', 'CHROMEOS']
try:
    print ('System Message : *Client Login.')
    client = None
    if args.apptype:
        tokenPath = Path('authToken.txt')
        if tokenPath.exists():
            tokenFile = tokenPath.open('r')
        else:
            tokenFile = tokenPath.open('w+')
        savedAuthToken = tokenFile.read().strip()
        authToken = savedAuthToken if savedAuthToken and not args.token else args.token
        idOrToken = authToken if authToken else print("# There are no read tokens, please scan the qr below.")
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
            idOrToken = authToken if authToken else print("# There are no read tokens, please scan the qr below.")
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
    print ('System Message: Error : %s' % str(error))
    if args.traceback: traceback.print_tb(error.__traceback__)
    sys.exit(1)

admin = "uac8e3eaf1eb2a55770bf10c3b2357c33"
    
if client:
    print ('\nAdmin : %s' % admin)
    print ('\nUrgent: Auth Token -> %s' % client.authToken)
    print ('Urgent: Timeline Token -> %s' % client.tl.channelAccessToken)
    print ('\nSystem Message : *Login Successfully.')
else:
    sys.exit('System Message : *Login Failed.')

myMid = client.profile.mid

programStart = time.time()
oepoll = OEPoll(client)
tmp_text = []

settings = livejson.File('setting.json', True, False, 4)

bool_dict = {
    True: ['Yes', 'Aktif', 'Sukses', 'Open', 'On'],
    False: ['No', 'Tidak Aktif', 'Gagal', 'Close', 'Off']
}



def helpmessage():
    if settings['setKey']['status'] == True:
        key = settings['setKey']['key'].title()
    else:
        key = ''
    helpMessage ="╭─「 General 」─── " + "\n" + \
                    "│ Prefix : " + key + "\n" + \
                    "│ " + key + "Me" + "\n" + \
                    "│ " + key + "maker" + "\n" + \
                    "│ " + key + "speed" + "\n" + \
                    "│ " + key + "runtime" + "\n" + \
                    "│ " + key + "relogin" + "\n" + \
                    "╰────────────"
    return helpMessage

def helpmsg4():
    if settings['setKey'] == True:
        key = settings['keyCommand']
    else:
        key = ''
    helpMsg4 =   "╭───「 Group 」" + "\n" + \
                    "├" + key + "Groupinfo" + "\n" + \
                    "├" + key + "Grouplist" + "\n" + \
                    "├" + key + "Memberlist" + "\n" + \
                    "├" + key + "Openqr" + "\n" + \
                    "├" + key + "Closeqr" + "\n" + \
                    "├" + key + "ChangeGroupName <name>" + "\n" + \
                    "├" + key + "ChangeGroupPict" + "\n" + \
                    "├" + key + "Kickall" + "\n" + \
                    "├" + key + "Cancelall" + "\n" + \
                    "├" + key + "Tagall" + "\n" + \
                    "├" + key + "Lurk" + "\n" + \
                    "├" + key + "kick <Mention>" + "\n" + \
                    "├" + key + "Vkick <Mention>" + "\n" + \
                    "├" + key + "Greet" + "\n" + \
                    "├────「 Remote 」" + "\n" + \
                    "├" + key + "Open <NumberGroup>" + "\n" + \
                    "├" + key + "Close <NumberGroup>" + "\n" + \
                    "╰────────────"
    return helpMsg4




def executeCmd(msg, text, txt, cmd, msg_id, receiver, sender, to, setKey):

    # // Bot Logouted His Device
    if cmd == '@logout device':
      client.sendReplyMessage(msg_id, to, '* Program terminated.')
      sys.exit('##----- PROGRAM STOPPED -----##')

    # // Bot Send His Creator Contact
    if cmd == "maker":
        client.sendContact(to,admin)

    elif cmd=="test_echo":
            msg="echo echo echo "
            client.sendMessage( to, msg)

    elif cmd=="test_msg":
            msg='Hi message'
            msg2="No mention"
            client.sendReplyMessage(msg_id, to, msg)
            client.sendMessage( to, msg2)
    elif cmd=="test_flex":
            msg=""" {
  "type": "bubble", // ①
  "body": { // ②
    "type": "box", // ③
    "layout": "horizontal", // ④
    "contents": [ // ⑤
      {
        "type": "text", // ⑥
        "text": "Hello,"
      },
      {
        "type": "text", // ⑥
        "text": "World!"
      }
    ]
  }
}
"""
            client.sendFlexMessage( to, msg)            
    
    elif cmd == "group":
            helpMsg4 = helpmsg4()
            ty = client.getContact(sender)
            a={'MSG_SENDER_NAME': client.getContact(sender).displayName, 'MSG_SENDER_ICON': 'http://dl.profile.line.naver.jp' + str(ty.picturePath)}
            client.sendReplyMessage(msg_id, to, str(helpMsg4), contentMetadata=a)
    
    elif cmd == 'groupinfo':
        if msg.toType != 2: return client.sendReplyMessage(msg_id, to, 'Failed display group info, use this command only on group chat')
        group = client.getCompactGroup(to)
        try:
            ccreator = group.creator.mid
            gcreator = group.creator.displayName
        except:
            ccreator = None
            gcreator = 'Not found'
        if not group.invitee:
            pendings = 0
        else:
            pendings = len(group.invitee)
        qr = 'Close' if group.preventedJoinByTicket else 'Open'
        if group.preventedJoinByTicket:
            ticket = 'Not found'
        else:
            ticket = 'https://line.me/R/ti/g/' + str(client.reissueGroupTicket(group.id))
        created = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(int(group.createdTime) / 1000))
        path = 'http://dl.profile.line-cdn.net/' + group.pictureStatus
        res = '╭───「 Group Info 」'
        #res += '\n├ ID : ' + group.id
        res += '\n├ Name : ' + group.name
        res += '\n├ Creator : ' + gcreator
        res += '\n├ Created Time : ' + created
        res += '\n├ Member Count : ' + str(len(group.members))
        res += '\n├ Pending Count : ' + str(pendings)
        #res += '\n├ QR Status : ' + qr
        #res += '\n├ Ticket : ' + ticket
        #res += '\n╰───「 Self Bot 」'
        res += '\n╰────────────'
        #client.sendImageWithURL(to, path)  # Owner avatar
        #if ccreator: # tag creator
        #    client.sendContact(to, ccreator)
        client.sendReplyMessage(msg_id, to, res)
    
    elif cmd.startswith('grouplist'):
        textt = removeCmd(text, setKey)
        texttl = textt.lower()
        gids = client.getGroupIdsJoined()
        gnames = []
        ress = []
        res = '╭───「 Group List 」'
        res += '\n├ List:'
        if gids:
            groups = client.getGroups(gids)
            no = 0
            if len(groups) > 200:
                parsed_len = len(groups)//200+1
                for point in range(parsed_len):
                    for group in groups[point*200:(point+1)*200]:
                        no += 1
                        res += '\n│ %i. %s//%i' % (no, group.name, len(group.members))
                        gnames.append(group.name)
                    if res:
                        if res.startswith('\n'): res = res[1:]
                        if point != parsed_len - 1:
                            ress.append(res)
                    if point != parsed_len - 1:
                        res = ''
            else:
                for group in groups:
                    no += 1
                    res += '\n│ %i. %s//%i' % (no, group.name, len(group.members))
                    gnames.append(group.name)
        else:
            res += '\n│ Nothing'
        res += '\n├ Usage : '
        res += '\n│ • {key}GroupList'
        res += '\n│ • {key}GroupList Leave <num/name/all>'
        res += '\n╰───「 Self Bot 」'
        ress.append(res)
        if cmd == 'grouplist':
            for res in ress:
                client.sendReplyMessage(msg_id, to, parsingRes(res).format_map(SafeDict(key=setKey.title())))
        elif texttl.startswith('leave '):
            texts = textt[6:].split(', ')
            leaved = []
            if not gids:
                return client.sendReplyMessage(msg_id, to, 'Failed leave group, nothing group in list')
            for texxt in texts:
                num = None
                name = None
                try:
                    num = int(texxt)
                except ValueError:
                    name = texxt
                if num != None:
                    if num <= len(groups) and num > 0:
                        group = groups[num - 1]
                        if group.id in leaved:
                            client.sendReplyMessage(msg_id, to, 'Already leave group %s' % group.name)
                            continue
                        client.leaveGroup(group.id)
                        leaved.append(group.id)
                        if to not in leaved:
                            client.sendReplyMessage(msg_id, to, 'Success leave group %s' % group.name)
                    else:
                        client.sendReplyMessage(msg_id, to, 'Failed leave group number %i, number out of range' % num)
                elif name != None:
                    if name in gnames:
                        group = groups[gnames.index(name)]
                        if group.id in leaved:
                            client.sendReplyMessage(msg_id, to, 'Already leave group %s' % group.name)
                            continue
                        client.leaveGroup(group.id)
                        leaved.append(group.id)
                        if to not in leaved:
                            client.sendReplyMessage(msg_id, to, 'Success leave group %s' % group.name)
                    elif name.lower() == 'all':
                        for gid in gids:
                            if gid in leaved:
                                continue
                            client.leaveGroup(gid)
                            leaved.append(gid)
                            time.sleep(0.8)
                        if to not in leaved:
                            client.sendReplyMessage(msg_id, to, 'Success leave all group ♪')
                    else:
                        client.sendReplyMessage(msg_id, to, 'Failed leave group with name `%s`, name not in list ♪' % name)
        else:
            for res in ress:
                client.sendReplyMessage(msg_id, to, parsingRes(res).format_map(SafeDict(key=setKey.title())))    
    
    
    # // Checking Speed of Bot Send an Message
    elif cmd == 'speed':
        start = time.time()
        client.sendReplyMessage(msg_id, to, 'Authenticating...')
        elapse = time.time() - start
        client.sendReplyMessage(msg_id, to, 'Message Sending Speed %s Seconds' % str(elapse))
    
    # // Runtime when Program Started
    elif cmd == "runtime":
        timeNow = time.time()
        runtime = timeNow - programStart
        runtime = timeChange(runtime)
        client.sendReplyMessage(msg_id, to, "The bot has been working for a while {}".format(str(runtime)))

    # // Restart the Program
    elif cmd == 'relogin':
        client.sendReplyMessage(msg_id, to, 'Successfully Repeating the Program!')
        settings['restartPoint'] = to
        restartProgram()
    
    elif 'spic' in text.lower():
                                try:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    u = key["MENTIONEES"][0]["M"]
                                    a = client.getContact(u).pictureStatus
                                    client.sendImageWithURL(receiver, 'http://dl.profile.line.naver.jp/'+a)
                                except Exception as e:
                                    client.sendText(receiver, str(e))
    elif 'scover' in text.lower():
                                try:
                                    key = eval(msg.contentMetadata["MENTION"])
                                    u = key["MENTIONEES"][0]["M"]
                                    a = channel.getProfileCoverURL(mid=u)
                                    client.sendImageWithURL(receiver, a)
                                except Exception as e:
                                    client.sendText(receiver, str(e))
    elif text.lower() == 'tagall':
                                group = client.getGroup(msg.to)
                                nama = [contact.mid for contact in group.members]
                                nm1, nm2, nm3, nm4, nm5, jml = [], [], [], [], [], len(nama)
                                if jml <= 100:
                                    client.mention(msg.to, nama)
                                if jml > 100 and jml < 200:
                                    for i in range(0, 100):
                                        nm1 += [nama[i]]
                                    client.mention(msg.to, nm1)
                                    for j in range(101, len(nama)):
                                        nm2 += [nama[j]]
                                    client.mention(msg.to, nm2)
                                if jml > 200 and jml < 300:
                                    for i in range(0, 100):
                                        nm1 += [nama[i]]
                                    client.mention(msg.to, nm1)
                                    for j in range(101, 200):
                                        nm2 += [nama[j]]
                                    client.mention(msg.to, nm2)
                                    for k in range(201, len(nama)):
                                        nm3 += [nama[k]]
                                    client.mention(msg.to, nm3)
                                if jml > 300 and jml < 400:
                                    for i in range(0, 100):
                                        nm1 += [nama[i]]
                                    client.mention(msg.to, nm1)
                                    for j in range(101, 200):
                                        nm2 += [nama[j]]
                                    client.mention(msg.to, nm2)
                                    for k in range(201, len(nama)):
                                        nm3 += [nama[k]]
                                    client.mention(msg.to, nm3)
                                    for l in range(301, len(nama)):
                                        nm4 += [nama[l]]
                                    client.mention(msg.to, nm4)
                                if jml > 400 and jml < 501:
                                    for i in range(0, 100):
                                        nm1 += [nama[i]]
                                    client.mention(msg.to, nm1)
                                    for j in range(101, 200):
                                        nm2 += [nama[j]]
                                    client.mention(msg.to, nm2)
                                    for k in range(201, len(nama)):
                                        nm3 += [nama[k]]
                                    client.mention(msg.to, nm3)
                                    for l in range(301, len(nama)):
                                        nm4 += [nama[l]]
                                    client.mention(msg.to, nm4)
                                    for m in range(401, len(nama)):
                                        nm5 += [nama[m]]
                                    client.mention(msg.to, nm5)             
                                client.sendText(receiver, "Members :"+str(jml))

    # // Bot Send Profile Of Sender
    if cmd == "me":
        paramz = client.getContact(sender)
        isi = "╭───「 Profile Info 」"
        isi += "\n│"
        isi += "\n│ • user id : " + paramz.mid
        isi += "\n│ • user name : " + paramz.displayName
        isi += "\n│ • user status : " + paramz.statusMessage
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
        hasil += "\n├ Title: " +str(judul)
        hasil += "\n╰──────────"
        hasil += '\n\n-> Results : \n'+str(data.__str__(contoh=False))
        client.sendReplyMessage(msg_id, to, str(hasil))
      except Exception as error:
          client.sendReplyMessage(msg_id, to, "#Command failed, said {} not found".format(judul))
          logError(error)


    # # IP CHECK
    # elif cmd.startswith("ipcheck "):
    #   try:
    #      proses = msg.text.split(" ")
    #      urutan = msg.text.replace(proses[0] + " ","")
    #      r = requests.get("http://apitrojans.herokuapp.com/checkip?ip={}".format(str(urutan)))
    #      data = r.text
    #      data = json.loads(data)
    #      ret_ = "╭──[ Ip Check ]"
    #      ret_ += "\n├ IP : {}".format(str(data["result"]["ip"]))
    #      ret_ += "\n├ Desimal : {}".format(str(data["result"]["decimal"]))
    #      ret_ += "\n├ Hostname : {}".format(str(data["result"]["hostname"]))
    #      ret_ += "\n├ ASN : {}".format(str(data["result"]["asn"]))
    #      ret_ += "\n├ ISP : {}".format(str(data["result"]["isp"]))
    #      ret_ += "\n├ Organisasi : {}".format(str(data["result"]["organization"]))
    #      ret_ += "\n├ Tipe : {}".format(str(data["result"]["type"]))
    #      ret_ += "\n├ Benua : {}".format(str(data["result"]["continent"]))
    #      ret_ += "\n├ Negara : {}".format(str(data["result"]["country"]))
    #      ret_ += "\n├ Wilayah : {}".format(str(data["result"]["region"]))
    #      ret_ += "\n├ Kota : {}".format(str(data["result"]["city"]))
    #      ret_ += "\n╰──[ Reighpuy @HelloWorld ]"
    #      client.sendReplyMessage(msg_id, to, str(ret_))
    #   except:client.sendReplyMessage(msg_id, to,"#Command Failed: {} Not found.".format(urutan))


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
                return client.sendReplyMessage(msg_id, to, 'not found Error.')
            errors = [err.strip() for err in filee.readlines()]
            filee.close()
            if not errors: return client.sendReplyMessage(msg_id, to, 'not foundError.')
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
                client.sendReplyMessage(msg_id, to, 'Failed to activate setkey, setkey is active')
            else:
                settings['setKey']['status'] = True
                client.sendReplyMessage(msg_id, to, 'Activated successfully Setkey.')
        elif texttl == 'off':
            if not settings['setKey']['status']:
                client.sendReplyMessage(msg_id, to, 'Disabling failed setkey, setkey has been deactivated')
            else:
                settings['setKey']['status'] = False
                client.sendReplyMessage(msg_id, to, 'Successfully deactivatedSetkey.')
        else:
            settings['setKey']['key'] = texttl
            client.sendReplyMessage(msg_id, to, 'Successfully changed key set to(%s)' % textt)

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
                            client.sendReplyMessage(msg_id, to, 'Already in a Group ' + group.name)
                            continue
                        client.acceptGroupInvitationByTicket(group.id, ticket)
                        if settings['autoJoin']['reply']:
                            if '@!' not in settings['autoJoin']['message']:
                                client.sendReplyMessage(msg_id, to, settings['autoJoin']['message'])
                            else:
                                client.sendMentionV2(to, settings['autoJoin']['message'], [sender])
                        client.sendReplyMessage(msg_id, to, 'Success Join Group' + group.name)
                try:
                    executeCmd(msg, text, txt, cmd, msg_id, receiver, sender, to, setKey)
                except TalkException as talk_error:
                    logError(talk_error)
                    if talk_error.code in [7, 8, 20]:
                        sys.exit(1)
                    client.sendReplyMessage(msg_id, to, '#Command Failed : ' + str(talk_error))
                except Exception as error:
                    logError(error)
                    client.sendReplyMessage(msg_id, to, '#Command Failed : ' + str(error))
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
        sys.exit('Order the system : *KEYBOARD INTERRUPT.')
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
            sys.exit('Order the system : *KEYBOARD INTERRUPT.')
        except Exception as error:
            logError(error)
            continue
        if ops:
            for op in ops:
                executeOp(op)
                oepoll.setRevision(op.revision)

if __name__ == '__main__':
    print ('Order the system : *RUN PROGRAM.\n#################################')
    runningProgram()
