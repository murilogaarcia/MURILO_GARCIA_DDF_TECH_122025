# Murilo Garcia – DDF TECH Case  
**Repositório:** `MURILO_GARCIA_DDF_TECH_122025`

Este repositório contém a implementação completa do case técnico DDF TECH, abrangendo **engenharia de dados, qualidade, modelagem analítica, integração em nuvem, governança de dados e visualização**.

O projeto simula um ambiente real de **plataforma analítica corporativa** utilizando dados de e-commerce (AdventureWorks), estruturados em arquitetura moderna de dados.

---

# 🎯 Objetivo do Case

Construir uma **plataforma de dados ponta a ponta** capaz de:

- Ingerir dados transacionais  
- Aplicar regras de qualidade  
- Modelar dados em Star Schema  
- Publicar dados em cloud  
- Catalogar ativos  
- Expor insights via dashboards  

Tudo de forma **reproduzível, governada e auditável**.

---

# 🧱 Arquitetura Geral

Fonte (AdventureWorks)
↓
PostgreSQL Local (Staging)
↓
ETL Python + SQL
↓
PostgreSQL Local (Gold / Star Schema)
↓
Data Quality Validation
↓
Neon (PostgreSQL Cloud)
↓
Dadosfera Pipeline
↓
Snowflake (Gold)
↓
Metabase (Dashboards)

---

# 📁 Estrutura do Repositório

MURILO_GARCIA_DDF_TECH_122025/
│
├── venv/              
│   └── Scripts/
│       └── activate
│
├── arquitetura/
├── dadosfera/
├── pipeline/
├── queries/
├── reproducibilidade/
├── notebooks/
├── scripts/
├── prints/
├── app.py
├── requirements.txt
└── README.md

---

# 🧠 Modelo Analítico (Star Schema)

A camada **Gold** foi modelada em **Star Schema**.

## Tabela Fato
| Tabela | Descrição |
|------|----------|
| `fact_sales` | Todas as vendas com métricas financeiras e chaves para dimensões |

## Dimensões
| Dimensão | Descrição |
|--------|----------|
| `dim_product` | Produtos, categorias e subcategorias |
| `dim_customer` | Clientes |
| `dim_date` | Datas |
| `dim_special_offer` | Promoções e descontos |

Esse modelo garante:
- Alta performance
- Facilidade de análise
- Governança clara

---

# 🧪 Data Quality

A plataforma possui uma camada de validação automática de qualidade:

Regras aplicadas:
- Chaves não nulas
- Datas válidas
- Valores financeiros positivos
- Consistência de quantidade

Relatórios são gerados em CSV e Markdown, garantindo **rastreabilidade e confiabilidade dos dados** antes da publicação em nuvem.

---

# ☁️ Publicação em Cloud

Os dados são publicados no seguinte stack:

| Camada | Tecnologia |
|------|-----------|
| Banco Cloud | Neon (PostgreSQL) |
| Data Warehouse | Snowflake |
| Governança | Dadosfera |
| BI | Metabase |

A sincronização é realizada por **pipelines Dadosfera**.

---

# 📊 Dashboards

O dashboard analítico apresenta:

- Receita líquida
- Lucro
- Top produtos
- Top categorias
- Evolução temporal
- Performance por oferta

Todos os dados vêm da **camada Gold no Snowflake**.

Evidências estão na pasta `/prints`.

---

# 🧾 SQL Analítico

As queries utilizadas incluem:

- Top 5 produtos por receita
- Top 5 categorias
- Receita por mês
- Margem por produto
- Vendas por cliente

Todas documentadas em:
/queries/queries.md

---

# 📚 Governança e Catálogo (Dadosfera)

Todos os ativos estão catalogados:

- Dataset Gold
- Tabelas
- Pipelines
- Dashboards

Com:
- Descrição
- Tags
- Metadados
- Data lineage

Ver:
/dadosfera/catalogo.md

---

# Power BI
  - Também foi feito um DashBoard no Power Bi como forma de complemento do projeto e mais uma opção de vizualização

# ♻️ Reprodutibilidade

O projeto é totalmente reproduzível a partir dos scripts e notebooks disponíveis.

O passo a passo completo está em:
/reproducibilidade/README.md



Inclui:
- Execução do ETL
- Validação de qualidade
- Migração para Neon
- Pipeline Dadosfera
- Validação no Snowflake
- Criação de dashboards

---

# 🧑‍💻 Autor

**Murilo Garcia**  
Case Técnico – DDF TECH – Dezembro 2025  

---

# 📌 Observação

Todo o trabalho avaliado está:
- Catalogado na Dadosfera
- Versionado neste repositório
- Totalmente reproduzível

Nenhum artefato externo é necessário para validação do case.

