# Open-Source SkyWater 130nm Sub-Threshold CMOS MEP Analyzer

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![PDK](https://img.shields.io/badge/PDK-SkyWater%20130nm-orange.svg)
![SPICE](https://img.shields.io/badge/Simulator-NGSPICE-green.svg)

## Overview
This repository provides an automated NGSPICE modeling framework to extract the **Minimum Energy Point (MEP)** and characterize small-signal voltage gain collapse in sub-threshold digital logic using the open-source **SkyWater 130nm CMOS PDK**.

Operating digital logic in sub-threshold ($V_{DD} < V_{th}$) minimizes dynamic power but causes exponential propagation delay degradation. This framework quantifies the convex energy trade-off $E_{\text{op}} = \alpha C_L V_{DD}^2 + I_{\text{off}} V_{DD} t_d$ across operating regimes ($0.20\text{V} \le V_{DD} \le 1.80\text{V}$).

---

## Key Experimental Results

| Supply Voltage ($V_{DD}$) | Operating Regime | Oscillation Freq | Stage Delay ($t_d$) | Power ($\mu\text{W}$) | Energy per Op ($E_{\text{op}}$) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| $0.50\text{ V}$ | Near-Threshold | $9.021\text{ MHz}$ | $11.080\text{ ns}$ | $0.314\text{ }\mu\text{W}$ | $3.476\text{ fJ}$ |
| **$0.60\text{ V}$** | **Global MEP ($V_{DD}^*$)** | **$76.638\text{ MHz}$** | **$1.305\text{ ns}$** | **$2.027\text{ }\mu\text{W}$** | **$2.644\text{ fJ}$** |
| $0.80\text{ V}$ | Super-Threshold | $455.922\text{ MHz}$ | $0.219\text{ ns}$ | $20.278\text{ }\mu\text{W}$ | $4.448\text{ fJ}$ |
| $1.00\text{ V}$ | Super-Threshold | $900.827\text{ MHz}$ | $0.111\text{ ns}$ | $62.071\text{ }\mu\text{W}$ | $6.890\text{ fJ}$ |
| $1.40\text{ V}$ | Super-Threshold | $1726.821\text{ MHz}$ | $0.058\text{ ns}$ | $232.219\text{ }\mu\text{W}$ | $13.448\text{ fJ}$ |
| $1.80\text{ V}$ | Nominal Super-$V_{th}$ | $2413.372\text{ MHz}$ | $0.041\text{ ns}$ | $546.545\text{ }\mu\text{W}$ | $22.647\text{ fJ}$ |

### Performance Metrics
* **Minimum Energy Point ($V_{DD}^*$)**: $0.60\text{ V}$
* **Minimum Energy per Operation ($E_{\min}$)**: $2.644\text{ fJ}$ ($8.56\times$ reduction vs. nominal $1.80\text{V}$)
* **Energy Savings**: **$88.32\%$** compared to standard $1.80\text{V}$ operation.

---

## Reproduce in Google Colab

Run the complete pipeline directly on Google Colab CPU without requiring a local SPICE environment:

```bash
git clone https://github.com/ashutoshmishra10182/sky130-subthreshold-mep-analyzer.git
cd sky130-subthreshold-mep-analyzer
python3 scripts/run_mep_sweep.py
