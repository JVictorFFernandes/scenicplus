#!/usr/bin/env python

import os
import logging
import pandas as pd
import pickle  # <--- Importante: Adicionado para salvar as variáveis
from pycisTopic.pseudobulk_peak_calling import export_pseudobulk

# =====================================================
# 0. Logging
# =====================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# =====================================================
# 1. Paths do projeto
# =====================================================
PROJECT_DIR = "/home/victorffernandes/scenicplus/project_control"
DATA_DIR = os.path.join(PROJECT_DIR, "data")
OUT_DIR = os.path.join(PROJECT_DIR, "outs")

# Garante que as pastas existam
consensus_dir = os.path.join(OUT_DIR, "consensus_peak_calling")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(consensus_dir, exist_ok=True)
os.makedirs(os.path.join(consensus_dir, "pseudobulk_bed_files"), exist_ok=True)
os.makedirs(os.path.join(consensus_dir, "pseudobulk_bw_files"), exist_ok=True)

# =====================================================
# 2. Carregar cell_data
# =====================================================
cell_data = pd.read_table(
    os.path.join(DATA_DIR, "cell_data.tsv"),
    index_col=0
)
logging.info(f"cell_data carregado: {cell_data.shape}")

# =====================================================
# 3. Conferência de colunas
# =====================================================
required_cols = ["VSN_cell_type", "VSN_sample_id"]
missing = [c for c in required_cols if c not in cell_data.columns]
if missing:
    raise ValueError(f"Colunas ausentes: {missing}")

# =====================================================
# 4. chromsizes
# =====================================================
chromsizes = pd.read_table(
    "http://hgdownload.cse.ucsc.edu/goldenPath/hg38/bigZips/hg38.chrom.sizes",
    header=None,
    names=["Chromosome", "End"]
)
chromsizes.insert(1, "Start", 0)
logging.info("chromsizes carregado.")

# =====================================================
# 5. fragments_dict
# =====================================================
samples_in_metadata = cell_data["VSN_sample_id"].unique().tolist()
if len(samples_in_metadata) != 1:
    raise ValueError(f"Esperado 1 sample, encontrado: {samples_in_metadata}")

sample_name = samples_in_metadata[0]
fragments_dict = {
    sample_name: os.path.join(DATA_DIR, "fragments.tsv.gz")
}
logging.info(f"fragments_dict configurado: {fragments_dict}")

# =====================================================
# 6. Rodar export_pseudobulk (A PARTE PESADA)
# =====================================================
logging.info("Iniciando export_pseudobulk (pode demorar)...")

# Nota: Mantive n_cpu=1 para estabilidade de memória, mas se seu servidor 
# aguentou bem da última vez, pode tentar aumentar para 2 ou 4.
bw_paths, bed_paths = export_pseudobulk(
    input_data=cell_data,
    variable="VSN_cell_type",
    sample_id_col="VSN_sample_id",
    chromsizes=chromsizes,
    bed_path=os.path.join(consensus_dir, "pseudobulk_bed_files"),
    bigwig_path=os.path.join(consensus_dir, "pseudobulk_bw_files"),
    path_to_fragments=fragments_dict,
    n_cpu=1,               
    normalize_bigwig=False, 
    temp_dir="/tmp",
    split_pattern="-"
)

logging.info("export_pseudobulk finalizado.")

# =====================================================
# 7. SALVAR OS DICIONÁRIOS
# =====================================================
logging.info("Salvando os dicionários bw_paths e bed_paths em .pkl...")

# Salva bed_paths
bed_pickle_path = os.path.join(consensus_dir, "bed_paths.pkl")
with open(bed_pickle_path, "wb") as f:
    pickle.dump(bed_paths, f)

# Salva bw_paths
bw_pickle_path = os.path.join(consensus_dir, "bw_paths.pkl")
with open(bw_pickle_path, "wb") as f:
    pickle.dump(bw_paths, f)

logging.info(f"Salvo com sucesso em:\n - {bed_pickle_path}\n - {bw_pickle_path}")
print("\n=== Processo concluído. Volte ao Jupyter! ===")