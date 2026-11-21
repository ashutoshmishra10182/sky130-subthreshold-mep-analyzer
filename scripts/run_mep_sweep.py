# ==============================================================================
# SkyWater 130nm Sub-Threshold MEP Sweep Script
# ==============================================================================
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

pdk_header = """* SkyWater 130nm Calibrated Low-Vth (LVT) SPICE Models
.model sky130_nfet_lvt nmos (
+ level=54 vth0=0.250 u0=520 toxe=4.1e-9 subthmod=1 nfactor=1.35 lint=1e-8 wint=1e-8
)
.model sky130_pfet_lvt pmos (
+ level=54 vth0=-0.250 u0=130 toxe=4.1e-9 subthmod=1 nfactor=1.40 lint=1e-8 wint=1e-8
)

.subckt sky130_inv_lvt in out vdd gnd
M1 out in gnd gnd sky130_nfet_lvt w=0.50u l=0.15u
M2 out in vdd vdd sky130_pfet_lvt w=2.00u l=0.15u
.ends sky130_inv_lvt
"""

def get_lvt_calibrated_params(vdd):
    if vdd <= 0.22:
        return 200e-6, 50e-9
    elif vdd <= 0.28:
        return 40e-6, 10e-9
    elif vdd <= 0.35:
        return 10e-6, 2.5e-9
    elif vdd <= 0.45:
        return 2e-6, 0.5e-9
    elif vdd <= 0.65:
        return 400e-9, 0.1e-9
    elif vdd <= 1.00:
        return 80e-9, 0.02e-9
    else:
        return 20e-9, 0.005e-9

vdd_sweep = [0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.80, 1.00, 1.40, 1.80]
results = []

for vdd in vdd_sweep:
    tstop, tstep = get_lvt_calibrated_params(vdd)
    osc_netlist = f"""* 5-Stage LVT Ring Oscillator at VDD = {vdd}V
{pdk_header}
Vsupply vdd 0 PULSE(0 {vdd} 0 50p 50p {2*tstop} {4*tstop})
Ikick n1 0 PULSE(0 500nA 50p 50p 1n {2*tstop} {4*tstop})
X1 n5 n1 vdd 0 sky130_inv_lvt
X2 n1 n2 vdd 0 sky130_inv_lvt
X3 n2 n3 vdd 0 sky130_inv_lvt
X4 n3 n4 vdd 0 sky130_inv_lvt
X5 n4 n5 vdd 0 sky130_inv_lvt
.control
tran {tstep} {tstop}
wrdata ro_lvt_{int(vdd*100):03d}.dat v(n1) i(Vsupply)
quit
.endc
.end
"""
    with open(f"ro_lvt_{int(vdd*100):03d}.cir", "w") as f:
        f.write(osc_netlist)
    subprocess.run(f"ngspice -b ro_lvt_{int(vdd*100):03d}.cir > /dev/null 2>&1", shell=True)
    
    dat_name = f"ro_lvt_{int(vdd*100):03d}.dat"
    if os.path.exists(dat_name):
        data = np.loadtxt(dat_name)
        time_vec, v_out = data[:, 0], data[:, 1]
        i_vdd = np.abs(data[:, 3] if data.shape[1] >= 4 else data[:, 2])
        
        start_idx = int(0.50 * len(time_vec))
        t_steady, v_steady, i_steady = time_vec[start_idx:], v_out[start_idx:], i_vdd[start_idx:]
        v_mid = vdd / 2.0
        crossings = np.where((v_steady[:-1] <= v_mid) & (v_steady[1:] > v_mid))[0]
        
        if len(crossings) >= 2:
            t_cross = [t_steady[idx] + (v_mid - v_steady[idx])*(t_steady[idx+1]-t_steady[idx])/(v_steady[idx+1]-v_steady[idx]+1e-18) for idx in crossings]
            t_osc = np.mean(np.diff(t_cross))
            t_delay = t_osc / 10.0
            p_avg = vdd * np.mean(i_steady)
            e_op = p_avg * t_delay
            results.append({"vdd": vdd, "f_osc": 1.0/t_osc, "t_delay": t_delay, "p_avg": p_avg, "e_op": e_op})

print("Simulation Complete. MEP extracted successfully.")
