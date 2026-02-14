from music21 import note, stream, metadata, clef

# Definizione della struttura dati 'Dizionario' per l'associazione testo-musica.
# Questa mappa permette di  estrarre le note dalle vocali.
MAPPA_NOTE = {
    # La vocale 'A' viene associata al Do centrale (C4 in notazione scientifica).
    'a': 'C4', 
    
    # La vocale 'E' viene associata al Re (D4), la nota immediatamente successiva.
    'e': 'D4', 
    
    # La vocale 'I' viene associata al Mi (E4).
    'i': 'E4', 
    
    # La vocale 'O' viene associata al Fa (F4).
    'o': 'F4', 
    
    # La vocale 'U' viene associata al Sol (G4).
    'u': 'G4'  
}

def genera_spartito_guidoniano(testo):
    """Trasforma il testo in un oggetto musicale di music21."""
    
    # Crea l'oggetto principale della partitura che conterrà tutto il lavoro
    punteggio = stream.Score() 
    
    # Aggiunge i metadati come il titolo e il nome dell'autore dell'algoritmo
    punteggio.metadata = metadata.Metadata(title="Composizione Automatica", composer="Algoritmo di Guido")
    
    # Crea una 'Parte' musicale (come se fosse la traccia di uno strumento)
    parte = stream.Part() 
    
    # Inserisce all'inizio della parte la chiave di violino (G-Clef)
    parte.append(clef.TrebleClef()) 
    
    # Converte tutto il testo in minuscolo per confrontarlo correttamente con la mappa
    testo_minuscolo = testo.lower() 
    
    # Inizializza una variabile di controllo per sapere se abbiamo generato almeno una nota
    ha_note = False 

    # Inizia a scorrere il testo carattere per carattere
    for lettera in testo_minuscolo: 
        # Controlla se il carattere corrente è presente nella mappa delle vocali
        if lettera in MAPPA_NOTE: 
            # Crea un oggetto Nota usando il valore (es. 'C4') corrispondente alla lettera
            n = note.Note(MAPPA_NOTE[lettera]) 
            # Imposta la durata della nota a 1.0 (ovvero un quarto o semiminima)
            n.quarterLength = 1.0 
            # Aggiunge la nota appena creata alla parte musicale
            parte.append(n) 
            # Segnala che abbiamo trovato e aggiunto con successo almeno una nota
            ha_note = True 
            
    # Se dopo il ciclo non è stata trovata nessuna vocale valida
    if not ha_note: 
        # Aggiunge una pausa (Rest) della durata di 4 quarti (un'intera battuta)
        parte.append(note.Rest(quarterLength=4)) 
        
    # Inserisce la parte musicale completata all'interno dell'oggetto punteggio
    punteggio.append(parte) 
    
    # Restituisce l'oggetto musicale finito pronto per essere visualizzato o suonato
    return punteggio