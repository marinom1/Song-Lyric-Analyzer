import os
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
        for F in (StartPage, ViewAllSongsFromJSON, SelectSongsToIgnore, FindKeywordCountInSong, FindKeywordCountInAllSongs, ViewLyrics,
                  FindKeyWordCountInSongByArtist, FindPhraseCountInSong):
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
        label1 = tk.Label(self, text=file_name, font=controller.title_font)
        label1.pack(side="top", fill="x", pady=10)
        number_of_bad_songs = 0
        if bad_song_indices:
            number_of_bad_songs = len(bad_song_indices)
            label2 = tk.Label(self, text="You selected " + str(number_of_bad_songs) + " songs to ignore", font=controller.title_font)
            label2.pack(side="top", fill="x", pady=10)
        if invalid_file:
            label2 = tk.Label(self, text="Please select a valid json file", font=controller.title_font)
            label2.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Select File", width=30,command=lambda: [select_file()])
        button1.pack()
        button = tk.Button(self, text="Quick Select File (For testing purposes)", width=30, command=lambda: [quick_select_file()])
        button.pack()
        if data_is_loaded:
            button2 = tk.Button(self, text="View All Songs From JSON", width=30,command=lambda: [update_ViewAllSongsFromJSON(), controller.show_frame("ViewAllSongsFromJSON")])
            button2.pack()
            button2 = tk.Button(self, text="View Song Lyrics", width=30,
                                command=lambda: [update_ViewLyrics(), controller.show_frame("ViewLyrics")])
            button2.pack()
            button3 = tk.Button(self, text="Select Songs To Ignore",width=30,
                                command=lambda: [update_SelectBadSongIndices(), controller.show_frame("SelectSongsToIgnore")])
            button3.pack()
            button4 = tk.Button(self, text="Find Keyword Count In A Song",width=30,
                                command=lambda: [update_FindKeywordCountInSong(), controller.show_frame("FindKeywordCountInSong")])
            button4.pack()
            button5 = tk.Button(self, text="Find Keyword Count In All Songs",width=30,
                                command=lambda: [update_FindKeywordCountInAllSongs(), controller.show_frame("FindKeywordCountInAllSongs")])
            button5.pack()
            button6 = tk.Button(self, text="Find Keyword Count In Song By Artist", width=30,
                                command=lambda: [update_FindKeyWordCountInSongByArtist(), controller.show_frame("FindKeyWordCountInSongByArtist")])
            button6.pack()
            button7 = tk.Button(self, text="Find Phrase Count In Song", width=30,
                                command=lambda: [update_FindPhraseCountInSong(),
                                                 controller.show_frame("FindPhraseCountInSong")])
            button7.pack()
        exit_button = tk.Button(self, text="Exit Program",width=30,
                            command=lambda: [exit(0)])
        exit_button.pack()

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

        def update_ViewAllSongsFromJSON():
            app.frames["ViewAllSongsFromJSON"].destroy()
            app.frames["ViewAllSongsFromJSON"] = ViewAllSongsFromJSON(parent, controller)
            app.frames["ViewAllSongsFromJSON"].grid(row=0, column=0, sticky="nsew")

        def update_SelectBadSongIndices():
            app.frames["SelectSongsToIgnore"].destroy()
            app.frames["SelectSongsToIgnore"] = SelectSongsToIgnore(parent, controller)
            app.frames["SelectSongsToIgnore"].grid(row=0, column=0, sticky="nsew")

        def update_FindKeywordCountInSong():
            app.frames["FindKeywordCountInSong"].destroy()
            app.frames["FindKeywordCountInSong"] = FindKeywordCountInSong(parent, controller)
            app.frames["FindKeywordCountInSong"].grid(row=0, column=0, sticky="nsew")

        def update_FindKeywordCountInAllSongs():
            app.frames["FindKeywordCountInAllSongs"].destroy()
            app.frames["FindKeywordCountInAllSongs"] = FindKeywordCountInAllSongs(parent, controller)
            app.frames["FindKeywordCountInAllSongs"].grid(row=0, column=0, sticky="nsew")

        def update_ViewLyrics():
            app.frames["ViewLyrics"].destroy()
            app.frames["ViewLyrics"] = ViewLyrics(parent, controller)
            app.frames["ViewLyrics"].grid(row=0, column=0, sticky="nsew")

        def update_FindKeyWordCountInSongByArtist():
            app.frames["FindKeyWordCountInSongByArtist"].destroy()
            app.frames["FindKeyWordCountInSongByArtist"] = FindKeyWordCountInSongByArtist(parent, controller)
            app.frames["FindKeyWordCountInSongByArtist"].grid(row=0, column=0, sticky="nsew")

        def update_FindPhraseCountInSong():
            app.frames["FindPhraseCountInSong"].destroy()
            app.frames["FindPhraseCountInSong"] = FindPhraseCountInSong(parent, controller)
            app.frames["FindPhraseCountInSong"].grid(row=0, column=0, sticky="nsew")

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


