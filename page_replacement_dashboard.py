import random
from collections import deque, OrderedDict
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

# ----------- Algorithms ------------

def fifo_page_replacement(access_stream, num_frames):
    memory = set()
    queue = deque()
    page_faults = 0
    hits = 0
    for page in access_stream:
        if page in memory:
            hits += 1
        else:
            page_faults += 1
            if len(memory) >= num_frames:
                oldest = queue.popleft()
                memory.remove(oldest)
            memory.add(page)
            queue.append(page)
    hit_ratio = hits / len(access_stream)
    return page_faults, hit_ratio


def lru_page_replacement(access_stream, num_frames):
    memory = OrderedDict()
    page_faults = 0
    hits = 0
    for page in access_stream:
        if page in memory:
            hits += 1
            memory.move_to_end(page)
        else:
            page_faults += 1
            if len(memory) >= num_frames:
                memory.popitem(last=False)
            memory[page] = True
    hit_ratio = hits / len(access_stream)
    return page_faults, hit_ratio


def optimal_page_replacement(access_stream, num_frames):
    memory = set()
    frame_list = []
    page_faults = 0
    hits = 0
    for i, page in enumerate(access_stream):
        if page in memory:
            hits += 1
        else:
            page_faults += 1
            if len(memory) < num_frames:
                memory.add(page)
                frame_list.append(page)
            else:
                farthest = -1
                index_to_replace = -1
                for j, frame_page in enumerate(frame_list):
                    try:
                        index = access_stream[i + 1:].index(frame_page)
                    except ValueError:
                        index = float('inf')
                    if index > farthest:
                        farthest = index
                        index_to_replace = j
                page_to_remove = frame_list[index_to_replace]
                memory.remove(page_to_remove)
                frame_list[index_to_replace] = page
                memory.add(page)
    hit_ratio = hits / len(access_stream)
    return page_faults, hit_ratio


# New functions for step-by-step logs

def fifo_steps(access_stream, num_frames):
    memory = set()
    queue = deque()
    steps = []
    for page in access_stream:
        replaced = None
        hit = page in memory
        if not hit:
            if len(memory) >= num_frames:
                replaced = queue.popleft()
                memory.remove(replaced)
            memory.add(page)
            queue.append(page)
        steps.append({
            "Page": page,
            "Frames": list(queue),
            "Hit/Fault": "Hit" if hit else "Fault",
            # "Replaced": replaced  # removed per your request
        })
    return steps


def lru_steps(access_stream, num_frames):
    memory = OrderedDict()
    steps = []
    for page in access_stream:
        replaced = None
        hit = page in memory
        if hit:
            memory.move_to_end(page)
        else:
            if len(memory) >= num_frames:
                replaced, _ = memory.popitem(last=False)
            memory[page] = True
        steps.append({
            "Page": page,
            "Frames": list(memory.keys()),
            "Hit/Fault": "Hit" if hit else "Fault",
            # "Replaced": replaced
        })
    return steps


def optimal_steps(access_stream, num_frames):
    memory = set()
    frame_list = []
    steps = []
    for i, page in enumerate(access_stream):
        replaced = None
        hit = page in memory
        if not hit:
            if len(memory) < num_frames:
                memory.add(page)
                frame_list.append(page)
            else:
                farthest = -1
                index_to_replace = -1
                for j, frame_page in enumerate(frame_list):
                    try:
                        index = access_stream[i + 1:].index(frame_page)
                    except ValueError:
                        index = float('inf')
                    if index > farthest:
                        farthest = index
                        index_to_replace = j
                replaced = frame_list[index_to_replace]
                memory.remove(replaced)
                frame_list[index_to_replace] = page
                memory.add(page)
        steps.append({
            "Page": page,
            "Frames": list(frame_list),
            "Hit/Fault": "Hit" if hit else "Fault",
            # "Replaced": replaced
        })
    return steps


# ----------- Streamlit UI ------------

st.title("📊 Page Replacement Algorithms Dashboard")

# User inputs
NUM_PAGES = st.slider("Number of Virtual Pages", min_value=5, max_value=30, value=10)
ACCESS_STREAM_LENGTH = st.slider("Memory Access Stream Length", min_value=20, max_value=200, value=50)
MAX_FRAMES = st.slider("Maximum Number of Frames", min_value=1, max_value=20, value=10)
seed = st.number_input("Random Seed (for reproducibility)", min_value=0, max_value=9999, value=42)

