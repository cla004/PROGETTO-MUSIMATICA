import customtkinter as ctk # Grafica moderna
import pygame # Audio interno
import threading # Per non bloccare la finestra durante i calcoli
from motore_musicale.traduttore import genera_spartito_guidoniano, MAPPA_NOTE 
from motore_musicale.gioco_dadi import genera_musica_dadi 

class FinestraPrincipale(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Musimatica: Guido d'Arezzo & Mozart")
        self.geometry("850x850")
        pygame.mixer.init()

        # --- HEADER ---
        self.label_titolo = ctk.CTkLabel(self, text="SISTEMI COMPOSITIVI ALGORITMICI", 
                                         font=ctk.CTkFont(size=26, weight="bold"))
        self.label_titolo.pack(pady=20)

        # --- TABVIEW (Navigazione Schede) ---
        self.tabview = ctk.CTkTabview(self, width=750, height=200, command=self.gestisci_cambio_tab)
        self.tabview.pack(padx=20, pady=10)
        
        self.tab_guido = self.tabview.add("Metodo Guido d'Arezzo")
        self.tab_mozart = self.tabview.add("Gioco dei Dadi (Mozart)")

        # --- SCHEDA GUIDO ---
        self.entry_testo = ctk.CTkEntry(self.tab_guido, width=450, placeholder_text="Inserisci testo per il Soggetto Cavato...")
        self.entry_testo.pack(pady=10)
        self.entry_testo.bind("<KeyRelease>", self.logica_guido)
        
        self.btn_info_guido = ctk.CTkButton(self.tab_guido, text="ℹ️ INFO ALGORITMO", 
                                             command=self.mostra_info_guido, fg_color="#555", width=140)
        self.btn_info_guido.pack(pady=5)

        # --- SCHEDA MOZART ---
        self.btn_roll = ctk.CTkButton(self.tab_mozart, text="🎲 GENERA SEQUENZA ALEATORIA", 
                                       command=self.logica_mozart, fg_color="#9b59b6", font=ctk.CTkFont(weight="bold"), width=250)
        self.btn_roll.pack(pady=10)
        
        self.btn_info_mozart = ctk.CTkButton(self.tab_mozart, text="ℹ️ INFO ALGORITMO", 
                                              command=self.mostra_info_mozart, fg_color="#555", width=140)
        self.btn_info_mozart.pack(pady=5)

        # --- CONSOLE DI ANALISI (COMUNE) ---
        self.label_analisi = ctk.CTkLabel(self, text="LOGICA E ANALISI DELL'ALGORITMO ATTIVO:", font=ctk.CTkFont(size=12, weight="bold"))
        self.label_analisi.pack(pady=(10, 0))
        self.box_analisi = ctk.CTkTextbox(self, width=720, height=250, font=ctk.CTkFont(family="Courier", size=13))
        self.box_analisi.pack(pady=10)
        self.box_analisi.configure(state="disabled")

        # --- CONTROLLI COMUNI ---
        self.frame_controlli = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_controlli.pack(pady=20)

        self.btn_spartito = ctk.CTkButton(self.frame_controlli, text="VEDI SPARTITO", command=self.mostra_spartito, width=180)
        self.btn_spartito.grid(row=0, column=0, padx=10)

        self.btn_audio = ctk.CTkButton(self.frame_controlli, text="ASCOLTA AUDIO", command=self.riproduci_audio, fg_color="#2ecc71", width=180)
        self.btn_audio.grid(row=0, column=1, padx=10)

        self.btn_stop = ctk.CTkButton(self.frame_controlli, text="STOP", command=lambda: pygame.mixer.music.stop(), fg_color="#e74c3c", width=180)
        self.btn_stop.grid(row=0, column=2, padx=10)

        self.status = ctk.CTkLabel(self, text="Pronto.", text_color="gray")
        self.status.pack(side="bottom", pady=10)
        self.partitura_attuale = None

    # --- POP-UP INFO ---

    def mostra_info_guido(self):
        w = ctk.CTkToplevel(self)
        w.title("Info: Guido d'Arezzo")
        w.geometry("500x300")
        w.attributes("-topmost", True)
        t = ("TEORIA DI GUIDO D'AREZZO\n\n"
             "L'algoritmo utilizza la tecnica del 'Soggetto Cavato'.\n"
             "Estrae le vocali dal testo e le mappa sull'esacordo guidoniano.\n\n"
             "Mappatura: A=Do | E=Re | I=Mi | O=Fa | U=Sol\n\n"
             "Sistema DETERMINISTICO.")
        ctk.CTkLabel(w, text=t, justify="left", padx=20, pady=20).pack()

    def mostra_info_mozart(self):
        w = ctk.CTkToplevel(self)
        w.title("Info: Mozart")
        w.geometry("500x300")
        w.attributes("-topmost", True)
        t = ("IL GIOCO DEI DADI (MOZART)\n\n"
             "Sistema di composizione STOCASTICA basato sulla combinatoria.\n"
             "Il lancio di due dadi seleziona battute pre-scritte compatibili.\n\n"
             "Ogni battuta rispetta le regole dell'armonia del XVIII secolo.\n"
             "Sistema ALEATORIO.")
        ctk.CTkLabel(w, text=t, justify="left", padx=20, pady=20).pack()

    # --- LOGICHE DI GESTIONE ---

    def gestisci_cambio_tab(self):
        if self.tabview.get() == "Metodo Guido d'Arezzo":
            self.logica_guido()
        else:
            self.pulisci_console()

    def pulisci_console(self):
        self.box_analisi.configure(state="normal")
        self.box_analisi.delete("1.0", "end")
        self.box_analisi.configure(state="disabled")

    def logica_guido(self, event=None):
        self.pulisci_console()
        testo = self.entry_testo.get()
        if testo.strip():
            self.box_analisi.configure(state="normal")
            analisi = [f" • Vocale '{c}' -> Nota: {MAPPA_NOTE[c]}" for c in testo.lower() if c in MAPPA_NOTE]
            header = "🔍 ANALISI GUIDO D'AREZZO\n" + "-"*45 + "\n"
            self.box_analisi.insert("1.0", header + "\n".join(analisi))
            self.box_analisi.configure(state="disabled")
            self.partitura_attuale = genera_spartito_guidoniano(testo)

    def logica_mozart(self):
        """Genera il report dei dadi usando d1 e d2 dal tuo dizionario."""
        self.pulisci_console()
        
        def task():
            # p è lo spartito, dettagli è la lista che contiene i tuoi dizionari
            p, dettagli = genera_musica_dadi() 
            self.partitura_attuale = p
            
            self.box_analisi.configure(state="normal")
            
            report = "🎲 REPORT DI COMPOSIZIONE ALEATORIA (MOZART)\n" + "="*45 + "\n\n"
            
            for d in dettagli:
                # Usiamo d['dado1'] e d['dado2'] come hai impostato tu
                report += f"BATTUTA {d['battuta']}: Tiri [{d['dado1']} + {d['dado2']}] = Somma {d['somma']}\n"
                report += f"  > Note Prodotte: {', '.join(d['note'])}\n"
                report += "-"*40 + "\n"
            
            # Inseriamo il testo nella console e blocchiamo la modifica
            self.box_analisi.insert("1.0", report)
            self.box_analisi.configure(state="disabled")
            self.status.configure(text="Dadi lanciati! Melodia generata.", text_color="purple")
            
        threading.Thread(target=task, daemon=True).start()

    # --- FUNZIONI COMUNI ---

    def mostra_spartito(self):
        if self.partitura_attuale:
            threading.Thread(target=self.partitura_attuale.show, args=('musicxml',), daemon=True).start()

    def riproduci_audio(self):
        if self.partitura_attuale:
            def task():
                self.partitura_attuale.write('midi', fp="temp.mid")
                pygame.mixer.music.load("temp.mid")
                pygame.mixer.music.play()
            threading.Thread(target=task, daemon=True).start()