class ViewAllSongsFromJSON(tk.Frame):  # View All Songs From JSON
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="List of songs in json", font=controller.title_font)
        label.grid(row=0, column=1, columnspan=2)
        listbox = Listbox(self, height= 20, width=55)
        listbox.grid(row=1, column=1, columnspan=2)
        scrollbar = Scrollbar(self)
        scrollbar.grid(row=1, column=3, sticky="NSW")
        if data_is_loaded:
            list_of_songs = printAllSongsFromJSON(data)
            for i in range(len(list_of_songs)):
                listbox.insert(END, str(i)+": "+list_of_songs[i])

        listbox.config(yscrollcommand=scrollbar.set)
        bolded = font.Font(weight='bold')
        listbox.config(font=bolded)
        scrollbar.config(command=listbox.yview)

        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, sticky="NW")


class ViewLyrics(tk.Frame):  # View Song Lyrics
    def __init__(self, parent, controller):
        def selected_item(event):
            selected_song.set(listbox1.get(listbox1.curselection()))
            song_index = listbox1.get(0, "end").index(selected_song.get())
            text.configure(state="normal")
            text.delete(1.0, "end")
            text.insert(END, data['songs'][song_index]['lyrics'])
            text.configure(state="disabled")

        def do_popup(event):
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, sticky="NW")
        label = tk.Label(self, text="View Song Lyrics", font=controller.title_font)
        label.grid(row=0, column=1, columnspan=2)
        label1 = tk.Label(self, text="Click a song to see its lyrics")
        label1.grid(row=1, column=0)
        listbox1 = Listbox(self, height=32, width=30)
        listbox1.grid(row=2, column=0)
        scrollbar1 = Scrollbar(self)
        scrollbar1.grid(row=2, column=1, sticky="NSW")
        if data_is_loaded:
            list_of_songs = printAllSongsFromJSON(data)
            for i in range(len(list_of_songs)):
                listbox1.insert(END, str(i) + ": " + list_of_songs[i])
        selected_song = tk.StringVar()
        selected_song.set("No selection yet")
        label = tk.Label(self, textvariable=selected_song, font=controller.title_font)
        label.grid(row=1, column=2)
        listbox1.config(yscrollcommand=scrollbar1.set)
        listbox1.bind('<<ListboxSelect>>', selected_item)
        scrollbar1.config(command=listbox1.yview)

        # The Text widget to display the lyrics in
        genius_font=tkfont.Font(family="Programme", size=14)
        text = Text(self, wrap="word", height=17, width=52)
        text.grid(row=2, column=2)
        scrollbar2 = Scrollbar(self)
        scrollbar2.grid(row=2, column=3, sticky="NSW")
        scrollbar2.config(command=text.yview)
        text['yscrollcommand'] = scrollbar2.set
        text.configure(font=genius_font, spacing1=4, spacing2=4, spacing3=4)
        # Right click menu to copy
        m = Menu(self, tearoff=0)
        m.add_command(label="Copy")
        text.bind("<Button-3>", do_popup)


