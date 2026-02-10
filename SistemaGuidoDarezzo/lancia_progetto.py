# Importiamo la classe principale dal pacchetto della GUI
from visualizzazione_gui.interfaccia import FinestraPrincipale

def avvio_sistema():
    """
    Funzione di inizializzazione del software.
    Crea l'istanza dell'interfaccia e avvia il loop principale.
    """
    try:
        # Creazione dell'applicazione
        app = FinestraPrincipale()
        
        # Messaggio di conferma nel terminale
        print("--- Sistema Guidoniano Avviato con Successo ---")
        print("Pronto per la composizione algoritmica.")
        
        # Avvio del ciclo di eventi della finestra
        app.mainloop()
        
    except Exception as e:
        print(f"Errore durante l'avvio dell'applicazione: {e}")

if __name__ == "__main__":
    avvio_sistema()