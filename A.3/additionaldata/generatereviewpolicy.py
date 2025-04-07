import csv
import os

# 📂 Ruta de salida
BASE = os.path.dirname(__file__)
OUTPUT_POLICIES = os.path.join(BASE, "reviewpolicy_nodes.csv")

# 🎯 Lista de políticas: (ID, número de revisores)
policies = [
    ("rp1", 2),
    ("rp2", 3),
    ("rp3", 4),
]

# 💾 Escribir CSV
with open(OUTPUT_POLICIES, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["review_policy_id:ID(ReviewPolicy)", "number_of_reviewers"])
    writer.writerows(policies)

print(f"✅ Archivo generado: {OUTPUT_POLICIES}")
