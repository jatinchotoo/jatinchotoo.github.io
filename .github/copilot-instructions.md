# Copilot Instructions for jatinchotoo.github.io

## Project Overview
This is a portfolio site for **strategic finance and decision engineering**. It combines a static HTML portfolio ([index.html](index.html)) with multiple demonstration projects showcasing FP&A automation, capital efficiency, and financial data pipeline expertise. The mission: deterministic financial systems that reduce decision latency.

## Architecture & Major Components

### Portfolio Presentation Layer
- **index.html**: Single-page hero site with Tailwind CSS styling + dark theme. Contains navigation to CV, GitHub projects, and LinkedIn. Uses Plus Jakarta Sans typography and radial gradient backgrounds.
- **assets/images/**: Images for visual sections (risk_management.jpg, project screenshots)
- **cv/**: PDF files (2-page brief, full CV) linked from HTML

### Financial Engineering Projects (Modular Python/SQL Pipelines)

#### Project 2: Global Alpha Engine (Multi-Currency Consolidation)
- **Pattern**: ETL with data integrity recovery
- **Location**: [Project_2_Global_Alpha_Clean/](Project_2_Global_Alpha_Clean/)
- **Pipeline**: `pipeline.py` → `analytics.py` → reports (CSV/Excel)
- **Key Logic**:
  - String-splitting layer to unpack hybrid CSV data
  - Case-insensitive column normalization (Revenue vs REVENUE)
  - Fuzzy matching for disparate regional charts of accounts
  - Currency translation (GBP, EUR, NGN → USD) via `FX_Rate_to_USD`
  - ROIC calculation: `NOPAT / Invested_Capital` (assumes 25% tax rate)
- **Data Governance**: Identifies NaN (missing data) for audit trails
- **Output**: `Master_Consolidated_Fact.csv` → `Final_ROIC_Report.csv`

#### Project 5: Sovereign Engine (Deterministic Ledger Generation)
- **Location**: `Project 5 Sovereign Engine/`
- **Purpose**: Generates IFRS-style general ledger data (`ESFE_FACT_GL.csv`)
- **Pattern**: Ensures debit/credit integrity—never both populated for a single entry
- **Data Model**: txn_date, account_code, account_name, debit, credit, entity, description
- **Entities**: Multi-entity support (Equinox Corp, Sovereign Ltd, etc.)

#### Other Projects
- **Project 1**: SaaS KPI Telemetry (SQL + Power BI dashboards)
- **Project 3**: Lumina AI FinOps Auditing (cloud spend optimization)
- **Project 4**: Axiom Zero Settlement (high-volume reconciliation)

## Developer Conventions & Patterns

### Python Data Pipelines
1. **Path Management**: All scripts use `os.path.join()` and `os.getcwd()` to support relative paths
2. **Data Folder Structure**: Raw CSVs/Excel → `/data` subfolder; processed outputs remain in `/data`
3. **Error Handling**: Check file existence before loading; print ✅/❌ status messages
4. **Column Normalization**: Always standardize to `.lower()`, `.strip()`, remove underscores/spaces before merging
5. **Currency Logic**: Map entities → countries → FX rates; use `.fillna(1.0)` for missing rates
6. **Pandas Operations**: Use `.groupby()` aggregations, `.merge()` for lookups, `.str.contains()` for pattern matching
7. **Financial Calculations**: Assume standard tax rates (25% NOPAT), calculate ROIC with zero-division guards

### HTML/CSS Standards
- **Styling**: Tailwind CSS + inline `<style>` block for custom animations
- **Typography**: Plus Jakarta Sans font; semantic sizing with `clamp()` for responsive headings
- **Interactivity**: Smooth scroll, hover effects on cards (border color + transform), backdrop-filter blur
- **Layout**: `max-w-6xl` grid containers, gap spacing standardized to `2rem`
- **Navigation**: Fixed pill-styled navbar with GitHub/LinkedIn links

### Git & Deployment
- Repository tracks both portfolio site and project source code
- Static site deploys via GitHub Pages (`.git/` present)
- Projects reference external GitHub repos via links in HTML

## Critical Workflows

### Running a Data Pipeline
```bash
cd Project_2_Global_Alpha_Clean
python pipeline.py      # ETL: Load raw files → Master_Consolidated_Fact.csv
python analytics.py     # Analytics: Calculate ROIC → Final_ROIC_Report.csv + Excel
```

### Data Integrity Checks
- Verify `/data` folder contains expected CSVs/Excel before running
- Check for NaN entities (missing Balance Sheet data triggers audit flag)
- Validate column names post-normalization (case-insensitivity is critical)

### Updating Portfolio Site
- Edit `index.html` for content updates
- Add new project cards in `#intelligence` section
- Update `readme.md` for high-level project descriptions
- Push to GitHub → automatic GitHub Pages deploy

## Integration Points & Dependencies

### External APIs & Services
- Tailwind CSS CDN (https://cdn.tailwindcss.com)
- Google Fonts CDN (Plus Jakarta Sans)
- Font Awesome icons (https://cdnjs.cloudflare.com/ajax/libs/font-awesome)
- GitHub project links (README cards reference external GitHub repos)
- LinkedIn profile embedded in navbar

### Python Libraries (Standard Stack)
- `pandas`: Data loading, groupby, merges, Excel I/O
- `os`: Path management
- `matplotlib` & `seaborn`: Visualization (Project 2 analytics)
- `datetime`: Date generation (Project 5 Sovereign Engine)
- `random`: Deterministic data generation for demo

### Data Sources
- **Raw Input**: Regional CSVs with disparate schemas (BioGrowth, CryptoFlow, etc.)
- **Mapping Tables**: Account_Mapping.xlsx, Currency_Master.xlsx (lookup tables for normalization)
- **Output Artifacts**: CSV + Excel reports, executive dashboards

## Key Decisions & Why

- **Deterministic Systems**: Financial logic is explicit, auditable, and repeatable—not statistical
- **Multi-Currency Consolidation**: Leverages mapping tables + FX rates to unify reporting across geographies
- **Data Integrity Recovery Layer**: Handles malformed hybrid files (embedded delimiters) through preprocessing string-split
- **Modular ETL Design**: Separates data ingestion (pipeline.py) from business logic (analytics.py) for maintainability
- **IFRS-Aligned Ledgers**: Project 5 enforces debit/credit double-entry rules at generation
- **Portfolio as Marketing**: Single-page HTML showcases projects; links direct to GitHub for deeper engagement

## Common Tasks

| Task | File(s) | Pattern |
|------|---------|---------|
| Add project to portfolio | [index.html](index.html) `#intelligence` section | Copy `.asset-card` structure; update mandate label, description, GitHub link |
| Fix data normalization | [pipeline.py](Project_2_Global_Alpha_Clean/pipeline.py) line ~40 | Add `.str.upper().str.strip()` or `.str.lower()` on problem column |
| Recalculate financial metrics | [analytics.py](Project_2_Global_Alpha_Clean/analytics.py) line ~35 | Modify NOPAT formula (e.g., `* 0.80` for 20% tax) or ROIC denominator |
| Generate new ledger | `Project 5 Sovereign Engine/layer1_core_ledger.py` | Adjust `start_date`, account list, entity list, or amount range |
| Update CV link | [index.html](index.html) navbar | Edit `href` path to cv/ PDF filename |