if st.button("🚀 Generate & Analyze"):

    random.seed(seed)
    access_stream = [random.randint(0, NUM_PAGES - 1) for _ in range(ACCESS_STREAM_LENGTH)]

    st.markdown(f"### 🧠 Virtual Pages: `{NUM_PAGES}`")
    st.markdown(f"### 🔢 Memory Access Stream (first 20 shown):")
    st.code(str(access_stream[:20]) + " ...")

    fifo_faults_list = []
    fifo_hit_ratios = []
    lru_faults_list = []
    lru_hit_ratios = []
    optimal_faults_list = []
    optimal_hit_ratios = []

    for frames in range(1, MAX_FRAMES + 1):
        fifo_faults, fifo_hits = fifo_page_replacement(access_stream, frames)
        lru_faults, lru_hits = lru_page_replacement(access_stream, frames)
        optimal_faults, optimal_hits = optimal_page_replacement(access_stream, frames)

        fifo_faults_list.append(fifo_faults)
        fifo_hit_ratios.append(fifo_hits)
        lru_faults_list.append(lru_faults)
        lru_hit_ratios.append(lru_hits)
        optimal_faults_list.append(optimal_faults)
        optimal_hit_ratios.append(optimal_hits)

    frame_sizes = list(range(1, MAX_FRAMES + 1))

    # ----------- Plot Section -----------
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # 1. Page Faults Line Plot
    axs[0].plot(frame_sizes, fifo_faults_list, label='FIFO', marker='o', color='skyblue')
    axs[0].plot(frame_sizes, lru_faults_list, label='LRU', marker='o', color='lightgreen')
    axs[0].plot(frame_sizes, optimal_faults_list, label='Optimal', marker='o', color='salmon')
    axs[0].set_title("📉 Page Faults vs Frame Size")
    axs[0].set_xlabel("Number of Frames")
    axs[0].set_ylabel("Page Faults")
    axs[0].legend()
    axs[0].grid(True, linestyle='--', alpha=0.6)

    # 2. Hit Ratio Line Plot
    axs[1].plot(frame_sizes, fifo_hit_ratios, label='FIFO', marker='o', color='skyblue')
    axs[1].plot(frame_sizes, lru_hit_ratios, label='LRU', marker='o', color='lightgreen')
    axs[1].plot(frame_sizes, optimal_hit_ratios, label='Optimal', marker='o', color='salmon')
    axs[1].set_title("📈 Hit Ratio vs Frame Size")
    axs[1].set_xlabel("Number of Frames")
    axs[1].set_ylabel("Hit Ratio")
    axs[1].set_ylim(0, 1.05)
    axs[1].legend()
    axs[1].grid(True, linestyle='--', alpha=0.6)

    # 3. Final Frame Comparison (Bar Graphs)
    algos = ['FIFO', 'LRU', 'Optimal']
    faults_at_max = [fifo_faults_list[-1], lru_faults_list[-1], optimal_faults_list[-1]]
    hits_at_max = [fifo_hit_ratios[-1], lru_hit_ratios[-1], optimal_hit_ratios[-1]]
    width = 0.35
    x = [0, 1, 2]

    axs[2].bar([p - width / 2 for p in x], faults_at_max, width=width, label='Page Faults',
               color=['skyblue', 'lightgreen', 'salmon'])
    axs[2].bar([p + width / 2 for p in x], hits_at_max, width=width, label='Hit Ratios',
               color=['navy', 'green', 'darkred'])
    axs[2].set_xticks(x)
    axs[2].set_xticklabels(algos)
    axs[2].set_title(f"📊 Comparison at {MAX_FRAMES} Frames")
    axs[2].set_ylabel("Values")
    axs[2].legend()
    axs[2].grid(axis='y', linestyle='--', alpha=0.6)

    # Bar annotations
    for rect in axs[2].patches:
        height = rect.get_height()
        axs[2].annotate(f'{height:.2f}' if isinstance(height, float) else f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)

    st.pyplot(fig)

    # ----------- CSV Export -----------
    import csv
    from io import StringIO

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow([
        "Step",
        "FIFO_Page_Faults", "FIFO_Hit_Ratio",
        "LRU_Page_Faults", "LRU_Hit_Ratio",
        "Optimal_Page_Faults", "Optimal_Hit_Ratio"
    ])

    for i in range(MAX_FRAMES):
        csv_writer.writerow([
            i + 1,
            fifo_faults_list[i], fifo_hit_ratios[i],
            lru_faults_list[i], lru_hit_ratios[i],
            optimal_faults_list[i], optimal_hit_ratios[i]
        ])

    csv_buffer.seek(0)
    st.download_button(
        label="📥 Download CSV Results",
        data=csv_buffer.getvalue(),
        file_name='page_replacement_results.csv',
        mime='text/csv'
    )

    # ----------- Stepwise Comparison Table -----------

    fifo_log = fifo_steps(access_stream, MAX_FRAMES)
    lru_log = lru_steps(access_stream, MAX_FRAMES)
    optimal_log = optimal_steps(access_stream, MAX_FRAMES)

    combined_rows = []
    for i in range(len(access_stream)):
        combined_rows.append({
            "Step": i + 1,
            "Page Accessed": access_stream[i],

            "FIFO Frames": ", ".join(map(str, fifo_log[i]["Frames"])),
            "FIFO Hit/Fault": fifo_log[i]["Hit/Fault"],

            "LRU Frames": ", ".join(map(str, lru_log[i]["Frames"])),
            "LRU Hit/Fault": lru_log[i]["Hit/Fault"],

            "Optimal Frames": ", ".join(map(str, optimal_log[i]["Frames"])),
            "Optimal Hit/Fault": optimal_log[i]["Hit/Fault"],
        })

    df_comparison = pd.DataFrame(combined_rows)

    # Reset index to avoid unnamed index column in Streamlit
    df_comparison_reset = df_comparison.reset_index(drop=True)

    st.markdown("### 📋 Page Replacement Comparison")

    # Hide the index column in Streamlit display
    st.dataframe(df_comparison_reset.style.hide(axis="index"), height=500)