class SelectSongsToIgnore(tk.Frame):  # Select Songs To Ignore
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, columnspan=2, sticky="NW")
        label = tk.Label(self, text="Presets:", font=controller.medium_font)
        label.grid(row=1, column=0, columnspan=2)
        # Show presets, if any
        there_are_existing_presets, loaded_presets = load_existing_presets()
        if there_are_existing_presets:
            for i in range(len(loaded_presets['presets'])):
                button = tk.Button(self, text=loaded_presets['presets'][i]['name'], command=lambda name=i: [set_bad_song_indices(name), update_StartPage(), controller.show_frame("StartPage")])
                button.grid(row=i+2, column=0)
                button = tk.Button(self, text="Del " + loaded_presets['presets'][i]['name'],command=lambda name=-i: [delete_preset(name), update_SelectBadSongIndices()])
                button.grid(row=i+2, column=1)
        label = tk.Label(self, text="Select Songs To Ignore", font=controller.title_font)
        label.grid(row=0, column=2)
        button = tk.Button(self, text="Confirm and make preset",
                           command=lambda: [get_bad_indices_and_save_to_file(), controller.show_frame("StartPage")])
        button.grid(row=3, column=3)
        label = tk.Label(self, text="Make a new Preset")
        label.grid(row=0, column=3)
        label = tk.Label(self, text="Name of preset: ")
        label.grid(row=1, column=3)
        preset_name_var = tk.StringVar()
        entry = tk.Entry(self, width=15, textvariable=preset_name_var)
        entry.insert(END, "Khalid")
        entry.grid(row=2, column=3)
        button = tk.Button(self, text="Confirm",
                           command=lambda: [get_bad_indices(), update_StartPage(), controller.show_frame("StartPage")])
        button.grid(row=2, column=2)
        checklist = tk.Text(self, height = 20, width=55, cursor="arrow")
        checklist.grid(row=4, column=2, rowspan=10, columnspan=2)
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.grid(row=4, column=4, rowspan=10, sticky="NSW")
        instructions = "Checking off a song will\nhide it from lists in\nother lyric analysis tools\nto prevent cluttered\n song lists and to\nignore songs in searches"
        label = tk.Label(self, text=instructions)
        label.grid(row=i+6, column=0, columnspan=2)
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

            def _on_mousewheel(event):
                checklist.yview_scroll(int(-1 * (event.delta / 120)), "units")

            checklist.bind_all("<MouseWheel>", _on_mousewheel)
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

        def get_bad_indices_and_save_to_file():
            global bad_song_indices
            bad_song_indices = []
            for i in range(len(button_statuses)):
                if button_statuses[i].get() == 1:  # If 1, then it's a bad song index
                    print(i, "was checked")
                    bad_song_indices.append(i)
            # now save to file
            there_are_existing_presets, loaded_presets = load_existing_presets()
            # if there aren't any existing profiles in profiles.json
            if there_are_existing_presets == False:
                # Must create the json object from scratch first since it does not exist yet
                data = {}
                data['presets'] = []

                # Now append to profiles.json
                data['presets'].append({
                    'name': preset_name_var.get(),
                    'bad_song_indices': bad_song_indices
                })
                with open('presets.json', 'w') as outfile:
                    json.dump(data, outfile, indent=2, sort_keys=False)

            # else if there are already existing profiles in profiles.json
            elif there_are_existing_presets == True:
                # Simply append the new profile data to the profiles.json file
                loaded_presets['presets'].append({
                    'name': preset_name_var.get(),
                    'bad_song_indices': bad_song_indices
                })
                with open('presets.json', 'w') as outfile:
                    json.dump(loaded_presets, outfile, indent=2, sort_keys=False)

        def set_bad_song_indices(name):
            #name is index of preset in json
            global bad_song_indices
            bad_song_indices = loaded_presets["presets"][name]["bad_song_indices"]
            print("bad song indices is now:", bad_song_indices)

        def update_StartPage():  # Removes need for refresh button
            app.frames["StartPage"].destroy()
            app.frames["StartPage"] = StartPage(parent, controller)
            app.frames["StartPage"].grid(row=0, column=0, sticky="nsew")

        def update_SelectBadSongIndices():  # Removes need for refresh button
            app.frames["SelectSongsToIgnore"].destroy()
            app.frames["SelectSongsToIgnore"] = SelectSongsToIgnore(parent, controller)
            app.frames["SelectSongsToIgnore"].grid(row=0, column=0, sticky="nsew")

        def delete_preset(index):
            with open('presets.json', 'r') as outfile:
                loaded_presets = json.load(outfile)

            del loaded_presets["presets"][index]
            os.remove("presets.json")
            with open("presets.json", "w") as file:
                json.dump(loaded_presets, file, indent=2, sort_keys=False)
            # controller.show_frame("PageEleven")


