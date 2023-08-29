#Imports modules that we use later
import scratchattach as scratch3 #scratchattach gives access to the scratch api
import secrets #gives us a secure random number generator
import pickle #allows us to write our lists to files
import os #allows us to check for said files so we don't cause errors

#make sure to change "SESSION_TOKEN", "USERNAME" and "PROJECT_ID" to yours!
session = scratch3.Session("SESSION_TOKEN", username="USERNAME") #this line logs us in to the scratch api
conn = session.connect_cloud("PROJECT_ID") #here we go to the spesific project we want to use

client = scratch3.CloudRequests(conn)

directory = os.getcwd()
files = os.listdir(directory)

for file in files:
    if file.startswith("encryption"):
        os.remove(file)
        print(f"Deleted file {file}")

@client.request
def ping(): #this is a basic definition for when a ping request is sent
    print("Ping request received")
    return "pong" #the return command sends whatever data is given back to the project

@client.event
def on_ready():
    print("Request handler is running") #notifies us the server is up
    
@client.request
def get_elo(argument1): #elo is just your score, so if you want, you can change elo to whatever you want
    if os.path.isfile("data_list"): #first we check if we already have a list of users
        with open("data_list", "rb") as fp: #if we do, we open it as data_list
            data_list = pickle.load(fp)
    else:
        data_list = [] #if we don't, data_list is blank
    user = argument1 #in our scratch code, argument1 is the username, so to make this easier to read, we are naming it "user"
    if user in data_list: #if the user already has a score..
        username_index = data_list.index(user) #get the username index
        elo = data_list[username_index + 1] #add one onto it, which is their score now
        print(f"Sending elo: {elo} to user: {user}")
        addition = []
        encryption = []
        for i in range(len(elo)): #encrypt it using random numbers
            while True:
                add_elo = secrets.randbelow(10)
                if int(elo[i]) + add_elo < 10:
                    addition.append(int(elo[i]) + add_elo)
                    encryption.append(add_elo)
                    break
        addition.append(100) #code 100 means continue with operation
        with open(f"encryption_{user}", "wb") as fp: #temporarily save encryption, so we can remove it on next pass
            pickle.dump(encryption, fp)
        return addition #and finally, send the encrypted score back
    else:
        print(f"User: {user} has no elo")
        return "no" #if the user has no score set, return back "no"
    
@client.request
def remove_encryption(argument1, argument2): #now that the scratch code has added it's own encryption, we can remove ours
    user = argument2
    with open(f"encryption_{user}", "rb") as fp: #open encryption numbers
        encryption = pickle.load(fp)
    send_list = []
    math_finished = argument1.replace(" ", "") #fix spaces because it's a list
    for i in range(len(math_finished)): #remove encryption
        send_list.append(int(math_finished[i]) - encryption[i])
    os.remove(f"encryption_{user}")
    send_list.append(200) #code 200 means finished with operation!
    return send_list #and finally, send everything back so the scratch code can decrypt the final answer

@client.request
def add_encryption(argument1, argument2): #this is all duplicated basically, the only difference is it's saving elo instead of getting it
    send_list = []
    math_finished = argument1.replace(" ", "")
    encryption = []
    for i in range(len(math_finished)):
        while True:
            add_elo = secrets.randbelow(10)
            if int(math_finished[i]) + add_elo < 10:
                send_list.append(int(math_finished[i]) + add_elo)
                encryption.append(add_elo)
                break
    send_list.append(100)
    with open(f"encryption_{user}", "wb") as fp:
        pickle.dump(encryption, fp)
    return send_list

@client.request
def set_elo(argument1, argument2):
    user = argument1
    math_finished = argument2.replace(" ", "")
    data_list = []
    with open(f"encryption_{user}", "rb") as fp:
        encryption = pickle.load(fp)
    for i in range(len(math_finished)):
        data_list.append(int(math_finished[i]) - encryption[i])
    os.remove(f"encryption_{user}")
    save_list = ''.join(str(v) for v in data_list)
    if os.path.isfile("data_list"):
        with open("data_list", "rb") as fp:
            data_list = pickle.load(fp)
        if user in data_list:
            username_index = data_list.index(user)
            if not data_list[username_index + 1] == save_list:
                temp_list = [s.replace(data_list[username_index + 1], save_list) for s in data_list]
                data_list = temp_list
        else:
            data_list.append(user)
            data_list.append(save_list)
    else:
        data_list = []
        data_list.append(user)
        data_list.append(save_list)
    print(f"Saving: {data_list}")
    with open("data_list", "wb") as fp:
        pickle.dump(data_list, fp)
    return "200"
client.run() #run the code!
