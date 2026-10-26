# SPDX-License-Identifier: Apache-2.0
"""linee-guida-2026-rag-it: BM25 retrieval over 2026 CC BY guideline abstracts + confidence gate + MedGemma via Ollama.
Strumento informativo e di ricerca: NON per diagnosi o terapia."""
import json, math, re, os, urllib.request
from collections import Counter

MODEL = os.environ.get("LG_MODEL", "linee-guida-2026-rag-it")   # Ollama tag created from ../ollama/Modelfile
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
GATE = (0.6, 0.7, 1.01)   # (t_r, t_c, t_n) tuned on dev only: use RAG iff rr>=t_r and p_rag>=t_c and p_norag<t_n
HEADER = ("Reference passages follow. Use them ONLY if they directly answer the question. If they are irrelevant, incomplete "
          "or contradict well-established medical knowledge, ignore them and answer from your own knowledge.")
tok = lambda s: re.findall(r"[a-z0-9]{2,}", s.lower())

class Index:
    """BM25 (k1=1.2, b=0.75) over chunks.jsonl; rr = top score / max attainable score for the query (0..1)."""
    def __init__(self, chunks_path):
        self.C = [json.loads(l) for l in open(chunks_path, encoding="utf-8")]
        self.TF = [tok(c["title"] + " " + c["text"]) for c in self.C]
        self.N = len(self.C); self.avg = sum(map(len, self.TF)) / self.N
        self.DF = Counter(w for t in self.TF for w in set(t)); self.TFC = [Counter(t) for t in self.TF]
    def idf(self, w): return math.log(1 + (self.N - self.DF[w] + .5) / (self.DF[w] + .5))
    def search(self, q, k=3):
        qs = set(tok(q)); S = []
        for n, (tf, L) in enumerate(zip(self.TFC, self.TF)):
            S.append((sum(self.idf(w) * tf[w] * 2.2 / (tf[w] + 1.2 * (.25 + .75 * len(L) / self.avg)) for w in qs if w in tf), n))
        S.sort(reverse=True); mx = sum(self.idf(w) for w in qs if w in self.DF) or 1
        return [(round(s / mx, 4), self.C[n]) for s, n in S[:k]]

def block(P):
    return HEADER + "\n\nPASSAGES:\n" + "\n\n".join("[%d] %s\n%s" % (i + 1, c["title"], c["text"]) for i, (s, c) in enumerate(P)) + "\n\nQUESTION:\n"

def _post(path, body):
    r = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=600))

def probs(u, letters="ABCD"):
    """Letter distribution from the first generated token (raw Gemma prompt, prefill 'Answer:')."""
    pr = "<start_of_turn>user\n" + u.strip() + "\nRespond with the single letter only.<end_of_turn>\n<start_of_turn>model\nAnswer:"
    r = _post("/api/generate", {"model": MODEL, "prompt": pr, "raw": True, "stream": False,
              "options": {"temperature": 0, "num_predict": 1, "num_ctx": 8192, "seed": 0}, "logprobs": True, "top_logprobs": 20})
    best = {}
    for lp in (r.get("logprobs") or [])[:1]:
        for x in lp.get("top_logprobs", []) + [lp]:
            t = re.sub(r'[\s\*\(\)\.:\[\]"]', "", x.get("token") or "").upper()
            if len(t) == 1 and t in letters: best[t] = max(best.get(t, -1e9), x["logprob"])
    z = sum(math.exp(v) for v in best.values()) or 1
    return {t: math.exp(v) / z for t, v in best.items()}

top = lambda p: max(p, key=p.get) if p else "?"

def answer(index, u, gate=GATE, k=3):
    """Returns dict with final letter, whether RAG was used, and the passages (sources) shown to the model."""
    P = index.search(u, k); pn = probs(u); pr = probs(block(P) + u); tr, tc, tn = gate
    use = bool(pr) and P[0][0] >= tr and max(pr.values()) >= tc and (max(pn.values()) if pn else 0) < tn
    return {"answer": top(pr if use else pn), "rag_used": use, "rr": P[0][0], "p_norag": pn, "p_rag": pr,
            "sources": [{"doc_id": c["doc_id"], "title": c["title"], "score": s, "text": c["text"]} for s, c in P]}
