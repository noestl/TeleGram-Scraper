import configparser
import os
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, \
    InputPeerChat
from telethon.errors.rpcerrorlist import PeerFloodError, \
    UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time
import random

cpass = configparser.RawConfigParser()
cpass.read('config.data')


re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

            version : 3.1
youtube.com/channel/UCnknCgg_3pVXS27ThLpw3xQ
        """)


try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

# input_file = sys.argv[1]
input_file = 'members_test.csv'
users = []


with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    # print(chat)
    try:
        # if chat.megagroup == True:
        groups.append(chat)
    except:
        continue

print('Choose a group to add members:')
i = 0
for group in groups:
    print(str(i) + '- ' + group.title)
    i += 1

g_index = input("Enter a Number: ")
target_group = groups[int(g_index)]

# try:
#     print(f"""target_group.id: {target_group.id}""")
#     print(f"""target_group.access_hash: {target_group.access_hash}""")
# except Exception:
#     pass

target_group_entity = InputPeerChannel(target_group.id,
                                       target_group.access_hash)
# target_group_entity = InputPeerChat(target_group.id)

# mode = int(input("Enter 1 to add by username or 2 to add by ID: "))
print("mode = 2 = to add by ID")
mode = 2 # add only with the id

n = 0

for user in users:
    n += 1
    if n % 50 == 0:
        time.sleep(900)
    try:
        print("Adding {}".format(user['id']))
        if mode == 1:
            if user['username'] == "":
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit("Invalid Mode Selected. Please Try Again.")

        print(f"""target_group_entity: {target_group_entity}""")
        print(f"""[user_to_add]: {[user_to_add]}""")

        client(InviteToChannelRequest(target_group_entity, [user_to_add]))


        # print("Waiting for 60-180 Seconds...")
        # time.sleep(random.randrange(60, 180))
    except PeerFloodError:
        print(
            "Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
    except UserPrivacyRestrictedError:
        print(
            "The user's privacy settings do not allow you to do this. Skipping.")
    except:
        traceback.print_exc()
        print("Unexpected Error")
        continue

