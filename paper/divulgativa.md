# Un'intelligenza artificiale medica che "consulta la biblioteca" prima di rispondere

*Versione divulgativa dell'articolo "Retrieval over 2026 Clinical Guidelines Recovers Post-Cutoff Knowledge in MedGemma-27B: an Open, Verifiable Pilot"*

**Giovanni Del Papa** — Ricercatore indipendente, Italia — giovanni.delpapa@live.it
Preprint (non ancora revisionato da altri esperti), ottobre 2026

## Il problema: un'intelligenza artificiale ferma nel tempo

I modelli di intelligenza artificiale che rispondono a domande di medicina imparano leggendo enormi quantità di testi, ma solo fino a un certo giorno: la data in cui termina il loro addestramento. Da quel momento in poi è come se si fossero addormentati. La medicina, invece, non si ferma: ogni anno escono nuove linee guida, cioè le raccomandazioni ufficiali che indicano ai medici come comportarsi. Un modello addestrato in passato semplicemente non può conoscere le linee guida pubblicate dopo.

## L'idea: prima di rispondere, consultare la biblioteca aggiornata

Immaginiamo uno studente molto preparato, che però ha smesso di studiare un anno fa. Se gli chiediamo qualcosa di recente, rischia di sbagliare. Ma se, prima di rispondere, gli permettiamo di andare in una biblioteca aggiornata, cercare i documenti giusti e leggerli, la sua risposta migliora.

È esattamente quello che fa il nostro sistema. Quando arriva una domanda:

1. cerca, in un archivio di documenti recenti, i passaggi più pertinenti;
2. li mette davanti al modello insieme alla domanda;
3. il modello risponde tenendo conto di quei documenti.

C'è anche un "controllo di sicurezza": il sistema usa i documenti trovati solo quando la ricerca sembra davvero affidabile; altrimenti lascia rispondere il modello con le sue sole conoscenze. Le regole di questo controllo sono state decise in anticipo, su un gruppo di domande di prova separato.

## Cosa abbiamo fatto

- Abbiamo raccolto **773 documenti**: riassunti di linee guida e documenti di consenso pubblicati per la prima volta nel **2026**, tutti con licenza aperta (presi dall'archivio pubblico Europe PMC).
- Abbiamo usato un modello medico aperto, **MedGemma-27B**, fatto girare in locale su un piccolo computer (un Mac mini), senza servizi esterni.
- Abbiamo preparato **131 domande di verifica** a scelta multipla (quattro opzioni) su questi documenti, tenute separate da quelle usate per regolare il sistema.
- Il test finale è stato eseguito **una sola volta**, per evitare di "aggiustare" i risultati a posteriori.

## I risultati, in parole semplici

- **Senza consultare i documenti**, il modello rispondeva correttamente a circa **65 domande su 100**.
- **Consultando i documenti**, è salito a circa **91 risposte giuste su 100**.
- Su 131 domande, le risposte corrette sono passate da 85 a 119: **37 domande sono diventate giuste, 3 sono diventate sbagliate**.
- Il sistema **trova il documento giusto 99 volte su 100**.

![Percentuale di risposte giuste nel test finale: senza consultare i documenti, consultandoli con il controllo di sicurezza, e consultandoli sempre. Le barre sottili indicano il margine di incertezza.](fig_accuracy.png){width=60%}

Curiosamente, usando i documenti *sempre* (senza controllo di sicurezza) il risultato sarebbe stato ancora leggermente migliore, circa 95 su 100; abbiamo comunque mantenuto il controllo così come era stato deciso in partenza, per correttezza.

## Perché diciamo che è "aperto e verificabile"

Chiunque può controllare il lavoro. Sono pubblici e scaricabili: i documenti usati, l'indice di ricerca, le domande, le risposte attese, il risultato di ogni singola domanda, il codice e le istruzioni per rifare l'esperimento da zero. Per ogni documento è indicata la fonte e verificata la licenza aperta. Non ci sono "scatole nere".

## I limiti, detti onestamente

- **È un test "a libro aperto".** Le domande sono state create dallo stesso modello a partire dagli stessi documenti che poi può consultare. È un po' come fare un compito avendo davanti il libro da cui sono state tratte le domande: il vantaggio del metodo è quindi favorito.
- **Nessun medico ha rivisto le domande.** Alcuni documenti, inoltre, non sono strettamente clinici (ad esempio riguardano metodi di ricerca).
- **Il campione è piccolo** (131 domande), con un solo modello, solo riassunti e solo fonti in inglese.
- **Nei test generali di medicina il metodo non ha aiutato.** In esperimenti precedenti su raccolte di domande mediche indipendenti (PubMedQA, MedMCQA), consultare documenti non ha migliorato i risultati. Il miglioramento osservato qui riguarda quindi le **informazioni nuove** presenti nei documenti, non un "ragionamento medico" migliore in generale.

## Avvertenza importante

Questo è uno strumento **solo di ricerca e informazione**. **Non è un dispositivo medico** e **non va usato per diagnosi, terapie o decisioni cliniche**. Il progetto **non è affiliato né approvato da Google** (che ha sviluppato MedGemma), e non implica l'approvazione degli autori dei documenti usati.

## Prossimi passi

È in corso una **versione 2**, molto più ampia: circa **14.000 documenti con testo completo** (non solo riassunti) e circa **2.000 domande**, per verificare se i risultati reggono su scala più grande.

## Link

- Articolo (preprint su Zenodo): <https://doi.org/10.5281/zenodo.23664675> (DOI 10.5281/zenodo.23664675)
- Codice, domande e risultati: <https://huggingface.co/odelpa/linee-guida-2026-rag-it>
- Indice dei documenti: <https://huggingface.co/datasets/odelpa/linee-guida-2026-rag-it-index>
