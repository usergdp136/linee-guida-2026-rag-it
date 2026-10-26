# SPDX-License-Identifier: Apache-2.0
"""Valutatore: base vs base+RAG su data/questions_{dev,test}.json. accuratezza = corrette/n; delta = acc_RAG - acc_base;
SE appaiata = sd(d_i)/sqrt(n) con d_i in {-1,0,1}; z = delta/SE.  Uso: python evaluate.py test ../dataset/chunks.jsonl"""
import json, math, sys
from linee_guida_rag import Index, answer
split, chunks = sys.argv[1], sys.argv[2]
Q = json.load(open("data/questions_%s.json" % split, encoding="utf-8")); ix = Index(chunks); R = []
for q in Q:
    a = answer(ix, q["prompt"]); R.append({"gold": q["answer"], "rag": a["answer"], "base": max(a["p_norag"], key=a["p_norag"].get) if a["p_norag"] else "?", "used": a["rag_used"]})
n = len(R); d = [(r["rag"] == r["gold"]) - (r["base"] == r["gold"]) for r in R]; m = sum(d) / n
se = math.sqrt(sum((x - m) ** 2 for x in d) / (n - 1) / n)
print(json.dumps({"n": n, "base": sum(r["base"] == r["gold"] for r in R) / n, "rag_gated": sum(r["rag"] == r["gold"] for r in R) / n,
                  "delta": m, "se": se, "z": m / se if se else None, "rag_used": sum(r["used"] for r in R)}, indent=1))
