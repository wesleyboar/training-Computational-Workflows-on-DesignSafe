# Decision Matrix
***Decision Matrix for OpenSees on DesignSafe***

| Relative Scope   | DesignSafe Platform  | Interface                    | Sequential OpenSees | Parallel OpenSeesSP | Parallel OpenSeesMP | OpenSeesPy     |
|------------------|----------------------|-------------------------------|----------------------|----------------------|----------------------|----------------|
| **Small-Medium**        | JupyterHubᶜᵈ      | Terminal                | 🖥️ Run Input Script | ⚙️ Run via MPI  | ⚙️ Run via MPI  | 🖥️ Run Input Script |
|                  |                      | Python Jupyter Notebook       | 💻 Run via *os* shell command  | 💻 Run MPI via *os* shell command | 💻 Run MPI via *os* shell command | 🖥️ Integrate into Notebook cells or via shell command |
| **Small-Medium** | Web Portal           | OpenSees-Express VMᵃ         | 📤 Submit Seq Job    | 🔴 Not Available    | 🔴 Not Available      | 🔴 Not Available |
|                  | Web Portal           | Submit on HPCᵇ    | 🔶 Less Efficient      | 📤 Submit to HPC     | 📤 Submit to HPC     | 📤 Submit to HPC |
|                  | Tapis in JupyterHub  | OpenSeesSP/MP Submit on HPCᵇ    | 🔶 Less Efficient      | 📤 Submit to HPC     | 📤 Submit to HPC     | 📤 Submit to HPC |
| **Large–Extra-Large** | HPC & TACCᵉ     | SSH to HPC and submit via Launcher                | 🔶 Less Efficient     | 📤 Submit to HPC     | 📤 Submit to HPC     | 📤 Submit to HPC |
|                  |                      | Submit via Tapis3 from JupyterHub | 🔶 Less Efficient| 📤 Submit to HPC| 📤 Submit to HPC| 📤 Submit to HPC |
| **Very Many Jobs** | HPC & TACCᵉ     | SSH to HPC and submit via Launcher                | 📤 Submit to HPC     | 📤 Submit to HPC     | 📤 Submit to HPC     | 📤 Submit to HPC |
|                  |                      | Submit via Tapis3 from JupyterHubᵈ | 📤 Submit to HPC| 📤 Submit to HPC| 📤 Submit to HPC| 📤 Submit to HPC |

Legend (symbols):
- 🖥️ Run interactively (small jobs, direct access in terminal or notebook)
- 💻 Run via OS package or shell commands in Jupyter Notebook (e.g. `!opensees`, `subprocess`)
- ⚙️ Run via MPI (parallel execution for small or large jobs)
- 📤 Submit jobs to VM, HPC, or Launcher
- 🔶 Less efficient method
- 🔴 Not available
- – Feature planned or not yet supported

Footnotes:


ᵃ OpenSees-Express runs in its own dedicated shared-resource VM. It only has one node and few processors. -- **NO QUEUE**<br>
ᵇ The current Execution System on DesignSafe for the Web Portal is Stampede3. It requires an **Allocation + QUEUE Wait**<br>
ᶜ JupyterHub runs on its own dedicated shared-resource VM   -- **NO QUEUE Wait**<br>
ᵈ JupyterHub has options for Python, MATLAB, R, and Julia  <br>
ᵉ TACC has more Execution Systems and queues. It requires an **Allocation + QUEUE Wait**<br>