class FindKeywordCountInSong(tk.Frame):  # Find Keyword Count In Song
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, sticky="NW")
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
        entry.insert(END, "time")
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
                if i not in bad_song_indices:
                    checklist.window_create("end", window=radiobutton)
                    checklist.insert("end", "\n")

            checklist.config(yscrollcommand=scrollbar.set, font=bolded)
            def _on_mousewheel(event):
                checklist.yview_scroll(int(-1 * (event.delta / 120)), "units")
            checklist.bind_all("<MouseWheel>", _on_mousewheel)
            scrollbar.config(command=checklist.yview)

            # disable the widget so users can't insert text into it
            checklist.configure(state="disabled")


        def conduct_count():
            keyword_count = findKeywordCountInSong(data, keyword_var.get(), radio_group.get())
            message.set("The number of times \""+ keyword_var.get() + "\" is said in \n" + data['songs'][radio_group.get()]['title'] + " is: " + str(keyword_count))


class FindKeywordCountInAllSongs(tk.Frame):  # Find Keyword Count In All Songs
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, sticky="NW")
        button1 = tk.Button(self, text="Search", command=lambda: [conduct_count()])
        button1.grid(row=0, column=5)
        message = tk.StringVar()
        label = tk.Label(self, text="Find Keyword Count In All Songs", font=controller.title_font)
        label.grid(row=0, column=3)
        label = tk.Label(self, textvariable=message, font=controller.medium_font)
        label.grid(row=6, column=3)
        label1 = tk.Label(self, text="Enter keyword you want to search and count")
        label1.grid(row=2, column=3)
        keyword_var = tk.StringVar()
        entry = tk.Entry(self, width=15, textvariable=keyword_var)
        entry.insert(END, "time")
        entry.grid(row=3, column=3)
        label2 = tk.Label(self, text="List of songs that will be included in the count")
        label2.grid(row=4, column=3)

        # Listbox and scrollbar to show songs program will count in
        listbox = Listbox(self, width=55)
        listbox.grid(row=5, column=3)
        scrollbar = Scrollbar(self)
        scrollbar.grid(row=5, column=4, sticky='NS')
        if data_is_loaded:
            list_of_songs = printGoodSongsFromJSON(data, bad_song_indices)
            for i in range(len(list_of_songs)):
                listbox.insert(END, str(i) + ": " + list_of_songs[i])

        listbox.config(yscrollcommand=scrollbar.set)
        bolded = font.Font(weight='bold')
        listbox.config(font=bolded)
        scrollbar.config(command=listbox.yview)


        def conduct_count():
            keyword_count = findKeywordCountInAllSongs(data, keyword_var.get(), bad_song_indices)
            message.set("The number of times \""+ keyword_var.get() + "\" is said is: " + str(keyword_count))


