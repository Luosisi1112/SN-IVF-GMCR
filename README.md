# GMCR Project Data File Structure Documentation

This document provides a detailed introduction to the data files in the SN–IVF–GMCR project.

---

## Directory Structure Overview

```
SN–IVF–GMCR-data/
├── data/                              # Raw input data
├── consensus_model_output/             # Consensus model calculation results
├── feasible_and_reachable_sets_output/ # Feasible set and reachable set analysis
└── heterogeneous_gmcr_output/         # SN–IVF–GMCR comparison experiments
```

---

## 1. data/ - Raw Input Data

Stores input data files for the SN–IVF–GMCR model, including decision-makers' preference information and social network relationship data.

| File | Format | Description |
|------|--------|-------------|
| `preferences.xlsx` | Excel | Preference evaluation data of decision-makers for different states |
| `social_matrices_CDM.csv` | CSV | Social network matrices of Compound Decision-Makers (CDM), including trust, distrust, and interaction frequency information |
| `social_matrices_DMs.csv` | CSV | Social network matrices data among Compound Decision-Makers |

---

## 2. consensus_model_output/ - Consensus Model Output

Stores calculation results and visualizations of the consensus reaching model, documenting the process of different compound decision-makers reaching consensus through social network analysis.

### Consensus Result Files

| File | Description |
|------|-------------|
| `consensus_results_G.xlsx` | Preference data of Government decision-makers (Group G) |
| `consensus_results_M.xlsx` | Consensus results of Manufacturer group (Group M), containing compound decision-maker consensus results reached by three manufacturers M1, M2, and M3 through social network analysis |
| `consensus_results_R.xlsx` | Consensus results of Retailer group (Group R), containing compound decision-maker consensus results reached by three retailers R1, R2, and R3 through social network analysis |

### Manufacturer Group Consensus Visualization (consensus_plots_M/)

| File | Description |
|------|-------------|
| `consensus_comparison_M_final.png` | Final consensus vs. initial preference comparison chart for M scenario |
| `consensus_comparison_M_initial.png` | Initial state consensus comparison chart for M scenario |
| `individual_consensus_comparison_M.png` | Individual manufacturer consensus level comparison chart |
| `inner_convergence_M.png` | Internal convergence process visualization chart for manufacturer group consensus |
| `inner_convergence_M.pdf` | Internal convergence process report document for manufacturer group consensus |
| `inner_convergence_M_analysis.xlsx` | Detailed analysis data of the convergence process |
| `inner_convergence_M_data.csv` | Raw data file of the convergence process |

#### individual_matrices/ - Individual Preference Matrices

| File | Description |
|------|-------------|
| `individual_preference_M1.png` | Preference matrix visualization for Manufacturer M1 |
| `individual_preference_M2.png` | Preference matrix visualization for Manufacturer M2 |
| `individual_preference_M3.png` | Preference matrix visualization for Manufacturer M3 |

### Retailer Group Consensus Visualization (consensus_plots_R/)

| File | Description |
|------|-------------|
| `consensus_comparison_R_final.png` | Final consensus vs. initial preference comparison chart for R scenario |
| `consensus_comparison_R_initial.png` | Initial state consensus comparison chart for R scenario |
| `individual_consensus_comparison_R.png` | Individual retailer consensus level comparison chart |
| `inner_convergence_R.png` | Internal convergence process visualization chart for retailer group consensus |
| `inner_convergence_R.pdf` | Internal convergence process report document for retailer group consensus |
| `inner_convergence_R_analysis.xlsx` | Detailed analysis data of the convergence process |
| `inner_convergence_R_data.csv` | Raw data file of the convergence process |

#### individual_matrices/ - Individual Preference Matrices

| File | Description |
|------|-------------|
| `individual_preference_R1.png` | Preference matrix visualization for Retailer R1 |
| `individual_preference_R2.png` | Preference matrix visualization for Retailer R2 |
| `individual_preference_R3.png` | Preference matrix visualization for Retailer R3 |

---

## 3. feasible_and_reachable_sets_output/ - Feasible and Reachable Sets Output

Stores results of state feasibility analysis and reachability analysis, used to study the possibility of strategy transitions among conflicting parties.

### State Analysis Files

| File | Description |
|------|-------------|
| `feasible_states.xlsx` | Feasible states table, containing feasible strategy combination states after multi-constraint filtering |
| `reachable_matrices.xlsx` | Reachability matrices for each decision-maker, used to represent state transition relationships and reachability analysis |

### State Transition Diagrams

| File | Description |
|------|-------------|
| `gmcr_state_transition_special.html` | Interactive state transition diagram main file, visualizing all feasible states and their transition relationships |
| `gmcr_state_transition_G_special.html` | State transition diagram from Government's perspective |
| `gmcr_state_transition_M_special.html` | State transition diagram from Manufacturers' perspective |
| `gmcr_state_transition_R_special.html` | State transition diagram from Retailers' perspective |

---

## 4. heterogeneous_gmcr_output/ - SN–IVF–GMCR Comparison Experiments

Stores calculation results and parameter comparison experiment data of the SN–IVF–GMCR model, used to analyze the impact of different parameter settings on model stability.

### Main Result Files

| File | Description |
|------|-------------|
| `heterogeneous_gmcr_results.xlsx` | SN–IVF–GMCR calculation results |

### Strategic attitudes Parameter Comparison Experiments ($\sigma_k$)

| Parameter Value | Result File |
|----------------|-------------|
| $\sigma_k$=0 | `Comparative_experiment_sigma0.xlsx` |
| $\sigma_k$=0.5 | `heterogeneous_gmcr_results.xlsx`|
| $\sigma_k$=1 | `Comparative_experiment_sigma1.xlsx` |

### Threshold Parameter Comparison Experiments ($\tau_k$)

| Parameter Value | Result File |
|----------------|-------------|
| $\tau_k$=3 | `Comparative_experiment_threshold3.xlsx` |
| $\tau_k$=4 | `Comparative_experiment_threshold4.xlsx` |
| $\tau_k$=5 | `heterogeneous_gmcr_results.xlsx` |
| $\tau_k$=6 | `Comparative_experiment_threshold6.xlsx` |
| $\tau_k$=7 | `Comparative_experiment_threshold7.xlsx` |
