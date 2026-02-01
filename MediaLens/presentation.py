import customtkinter as ctk

# ===== THEME =====
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

BG_MAIN = "#0f172a"
CARD_BG = "#1e293b"
NAV_ACTIVE_BG = "#1e3a8a"
NAV_NORMAL_BG = "transparent"


# ===== APP =====
class MediaLensPresentation:
    def __init__(self):
        self.nav_buttons = {}
        self.font_title = 40
        self.font_header = 34
        self.font_body = 22

        self.wrap_width = 1100

        ctk.set_widget_scaling(1.4)
        ctk.set_window_scaling(1.4)

        self.root = ctk.CTk()
        self.root.title("MediaLens AI — SOČ prezentácia")
        self.root.geometry("1200x750")
        self.root.attributes('-fullscreen', True)
        self.root.minsize(1100, 700)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_main()

        self.title()

    # ===== LAYOUT =====
    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.root, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebar,
            text="MediaLens AI",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(30, 20))

        self.add_nav("SOČ", self.title, "soc")
        self.add_nav("Problematika", self.problem, "problem")
        self.add_nav("Cieľ práce", self.goal, "goal")
        self.add_nav("Technológie a postup", self.tech, "tech")
        self.add_nav("Systém MediaLens", self.medialens, "medialens")
        self.add_nav("Výsledky a overenie", self.functionality, "functionality")
        self.add_nav("Ukážka", self.video, "video")
        self.add_nav("Závery a prínos práce", self.results, "results")
        self.add_nav("Plány a budúci rozvoj", self.future, "future")
        self.add_nav("      Rozšírenie datasetu", self.future_data, "future_data")
        self.add_nav("      Hlbšia analýza", self.future_anal, "future_anal")
        self.add_nav("      Optimalizácia modelov", self.future_model, "future_model")
        self.add_nav("Koniec", self.thanks, "thanks")

    def add_nav(self, text, cmd, key):
        btn = ctk.CTkButton(
            self.sidebar,
            text=text,
            fg_color=NAV_NORMAL_BG,
            hover_color=NAV_ACTIVE_BG,
            anchor="w",
            command=lambda: self.activate_nav(key, cmd)
        )
        btn.pack(fill="x", padx=20, pady=6)
        self.nav_buttons[key] = btn

    def activate_nav(self, key, cmd):
        # reset všetkých
        for b in self.nav_buttons.values():
            b.configure(fg_color=NAV_NORMAL_BG)

        # zvýrazni aktívny
        self.nav_buttons[key].configure(fg_color=NAV_ACTIVE_BG)

        # zobraz slide
        cmd()

    def build_main(self):
        self.main = ctk.CTkFrame(self.root, fg_color=BG_MAIN, corner_radius=15)
        self.main.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def clear_main(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ===== UI HELPERS =====
    def header(self, text):
        ctk.CTkLabel(
            self.main,
            text=text,
            font=ctk.CTkFont(size=self.font_header, weight="bold"),
            wraplength=self.wrap_width,
            justify="left"
        ).pack(anchor="w", padx=50, pady=(40, 25))

    def card(self):
        frame = ctk.CTkFrame(self.main, fg_color=CARD_BG, corner_radius=16)
        frame.pack(fill="both", expand=True, padx=40, pady=20)
        return frame

    def bullet(self, parent, text):
        ctk.CTkLabel(
            parent,
            text="• " + text,
            font=ctk.CTkFont(size=self.font_body),
            wraplength=self.wrap_width,
            justify="left"
        ).pack(anchor="w", padx=50, pady=8)

    def tab_bullet(self, parent, text):
        ctk.CTkLabel(
            parent,
            text="• " + text,
            font=ctk.CTkFont(size=self.font_body - 2),
            wraplength=self.wrap_width,
            justify="left"
        ).pack(anchor="w", padx=70, pady=6)

    def section(self, parent, text):
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=self.font_body + 2, weight="bold"),
            wraplength=self.wrap_width,
            justify="left"
        ).pack(anchor="w", padx=50, pady=(18, 6))

    def spacer(self, parent, h=10):
        ctk.CTkFrame(parent, fg_color="transparent", height=h).pack(fill="x")

    # ===== SLIDES =====
    def title(self):
        self.clear_main()
        self.header("Súkromná stredná odborná škola, Ul. 29 Augusta 4812, Poprad")
        card = self.card()

        self.bullet(card, "Využitie hybridných NLP modelov pri detekcii manipulatívnych techník v mediálnych titulkoch")
        self.bullet(card, "Leo Ondrejka")
        self.bullet(card, "Č. odboru: 11 - Informatika")

    def problem(self):
        self.clear_main()
        self.header("Problematika")
        card = self.card()

        self.bullet(card, "Informačné preťaženie")
        self.bullet(card, "Kognitívne skraty")
        self.bullet(card, "Vplyv na verejnú mienku")

    def goal(self):
        self.clear_main()
        self.header("Cieľ práce")
        card = self.card()

        self.bullet(card, "Vytvoriť funkčný prototyp detekčného systému")
        self.bullet(card, "Zamerať sa na slovenský jazyk")
        self.bullet(card, "Kombinovať prístupy:")
        self.tab_bullet(card, "Lexikálny")
        self.tab_bullet(card, "Kontextový")

    def tech(self):
        self.clear_main()
        self.header("Použité technológie a postup")
        card = self.card()

        self.bullet(card, "Jazyk: Python")
        self.bullet(card, "Knižnice: Scikit-Learn, Transformers, Torch")
        self.bullet(card, "Hybridný model:")
        self.tab_bullet(card, "TF-IDF: Štatistika slov.")
        self.tab_bullet(card, "BERT: Hlboké učenie.")
        self.bullet(card, "Klasifikátor: Random Forest")
        self.bullet(card, "Dáta: Vlastný zber + augmentácia")

    def medialens(self):
        self.clear_main()
        self.header("Systém MediaLens")
        card = self.card()

        self.bullet(card, "Desktopová aplikácia: Na tréning a analýzu textu")
        self.bullet(card, "Rozšírenie do prehliadača: Okamžitá kontrola pri čítaní webu")
        self.bullet(card, "Self-learning modul:")
        self.tab_bullet(card, "Model sa „doučuje“ za behu")
        self.tab_bullet(card, "Bezpečnostná poistka: Učí sa len pri istote > 85 %")

    def functionality(self):
        self.clear_main()
        self.header("Výsledky a overenie")
        card = self.card()

        self.bullet(card, "Úspešnosť AI:")
        self.tab_bullet(card, "Vysoká pri clickbaite a dramatizácii (zjavné znaky)")
        self.tab_bullet(card, "Nižšia pri jemných logických klamoch (subtílna manipulácia).")
        self.bullet(card, "Dotazníkový prieskum (90+ respondentov):")
        self.tab_bullet(card, "Ľudia tiež zlyhávajú pri jemnej manipulácii.")

    def video(self):
        self.clear_main()
        self.header("Ukážka Systému")
        card = self.card()

    def results(self):
        self.clear_main()
        self.header("Závery a prínos práce")
        card = self.card()

        self.bullet(card, "Splnenie cieľov: Funkčný prototyp pre slovenský jazyk")
        self.bullet(card, "Hlavný prínos:")
        self.tab_bullet(card, "Podpora mediálnej gramotnosti (nie cenzúra)")
        self.tab_bullet(card, "Rozvoj kritického myslenia")
        self.tab_bullet(card, "Nástroj pre vzdelávanie a rýchlu orientáciu")

    def future(self):
        self.clear_main()
        self.header("Plány a budúci rozvoj")
        card = self.card()

        self.bullet(card, "Rozšírenie datasetu")
        self.bullet(card, "Hlbšia analýza")
        self.bullet(card, "Optimalizácia modelov")

    def future_data(self):
        self.clear_main()
        self.header("Rozšírenie datasetu")
        card = self.card()

        self.bullet(card, "Zber väčšieho množstva dát pre lepšiu generalizáciu")
        self.bullet(card, "Vyváženie tried (viac manipulatívnych príkladov).")

    def future_anal(self):
        self.clear_main()
        self.header("Hlbšia analýza:")
        card = self.card()

        self.bullet(card, "Prechod z titulkov na analýzu celých článkov.")
        self.bullet(card, "Overovanie faktov (fact-checking) voči externým zdrojom.")

    def future_model(self):
        self.clear_main()
        self.header("Optimalizácia modelov ")
        card = self.card()

        self.bullet(card, "TF-IDF + SVM (Support Vector Machine).")
        self.bullet(card, "BERT + Logistic Regression.")
        self.bullet(card, "MLP (Multi-Layer Perceptron - neurónové siete).")

    def thanks(self):
        self.clear_main()
        self.header("Ďakujem za pozornosť")
        card = self.card()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    MediaLensPresentation().run()
