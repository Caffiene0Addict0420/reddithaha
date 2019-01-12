from ezy_multiplayer import *
import traceback
import PySimpleGUI27 as sg

def get_server(ip = "", port = ""):
    try:
        layout =  [[sg.Text("Connect To Server")],
                   [sg.InputText(ip), sg.Text(" (IP)")],
                   [sg.InputText(port), sg.Text(" (PORT)")],
                   [sg.OK()]]

        w = sg.Window('Connect To Server', keep_on_top = True).Layout(layout)    
        all  = w.Read()
        if all[0] != None:
            w.Close()
            pickle.dump((all[1][0], all[1][1]), open("server.data", "wb"))
            return(all[1][0], all[1][1])
    except:
        traceback.print_exc()
    return(False, False)

def text_msg(title, msg):
    layout = [[sg.Text(msg)]]
    w = sg.Window(title, keep_on_top = True).Layout(layout)   

def update_everything(username = "", password = "", client_id = "", client_secret = "", subs = "slavelabour+forhire", keywords = ["artwork", "photoshop"], comment = "", title = "", body = "Hello, *un*, I saw your post, (*ln*) and thought I would PM you"):
    try:
        if keywords == []:
            keywords = ""
        else:
            keys = ""
            for k in keywords:
                if keys == "":
                    keys = keys + k
                else:
                    keys = keys + "," + k
            keywords = keys
                
        layout = [[sg.Text("Reddit Settings (For Bot Login):")],
                  [sg.InputText(username), sg.Text(" (Username)")], #0
                  [sg.InputText(password), sg.Text(" (Password)")], #1
                  [sg.InputText(client_id), sg.Text(" (Reddit Client ID)")], #2
                  [sg.InputText(client_secret), sg.Text(" (Reddit Client Secret)")], #3
                  [sg.Text("Post Finder Settings:")],
                  [sg.InputText(subs), sg.Text(" (Subreddits, seperated by a '+')")], #4
                  [sg.InputText(keywords), sg.Text(" (Keywords, seperated by a comma)")], #5
                  [sg.Text("Message Settings:")],
                  [sg.InputText(comment), sg.Text(" (Comment to OP)")], #6
                  [sg.InputText(title), sg.Text(" (Title of PM)")],#7
                  [sg.InputText(body), sg.Text(" (Body of PM, use '*nl*' for newline)")], #8
                  [sg.Text("For the body of PM use: \n -> *nl* for a newline\n -> *un* for the original poster's username\n -> *ln* for a link to the original post")],
                  [sg.OK()]
                 ]
        w = sg.Window('Update Settings', keep_on_top = True).Layout(layout)    
        all  = w.Read()
        if all[0] != None: #fixing
            w.Close()
            all[1][8] = all[1][8].replace("*nl*", "\n") #making new line characters
            all[1][5] = all[1][5].split(",")
            return all[1]
    except Exception as e:
        traceback.print_exc()
        text_msg("Error",e)
    return(False, False)

try:
    a = pickle.load(open("server.data", "rb")) 
    host, port = get_server(a[0], a[1])
except Exception as e:
    host, port = get_server()

if host == "":
    host = get_ip()

port = int(port)    

multiplayer = connectServer(host, port)

try:
    send_data(multiplayer, "get_everything")
    everything = get_data(multiplayer)
    if everything == "False":
        new = update_everything()
    else:
        new = update_everything(everything[0], everything[1], everything[2], everything[3], everything[4], everything[5], everything[6], everything[7], everything[8])
    send_data(multiplayer, {"set_everything":new})
    response = get_data(multiplayer)
    if response == "False":print("An Error Occured")
except:
    traceback.print_exc()

while True:pass