from functions.utils import *

class App(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.screen = None
        self.messages = config()
        self.email_var = ctk.StringVar(value=self.messages["entrys"]["email"])
        self.name_var = ctk.StringVar(value=self.messages["entrys"]["name"])
        self.lastname_var = ctk.StringVar(value=self.messages["entrys"]["lastname"])
        self.post_var = ctk.StringVar(value=self.messages["entrys"]["post"])
        self.age_var = ctk.StringVar(value="0")
        self.setup_ui()

    def setup_ui(self):
        self.pantalla = ctk.CTkFrame(self, width=600, height=300, corner_radius=5)
        self.geometry("600x300+1970+200")
        self.title(self.messages["title_screen"])
        self.maxsize(width=600, height=300)
        self.minsize(width=600, height=300)

        self.create_labels()
        self.create_inputs()
        self.pantalla.pack()

    def create_labels(self):
        title = ctk.CTkLabel(self.screen, text=self.messages["title"], fg_color="gray", text_color="black", width=50, height=50, corner_radius=10)
        title.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

    def create_inputs(self):

        self.name_input = ctk.CTkEntry(self.screen, textvariable=self.name_var, text_color="black", fg_color="white")
        self.name_input.place(relx=0.2, rely=0.3, anchor=ctk.CENTER)

        self.lastname_input = ctk.CTkEntry(self.screen, textvariable=self.lastname_var, text_color="black", fg_color="white")
        self.lastname_input.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        self.email_input = ctk.CTkEntry(self.screen, textvariable=self.email_var, text_color="black", fg_color="white")
        self.email_input.place(relx=0.2, rely=0.5, anchor=ctk.CENTER)

        self.post_input = ctk.CTkEntry(self.screen, textvariable=self.post_var, text_color="black", fg_color="white")
        self.post_input.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.age_input = ctk.CTkEntry(self.screen, textvariable=self.age_var, text_color="black", fg_color="white")
        self.age_input.place(relx=0.2, rely=0.7, anchor=ctk.CENTER)

        self.name_input.bind("<FocusIn>", lambda event: clear_text(event, self.name_input, self.messages["entrys"]["name"]))
        self.lastname_input.bind("<FocusIn>", lambda event: clear_text(event, self.lastname_input, self.messages["entrys"]["lastname"]))
        self.email_input.bind("<FocusIn>", lambda event: clear_text(event, self.email_input, self.messages["entrys"]["email"]))
        self.post_input.bind("<FocusIn>", lambda event: clear_text(event, self.post_input, self.messages["entrys"]["post"]))

        self.name_input.bind("<FocusOut>", lambda event: restore_text(event, self.name_input, self.messages["entrys"]["name"]))
        self.lastname_input.bind("<FocusOut>", lambda event: restore_text(event, self.lastname_input, self.messages["entrys"]["lastname"]))
        self.email_input.bind("<FocusOut>", lambda event: restore_text(event, self.email_input, self.messages["entrys"]["email"]))
        self.post_input.bind("<FocusOut>", lambda event: restore_text(event, self.post_input, self.messages["entrys"]["post"]))

        self.button = ctk.CTkButton(self.screen, text="ADD", width=100, height=50, corner_radius=10, border_color="white", text_color="black", command=lambda: self.clicked_button(self.email_input.get(), self.name_input.get(), self.lastname_input.get(), self.post_input.get(), self.age_input.get()))
        self.button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        self.button_search = ctk.CTkButton(self.screen, text="Search", width=100, height=30, corner_radius=8, text_color="black", command=self.screen_search)
        self.button_search.place(relx=0.8, rely=0.3, anchor=ctk.CENTER)

    def clicked_button(self, entry_email, entry_name, entry_lastname, entry_post, entry_age):
        if not check_email(self, entry_email):
            messagebox(message=self.messages["errors"]["email_invalid"], icon="warning", option_1="Retry")
            return

        if check_name_db(self, entry_name):
            messagebox(message=self.messages["errors"]["user_invalid"], icon="warning", option_1="Retry")
            return

        if check_email_db(self, entry_email):
            messagebox(message=self.messages["errors"]["email_registered"], icon="warning", option_1="Retry")
            return

        if not entry_age.isdigit():
            messagebox(message=self.messages["errors"]["error_number"], icon="warning", option_1="Retry")
            return

        add_employee(None, entry_email, entry_name, entry_lastname, entry_post, entry_age)


    def screen_search(self):
        disabled_all(self)
        new_screen = ctk.CTkToplevel()
        new_screen.title(self.messages["title_screen_search"])
        new_screen.geometry("300x100+1440+200")
        new_screen.maxsize(width=300, height=100)
        new_screen.minsize(width=300, height=100)

        search_title = ctk.CTkLabel(new_screen, text=self.messages["title_search"], text_color="white")
        search_title.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        search_title.pack()

        search_email = ctk.CTkEntry(new_screen, textvariable=self.email_var)
        search_email.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)
        search_email.bind("<FocusIn>", lambda event: clear_text(event, search_email, self.messages["entrys"]["email"]))
        search_email.bind("<FocusOut>", lambda event: restore_text(event, search_email, self.messages["entrys"]["email"]))
        search_email.pack()

        button_search = ctk.CTkButton(new_screen, text="Search", width=100, height=30, corner_radius=8, command=lambda: search_employee(search_email.get()))
        button_search.place(relx=0.5, rely=1, anchor=ctk.CENTER)
        button_search.pack()

        new_screen.wait_window()
        enabled_all(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()