# IL10 -819/-592 and grandiosity in schizophrenia

Analysis code for the manuscript "Interleukin pathway genotype and the grandiosity
dimension of psychosis" (Poznan cohort, n = 489).

Repository: https://github.com/maksbrzezicki/il10-grandiosity

Every number, table and figure in the manuscript and its supplementary material is
produced by the two notebooks here. Nothing was computed outside them and no value
was entered by hand.

## Source data

The analysis reads two files:

    interleukiny_genotypy.xlsx   genotypes, 26 interleukin-pathway markers, cases and controls
    opcrit_baza.xlsx             OPCRIT item-level ratings

They hold individual-level clinical and genotype data and are **not distributed here**.
Access is governed by the original participant consent and the approval of the
Bioethics Committee of Poznan University of Medical Sciences. Requests should be
directed to the corresponding author, as stated in the Data Availability Statement.

If you hold the data, place both files beside the notebooks, or edit `GENO_PATH` and
`OPCRIT_PATH` in the configuration cell. `inputs.sha256` records the SHA-256 digest of
each, so you can confirm your copies are the ones used for the published results.

## Contents

    main_analysis.ipynb          panel-level tests, gene-set screen (SKAT), localisation,
                                 Firth estimates, discovery and held-out split, jackknife,
                                 specificity, split-half, Table 1, Figures 1 and 2
    revision_analyses.ipynb      Supplementary Tables S1 to S6, anomaly detection and its
                                 sensitivity analysis, case-control comparison,
                                 stratification and medication checks, Figure 3

    Table1_demographics.csv                     Table 1 as published
    Supplementary_Table_S1_markers.csv ... S6    the six supplementary tables
    Figure1_narrative.tif, Figure2_contribution.tif, Figure3_anomaly.tif
    main_manifest.json           every headline result, with the value the paper reports
    revision_manifest.json       154 recorded values, each with its rounding

    requirements.txt             exact package versions of the verification run
    run_all.sh                   installs the environment, runs both notebooks, checks hashes
    inputs.sha256                digests of the two source files
    outputs.sha256               digests of the twelve generated artefacts
    overlap_check.py             reports any pair of text elements in a figure whose drawn
                                 boxes intersect

## Reproducing

    bash run_all.sh

or open `main_analysis.ipynb` and then `revision_analyses.ipynb` and run each from top to
bottom in a fresh kernel. The main notebook takes about a minute, the revision notebook
about two.

Both notebooks are seeded from a single master seed. Executing a notebook rewrites its
stored outputs, so the `.ipynb` files change on every run and are deliberately not
covered by the checksums; what is checked is the data going in and the artefacts coming
out.

## What the notebooks check for you

Each notebook stops rather than producing a quietly wrong answer:

- The data-loading cell raises with an explanatory message if either source file is absent.
- Integrity checks assert the derived analysis set against the published cohort: 490
  linked patients, 489 analysed, 26 markers across 8 genes, 133 with grandiosity, and
  169 of 12,714 dosage cells (1.33%) mean-imputed.
- A verification cell at the end of each notebook compares every result quoted in the
  manuscript against the value this run produced, and raises if any disagree. On the
  reference environment all 23 headline results and all 17 checked revision values match.
- `sha256sum -c outputs.sha256` confirms that the twelve artefacts are byte-identical to
  the published ones.

Figure typography can be re-checked after any change:

    python overlap_check.py main_analysis.ipynb 2,4,6,8,12,14,16,18,20,22   # Figure 1
    python overlap_check.py main_analysis.ipynb 2,4,6,8,12,14,16,18,20,24   # Figure 2
    python overlap_check.py revision_analyses.ipynb 2,3,4,5,7,9,11,13,15,17,19,21,23,25   # Figure 3

Each should report zero overlapping text pairs.

## Figures

Built to the journal specification: at most 180 mm wide, 300 dpi at final size, no text
smaller than 8 pt at that size, RGB TIFF with LZW compression, each under 1 MB. The
settings live in `FIG_RC` and `save_tiff`, defined once in the configuration cell of each
notebook, so the three figures cannot drift apart. Final sizes are 181 x 194 mm,
180 x 204 mm and 164 x 221 mm.

## Environment

Python 3.12.3 with the versions pinned in `requirements.txt`. The published results also
reproduce exactly under statsmodels 0.15.0, which differs from the 0.14.6 named in the
Methods; every printed value was identical.

## Colour

The diverging contribution map in Figure 2 runs green to cream to purple. The patient
grandiosity strip beside it uses a neutral grey ramp, so it shares no hue with either
pole. A grey ramp is invariant under the Machado, Oliveira and Fernandes (2009)
simulation matrices for protanopia, deuteranopia and tritanopia, since each matrix has
unit row sums, so the two encodings cannot be confused under any of them.

## Conventions

Sex is OPCRIT item 3, coded 0 for male and 1 for female, as given in the cohort data
dictionary. The gene symbol (IL10) denotes the gene, its markers and its gene set; the
spelled-out name (interleukin-10) denotes the cytokine.
