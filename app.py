import gpg
import os
import random
import logging
from tkinter import *

data = []
restrictedfiles = []
box = []


class App:
    def __init__(self):
        global root, logger, listBox, decryptEntry
        LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
        # Logger Info
        logging.basicConfig(filename="Contacts.log",
                            level=logging.DEBUG, format=LOG_FORMAT)
        logger = logging.getLogger()
        # Banner
        banner = """
 _    _                  _       _   _
| |  | |                (_)     | | | |
| |__| |_   _  __ _  ___ _ _ __ | |_| |__   __ ___  __
|  __  | | | |/ _` |/ __| | '_ | __| '_ / _`  /    / /
| |  | | |_| | (_| | (__| | | | | |_| | | | (_| |>  <
|_|  |_| _,  |__,_|___|_|_| |_|__|_| |_|__,_/_/_/  /___
         __/ |
        |___/
        """
        root = Tk()
        tItle = "Contact-List"
        root.title(tItle)
        root.geometry("400x400")
        c = gpg.Context()
        self.recipient = "YOURKEYIDHERE"
        # Entry
        e = Entry(root, width=40, borderwidth=3)
        e.grid(row=0, column=0, columnspan=9)
        decryptEntry = Entry(root, width=40, borderwidth=3)
        decryptEntry.grid(row=15, column=0)
        # Label
        labelData = Label(root, text=banner)
        labelData.grid(row=20, column=0)
        listBox = Listbox(root, width=40, height=10)
        listBox.grid(row=1, column=0, columnspan=5, rowspan=9)
        # Buttons
        button_quit = Button(root, text="Exit", command=root.quit)
        button_Delete = Button(root, text="Delete", command=self.delete)
        button_Search = Button(root, text="Search", command=self.search)
        button_New = Button(root, text="Add", command=self.new)
        button_Decrypt = Button(root, text="View", command=self.decryptFile)
        button_Refresh = Button(root, text="Refresh", command=self.refresh)
        # Buttons to Grid
        button_quit.grid(row=20, column=10)
        button_Delete.grid(row=2, column=10)
        button_Search.grid(row=0, column=10)
        button_New.grid(row=3, column=10)
        button_Decrypt.grid(row=4, column=10)
        button_Refresh.grid(row=5, column=10)
        root.mainloop()

    def generator(self):
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?></';|][=-()*&^%$#@!`~"
        passlen = 35
        password = ""
        for x in range(0, passlen):
            password_char = random.choice(chars)
            password = password + password_char
        print("Here is your Password:  %s" % (password))
        logger.info("User Generated a Password for %s." % (fn))
        return password

    def new(self):
        global fu, fp, fn, com, ex
        ft = input("What will the File be Called? \n (Will Format to Lowercase) \n (This Will OVERWRITE Files of the SAME NAME) \n Quit To Exit Clean:  ").lower()
        if ft == "quit":
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            fn = ft + ".txt"
            print(fn)
            com = input("Contact Name: ")
            fu = input("Contact Primary EMail:  ")
            fp = input("Contact Phone #:  ")
            ex = input("Extra Details:  ")
            pw = input(
                "Do You Need a Password For this Person ONLY?(35)(Y/N): ").lower()
            if pw == "y":
                self.generator()
                input("Enter To Encryption and End... THIS WILL CLEAR!!")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Refresh Bro...")
                self.create()

            else:
                input("Enter To Encryption and End... THIS WILL CLEAR!!")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Refresh Bro...")
                self.create()

    def encryption(self):
        a_key = self.recipient
        with open(fn, "rb") as afile:
            text = afile.read()
            c = gpg.core.Context(armor=True)
            rkey = list(c.keylist(pattern=a_key, secret=False))
            ciphertext, result, sign_result = c.encrypt(text, recipients=rkey,
                                                        always_trust=True,
                                                        add_encrypt_to=True)
        with open("{0}.asc".format(fn), "wb") as bfile:
            bfile.write(ciphertext)
            logger.info("User Made a New File: %s" % (fn))
            os.remove(fn)

    def decryptFile(self):
        fn = str(listBox.get(ANCHOR))
        with open("{0}".format(fn), "rb") as cfile:
            plaintext, result, verify_result = gpg.Context().decrypt(cfile)
            decryptEntry.insert(0, plaintext)
            logger.info("User Viewed/Decrypted %s" % (fn))
            print("CLEAR THE TEXT FIELD WHEN DONE...  ")

    def delete(self):
        cz = listBox.get(ANCHOR)
        selection = input("Are You Sure? It's PERMANENT!(Y/n)  ")
        if selection.lower() == "y":
            os.remove(cz)
            listBox.delete(ANCHOR)
            box.remove(cz)
            logger.info("User Deleted %s" % (cz))

        elif selection.lower() == "n":
            os.system('cls' if os.name == 'nt' else 'clear')

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Please Only Y or N...  ")
            delete()

    def search(self):
        print("This Function Is Not Yet Available...  ")

    def create(self):
        with open(fn, 'w+') as filen:
            text = str(com + '\n' + fu + '\n' + fp + '\n' + ex)
            filen.write(text)
        self.encryption()

    def refresh(self):
        # Resticted Files
        with open('restrictedfiles.txt') as f:
            for datas in f.readlines():
                data.append(datas)
            for line in data:
                restrictedfiles.append(line.strip('\n'))
        # Current Files
        files = []
        for file in os.listdir(os.getcwd()):
            if file not in restrictedfiles:
                files.append(file)
        # print(files)
        for item in files:
            box.append(item)
            if box.count(item) == 1:
                listBox.insert(END, item)
