import tkinter as tk
from tkinter import font as tkfont, font
from tkinter.filedialog import askopenfilename
from tkinter import *
import ntpath
import json
from functionDefinitions import *

# Global Variables
file_path = ""
file_name = ""
data = ""
data_is_loaded = False
invalid_file = False
bad_song_indices = []

class SongLyricAnalyzer(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Times New Roman', size=18, weight="bold")
        self.medium_font = tkfont.Font(family='Times New Roman', size=12, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Song Lyric Analyzer", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        label = tk.Label(self, text=file_name, font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        if invalid_file:
            label = tk.Label(self, text="Please select a valid json file", font=controller.title_font)
            label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Select File", command=lambda: [select_file()])
        button1.pack()
        button = tk.Button(self, text="Quick Select File (For testing purposes)", command=lambda: [quick_select_file()])
        button.pack()
        if data_is_loaded:
            button2 = tk.Button(self, text="View All Songs From JSON", command=lambda: [update_PageOne(), controller.show_frame("PageOne")])
            button2.pack()
            button3 = tk.Button(self, text="Select Songs To Ignore",
                                command=lambda: [update_PageTwo(), controller.show_frame("PageTwo")])
            button3.pack()
            button4 = tk.Button(self, text="Find Keyword Count In A Song",
                                command=lambda: [update_PageThree(), controller.show_frame("PageThree")])
            button4.pack()
        button5 = tk.Button(self, text="Exit Program",
                            command=lambda: [exit(0)])
        button5.pack()

        def select_file():
            global file_path
            global file_name
            global data
            global data_is_loaded
            global invalid_file
            file_path = askopenfilename()  # This gets full path
            file_name = ntpath.basename(file_path)  # This gets only the file name
            try:
                with open(file_path) as json_file:
                    data = json.load(json_file)
                data_is_loaded = True
                invalid_file = False
                update_StartPage()
            except:
                print("data not loaded, invalid file")
                data_is_loaded = False
                invalid_file = True
                update_StartPage()

        def update_StartPage():  # Removes need for refresh button
            app.frames["StartPage"].destroy()
            app.frames["StartPage"] = StartPage(parent, controller)
            app.frames["StartPage"].grid(row=0, column=0, sticky="nsew")

        def update_PageOne():
            app.frames["PageOne"].destroy()
            app.frames["PageOne"] = PageOne(parent, controller)
            app.frames["PageOne"].grid(row=0, column=0, sticky="nsew")

        def update_PageTwo():
            app.frames["PageTwo"].destroy()
            app.frames["PageTwo"] = PageTwo(parent, controller)
            app.frames["PageTwo"].grid(row=0, column=0, sticky="nsew")

        def update_PageThree():
            app.frames["PageThree"].destroy()
            app.frames["PageThree"] = PageThree(parent, controller)
            app.frames["PageThree"].grid(row=0, column=0, sticky="nsew")

        def quick_select_file():
            global file_path
            global file_name
            global data
            global data_is_loaded
            global invalid_file
            file_path = "C:\\Users\\marinom1\\PycharmProjects\\Song-Lyric-Analyzer\\Lyrics_Khalid_all.json"
            file_name = "Lyrics_Khalid_all.json"
            with open(file_path) as json_file: data = json.load(json_file)
            data_is_loaded = True
            invalid_file = False
            update_StartPage()


class PageOne(tk.Frame):  # View All Songs From JSON
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="List of songs in json")
        label.pack(side="top", fill="x", pady=10)
        listbox = Listbox(self, width=55)
        listbox.pack(side=LEFT, fill=BOTH)
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=LEFT, fill=BOTH)
        if data_is_loaded:
            list_of_songs = printAllSongsFromJSON(data)
            for i in range(len(list_of_songs)):
                listbox.insert(END, str(i)+": "+list_of_songs[i])

        listbox.config(yscrollcommand=scrollbar.set)
        bolded = font.Font(weight='bold')
        listbox.config(font=bolded)
        scrollbar.config(command=listbox.yview)

        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):  # Select Bad Song Indices
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select Bad Song Indices", font=controller.title_font)
        label.grid(row=0, column=1)
        button = tk.Button(self, text="Confirm",
                           command=lambda: [get_bad_indices(), controller.show_frame("StartPage")])
        button.grid(row=1, column=1)
        button1 = tk.Button(self, text="Cancel",
                           command=lambda: [controller.show_frame("StartPage")])
        button1.grid(row=2, column=1)
        checklist = tk.Text(self, height = 20, width=55, cursor="arrow")
        checklist.grid(row=3, column=1, rowspan=10)
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.grid(row=3, column=2, rowspan=10, sticky="NS")
        instructions = "Checking off a song will\nhide it from lists in\nother lyric analysis tools\nto prevent cluttered\n song lists"
        label = tk.Label(self, text=instructions)
        label.grid(row=5, column=0)


        if data_is_loaded:
            list_of_songs = printAllSongsFromJSON(data)
            button_statuses = []
            bolded = font.Font(weight='bold')
            for i in range(len(list_of_songs)):
                if i in bad_song_indices:
                    is_checked = tk.IntVar(value=1)
                else:
                    is_checked = tk.IntVar()
                button_statuses.append(is_checked)
                checkbutton = tk.Checkbutton(checklist, text=list_of_songs[i], variable=is_checked, font=bolded)
                checklist.window_create("end", window=checkbutton)
                checklist.insert("end", "\n")

            checklist.config(yscrollcommand=scrollbar.set, font=bolded)
            scrollbar.config(command=checklist.yview)

            # disable the widget so users can't insert text into it
            checklist.configure(state="disabled")

        def get_bad_indices():
            global bad_song_indices
            bad_song_indices = []
            for i in range(len(button_statuses)):
                if button_statuses[i].get() == 1:  # If 1, then it's a bad song index
                    print(i, "was checked")
                    bad_song_indices.append(i)