class FindKeyWordCountInSongByArtist(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, sticky="NW")
        button1 = tk.Button(self, text="Search", command=lambda: [conduct_count()])
        button1.grid(row=0, column=5)
        message = tk.StringVar()
        label = tk.Label(self, text="Find Keyword Count In Song By Artist", font=controller.title_font)
        label.grid(row=0, column=3)
        label = tk.Label(self, textvariable=message, font=controller.medium_font)
        label.grid(row=8, column=3)
        label1 = tk.Label(self, text="Enter keyword you want to search and count")
        label1.grid(row=2, column=3)
        keyword_var = tk.StringVar()
        entry1 = tk.Entry(self, width=15, textvariable=keyword_var)
        entry1.insert(END, "time")
        entry1.grid(row=3, column=3)
        label2 = tk.Label(self, text="Enter the Artist's name")
        label2.grid(row=4, column=3)
        artist_var = tk.StringVar()
        entry2 = tk.Entry(self, width=15, textvariable=artist_var)
        entry2.insert(END, "Khalid")
        entry2.grid(row=5, column=3)
        label3 = tk.Label(self, text="Select the song you want to search in")
        label3.grid(row=6, column=3)

        # Make scrollable so user can select ONE song
        checklist = tk.Text(self, height=15, width=55, cursor="arrow", bg = '#F0F0F0')
        checklist.grid(row=7, column=3)
        scrollbar = tk.Scrollbar(self, orient="vertical")
        scrollbar.grid(row=7, column=4, sticky='NS')
        radio_group = tk.IntVar(value=0)
        if data_is_loaded:
            list_of_songs = printGoodSongsFromJSON(data, bad_song_indices)
            bolded = font.Font(weight='bold')
            for i in range(len(list_of_songs)):
                radiobutton = Radiobutton(checklist, text=list_of_songs[i], variable=radio_group, value=i)
                if i not in bad_song_indices:
                    checklist.window_create("end", window=radiobutton)
                    checklist.insert("end", "\n")

            checklist.config(yscrollcommand=scrollbar.set, font=bolded)
            def _on_mousewheel(event):
                checklist.yview_scroll(int(-1 * (event.delta / 120)), "units")
            checklist.bind_all("<MouseWheel>", _on_mousewheel)
            scrollbar.config(command=checklist.yview)

            # disable the widget so users can't insert text into it
            checklist.configure(state="disabled")

        def conduct_count():
            keyword_count = findKeywordCountInSongByArtist(data, keyword_var.get(), radio_group.get(), artist_var.get())
            message.set("The number of times \""+ keyword_var.get() + "\" is said in \n" + data['songs'][radio_group.get()]['title'] + " by " + artist_var.get() +  " is: " + str(keyword_count))


class FindPhraseCountInSong(tk.Frame): # Find Phrase Count In Song
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("StartPage"))
        button.grid(row=0, column=0, sticky="NW")
        button1 = tk.Button(self, text="Search", command=lambda: [conduct_count()])
        button1.grid(row=0, column=5)
        message = tk.StringVar()
        label = tk.Label(self, text="Find Phrase Count In Song", font=controller.title_font)
        label.grid(row=0, column=3)
        label = tk.Label(self, textvariable=message, font=controller.medium_font)
        label.grid(row=6, column=3)
        label1 = tk.Label(self, text="Enter Phrase you want to search and count")
        label1.grid(row=2, column=3)
        phrase_var = tk.StringVar()
        entry = tk.Entry(self, width=15, textvariable=phrase_var)
        entry.insert(END, "my time")
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
                if i not in bad_song_indices:
                    checklist.window_create("end", window=radiobutton)
                    checklist.insert("end", "\n")

            checklist.config(yscrollcommand=scrollbar.set, font=bolded)
            def _on_mousewheel(event):
                checklist.yview_scroll(int(-1 * (event.delta / 120)), "units")
            checklist.bind_all("<MouseWheel>", _on_mousewheel)
            scrollbar.config(command=checklist.yview)

            # disable the widget so users can't insert text into it
            checklist.configure(state="disabled")


        def conduct_count():
            keyword_count = findPhraseCountInSong(data, phrase_var.get(), radio_group.get())
            message.set("The number of times \""+ phrase_var.get() + "\" is said in \n" + data['songs'][radio_group.get()]['title'] + " is: " + str(keyword_count))



if __name__ == "__main__":
    app = SongLyricAnalyzer()
    app.title('Song Lyric Analyzer')
    app.geometry("800x600")
    app.mainloop()

