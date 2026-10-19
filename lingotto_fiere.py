class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand_assegnato = None

    def get_codice(self):
        return self.codice

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        if self.stand_assegnato is not None:
            return f"{self.codice}: {self.nome} {self.cognome} - Stand: {self.stand_assegnato.codice}"
        return f"{self.codice}: {self.nome} {self.cognome} - Nessuno stand assegnato"

class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)
        self.espositore = None
        self.disponibile = True

    def get_codice(self):
        return self.codice

    def calcola_prezzo(self):
        return self.prezzo_base

    def is_disponibile(self):
        return self.disponibile

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __lt__(self, other):
        if isinstance(other, Stand):
            return self.calcola_prezzo() < other.calcola_prezzo()
        return NotImplemented

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Standard | {int(self.superficie)} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}"

class StandPreseElettriche(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.numero_prese = int(numero_prese)

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.numero_prese)

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Prese Extra | {int(self.superficie)} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Prese aggiuntive: {self.numero_prese} - {stato}"

class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def calcola_prezzo(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.disponibile else f"Assegnato a {self.espositore.codice}"
        return f"{self.codice}: Premium ({self.posizione}) | {int(self.superficie)} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}"

class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self.stand = {}  # Dizionario codice_stand -> oggetto Stand
        self.espositori = {}  # Dizionario codice_espositore -> oggetto Espositore

    """Aggiungere setter e getter se necessari"""

    def get_nome(self):
        return self.nome

    def set_nome(self, nuovo_nome):
        self.nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        with open(file_path, "r", encoding="utf-8") as file:
            for riga in file:
                riga = riga.strip()
                if riga != "":
                    campi = riga.split(",")
                    codice = campi[0]

                    if codice.startswith("ES"):
                        _, nome, cognome = campi
                        nuovo_espositore = Espositore(codice, nome, cognome)
                        self.espositori[codice] = nuovo_espositore

                    elif codice.startswith("ST"):
                        superficie = campi[1]
                        padiglione = campi[2]
                        prezzo_base = campi[3]

                        if len(campi) == 4:
                            nuovo_stand = Stand(codice, superficie, padiglione, prezzo_base)
                        elif len(campi) == 5:
                            valore_extra = campi[4]
                            if valore_extra.isdigit():
                                nuovo_stand = StandPreseElettriche(codice, superficie, padiglione, prezzo_base, valore_extra)
                            else:
                                nuovo_stand = StandPremium(codice, superficie, padiglione, prezzo_base, valore_extra)

                        self.stand[codice] = nuovo_stand

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        if codice_stand not in self.stand:
            raise ValueError(f"Stand {codice_stand} non trovato.")
        if codice_espositore not in self.espositori:
            raise ValueError(f"Espositore {codice_espositore} non trovato.")

        obj_stand = self.stand[codice_stand]
        obj_espositore = self.espositori[codice_espositore]

        if not obj_stand.is_disponibile():
            raise ValueError(f"Lo stand {codice_stand} è già stato assegnato.")
        if obj_espositore.stand_assegnato is not None:
            raise ValueError(f"L'espositore {codice_espositore} ha già uno stand assegnato.")

        # Assegnazione bidirezionale
        obj_stand.espositore = obj_espositore
        obj_stand.disponibile = False
        obj_espositore.stand_assegnato = obj_stand

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for espositore in self.espositori.values():
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        lista_stand = list(self.stand.values())
        return sorted(lista_stand)
