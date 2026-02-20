import random  # Libreria per generare numeri casuali (scelta note casuale per ogni vocale)
from music21 import stream, note, tempo, metadata  # Componenti di music21 per creare spartiti digitali

def genera_spartito_guidoniano(testo):
    """
    Genera uno spartito music21 a partire dal testo fornito,
    usando il metodo del "Soggetto Cavato" di Guido d'Arezzo.
    Salva anche i file MIDI e MusicXML.
    Restituisce lo stream music21 creato.
    """

    # --- CREA LO SPARTITO ---
    # Lo Stream è l'oggetto principale di music21 dove si aggiungono note, accordi, tempo, ecc.
    s = stream.Stream()
    
    # Imposta il tempo del brano (battiti per minuto)
    s.append(tempo.MetronomeMark(number=90))  # 90 BPM, andamento moderato
    
    # --- METADATI DEL BRANO ---
    s.metadata = metadata.Metadata()  # Inizializza contenitore metadati
    s.metadata.title = f"Melodia di Guido per: {testo}"  # Titolo dello spartito
    
    # --- DEFINIZIONE DELLE NOTE DISPONIBILI ---
    # Qui definiamo le altezze (pitch) su cui si "cicleranno" le vocali del testo
    # Sono distribuite su 3 ottave per variare la melodia
    pitch_list = [
        'G3', 'A3', 'B3', 'C4', 'D4',  # Ottava bassa
        'E4', 'F4', 'G4', 'A4', 'B4',  # Ottava centrale
        'C5', 'D5', 'E5', 'F5', 'G5'   # Ottava alta
    ]
    
    # Lista delle vocali base su cui l'algoritmo associa le note
    vocali_base = ['a', 'e', 'i', 'o', 'u']
    
    # --- CREAZIONE DELLA MAPPA VOCALI → NOTE ---
    # Mappa ogni vocale a una lista di note disponibili
    mappa_guido = {}
    for v in vocali_base:
        # Inizialmente ogni vocale non ha note associate
        mappa_guido[v] = []

    # Distribuisce ciclicamente le note della pitch_list alle 5 vocali
    # i % 5 permette di ripartire dall'inizio delle vocali quando si superano le 5 note
    for i in range(len(pitch_list)):
        p = pitch_list[i]  # Nota corrente
        vocale = vocali_base[i % 5]  # Determina a quale vocale assegnare la nota
        mappa_guido[vocale].append(p)  # Aggiorna la mappa

    # --- ESTRAZIONE DELLE VOCALI DAL TESTO ---
    testo = testo.lower()  # Trasforma il testo in minuscolo per confrontare correttamente le vocali
    vocali_nel_testo = []  # Lista che conterrà solo le vocali trovate

    # Scansiona ogni carattere del testo
    for char in testo:
        if char in vocali_base:  # Se il carattere è una vocale
            vocali_nel_testo.append(char)  # Aggiungi alla lista delle vocali del testo

    # Se non ci sono vocali nel testo, termina la funzione
    if not vocali_nel_testo:
        print("Nessuna vocale trovata.")
        return None

    # --- CREAZIONE DELLA MELODIA ---
    # Per ogni vocale nel testo, scegliamo una nota casuale dalla mappa
    for v in vocali_nel_testo:
        pitch_scelto = random.choice(mappa_guido[v])  # Nota casuale associata alla vocale
        n = note.Note(pitch_scelto)  # Creazione dell'oggetto Note di music21
        n.quarterLength = 1.0  # Durata della nota: 1.0 = semiminima (quarter note)
        s.append(n)  # Aggiunge la nota allo spartito digitale

    # --- SALVATAGGIO DEI FILE ---
    # MIDI: file audio riproducibile in qualsiasi player o DAW
    s.write('midi', fp='melodia_guido_m21.mid')
    
    # MusicXML: file spartito standard apribile in MuseScore, Finale, Sibelius, ecc.
    s.write('musicxml', fp='melodia_guido.xml')
    
    # Messaggi finali di conferma
    print(f"Melodia generata con successo! ({len(vocali_nel_testo)} note)")
    print("File salvati: 'melodia_guido_m21.mid' e 'melodia_guido.xml'")

    # --- RESTITUISCE LO SPARTITO ---
    # Questo permette alla GUI di visualizzarlo o riprodurlo
    return s,mappa_guido
