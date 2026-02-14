import customtkinter as ctk # Importa la libreria per creare interfacce grafiche moderne
from motore_musicale.traduttore import genera_spartito_guidoniano # Importa la funzione per convertire il testo in spartito musicale

ctk.set_appearance_mode("Dark") # Imposta il tema visivo dell'applicazione sulla modalità scura
ctk.set_default_color_theme("blue") # Definisce il blu come colore primario per i widget (bottoni, barre, ecc.)

class FinestraPrincipale(ctk.CTk): # Inizia la definizione della classe principale che gestisce la finestra dell'app
    def __init__(self): # Metodo costruttore che inizializza la finestra quando viene creata
        super().__init__() # Chiama il costruttore della classe base ctk.CTk per configurare la finestra correttamente
        self.title("Guido d'Arezzo Digital Composer") # Imposta il testo che apparirà nella barra del titolo della finestra
        self.geometry("700x500") # Stabilisce le dimensioni iniziali della finestra (larghezza 700px, altezza 500px)
        self.partitura_attuale = None # Crea una variabile di istanza per memorizzare temporaneamente la musica generata

        # Titolo Header
        self.label_titolo = ctk.CTkLabel(self, text="SISTEMA COMPOSITIVO MUSIMATICA",  # Crea un'etichetta di testo per l'intestazione
                                         font=ctk.CTkFont(size=24, weight="bold", family="Helvetica")) # Imposta il font grande, in grassetto e stile Helvetica
        self.label_titolo.pack(pady=(40, 10)) # Posiziona il titolo nella finestra con margini verticali (40 sopra, 10 sotto)

        # Input Testo
        self.entry_testo = ctk.CTkEntry(self, width=500, height=45, placeholder_text="Scrivi la tua frase qui...") # Crea la barra di inserimento testo con un testo suggerito
        self.entry_testo.pack(pady=20) # Posiziona la barra di testo con un margine di 20 pixel per distanziarla dagli altri elementi

        # Container Bottoni
        self.frame_bottoni = ctk.CTkFrame(self, fg_color="transparent") # Crea una cornice (frame) invisibile per raggruppare i bottoni orizzontalmente
        self.frame_bottoni.pack(pady=20) # Posiziona il contenitore dei bottoni con un margine verticale

        # Bottone 1: Visualizza Spartito
        self.btn_spartito = ctk.CTkButton(self.frame_bottoni, text="VEDI SPARTITO",  # Crea il pulsante per mostrare lo spartito grafico
                                          command=self.mostra_spartito, # Associa la pressione del tasto alla funzione 'mostra_spartito'
                                          fg_color="#3498db", hover_color="#2980b9", # Imposta il colore blu e la tonalità che appare quando ci si passa sopra
                                          width=200, height=50, font=ctk.CTkFont(weight="bold")) # Imposta dimensioni e testo in grassetto per il pulsante
        self.btn_spartito.grid(row=0, column=0, padx=10) # Posiziona il pulsante nella prima colonna della griglia interna al frame

        # Bottone 2: Ascolta Audio
        self.btn_audio = ctk.CTkButton(self.frame_bottoni, text="RIPRODUCI AUDIO",  # Crea il pulsante per la riproduzione sonora
                                        command=self.riproduci_audio, # Associa la pressione del tasto alla funzione 'riproduci_audio'
                                        fg_color="#e67e22", hover_color="#d35400", # Imposta il colore arancione e la tonalità di hover
                                        width=200, height=50, font=ctk.CTkFont(weight="bold")) # Imposta dimensioni e stile del testo del pulsante
        self.btn_audio.grid(row=0, column=1, padx=10) # Posiziona il pulsante nella seconda colonna della griglia interna al frame

        # Status Bar
        self.status = ctk.CTkLabel(self, text="Pronto per comporre.", text_color="gray") # Crea un'etichetta in basso per fornire feedback all'utente
        self.status.pack(side="bottom", pady=20) # Posiziona l'etichetta di stato ancorandola al bordo inferiore della finestra

    def elabora(self): # Definisce la funzione per validare il testo e chiamare l'algoritmo musicale
        testo = self.entry_testo.get() # Recupera la stringa di testo inserita dall'utente nella barra di input
        if not testo.strip(): # Controlla se il testo è vuoto o composto solo da spazi
            self.status.configure(text="Inserisci del testo!", text_color="red") # Se vuoto, mostra un errore rosso nella barra di stato
            return None # Esce dalla funzione restituendo nulla
        return genera_spartito_guidoniano(testo) # Chiama il traduttore musicale e restituisce l'oggetto spartito creato

    def mostra_spartito(self): # Definisce la funzione per aprire lo spartito in un software esterno (come MuseScore)
        p = self.elabora() # Esegue l'elaborazione del testo per ottenere la musica
        if p: # Se la musica è stata generata con successo
            self.status.configure(text="Apertura MuseScore in corso...", text_color="cyan") # Aggiorna lo stato per avvisare dell'apertura del programma
            p.show('musicxml') # Utilizza il metodo di music21 per esportare e visualizzare il file in formato MusicXML

    def riproduci_audio(self): # Definisce la funzione per suonare le note generate
        p = self.elabora() # Esegue l'elaborazione del testo per ottenere la musica
        if p: # Se la musica è stata generata correttamente
            self.status.configure(text="Riproduzione MIDI in corso...", text_color="orange") # Cambia il testo di stato per indicare che l'audio sta partendo
            p.show('midi') # Utilizza il sintetizzatore MIDI di sistema per far suonare le note