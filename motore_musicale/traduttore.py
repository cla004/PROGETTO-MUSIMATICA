import random # Importa la libreria per generare numeri casuali (fondamentale per la scelta della nota)
from music21 import stream, note, tempo, metadata # Importa i componenti di music21 per gestire la musica

def compositore_guido_music21(testo):
    # Creiamo un oggetto 'Stream', che è un ogetto di music 21 per gestrie le note e le sue caratterstiche come 
    # tempo, chiavi,accordi, ecc. In questo caso lo useremo per costruire la nostra melodia.
    s = stream.Stream()
    
    # Aggiunge l'indicazione del tempo: qui impostiamo 90 battiti al minuto (un andamento moderato)
    s.append(tempo.MetronomeMark(number=90))
    
    # Inizializza il contenitore dei metadati (informazioni sul brano)
    s.metadata = metadata.Metadata()
    
    # Imposta il titolo dello spartito includendo il testo inserito 
    s.metadata.title = f"Melodia di Guido per: {testo}"
    
    # Definiamo la lista delle altezze (pitch) disponibili: coprono circa due ottave
    # Queste sono le note su cui "cicleranno" le nostre vocali
    pitch_list = [
        'G3', 'A3', 'B3', 'C4', 'D4',  # Associa a: a, e, i, o, u (ottava bassa)
        'E4', 'F4', 'G4', 'A4', 'B4',  # Associa a: a, e, i, o, u (ottava centrale)
        'C5', 'D5', 'E5', 'F5', 'G5'   # Associa a: a, e, i, o, u (ottava alta)
    ]
    
    # Definiamo le 5 vocali standard che l'algoritmo cercherà nel testo
    vocali_base = ['a', 'e', 'i', 'o', 'u']
    
    # Creiamo un dizionario (mappa) dove ogni vocale inizialmente non ha note associate { 'a': [], 'e': [], ... }
   # Creiamo un dizionario vuoto
mappa_guido = {}

# Per ogni elemento contenuto nella lista 'vocali_base'
for v in vocali_base:
    
    # Inseriamo nel dizionario una nuova chiave 'v'
    # associandole come valore una lista vuota
    mappa_guido[v] = []

    
    # Questo ciclo distribuisce le note contenute in 'pitch_list'
# nelle 5 vocali presenti in 'vocali_base'
for i in range(len(pitch_list)):
    
    # Recuperiamo la nota nella posizione i-esima
    p = pitch_list[i]
    
    # L'operatore modulo (%) serve per far ripartire il conteggio
    # dopo aver raggiunto la quinta vocale.
    # In questo modo, dopo la 'u' si ricomincia dalla 'a'
    vocale = vocali_base[i % 5]
    
    # Aggiungiamo la nota corrente (p)
    # alla lista associata alla vocale corrispondente nel dizionario
    mappa_guido[vocale].append(p)
    
    # Trasforma tutto il testo inserito dall'utente in minuscolo
# così evitiamo problemi nel confronto con le vocali
testo = testo.lower()

# Creiamo una lista vuota che conterrà solo le vocali trovate nel testo
vocali_nel_testo = []

# Scorriamo ogni carattere del testo
for char in testo:
    
    # Se il carattere corrente è una vocale tra quelle definite in vocali_base
    if char in vocali_base:
        
        # Aggiungiamo la vocale alla lista
        vocali_nel_testo.append(char)

# Se l'utente ha scritto qualcosa senza vocali (esempio: "123")
# il programma si interrompe qui
if not vocali_nel_testo:
    print("Nessuna vocale trovata.")
    return

# Inizia la fase di creazione della melodia
for v in vocali_nel_testo:
    
    # Per ogni vocale trovata nel testo,
    # scegliamo casualmente UNA nota tra quelle associate
    pitch_scelto = random.choice(mappa_guido[v])
    
    # Creiamo l'oggetto nota compatibile con music21
    n = note.Note(pitch_scelto)
    
    # Impostiamo la durata della nota:
    # 1.0 corrisponde a una semiminima (quarter note)
    n.quarterLength = 1.0
    
    # Aggiungiamo la nota allo spartito digitale
    s.append(n)

# Creazione del file MIDI (ascoltabile con qualsiasi player o DAW)
s.write('midi', fp='melodia_guido_m21.mid')

# Creazione del file MusicXML (apribile in MuseScore, Finale, ecc.)
s.write('musicxml', fp='melodia_guido.xml')

# Messaggi finali di conferma
print(f"Melodia generata con successo! ({len(vocali_nel_testo)} note)")
print("File salvati: 'melodia_guido_m21.mid' e 'melodia_guido.xml'")
