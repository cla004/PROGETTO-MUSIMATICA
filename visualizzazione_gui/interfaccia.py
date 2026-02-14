import customtkinter as ctk # Importa la libreria per l'interfaccia grafica moderna
import pygame # Libreria per gestire la riproduzione audio interna
import os # Libreria per la gestione dei file sul sistema operativo
import threading # Libreria fondamentale per eseguire processi in parallelo ed evitare blocchi
from motore_musicale.traduttore import genera_spartito_guidoniano, MAPPA_NOTE # Importa la logica musicale e i dati

ctk.set_appearance_mode("Dark") # Imposta il tema scuro dell'interfaccia
ctk.set_default_color_theme("blue") # Imposta il blu come colore predefinito dei componenti

class FinestraPrincipale(ctk.CTk): # Inizia la definizione della classe della finestra principale
    def __init__(self): # Metodo di inizializzazione dell'applicazione
        super().__init__() # Esegue il costruttore della classe base CustomTkinter
        self.title("Guido d'Arezzo Digital Composer Pro") # Imposta il titolo della finestra
        self.geometry("800x650") # Imposta le dimensioni della finestra per ospitare i nuovi elementi
        
        pygame.mixer.init() # Inizializza il motore audio per permettere la riproduzione interna

        # --- INTESTAZIONE ---
        self.label_titolo = ctk.CTkLabel(self, text="SISTEMA COMPOSITIVO MEDIEVALE", 
                                         font=ctk.CTkFont(size=26, weight="bold")) # Crea il titolo dell'app
        self.label_titolo.pack(pady=(30, 10)) # Posiziona il titolo con margini verticali

        # --- INPUT TESTO ---
        self.entry_testo = ctk.CTkEntry(self, width=550, height=45, placeholder_text="Inserisci la frase da analizzare...") # Crea il campo di input
        self.entry_testo.pack(pady=20) # Posiziona il campo di input

        # --- SEZIONE ANALISI VOCALI ---
        self.label_analisi = ctk.CTkLabel(self, text="ANALISI LOGICA GUIDONIANA (VOCALI ESTRATTE):", 
                                          font=ctk.CTkFont(size=14, weight="bold")) # Etichetta per la sezione analisi
        self.label_analisi.pack(pady=(10, 5)) # Posiziona l'etichetta
        
        self.box_analisi = ctk.CTkTextbox(self, width=550, height=100, font=ctk.CTkFont(family="Courier", size=13)) # Box di testo per i risultati
        self.box_analisi.pack(pady=10) # Posiziona il box di analisi
        self.box_analisi.configure(state="disabled") # Disabilita l'editing manuale per renderlo di sola lettura

        # --- CONTENITORE BOTTONI ---
        self.frame_bottoni = ctk.CTkFrame(self, fg_color="transparent") # Crea una cornice invisibile per i tasti
        self.frame_bottoni.pack(pady=20) # Posiziona il frame dei bottoni

        # Bottone Spartito
        self.btn_spartito = ctk.CTkButton(self.frame_bottoni, text="VEDI SPARTITO", 
                                          command=self.mostra_spartito, fg_color="#3498db", width=180, height=45) # Tasto per MuseScore
        self.btn_spartito.grid(row=0, column=0, padx=10) # Posiziona il tasto a sinistra nella griglia

        # Bottone Play
        self.btn_audio = ctk.CTkButton(self.frame_bottoni, text="RIPRODUCI", 
                                        command=self.riproduci_audio, fg_color="#2ecc71", width=180, height=45) # Tasto per l'audio interno
        self.btn_audio.grid(row=0, column=1, padx=10) # Posiziona il tasto al centro nella griglia

        # Bottone Stop
        self.btn_stop = ctk.CTkButton(self.frame_bottoni, text="STOP", 
                                       command=self.ferma_audio, fg_color="#e74c3c", width=180, height=45) # Tasto per fermare l'audio
        self.btn_stop.grid(row=0, column=2, padx=10) # Posiziona il tasto a destra nella griglia

        # --- STATUS BAR ---
        self.status = ctk.CTkLabel(self, text="Sistema pronto.", text_color="gray") # Etichetta per i messaggi di stato
        self.status.pack(side="bottom", pady=20) # Ancora la barra di stato al fondo della finestra

    def aggiorna_analisi_visiva(self, testo): # Funzione per mostrare le vocali estratte nel box grafico
        self.box_analisi.configure(state="normal") # Abilita momentaneamente il box per scrivere i risultati
        self.box_analisi.delete("1.0", "end") # Svuota il contenuto precedente
        estrazione = [] # Crea una lista vuota per raccogliere le mappature
        for char in testo.lower(): # Scorre ogni carattere del testo inserito
            if char in MAPPA_NOTE: # Controlla se il carattere è una vocale presente nella mappa
                estrazione.append(f"Lettera '{char}' ---> Nota: {MAPPA_NOTE[char]}") # Aggiunge la corrispondenza alla lista
        
        testo_finale = "\n".join(estrazione) if estrazione else "Nessuna vocale trovata nel testo." # Crea il testo finale o un avviso
        self.box_analisi.insert("1.0", testo_finale) # Inserisce il risultato nel box dell'interfaccia
        self.box_analisi.configure(state="disabled") # Blocca nuovamente il box per l'utente

    def elabora(self): # Metodo per validare l'input e generare l'oggetto musicale
        testo = self.entry_testo.get() # Recupera il testo scritto dall'utente
        if not testo.strip(): # Verifica se il campo è vuoto o contiene solo spazi
            self.status.configure(text="Errore: Inserisci del testo!", text_color="red") # Mostra errore in rosso
            return None # Interrompe l'elaborazione
        self.aggiorna_analisi_visiva(testo) # Chiama l'analisi visiva delle vocali
        return genera_spartito_guidoniano(testo) # Restituisce lo spartito generato dall'algoritmo

    def mostra_spartito(self): # Metodo per aprire MuseScore senza bloccare l'interfaccia
        p = self.elabora() # Genera la partitura
        if p: # Se la partitura esiste
            self.status.configure(text="Sincronizzazione con MuseScore (Thread separato)...", text_color="cyan") # Aggiorna lo stato
            # Crea un Thread per eseguire p.show() in parallelo
            thread = threading.Thread(target=p.show, args=('musicxml',), daemon=True) 
            thread.start() # Avvia il thread senza fermare il loop della GUI
            self.focus_force() # Forza il focus sulla finestra per non farla sembrare inattiva

    def riproduci_audio(self): # Metodo per la riproduzione audio interna con threading
        p = self.elabora() # Genera la partitura
        if p: # Se la partitura esiste
            self.status.configure(text="Generazione audio interno...", text_color="orange") # Messaggio di attesa
            
            def task_audio(): # Funzione interna da eseguire nel thread parallelo
                nome_file = "anteprima.mid" # Definisce il nome del file temporaneo
                p.write('midi', fp=nome_file) # Crea fisicamente il file MIDI
                pygame.mixer.music.load(nome_file) # Carica il file nel player di pygame
                pygame.mixer.music.play() # Avvia la musica
                self.status.configure(text="In riproduzione...", text_color="#2ecc71") # Messaggio di successo
            
            # Lancia l'intera procedura audio in un thread separato per evitare freeze
            threading.Thread(target=task_audio, daemon=True).start()

    def ferma_audio(self): # Metodo per interrompere immediatamente l'audio
        pygame.mixer.music.stop() # Ferma il mixer di pygame
        self.status.configure(text="Riproduzione interrotta.", text_color="gray") # Reset dello stato