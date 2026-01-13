# Clinical X-Ray Simulator & Shielding Audit Tool

A high-fidelity **Diagnostic X-Ray Simulation** built in Python. This tool models the physics of electron acceleration, Tungsten target interaction (Bremsstrahlung), and probabilistic radiation shielding using a **Monte Carlo-inspired logic**.

## 🌟 Core Features

* **Stochastic Physics Engine:** Uses probability-based modeling for radiation attenuation rather than simple collision detection.
* **"No-Pass-Through" Anode Logic:** Enforces physical density boundaries, ensuring electrons interact only at the Anode surface (Focal Spot).
* **Dynamic Shielding Investigation:** Adjustable lead-equivalent shielding to study **Half-Value Layers (HVL)** and radiation leakage.
* **Real-time Intensity Monitor:** A live graphical feed of photon flux based on  and  inputs.
* **Data Logging System:** A dedicated **Green Save Button** that exports binary session data (hit-rates) to `.txt` files for external audit.

## 🔬 The Science Behind the Code

### 1. The Anode Interaction

The simulation implements a **Positional Lock** on the Anode face:



This prevents "phantom" penetration and accurately represents the site where kinetic energy is converted into X-ray photons.

### 2. Monte Carlo Shielding Logic

The shield uses a **Probability Threshold** () to determine if a particle is absorbed or leaks:

* A random integer () between  is generated upon collision.
* **Absorption:** If , the particle is removed (Safe).
* **Transmission:** If , the particle penetrates the barrier (Leakage).

## 🚀 Installation & Usage

### Prerequisites

* Python 3.11 or higher
* Pygame library

### Setup

1. Clone the repository:
```bash
git clone https://github.com/YourUsername/xray-simulator.git
cd xray-simulator

```


2. Install dependencies:
```bash
pip install pygame

```


3. Run the simulation:
```bash
python main.py

```



### How to Use

1. **Input Phase:** Enter the Voltage () and Current () in the console. Press **Enter** to proceed.
2. **Simulation Phase:** * Adjust the **Spawn Rate** and **Electron Speed**.
* Move the **Shield Thickness** slider to observe attenuation levels.
* Click the **SAVE SESSION LOG** button to export your data to `xray_data.txt`.



## 📊 Sample Data Output

The simulator logs data in a binary format representing photon "peaks":
`--- Session: 2026-01-13 10:12:19 ---`
`Settings: 120 kV, 12 mA`
`Intensity Peaks: [0, 1, 1, 0, 0, 1, 0, 1, 1, 1...]`

## 🛠 Project Structure

* `main.py`: Entry point, UI handling, and Data Logging logic.
* `src/settings.py`: Global constants and 600x500 viewport calibration.
* `src/particles.py`: Stochastic physics engine and particle management.
* `src/tubes.py`: Anode/Cathode geometry and surface impact logic.
* `src/shield.py`: Shielding attenuation and Lead-equivalence logic.

## 📜 References

* Bushong, S. C. (2020). *Radiologic Science for Technologists*.
* NCRP Report No. 147. *Structural Shielding Design*.

---