class PageThree(tk.Frame):  # Find Keyword Count In Song
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0)
        button1 = tk.Button(self, text="Search", command=lambda: [conduct_count()])
        button1.grid(row=0, column=5)
        message = tk.StringVar()
        label = tk.Label(self, text="Find Keyword Count In Song", font=controller.title_font)
        label.grid(row=0, column=3)
        label = tk.Label(self, textvariable=message, font=controller.medium_font)
        label.grid(row=6, column=3)
        label1 = tk.Label(self, text="Enter keyword you want to search and count")
        label1.grid(row=2, column=3)
        keyword_var = tk.StringVar()
        entry = tk.Entry(self, width=15, textvariable=keyword_var)
        entry.insert(END, "love")
        entry.grid(row=3, column=3)
        label2 = tk.Label(self, text="Select the song you want to search in")
        label2.grid(row=4, column=3)

        # Make scrollable so user can select ONE song
        checklist = tk.Text(self, height=15, width=55, cursor="arrow", bg = '#F0F0F0')
        checklist.grid(row=5, column=3)
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.grid(row=5, column=4, sticky='NS')
        radio_group = tk.IntVar(value=0)
        if data_is_loaded:
            list_of_songs = printGoodSongsFromJSON(data, bad_song_indices)
            bolded = font.Font(weight='bold')
            for i in range(len(list_of_songs)):
                radiobutton = Radiobutton(checklist, text=list_of_songs[i], variable=radio_group, value=i)
                checklist.window_create("end", window=radiobutton)
                checklist.insert("end", "\n")

            checklist.config(yscrollcommand=scrollbar.set, font=bolded)
            scrollbar.config(command=checklist.yview)

            # disable the widget so users can't insert text into it
            checklist.configure(state="disabled")


        def conduct_count():
            keyword_count = findKeywordCountInSong(data, keyword_var.get(), radio_group.get())
            message.set("The number of times \""+ keyword_var.get() + "\" is said in \n" + data['songs'][radio_group.get()]['title'] + " is: " + str(keyword_count))



if __name__ == "__main__":
    app = SongLyricAnalyzer()
    app.title('Song Lyric Analyzer')
    app.geometry("800x600")
    app.mainloop()