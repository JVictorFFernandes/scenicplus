# SCENIC+ Pipeline (Single-Cell Gene Regulatory Networks)

Este repositório documenta um pipeline modular para a execução do **SCENIC+** com foco em inferência de **Gene Regulatory Networks (GRNs)** integrando dados *single-cell* (RNA-seq e ATAC-seq), além de ferramentas auxiliares como `pycisTopic`, `pycistarget` e `scanpy`.

O objetivo deste pipeline é fornecer um guia completo, desde a **instalação do ambiente**, **configurações de sistema**, **preparo dos dados**, **organização de pastas**, até a **execução dos notebooks e scripts oficiais**.

---

# Sumário

* [Visão Geral do Pipeline](#visão-geral-do-pipeline)
* [Arquitetura Geral](#arquitetura-geral)
* [Requisitos](#requisitos)
* [Instalação e Configuração](#instalação-e-configuração)

  * [1. Instalar Mamba](#1-instalar-mamba)
  * [2. Configurar WSL2](#2-configurar-wsl2)
  * [3. Instalações Manuais 1.0 (Sistema)](#3-instalações-manuais-10-sistema)
  * [4. Clonar SCENIC+](#4-clonar-scenic)
  * [5. Criar Estrutura de Diretórios](#5-criar-estrutura-de-diretórios)
  * [6. Clonar Repositório do Projeto](#6-clonar-repositório-do-projeto)
  * [7. Mover Arquivos](#7-mover-arquivos)
  * [8. Configurar Ambientes Virtuais](#8-configurar-ambientes-virtuais)
* [Estrutura Final do Repositório](#estrutura-final-do-repositório)
* [Execução](#execução)
* [Referências](#referências)
* [Licença](#licença)

---

# Visão Geral do Pipeline

Este pipeline trabalha em **3 estágios principais**, cada um executado em seu próprio ambiente para evitar conflitos de dependências:

1. **scenicplus (PARTE 1)**
   Instalação de dependências do SCENIC+ e setup base.

2. **scenicplus_v3 (PARTE 2)**
   Ambiente contendo o `pycisTopic v3` e outras ferramentas auxiliares.

3. **scenicplus_obj (PARTE 3)**
   Ambiente final utilizando o `environment.yml` do SCENIC+, necessário para análises completas.

---

# Arquitetura Geral

Fluxo básico do pipeline:

```
Raw scRNA-seq + scATAC-seq
            |
         scanpy
            |
       pycisTopic
            |
    pycistarget database
            |
         SCENIC+
            |
     GRN gerada + regulons
```

---

# Requisitos

* Linux ou WSL2
* Git
* Conda/Mamba
* Recursos mínimos recomendados:

  * RAM > 32 GB
  * CPU > 8 cores
  * Armazenamento > 200 GB

---

# Instalação e Configuração

---

## 1. Instalar Mamba

Baixar instalador:

```bash
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
```

Executar script:

```bash
bash Miniforge3-$(uname)-$(uname -m).sh
```

Após instalar, recarregar terminal:

```bash
source ~/.bashrc
```

Verificar:

```bash
mamba --version
```

---

## 2. Configurar WSL2

Encerrar instâncias:

```powershell
wsl --shutdown
```

Editar arquivo:

```
notepad %UserProfile%\.wslconfig
```

Colocar:

```
[wsl2]
memory=60GB
processors=8
swap=64GB
localhostForwarding=true
```

Salvar e reiniciar terminal.

Verificar:

```bash
free -h
swapon --show
```

---

## 3. Instalações Manuais 1.0 (Sistema)

```bash
sudo apt update
sudo apt install build-essential
sudo apt install zlib1g-dev
sudo apt install libbz2-dev
sudo apt install liblzma-dev
```

---

## 4. Clonar SCENIC+

```bash
git clone https://github.com/aertslab/scenicplus
cd scenicplus
```

---

## 5. Criar Estrutura de Diretórios

```bash
mkdir -p myproject/{pycistopic/{data,outs/qc,tmp,blacklist},create_pycistarget_database/data,scanpy}
```

Entrar no projeto:

```bash
cd myproject
```

---

## 6. Clonar Repositório do Projeto

```bash
git clone https://github.com/JVictorFFernandes/scenicplus.git
```

---

## 7. Mover Arquivos

```bash
mv scenicplus/{environment.yml,workflow.ipynb,run_exportbulk.py, worflow_scanpy.ipynb, workflow_createpycistarget.ipynb} . \
&& rm -rf scenicplus \
&& mv {workflow.ipynb,run_exportbulk.py} pycistopic \
&& mv {worflow_scanpy.ipynb} scanpy \
&& mv {workflow_createpycistarget.ipynb} create_pycistarget_database
```

---

## 8. Configurar Ambientes Virtuais

---

### scenicplus (PARTE 1)

Criar ambiente:

```bash
mamba create -n scenicplus python=3.11.8
```

Ativar:

```bash
mamba activate scenicplus
```

Instalações:

```bash
pip install cython
pip install pybedtools --no-build-isolation
```

```bash
mamba install -c bioconda htslib
mamba install pandas
```

Checkout para branch correta:

```bash
git checkout development
```

Instalar pacotes dentro do repositório scenicplus:

```bash
pip install .
```

Desativar:

```bash
conda deactivate
```

---

### scenicplus_v3 (PARTE 2)

```bash
conda create -n scenicplus_v3 python=3.11 -y
conda activate scenicplus_v3
pip install git+https://github.com/aertslab/pycisTopic.git@pycistopic_v3
```

---

### scenicplus_obj (PARTE 3)

```bash
conda env create -n scenicplus_obj -f environment.yml
```

---

# Estrutura Final do Repositório

Estrutura esperada após setup:

```
myproject/
│
├── pycistopic/
│   ├── data/
│   ├── outs/
│   ├── tmp/
│   ├── blacklist/
│   └── workflow.ipynb
│
├── scanpy/
│   └── worflow_scanpy.ipynb
│
├── create_pycistarget_database/
│   ├── data/
│   └── workflow_createpycistarget.ipynb
│
├── environment.yml
└── run_exportbulk.py
```

---

# Execução

Cada notebook deverá ser executado dentro do respectivo ambiente:

| Módulo                          | Ambiente       |
| ------------------------------- | -------------- |
| scanpy preprocessing            | scenicplus_v3  |
| pycistopic LDA + topics         | scenicplus_v3  |
| pycistarget database            | scenicplus_obj |
| scenicplus export bulk/regulons | scenicplus     |

---

# Referências

* Aerts Lab – SCENIC+: [https://github.com/aertslab/scenicplus](https://github.com/aertslab/scenicplus)
* pycisTopic: [https://github.com/aertslab/pycisTopic](https://github.com/aertslab/pycisTopic)
* SCENIC (original): [https://github.com/aertslab/SCENIC](https://github.com/aertslab/SCENIC)

---

# Licença
