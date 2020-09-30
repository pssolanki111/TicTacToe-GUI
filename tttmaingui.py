import tkinter as tk
import threading as th
from pyautogui import size
from sys import exit as closeApp
import tkinter.messagebox as msgb
import tkinter.scrolledtext as sct
import os
import shelve as shl
import sqlite3 as sq
from datetime import datetime as dt
from playsound import playsound as ps


class BGM:
    def __init__(signal):
        while not signal:
            ps('lol.mp3', False)


class MenuBar(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)


class StBar(tk.Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)


class MidSpace(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)


class PriApp:
    def __init__(self, root):
        self.root = root
        self.StBar = StBar(self.root)
        self.MenuBar = MenuBar(self.root)
        self.MidSpace = MidSpace(self.root)
        self.StBar.configure(bg='#fff')
        self.MenuBar.configure(bg='#fff')
        self.MidSpace.configure(bg='#fff')
        self.canva = tk.Canvas(self.root, width=swidth, height=sheight - 60, bg='#fff')
        self.canva.grid(row=0, column=0)

        self.myDir = r'C:\Users\J.S.Solanki\Documents\TTT-pssolanki\AppData'
        self.tttBoard = {'1': '  ',
                         '2': '  ',
                         '3': '  ',
                         '4': '  ',
                         '5': '  ',
                         '6': '  ',
                         '7': '  ',
                         '8': '  ',
                         '9': '  '}

        try:
            os.makedirs(self.myDir)
        except FileExistsError:
            pass

        os.chdir(self.myDir)

        self.gameData = shl.open('gameData')
        self.gameData['test'] = ['Hello there, its a check', 11]
        self.gameData.close()

        self.resultData = sq.connect('resultData.db')
        self.c = self.resultData.cursor()
        self.c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='results' ''')
        if self.c.fetchone()[0] != 1:
            self.c.execute('''CREATE TABLE results
                                   ('res text', 'dt text')
                               ''')
        self.resultData.commit()
        self.resultData.close()

        self.flag = 0
        self.cPlayer = 1
        self.moveNumber = 0
        self.ng = 0
        self.rn = dt.today()

        # Intro Starts
        self.canva.create_text(midx - 10, midy - 200, text='Tic Tac Toe', font=('castellar', 25), fill='#00f')
        self.canva.create_text(midx + 175, midy - 118, text='from', font=('forte', 10), fill='#000')
        self.canva.create_text(midx + 230, midy - 118, text=' P S Solanki ', font=('forte', 10), fill='#00f')
        self.canva.create_line(midx - 285, midy - 150, midx + 270, midy - 150, fill='#00f')
        self.canva.create_line(midx - 285, midy - 148, midx + 270, midy - 148, fill='#00f')
        self.canva.create_line(midx + 193, midy - 106, midx + 268, midy - 106, fill='blue')
        self.canva.create_text(midx, midy + 250, text='Starting up........', font=('verdana', 13), fill='#00f')
        tk.Button(root).after(500, self.PlayerChoices)
        # Intro Ends

    def PlayerChoices(self):
        if self.flag == 0:
            def contt():
                self.p1name = str(self.p1n.get())
                self.p2name = str(self.p2n.get())
                self.p1player = str(self.p1p.get())
                self.p2player = str(self.p2p.get())

                if self.p1n.get() == '' or self.p2n.get() == '' or self.p1p.get() == '' or self.p2p.get() == '':
                    self.flag = 1
                    msgb.showerror(title='Empty input detected',
                                   message='Please make sure you don\'t leave any input field blank')
                    self.PlayerChoices()

                elif self.p1n.get() == self.p2n.get():
                    self.flag = 1
                    msgb.showerror(title='Invalid Input',
                                   message='Player names can\'t be the same\nPlease input again!')
                    self.PlayerChoices()

                elif self.p1p.get() == self.p2p.get():
                    self.flag = 1
                    msgb.showerror(title='Invalid Input',
                                   message='Player characters can\'t be the same\nPlease input again!')
                    self.PlayerChoices()

                elif len(self.p1player) > 1 or len(self.p2player) > 1:
                    self.flag = 1
                    msgb.showerror(title='Invalid Input',
                                   message='Player characters must not be more than one character')
                    self.PlayerChoices()

                else:
                    self.gameData = shl.open('gameData')

                    if self.p1name in self.gameData.keys() and self.p2name in self.gameData.keys():
                        tt = msgb.askyesno(title='Username already exists..',
                                           message='Please note that both Player1 & Player2 user names\n'
                                                   'already exist in our records.'
                                                   '\nAny new data (Your results & stats) will be saved to'
                                                   '\nThe same user names. Do you wish to proceed?')
                        if tt:
                            self.tempwin.destroy()
                            self.gameData[self.p1name] = [self.p1name, 0, 0, 0, self.p1player]
                            self.gameData[self.p2name] = [self.p1name, 0, 0, 0, self.p2player]
                            self.gameData.close()
                            self.gamewin()
                        elif not tt:
                            self.gameData.close()
                            self.flag = 1
                            msgb.showinfo(title='Info',
                                          message='Alright! Please choose'
                                                  ' different user names')

                            self.PlayerChoices()

                    elif self.p1name in self.gameData.keys():
                        tt = msgb.askyesno(title='Username already exists..',
                                           message='Please note that Player1 user name already exists in our records.'
                                                   '\nAny new data (Your results & stats) will be saved to'
                                                   '\nThe same user name. Do you wish to proceed?')
                        if tt:
                            self.tempwin.destroy()
                            self.gameData[self.p1name] = [self.p1name, 0, 0, 0, self.p1player]
                            self.gameData[self.p2name] = [self.p1name, 0, 0, 0, self.p2player]
                            self.gameData.close()
                            self.gamewin()
                        elif not tt:
                            self.gameData.close()
                            self.flag = 1
                            msgb.showinfo(title='Info',
                                          message='Alright! Please choose a'
                                                  ' different username (Player1)')

                            self.PlayerChoices()

                    elif self.p2name in self.gameData.keys():
                        tt = msgb.askyesno(title='Username already exists..',
                                           message='Please note that Player2 username already exists in our records.'
                                                   '\nAny new data (Your results & stats) will be saved to'
                                                   '\nThe same username. Do you wish to proceed?')
                        if tt:
                            self.tempwin.destroy()
                            self.gameData[self.p1name] = [self.p1name, 0, 0, 0, self.p1player]
                            self.gameData[self.p2name] = [self.p1name, 0, 0, 0, self.p2player]
                            self.gameData.close()
                            self.gamewin()
                        elif not tt:
                            self.gameData.close()
                            self.flag = 1
                            msgb.showinfo(title='Info',
                                          message='Alright! Please choose a'
                                                  ' different username (Player2)')

                            self.PlayerChoices()
                    else:
                        self.gameData[self.p1name] = [self.p1name, 0, 0, 0, self.p1player]
                        self.gameData[self.p2name] = [self.p1name, 0, 0, 0, self.p2player]
                        self.gameData.close()
                        msgb.showinfo(title='Success',
                                      message='Welcome! Your registration is successful.'
                                              '\nPlease note that your results and stats\n'
                                              'will be saved with your user names. You can\n'
                                              'access them later in the app.')
                        self.gamewin()

            self.canva.destroy()
            self.tempwin = tk.Toplevel()
            self.tempwin.title('Select your preferences - TTT')
            self.tempwin.configure(bg='#fff')
            self.tempwin.geometry('325x350')
            self.tempwin.wm_geometry('+520+190')

            tk.Label(self.tempwin, text='Please Provide your Preferences', bg='#fff', fg='#f0f',
                     font=('Serif', 15)).grid(row=0, column=0, padx=5, columnspan=3, pady=15)
            tk.Label(self.tempwin, text='Player1 name     :', bg='#fff', font=('Serif', 10)).grid(row=1, column=0,
                                                                                                  pady=10)
            tk.Label(self.tempwin, text='Player2 name     :', bg='#fff', font=('Serif', 10)).grid(row=2, column=0,
                                                                                                  pady=10)

            self.p1n = tk.Entry(self.tempwin, width=33, borderwidth=3)
            self.p1n.grid(row=1, column=1, ipady=3)
            self.p1n.insert(tk.END, 'Your unique user name')
            self.p2n = tk.Entry(self.tempwin, width=33, borderwidth=3)
            self.p2n.grid(row=2, column=1, ipady=3)
            self.p2n.insert(tk.END, 'Your unique user name')

            tk.Label(self.tempwin, text='Player1 character:\n(\'X\' or \'0\' or other)', bg='#fff',
                     font=('Serif', 10)).grid(row=3, column=0, rowspan=2, padx=10, pady=10)
            self.p1p = tk.Entry(self.tempwin, width=33, borderwidth=3)
            self.p1p.grid(row=3, column=1, rowspan=2, ipady=3)
            self.p1p.insert(tk.END, 'Must be a single character')

            tk.Label(self.tempwin, text='Player2 character:\n(\'X\' or \'0\' or other)', bg='#fff',
                     font=('Serif', 10)).grid(
                row=5, column=0, rowspan=2, padx=10, pady=10)
            self.p2p = tk.Entry(self.tempwin, width=33, borderwidth=3)
            self.p2p.grid(row=5, column=1, rowspan=2, ipady=3)
            self.p2p.insert(tk.END, 'Must be a single character')

            self.p1n.bind("<FocusIn>", lambda args: self.p1n.delete(0, tk.END))
            self.p2n.bind("<FocusIn>", lambda args: self.p2n.delete(0, tk.END))
            self.p1p.bind("<FocusIn>", lambda args: self.p1p.delete(0, tk.END))
            self.p2p.bind("<FocusIn>", lambda args: self.p2p.delete(0, tk.END))

            self.cancelb = tk.Button(self.tempwin, text='Cancel & Exit', bg='#f00',
                                     width=12, fg='#fff', command=self.exitapp)
            self.cancelb.grid(row=7, ipadx=3, ipady=5, column=0, pady=40)
            self.conttb = tk.Button(self.tempwin, text='Continue', bg='#0f0', fg='#00f',
                                    width=12, command=contt)
            self.conttb.grid(row=7, ipadx=3, ipady=5, column=1, pady=40)

            self.cancelb.bind('<Enter>', lambda args: self.hoverbtn(4))
            self.conttb.bind('<Enter>', lambda args: self.hoverbtn(5))
            self.cancelb.bind('<Leave>', lambda args: self.leavebtn(4))
            self.conttb.bind('<Leave>', lambda args: self.leavebtn(5))

            self.tempwin.bind('<Return>', lambda args: self.conttb.invoke())

        elif self.flag == 1:
            def contt():
                self.p1name = str(self.p1n.get())
                self.p2name = str(self.p2n.get())
                self.p1player = str(self.p1p.get())
                self.p2player = str(self.p2p.get())

                if self.p1n.get() == '' or self.p2n.get() == '' or self.p1p.get() == '' or self.p2p.get() == '':
                    self.flag = 1
                    msgb.showerror(title='Empty input detected',
                                   message='Please make sure you don\'t leave any input field blank')
                    self.PlayerChoices()

                elif self.p1n.get() == self.p2n.get():
                    self.flag = 1
                    msgb.showerror(title='Invalid Input',
                                   message='Player names can\'t be the same\nPlease input again!')
                    self.PlayerChoices()

                elif self.p1p.get() == self.p2p.get():
                    self.flag = 1
                    msgb.showerror(title='Invalid Input',
                                   message='Player characters can\'t be the same\nPlease input again!')
                    self.PlayerChoices()

                elif len(self.p1player) > 1 or len(self.p2player) > 1:
                    self.flag = 1
                    msgb.showerror(title='Invalid Input',
                                   message='Player characters must not be more than one character')
                    self.PlayerChoices()

                else:
                    self.gameData = shl.open('gameData')

                    if self.p1name in self.gameData.keys() and self.p2name in self.gameData.keys():
                        tt = msgb.askyesno(title='Username already exists..',
                                           message='Please note that both Player1 & Player2 user names\n'
                                                   'already exist in our records.'
                                                   '\nAny new data (Your results & stats) will be saved to'
                                                   '\nThe same user names. Do you wish to proceed?')
                        if tt:
                            self.tempwin.destroy()
                            self.gameData[self.p1name] = [self.p1name, 0, 0, 0, self.p1player]
                            self.gameData[self.p2name] = [self.p1name, 0, 0, 0, self.p2player]
                            self.gameData.close()
                            self.gamewin()
                        elif not tt:
                            self.gameData.close()
                            self.flag = 1
                            msgb.showinfo(title='Info',
                                          message='Alright! Please choose'
                                                  ' different user names')

                            self.PlayerChoices()

                    elif self.p1name in self.gameData.keys():
                        tt = msgb.askyesno(title='Username already exists..',
                                           message='Please note that Player1 user name already exists in our records.'
                                                   '\nAny new data (Your results & stats) will be saved to'
                                                   '\nThe same user name. Do you wish to proceed?')
                        if tt:
                            self.tempwin.destroy()
                            self.gameData[self.p1name] = [self.p1name, 0, 0, 0, self.p1player]
                            self.gameData[self.p2name] = [self.p1name, 0, 0, 0, self.p2player]
                            self.gameData.close()
                            self.gamewin()
                        elif not tt:
                            self.gameData.close()
                            self.flag = 1
                            msgb.showinfo(title='Info',
                                          message='Alright! Please choose a'
                                                  ' different username (Player1)')

                            self.PlayerChoices()

                    elif self.p2name in self.gameData.keys():
                        tt = msgb.askyesno(title='Username already exists..',
                                           message='Please note that Player2 username already exists in our records.'
                                                   '\nAny new data (Your results & stats) will be saved to'
                                                   '\nThe same username. Do you wish to proceed?')
                        if tt:
                            self.tempwin.destroy()
                            self.gameData[self.p1name] = [self.p1name, 0, 0, 0, self.p1player]
                            self.gameData[self.p2name] = [self.p1name, 0, 0, 0, self.p2player]
                            self.gameData.close()
                            self.gamewin()
                        elif not tt:
                            self.gameData.close()
                            self.flag = 1
                            msgb.showinfo(title='Info',
                                          message='Alright! Please choose a'
                                                  ' different user name (Player2)')

                            self.PlayerChoices()
                    else:
                        self.gameData[self.p1name] = [self.p1name, 0, 0, 0, self.p1player]
                        self.gameData[self.p2name] = [self.p1name, 0, 0, 0, self.p2player]
                        self.gameData.close()
                        msgb.showinfo(title='Success',
                                      message='Welcome! Your registration is successful.'
                                              '\nPlease note that your results and stats\n'
                                              'will be saved with your user names. You can\n'
                                              'access them later in the app.')
                        self.gamewin()

            self.tempwin.destroy()
            self.tempwin = tk.Toplevel()
            self.tempwin.title('Select your preferences - TTT')
            self.tempwin.configure(bg='#fff')
            self.tempwin.geometry('325x350')
            self.tempwin.wm_geometry('+520+190')

            tk.Label(self.tempwin, text='Please Provide your Preferences', bg='#fff', fg='#f0f',
                     font=('Serif', 15)).grid(row=0, column=0, padx=5, columnspan=3, pady=15)
            tk.Label(self.tempwin, text='Player1 name     :', bg='#fff', font=('Serif', 10)).grid(row=1, column=0,
                                                                                                  pady=10)
            tk.Label(self.tempwin, text='Player2 name     :', bg='#fff', font=('Serif', 10)).grid(row=2, column=0,
                                                                                                  pady=10)

            self.p1n = tk.Entry(self.tempwin, width=33, borderwidth=3)
            self.p1n.grid(row=1, column=1, ipady=3)
            self.p1n.delete(0, tk.END)
            self.p1n.insert(0, self.p1name)
            self.p2n = tk.Entry(self.tempwin, width=33, borderwidth=3)
            self.p2n.grid(row=2, column=1, ipady=3)
            self.p2n.delete(0, tk.END)
            self.p2n.insert(0, self.p2name)

            tk.Label(self.tempwin, text='Player1 character:\n(\'X\' or \'0\' or other)', bg='#fff',
                     font=('Serif', 10)).grid(row=3, column=0, rowspan=2, padx=10, pady=10)
            self.p1p = tk.Entry(self.tempwin, width=33, borderwidth=3)
            self.p1p.grid(row=3, column=1, rowspan=2, ipady=3)
            self.p1p.delete(0, tk.END)
            self.p1p.insert(0, self.p1player)

            tk.Label(self.tempwin, text='Player2 character:\n(\'X\' or \'0\' or other)', bg='#fff',
                     font=('Serif', 10)).grid(
                row=5, column=0, rowspan=2, padx=10, pady=10)
            self.p2p = tk.Entry(self.tempwin, width=33, borderwidth=3)
            self.p2p.grid(row=5, column=1, rowspan=2, ipady=3)
            self.p2p.delete(0, tk.END)
            self.p2p.insert(0, self.p2player)

            self.cancelb = tk.Button(self.tempwin, text='Cancel & Exit', bg='#f00',
                                     width=12, fg='#fff', command=self.exitapp)
            self.cancelb.grid(row=7, ipadx=3, ipady=5, column=0, pady=40)
            self.conttb = tk.Button(self.tempwin, text='Continue', bg='#0f0', fg='#00f',
                                    width=12, command=contt)
            self.conttb.grid(row=7, ipadx=3, ipady=5, column=1, pady=40)

            self.cancelb.bind('<Enter>', lambda args: self.hoverbtn(4))
            self.conttb.bind('<Enter>', lambda args: self.hoverbtn(5))
            self.cancelb.bind('<Leave>', lambda args: self.leavebtn(4))
            self.conttb.bind('<Leave>', lambda args: self.leavebtn(5))

            self.tempwin.bind('<Return>', lambda args: self.conttb.invoke())

    @staticmethod
    def exitapp():
        closeApp()

    def gamewin(self):
        self.gameData = shl.open('gameData')

        if self.ng == 1:
            self.newgamebtn.destroy()
            self.stLabel.destroy()

        self.MenuBar.pack(side=tk.TOP, anchor=tk.NW)
        self.MidSpace.pack(side=tk.TOP, pady=85)
        self.StBar.pack(side=tk.BOTTOM, anchor=tk.SW)


        self.plList = {1: self.p1name,
                       2: self.p2name}

        self.htpb = tk.Button(self.MenuBar, text='How To Play', width=14,
                              bg='#000', fg='#fff', command=self.help)
        self.htpb.grid(row=0, column=0, padx=10, ipady=5, pady=7)
        self.htpb.bind("<Enter>", lambda args: self.hoverbtn(1))
        self.htpb.bind("<Leave>", lambda args: self.leavebtn(1))

        self.statb = tk.Button(self.MenuBar, text='Stats', width=14,
                               bg='#000', fg='#fff', command=self.showstats)
        self.statb.grid(row=0, column=1, padx=10, ipady=5, pady=7)
        self.statb.bind("<Enter>", lambda args: self.hoverbtn(6))
        self.statb.bind("<Leave>", lambda args: self.leavebtn(6))

        self.resb = tk.Button(self.MenuBar, text='Results', width=14,
                              bg='#000', fg='#fff', command=self.showres)
        self.resb.grid(row=0, column=2, padx=10, ipady=5, pady=7)
        self.resb.bind("<Enter>", lambda args: self.hoverbtn(7))
        self.resb.bind("<Leave>", lambda args: self.leavebtn(7))

        self.stLabel = tk.Label(self.StBar,
                                text=self.plList[self.cPlayer] + ' ! Play your move..(P' +
                                     str(self.cPlayer) + ' - ' +
                                    str(self.gameData[self.plList[self.cPlayer]][4]) + ')', bg='#000',
                                fg='#ff0', font=('roboto', 13))
        self.stLabel.pack(anchor=tk.W, padx=5)

        # Main Game Layout
        self.b1 = tk.Button(self.MidSpace, text=self.tttBoard['1'],
                            bg='#da5', fg='#250038', command=lambda: self.buttonpress(1),
                            font=('roboto', 20), width=2, height=1)
        self.b2 = tk.Button(self.MidSpace, text=self.tttBoard['2'],
                            bg='#745', fg='#380601', command=lambda: self.buttonpress(2),
                            font=('roboto', 20), width=2, height=1)
        self.b3 = tk.Button(self.MidSpace, text=self.tttBoard['3'],
                            bg='#da5', fg='#250038', command=lambda: self.buttonpress(3),
                            font=('roboto', 20), width=2, height=1)
        self.b4 = tk.Button(self.MidSpace, text=self.tttBoard['4'],
                            bg='#745', fg='#380601', command=lambda: self.buttonpress(4),
                            font=('roboto', 20), width=2, height=1)
        self.b5 = tk.Button(self.MidSpace, text=self.tttBoard['5'],
                            bg='#da5', fg='#250038', command=lambda: self.buttonpress(5),
                            font=('roboto', 20), width=2, height=1)
        self.b6 = tk.Button(self.MidSpace, text=self.tttBoard['6'],
                            bg='#745', fg='#380601', command=lambda: self.buttonpress(6),
                            font=('roboto', 20), width=2, height=1)
        self.b7 = tk.Button(self.MidSpace, text=self.tttBoard['7'],
                            bg='#da5', fg='#250038', command=lambda: self.buttonpress(7),
                            font=('roboto', 20), width=2, height=1)
        self.b8 = tk.Button(self.MidSpace, text=self.tttBoard['8'],
                            bg='#745', fg='#380601', command=lambda: self.buttonpress(8),
                            font=('roboto', 20), width=2, height=1)
        self.b9 = tk.Button(self.MidSpace, text=self.tttBoard['9'],
                            bg='#da5', fg='#250038', command=lambda: self.buttonpress(9),
                            font=('roboto', 20), width=2, height=1)

        self.buttonData = {1: self.b1,
                           2: self.b2,
                           3: self.b3,
                           4: self.b4,
                           5: self.b5,
                           6: self.b6,
                           7: self.b7,
                           8: self.b8,
                           9: self.b9}

        self.b1.grid(row=0, column=0, ipadx=40, ipady=40)
        self.b2.grid(row=0, column=1, ipadx=40, ipady=40)
        self.b3.grid(row=0, column=2, ipadx=40, ipady=40)
        self.b4.grid(row=1, column=0, ipadx=40, ipady=40)
        self.b5.grid(row=1, column=1, ipadx=40, ipady=40)
        self.b6.grid(row=1, column=2, ipadx=40, ipady=40)
        self.b7.grid(row=2, column=0, ipadx=40, ipady=40)
        self.b8.grid(row=2, column=1, ipadx=40, ipady=40)
        self.b9.grid(row=2, column=2, ipadx=40, ipady=40)

        self.gameData.close()

        if self.ng != 1:
            self.help()

    def hoverbtn(self, no):
        if no == 1:
            self.htpb.configure(bg='#00f', fg='#fff', text='Get Help')

        if no == 2:
            self.newgamebtn.configure(bg='#000', fg='#fff', text='Let\'s Go')

        if no == 3:
            self.gotitbtn.configure(bg='#f00', fg='#fff', text='Close')

        if no == 4:
            self.cancelb.configure(bg='#000', fg='#fff', text='Close The Game')

        if no == 5:
            self.conttb.configure(bg='#00f', fg='#fff', text='Let\'s Go!')

        if no == 6:
            self.statb.configure(fg='#fff', bg='#00f', text='View')

        if no == 7:
            self.resb.configure(bg='#00f', fg='#fff', text='View')

    def leavebtn(self, no):
        if no == 1:
            self.htpb.configure(bg='#000', fg='#fff', text='How To Play')

        if no == 2:
            self.newgamebtn.configure(bg='#00f', fg='#fff', text='Play Again')

        if no == 3:
            self.gotitbtn.configure(bg='#000', fg='#ff0', text='Got It')

        if no == 4:
            self.cancelb.configure(bg='#f00', fg='#ff0', text='Cancel & Exit')

        if no == 5:
            self.conttb.configure(bg='#0f0', fg='#00f', text='Continue')

        if no == 6:
            self.statb.configure(fg='#fff', bg='#000', text='Stats')

        if no == 7:
            self.resb.configure(bg='#000', fg='#fff', text='Results')

    def help(self):
        win2 = tk.Toplevel()
        win2.title('How To Play')
        win2.configure(bg='#fff')
        win2.geometry('450x550')
        win2.wm_geometry('+450+100')

        txtbox = sct.ScrolledText(win2, width=55, height=31, bg='#fff', fg='#f0f')
        txtbox.grid(row=0, column=0, sticky='nsew')
        txt = '      ** Welcome To The User Guide of TicTacToe **\n\n' \
              ' This is a simple game of classic Tic Tac Toe,\n developed just for fun by @pssolanki' \
              '\n\n* PLEASE NOTE * :: You can always bring this user guide\n\t\t  up by clicking the How' \
              ' To Play Button\t\t\t  to the Top Left of your screen.\n\n' \
              '\t\t\t\t\t\t\t\t\t  ** GAME BASICS **\n\n-> The game inherits its simple rules from the classic' \
              '    Tic Tac Toe.\n-> You got to choose your user names and characters at    the start' \
              '.\n-> On the main game window, you should see 9 buttons\n   arranged in 3x3 layout. ' \
              '\n\n\t\t\t\t\t\t\t\t\t   ** IMPORTANT **\n\n-> Always keep an eye out to the bottom left of your' \
              '\n   screens to know which player is supposed to play\n   the next move and also' \
              ' what is the character that\n   player is playing with to avoid confusion\n   & misinterpretation. ' \
              '\n-> A single player can\'t play two subsequent moves. The   moves have to' \
              ' rotate alternatively between the two\n   players.' \
              '\n-> The objective of each player is to create a match of   similar character' \
              ' ( must be his own character ),\n   such that the matched pattern covers ' \
              'any one\n   possible patterns out of horizontal, vertical\n   or diagonal.' \
              '\n-> A player who is able to create such a pattern before   his/her opponent ' \
              'WINS the game.' \
              '\n-> The game results in a draw if and only if no\n   matching pattern is created ' \
              'even after all 9\n   possible moves have been played out.' \
              '\n-> In both the cases - either some one wins or a draw -   A NEW BUTTON GETS' \
              ' ADDED TO THE INTERFACE - WITH THE\n   NAME \'New Game\' - TO THE TOP RIGHT OF THE ' \
              'SCREEN.' \
              '\n-> Selecting the button \'New Game\' initiates the\n   process of a new game - YOU ' \
              'GET TO KEEP OR CHANGE\n   YOUR USER NAMES - and a new game is initiated based\n   on' \
              ' your preferences.' \
              '\n\n\t\t\t\t\t\t\t\t  ** RESULTS & STATISTICS **\n\n' \
              '-> The game actually keeps a track of:\n\t> Number of games Played\n' \
              '\t> Number of games won\n\t> Number of games lost\n\t> The Result Time Line (' \
              ' explained below )\n   for' \
              ' every single user of the game.' \
              '\n-> Click on the Stats button to view the data any time    (You can also search for' \
              ' a specific user\'s data\n   with their user name.)\n' \
              '\n\t\t\t\t\t\t\t\t  ** RESULT TIME LINE **\n\n' \
              '-> The Results TimeLine is a text view of the results\n   of all the games been played' \
              ' so far\n   (including all the users).' \
              '\n-> It Lists the results sorted according to the date\n   and time Info of that particular' \
              ' game.\n\n' \
              '\t\t\t\t\t\t\t\t\t    ** SUPPORT **\n\n-> Please contact the developer @pssolanki in case\n   of ' \
              'a bug, suggestion, feature request or complaint\n   about the game.' \
              '\n\n\n\t\t\t\t\t\t\t\t\t--ALL RIGHTS RESERVED--\n\n\n\t\t\t\t\t\t\t\t\t     ***ENJOY***\n\n\n'

        txtbox.insert(1.0, txt)
        txtbox.configure(state=tk.DISABLED)
        self.gotitbtn = tk.Button(win2, text='Got It', bg='#000', height=2, font=('roboto', 10), fg='#ff0',
                                  command=win2.destroy)
        self.gotitbtn.grid(row=1, column=0, sticky='ew')

        self.gotitbtn.bind('<Enter>', lambda args: self.hoverbtn(3))
        self.gotitbtn.bind('<Leave>', lambda args: self.leavebtn(3))

    def buttonpress(self, k):

        if self.tttBoard[str(k)] == '  ':
            self.gameData = shl.open('gameData')
            self.buttonData[k].configure(text=self.gameData[self.plList[self.cPlayer]][4])

            self.tttBoard[str(k)] = self.gameData[self.plList[self.cPlayer]][4]
            self.moveNumber += 1

            if self.cPlayer == 1:
                self.cPlayer += 1
            elif self.cPlayer == 2:
                self.cPlayer -= 1

            if self.cPlayer == 2:
                self.stLabel.configure(text=self.plList[self.cPlayer] +
                                            ' ! Play your move.. (P' + str(self.cPlayer) + ' - ' +
                                            str(self.gameData[self.plList[self.cPlayer]][4]),
                                       bg='#f00', fg='yellow')
            else:
                self.stLabel.configure(text=self.plList[self.cPlayer] +
                                            ' ! Play your move..(P' + str(self.cPlayer) + ' - ' +
                                            str(self.gameData[self.plList[self.cPlayer]][4]),
                                       bg='#00f', fg='#fff')
            self.gameData.close()

        else:
            msgb.showinfo(title='Move Unavailable',
                          message='This move has already been played.'
                                  '\nPlease go with another move')
            self.gameData.close()

        if self.moveNumber >= 2:

            if self.tttBoard['1'] == self.tttBoard['2'] == self.tttBoard['3'] == self.p1player:
                self.afterwin(1, 2, 1, 2, 3)

            elif self.tttBoard['1'] == self.tttBoard['2'] == self.tttBoard['3'] == self.p2player:
                self.afterwin(2, 1, 1, 2, 3)

            elif self.tttBoard['4'] == self.tttBoard['5'] == self.tttBoard['6'] == self.p1player:
                self.afterwin(1, 2, 4, 5, 6)

            elif self.tttBoard['4'] == self.tttBoard['5'] == self.tttBoard['6'] == self.p2player:
                self.afterwin(2, 1, 4, 5, 6)

            elif self.tttBoard['7'] == self.tttBoard['8'] == self.tttBoard['9'] == self.p1player:
                self.afterwin(1, 2, 7, 8, 9)

            elif self.tttBoard['7'] == self.tttBoard['8'] == self.tttBoard['9'] == self.p2player:
                self.afterwin(2, 1, 7, 8, 9)

            elif self.tttBoard['1'] == self.tttBoard['4'] == self.tttBoard['7'] == self.p1player:
                self.afterwin(1, 2, 1, 4, 7)

            elif self.tttBoard['1'] == self.tttBoard['4'] == self.tttBoard['7'] == self.p2player:
                self.afterwin(2, 1, 1, 4, 7)

            elif self.tttBoard['2'] == self.tttBoard['5'] == self.tttBoard['8'] == self.p1player:
                self.afterwin(1, 2, 2, 5, 8)

            elif self.tttBoard['2'] == self.tttBoard['5'] == self.tttBoard['8'] == self.p2player:
                self.afterwin(2, 1, 2, 5, 8)

            elif self.tttBoard['3'] == self.tttBoard['6'] == self.tttBoard['9'] == self.p1player:
                self.afterwin(1, 2, 3, 6, 9)

            elif self.tttBoard['3'] == self.tttBoard['6'] == self.tttBoard['9'] == self.p2player:
                self.afterwin(2, 1, 3, 6, 9)

            elif self.tttBoard['1'] == self.tttBoard['5'] == self.tttBoard['9'] == self.p1player:
                self.afterwin(1, 2, 1, 5, 9)

            elif self.tttBoard['1'] == self.tttBoard['5'] == self.tttBoard['9'] == self.p2player:
                self.afterwin(2, 1, 1, 5, 9)

            elif self.tttBoard['3'] == self.tttBoard['5'] == self.tttBoard['7'] == self.p1player:
                self.afterwin(1, 2, 3, 5, 7)

            elif self.tttBoard['3'] == self.tttBoard['5'] == self.tttBoard['7'] == self.p2player:
                self.afterwin(2, 1, 3, 5, 7)

            elif self.moveNumber == 9:
                self.afterdraw()

            else:
                pass

    def afterwin(self, p, q, a, b, c):

        self.gameData = shl.open('gameData')
        self.resultData = shl.open('resultData')

        self.gameData[self.plList[p]] = [self.gameData[self.plList[p]][0],
                                         self.gameData[self.plList[p]][1] + 1,
                                         self.gameData[self.plList[p]][2] + 1,
                                         self.gameData[self.plList[p]][3],
                                         self.gameData[self.plList[p]][4]]

        self.gameData[self.plList[q]] = [self.gameData[self.plList[q]][0],
                                         self.gameData[self.plList[q]][1] + 1,
                                         self.gameData[self.plList[q]][2],
                                         self.gameData[self.plList[q]][3] + 1,
                                         self.gameData[self.plList[q]][4]]

        self.rn = str(dt.today()).split('.')[0]
        text = self.plList[p] + ' defeated ' + self.plList[q]
        self.resultData = sq.connect('resultData.db')
        self.c = self.resultData.cursor()
        self.c.execute("INSERT INTO results VALUES (:res, :dt)", {'res': text, 'dt': self.rn})
        self.resultData.commit()
        self.resultData.close()

        msgb.showinfo(title='Victory!',
                      message=''
                              + self.plList[p] + ' defeated '
                              + self.plList[q] +
                              '\n\nYou can click on the \'Play Again\' button to the Top'
                              '\nto play again :)')

        for x in self.buttonData.keys():
            if x == a or x == b or x == c:
                self.buttonData[x].configure(bg='#e0e', state=tk.DISABLED, fg='#000')

            else:
                self.buttonData[x].configure(state=tk.DISABLED, bg='#68ceff', fg='#fff')

        self.stLabel.configure(text='Victory To ' + self.gameData[self.plList[p]][0] + '!',
                               fg='#fff', bg='#00f')
        self.gameData.close()

        self.newgamebtn = tk.Button(self.MenuBar, text='Play Again', bg='#00f', fg='#fff',
                                    width=14, command=self.newgame)
        self.newgamebtn.grid(row=0, column=3, ipady=5, padx=10)
        self.newgamebtn.bind("<Enter>", lambda args: self.hoverbtn(2))
        self.newgamebtn.bind("<Leave>", lambda args: self.leavebtn(2))

    def afterdraw(self):

        msgb.showinfo(title='Game Draw !',
                      message='Game Drawn!\nWell Played both '
                              + self.p1name + ' & ' + self.p2name +
                              '\nYou can click on the \'Play Again\' button to the Top Right'
                              '\nto play again :)')

        for b in self.buttonData.keys():
            self.buttonData[b].configure(state=tk.DISABLED)

        self.stLabel.configure(text='Game Draw!',
                               fg='#fff', bg='#000')

        self.newgamebtn = tk.Button(self.MenuBar, text='Play Again', bg='#00f', fg='#fff',
                                    width=14, command=self.newgame)
        self.newgamebtn.grid(row=0, column=3, pady=5, ipady=5, padx=10)
        self.newgamebtn.bind("<Enter>", lambda args: self.hoverbtn(2))
        self.newgamebtn.bind("<Leave>", lambda args: self.leavebtn(2))

    def newgame(self):
        tt = msgb.askyesnocancel(title='New Game - Reserve User Names',
                                 message='Starting a new game !!\nWould you like to continue '
                                         'with the current User Names\nPlayer 1: ' + self.p1name +
                                         '\nPlayer 2: ' + self.p2name + ' ?')

        if tt:
            self.p1name = self.p1name
            self.p2name = self.p2name
            self.p1player = self.p1player
            self.p2player = self.p2player

            self.tttBoard = {'1': '  ',
                             '2': '  ',
                             '3': '  ',
                             '4': '  ',
                             '5': '  ',
                             '6': '  ',
                             '7': '  ',
                             '8': '  ',
                             '9': '  '}

            self.cPlayer = 1
            self.moveNumber = 0
            self.ng = 1

            self.gamewin()

        elif tt is None:
            pass

        elif not tt:
            msgb.showinfo(title='Info',
                          message='Alright ! Select your preferences on the next window.')

            self.tttBoard = {'1': '  ',
                             '2': '  ',
                             '3': '  ',
                             '4': '  ',
                             '5': '  ',
                             '6': '  ',
                             '7': '  ',
                             '8': '  ',
                             '9': '  '}

            self.cPlayer = 1
            self.moveNumber = 0
            self.flag = 0
            self.ng = 1

            self.PlayerChoices()

    def showstats(self):
        self.oneMoreWin = tk.Toplevel()
        self.oneMoreWin.state('zoomed')
        self.oneMoreWin.configure(bg='#fff')

        f1 = tk.Frame(self.oneMoreWin)
        f2 = tk.Frame(self.oneMoreWin)
        f1.pack(side=tk.TOP, anchor=tk.NW)
        f2.pack(side=tk.TOP, anchor=tk.SW)

        self.searchItem = tk.Entry(self.oneMoreWin, width=75, bg='#000', fg='#fff',
                                   font=('roboto', 15))
        self.searchItem.pack(ipady=15, anchor=tk.N, pady=10)
        self.searchItem.insert(0, ' Enter A User Name & Press Enter To Search')
        self.searchItem.bind('<FocusIn>', lambda args: self.searchItem.delete(0, tk.END))
        self.searchItem.bind('<Return>', lambda args: self.searchstats(self.searchItem.get()))

    def searchstats(self, query):
        print(query)

    def showres(self):
        pass


def createGUI():
    win = tk.Tk()
    try:
        swidth, sheight = size()
        midx = float(swidth) / 2
        midy = float(sheight) / 2
    except:
        swidth, sheight = 1360, 750
        midx = int(float(swidth) / 2)
        midy = int(float(sheight - 60) / 2)
        
    win.title('TicTacToe - pssolanki')
    win.state('zoomed')
    win.configure(bg='#fff')
    PriApp(win)
    win.mainloop()

if __name__ == '__main__':
    guiThread = th.Thread(target=createGUI)
    guiThread.start()
    musicThread = th.Thread(target=playBGM, args=0)
    musicThread.start()
