import tkinter as tk
from pyautogui import size


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
        self.canva = tk.Canvas(self.root, width=swidth, height=sheight-60, bg='#fff')
        self.canva.grid(row=0, column=0)

        # Intro Starts
        self.canva.create_text(midx - 10, midy - 200, text='Tic Tac Toe', font=('castellar', 25), fill='#00f')
        self.canva.create_text(midx + 175, midy - 118, text='from', font=('forte', 10), fill='#000')
        self.canva.create_text(midx + 230, midy - 118, text=' P S Solanki ', font=('forte', 10), fill='#00f')
        self.canva.create_line(midx - 285, midy - 150, midx + 270, midy - 150, fill='#00f')
        self.canva.create_line(midx - 285, midy - 148, midx + 270, midy - 148, fill='#00f')
        self.canva.create_line(midx + 193, midy - 106, midx + 268, midy - 106, fill='blue')
        self.canva.create_text(midx, midy + 250, text='Starting up........', font=('verdana', 13), fill='#00f')
        tk.Button(root).after(1000, self.gamewin)
        # Intro Ends

    def gamewin(self):
        self.canva.destroy()

        self.root.grid_rowconfigure(0, weight=3)
        self.root.grid_rowconfigure(1, weight=55)
        self.root.grid_rowconfigure(2, weight=2)

        self.MenuBar.grid(row=0, column=0)
        self.MidSpace.grid(row=1, column=0)
        self.StBar.grid(row=2, column=0)

        htpb = tk.Button(self.MenuBar, text='How To Play', bg='#00f', fg='#fff', command=self.help)
        htpb.grid(row=0, column=0, padx=20, ipadx=10, ipady=5, sticky=tk.N+tk.S)
        titleL = tk.Label(self.MenuBar, text='TIC TAC TOE', font=('ALGERIAN', 25), bg='#fff', fg='#f00')
        titleL.grid(row=0, column=1, padx=450, sticky=tk.N+tk.S)

        # Main Game Layout
        self.MidSpace.grid_columnconfigure(0, weight=33)
        self.MidSpace.grid_columnconfigure(1, weight=33)
        self.MidSpace.grid_columnconfigure(2, weight=33)

        tk.Frame(self.MidSpace).grid(row=0, sticky=tk.W+tk.E)
        tk.Frame(self.MidSpace).grid(row=0, column=2, sticky=tk.W+tk.E)
        gameframe = tk.Frame(self.MidSpace)
        gameframe.grid(row=0, column=1, sticky=tk.W+tk.E)

    @staticmethod
    def help():
        win2 = tk.Tk()
        win2.title('How To Play')
        win2.configure(bg='#fff')
        win2.geometry('500x400')
        win2.wm_geometry('+430+160')


if __name__ == '__main__':
    win = tk.Tk()
    try:
        swidth, sheight = size()
        midx = float(swidth) / 2
        midy = float(sheight) / 2
        res = str(swidth) + 'x' + str(sheight-60)
    except:
        swidth, sheight = 1360, 750
        midx = int(float(swidth) / 2)
        midy = int(float(sheight-60) / 2)
        res = '1360x750'

    win.title('TicTacToe - pssolanki')
    win.geometry(res)
    win.wm_geometry("+0+0")
    win.configure(bg='#fff')
    PriApp(win)
    win.mainloop()
