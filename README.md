# linee-guida-2026-rag-it (mirror GitHub)

**Link:** [Repo Hugging Face](https://huggingface.co/odelpa/linee-guida-2026-rag-it) · [Dataset indice HF (CC BY 4.0)](https://huggingface.co/datasets/odelpa/linee-guida-2026-rag-it-index) · DOI [10.5281/zenodo.23664674](https://doi.org/10.5281/zenodo.23664674) ([record Zenodo](https://zenodo.org/records/23665015)) · [Preprint PDF](https://zenodo.org/records/23665015/files/linee-guida-2026-rag-it_preprint.pdf) · [Hub pubblicazioni](https://odelpa-pubblicazioni.static.hf.space)

**In parole semplici:** MedGemma è il modello medico di Google. Con il RAG, prima di rispondere il sistema cerca i passaggi pertinenti nelle 773 linee guida italiane/internazionali del 2026 con licenza CC BY e risponde citandoli. Su 131 domande l'accuratezza passa da 0,649 a 0,908. Solo per ricerca: **non usare per diagnosi o decisioni cliniche.**

Questo repository **non contiene né ridistribuisce i pesi** di MedGemma. Uso del modello base soggetto ai [Termini HAI-DEF](https://developers.google.com/health-ai-developer-foundations/terms) e alla [Prohibited Use Policy](https://developers.google.com/health-ai-developer-foundations/prohibited-use-policy).

Licenze: codice Apache-2.0 (`LICENSE`); indice in `index/` CC BY 4.0 con attribuzione per documento (`index/ATTRIBUTION.md`, `index/LICENSE`, `NOTICE`). Indice anche su HF: `hf download odelpa/linee-guida-2026-rag-it-index --repo-type dataset --local-dir index`

---

Spiegazione semplice: [divulgativa.pdf](paper/divulgativa.pdf)

# linee-guida-2026-rag-it

> ⚠️ **DISCLAIMER — Strumento informativo e di ricerca. NON è un dispositivo medico e NON va usato per diagnosi, terapia o decisioni cliniche.** Le risposte possono essere errate o incomplete: verificare sempre sulla linea guida originale e rivolgersi a un professionista sanitario.

Pipeline RAG (retrieval BM25 + gate di confidenza + prompt) su **773 abstract di linee guida e consensus pubblicati nel 2026** con licenza **CC BY 4.0** (Europe PMC). Il modello linguistico usato è basato su MedGemma (MedGemma-27B text-it, GGUF Q4_K_M): questo pacchetto **non contiene né ridistribuisce i pesi** di MedGemma; il Modelfile Ollama rimanda al modello base, che l'utente scarica accettandone i termini.

Costruito su base completamente aperta e verificabile: corpus CC BY con attribuzione per documento, codice Apache-2.0, domande, risposte attese e risultati item per item inclusi.

## Termini del modello base
L'uso di MedGemma è regolato dai **[Termini di utilizzo Health AI Developer Foundations (HAI-DEF)](https://developers.google.com/health-ai-developer-foundations/terms)** e dalla **[Prohibited Use Policy HAI-DEF](https://developers.google.com/health-ai-developer-foundations/prohibited-use-policy)**. "linee-guida-2026-rag-it" è un nome nostro: il progetto non è affiliato a Google né approvato da Google; "basato su MedGemma" ha solo valore descrittivo.

## Risultati (MedGemma-27B Q4, base vs base+RAG)
| set | n | base | base + RAG (gate) | base + RAG (sempre attivo) |
|---|---|---|---|---|
| dev (taratura gate) | 86 | 0,744 | 0,977 | 0,977 |
| **test (eseguito una volta)** | **131** | **0,649** | **0,908** | 0,947 |

Test: Δ = +25,95 pt, SE appaiata 4,28 pt, z = 6,07 (37 risposte corrette in più, 3 in meno). Retrieval hit@1 0,992; parse_fail 0. Gate (t_r, t_c, t_n) = (0,6; 0,7; 1,01) tarato solo su dev.
Formule: accuratezza = corrette/n; Δ = acc_RAG − acc_base; SE = sd(d_i)/√n con d_i ∈ {−1,0,1} per item; z = Δ/SE.

## Limiti
- **Test "a libro aperto"**: ogni domanda è stata generata (da MedGemma, temperatura 0) a partire da un abstract che è anche nell'indice, e tenuta solo se il modello, avendo l'abstract davanti, sceglie la risposta attesa. Misura quindi la capacità di recuperare e usare informazione *nuova* (post-training) presente nel corpus, non la competenza clinica generale.
- Le domande non sono state riviste da clinici; alcune linee guida del corpus non sono cliniche (es. metodologia, bioinformatica).
- Solo abstract, non testo integrale; scelta multipla A–D; lingua delle fonti: inglese.

## Contenuto
- `dataset/` — indice (CC BY 4.0, separato dal codice), pubblicato come odelpa/linee-guida-2026-rag-it-index come repo dataset separato (nome previsto odelpa/linee-guida-2026-rag-it-index): `documents.jsonl` (metadati + abstract + attribuzione), `chunks.jsonl`, `ATTRIBUTION.md`, `license_check_europepmc_20261026.json`, `LICENSE`.
- `code/` — pipeline (`linee_guida_rag/rag.py`: retrieval, gate, prompt), valutatore `evaluate.py`, domande `data/questions_dev.json` (86) e `questions_test.json` (131), risultati `results/` — Apache-2.0.
- `ollama/Modelfile` — rimanda a MedGemma, senza pesi.
- `space/` — scheletro Gradio che mostra le fonti.

## Uso
```bash
ollama pull hf.co/unsloth/medgemma-27b-text-it-GGUF:Q4_K_M
ollama create linee-guida-2026-rag-it -f ollama/Modelfile
hf download odelpa/linee-guida-2026-rag-it-index --repo-type dataset --local-dir dataset
cd code && python evaluate.py test ../dataset/chunks.jsonl
```

## Articolo e citazione
Preprint (non revisionato): Del Papa G., *Retrieval over 2026 Clinical Guidelines Recovers Post-Cutoff Knowledge in MedGemma-27B: an Open, Verifiable Pilot*, Zenodo, 2026. DOI: [10.5281/zenodo.23664674](https://doi.org/10.5281/zenodo.23664674)

## Restrizioni d'uso e output
**Restrizioni d'uso vincolanti (HAI-DEF ToU §3.2).** Chi usa il modello base tramite questo pacchetto (incluso `ollama/Modelfile`) non deve usarlo: (1) per gli usi vietati dalla [Prohibited Use Policy](https://developers.google.com/health-ai-developer-foundations/prohibited-use-policy); (2) per qualsiasi uso che possa indurre un'autorità regolatoria sanitaria a considerare Google "fabbricante" di un dispositivo medico; (3) in violazione di leggi e regolamenti. Vedi il file `NOTICE`.

**Output generati da MedGemma.** Le domande in `code/data/` sono state generate automaticamente da MedGemma (Output ai sensi dei Termini HAI-DEF; per la §1.1(h) gli Output non sono Model Derivatives) e non sono state riviste da clinici. Derivano da abstract CC BY 4.0: l'attribuzione è in `ATTRIBUTION.md` del dataset. Chi le riusa ne è responsabile (§3.3).

Licenze: codice Apache-2.0; domande e risultati con obbligo di attribuzione alle fonti CC BY 4.0; modello base soggetto ai Termini HAI-DEF.
