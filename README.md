# 🚀 Project Overview

This project is a **Page Replacement Algorithms Dashboard** built with **Python** and **Streamlit** that simulates and compares popular page replacement algorithms — **FIFO**, **LRU**, and **Optimal** — using randomly generated memory access streams.

It lets users explore how different algorithms perform in terms of **page faults** and **hit ratios** as the number of available frames changes. Interactive sliders, plots, and tables provide an intuitive way to visualize and analyze the results.

---

# 🎯 Features

- **Simulate** FIFO, LRU, and Optimal page replacement algorithms over a customizable memory access stream.

- **Adjustable parameters** through UI sliders:
  - Number of virtual pages.
  - Length of memory access stream.
  - Number of page frames.
  - Random seed for reproducibility.

- **Dynamic plots** showing:
  - Page faults vs frame size.
  - Hit ratio vs frame size.
  - Side-by-side bar charts comparing final performance.

- **Stepwise detailed logs** showing page-by-page memory frame status and whether each access was a hit or fault.

- **Downloadable CSV report** summarizing results for all frame sizes.

- **Data table** to compare stepwise frame contents and hits/faults across all three algorithms.
