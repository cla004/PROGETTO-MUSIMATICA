# Importa il modulo per generare numeri casuali (simula il lancio dei dadi)
import random

# Importa dalla libreria music21 le classi necessarie
from music21 import note, stream, metadata, clef

# Dizionario che associa la somma dei dadi a una coppia di note
MATRICE_MOZART = {
    2: ['C4', 'E4'],   # Se la somma è 2, usa queste due note
    3: ['D4', 'F4'],   # Se la somma è 3
    4: ['E4', 'G4'],   # Se la somma è 4
    5: ['F4', 'A4'],   # Se la somma è 5
    6: ['G4', 'B4'],   # Se la somma è 6
    7: ['A4', 'C5'],   # Se la somma è 7
    8: ['B4', 'D5'],   # Se la somma è 8
    9: ['C5', 'E5'],   # Se la somma è 9
    10: ['G4', 'E4'],  # Se la somma è 10
    11: ['F4', 'D4'],  # Se la somma è 11
    12: ['C4', 'C4']   # Se la somma è 12
}

# Definizione della funzione che genera musica casuale
def genera_musica_dadi(numero_battute=8):  # numero_battute ha valore di default 8
    
    """Genera musica stocastica e restituisce i dettagli completi dei lanci."""
    
    # Crea uno spartito completo (Score)
    punteggio = stream.Score()
    
    # Aggiunge metadati allo spartito (titolo e compositore)
    punteggio.metadata = metadata.Metadata(title="Gioco dei Dadi", composer="W.A. Mozart")
    
    # Crea una parte musicale (una linea melodica)
    parte = stream.Part()
    
    # Inserisce la chiave di violino all'inizio della parte
    parte.append(clef.TrebleClef())
    
    # Crea una lista vuota per salvare i dettagli della composizione
    dettagli_composizione = []

    # Ciclo che si ripete per ogni battuta richiesta
    for i in range(numero_battute):
        
        # Simula il lancio di due dadi (numeri casuali da 1 a 6)
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        
        # Calcola la somma dei due dadi
        somma = d1 + d2
        
        # Recupera le note associate alla somma nel dizionario
        note_battuta = MATRICE_MOZART[somma]
        
        # Salva i dettagli della battuta in un dizionario
        dettagli_composizione.append({
            'battuta': i + 1,      # Numero della battuta
            'dado1': d1,           # Valore del primo dado
            'dado2': d2,           # Valore del secondo dado
            'somma': somma,        # Somma dei dadi
            'note': note_battuta   # Note generate
        })
        
        # Ciclo sulle due note della battuta
        for n_nome in note_battuta:
            
            # Crea un oggetto Nota con il nome della nota
            n = note.Note(n_nome)
            
            # Imposta la durata della nota a un quarto
            n.quarterLength = 1.0
            
            # Aggiunge la nota alla parte musicale
            parte.append(n)
    
    # Aggiunge la parte allo spartito completo
    punteggio.append(parte)
    
    # Restituisce sia lo spartito sia i dettagli della composizione
    return punteggio, dettagli_composizione
