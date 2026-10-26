# SPDX-License-Identifier: Apache-2.0
# Scheletro Space Gradio: mostra risposta + fonti (titolo, DOI, link Europe PMC, licenza). Da completare prima della pubblicazione.
import json, os, sys
import gradio as gr
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))
from linee_guida_rag import Index, answer
DS = os.environ.get("LG_DATASET", os.path.join(os.path.dirname(__file__), "..", "dataset"))
IX = Index(os.path.join(DS, "chunks.jsonl"))
META = {d["doc_id"]: d for d in map(json.loads, open(os.path.join(DS, "documents.jsonl"), encoding="utf-8"))}
DISCL = "⚠️ **Strumento informativo e di ricerca. Non usare per diagnosi o terapia.** Verificare sempre la linea guida originale."

def run(q, a, b, c, d):
    u = q + "\n" + "\n".join("%s. %s" % (k, v) for k, v in zip("ABCD", (a, b, c, d))) + "\nAnswer only with the letter of the correct answer."
    r = answer(IX, u)
    src = "\n\n".join("**[%d] %s** (score %.2f)  \ndoi:%s — [Europe PMC](%s) — CC BY 4.0  \n> %s" % (i + 1, s["title"], s["score"], META[s["doc_id"]]["doi"], META[s["doc_id"]]["url"], s["text"][:400])
                      for i, s in enumerate(r["sources"]))
    return "Risposta: **%s** (RAG %s)" % (r["answer"], "usato" if r["rag_used"] else "non usato"), src

with gr.Blocks(title="linee-guida-2026-rag-it") as demo:
    gr.Markdown("# linee-guida-2026-rag-it\n" + DISCL + "\nBasato su MedGemma (termini [HAI-DEF](https://developers.google.com/health-ai-developer-foundations/terms), [Prohibited Use Policy](https://developers.google.com/health-ai-developer-foundations/prohibited-use-policy)).")
    q = gr.Textbox(label="Domanda"); opts = [gr.Textbox(label=k) for k in "ABCD"]
    out = gr.Markdown(); fonti = gr.Markdown(label="Fonti")
    gr.Button("Rispondi").click(run, [q] + opts, [out, fonti])
if __name__ == "__main__":
    demo.launch()
