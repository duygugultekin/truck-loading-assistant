# 📦 3D Bin Packing Problem – Truck Loading Assistant

---

## 📌 Introduction

Efficient truck loading is essential for reducing costs, saving time, and supporting sustainable logistics. This project tackles the 3D Bin Packing Problem by developing a smart, route-aware placement system. The solution considers real-world constraints like stacking limits, rotation permissions, and delivery sequences. Through visual simulations and intelligent algorithms, the system helps maximize volume utilization and improve operational decision-making.

---

## 🔍 Problem Overview

Initially inspired by real-world stacking challenges involving mechanical parts with irregular shapes — such as wheels with protrusions — this project addresses a more realistic version of the 3D Bin Packing Problem.

Traditional bin packing assumes perfectly rectangular boxes and uniform placement rules. However, in practice, logistics and warehouse operations face a different reality:

📦 **Manual stacking decisions** often result in poor space utilization.  
🔁 **Rotation and stacking rules** are commonly ignored, leading to unstable or infeasible placements.  
🚚 **Delivery sequence** is not considered in loading order, causing unloading conflicts.  
📉 **Excess truck usage** due to inefficient volume planning increases operational costs.  
🧱 **Protrusions and physical non-uniformities** (e.g., wheel rims) cause wasted vertical space if not algorithmically accounted for.

This project simulates a more realistic environment where:
- **Objects may have non-ideal dimensions** that require orientation optimization.
- **Layer-based and contact-sensitive placement logic** reflects how actual loads are physically supported.
- **Algorithmic strategies replace human intuition**, improving consistency, performance, and efficiency.

> Efficient truck loading is essential for reducing costs, saving time, and supporting sustainable logistics. The solution developed in this project is designed to automate and optimize placement decisions under realistic constraints — helping maximize volume usage and operational efficiency.

---

## ⚙️ Methodology

This project progressed through multiple algorithmic strategies, evolving from theoretical exploration to a practical, GUI-driven implementation.

---

### 🔹 Phase 1 – Foundational Strategies (Offline)

#### ✅ Exact Method
Exhaustive combinatorial method for small-scale datasets. Guarantees optimal placement but not scalable due to high time complexity.

#### 🧬 Genetic Algorithm
Used to optimize box placement order via crossover and mutation operations. Showed improvement over basic heuristics but was too slow for real-time use.

#### 📦 First Fit Decreasing (FFD)
Boxes sorted by volume (descending) and placed in the first space where they fit. Fast but not delivery-aware or rotation-optimized.

---

### 🔸 Phase 2 – Route-Aware Placement in GUI

#### 🔁 Greedy Sorting
Boxes are sorted based on volume or delivery priority using a greedy heuristic.

#### 📐 FFD-Based Placement with Rotation
Each box is:
- Tested in allowable rotations
- Placed at the first valid space without overlap
- Rejected if no feasible space found

#### 🧱 Layer-Based Model
A layer-oriented structure is used to pack boxes vertically, respecting surface constraints. Mimics real-world stacking patterns in trucks.

---
## 🖥️ How It Works

The project includes a Python-based GUI that allows users to simulate and visualize the box packing process in a container. The workflow is as follows:

### 🔽 Input
- Container dimensions and box list are provided via JSON or manual entry.
- Optional settings include:
  - Rotation permissions
  - Delivery order
  - Stacking constraints

### 🧠 Algorithm
- Boxes are sorted using a greedy strategy (e.g., volume-based or delivery-aware).
- A modified First Fit Decreasing algorithm places each box in the first valid position:
  - Tries multiple rotations
  - Checks boundary limits and collisions
  - Applies layer-based stacking logic
- Boxes that cannot be placed are logged as unplaced.

### 🖼️ Visualization
- Matplotlib is used to generate:
  - 2D/3D container views
  - Color-coded boxes with position and size
- Users can inspect, zoom, and save visual results.

### 📤 Output
- Reports include:
  - List of placed and unplaced boxes
  - Volume utilization %
  - Runtime in seconds
  - Exportable plots and JSON data

### ✅ GUI Features
- Rotation-aware placement
- Layer-by-layer stacking simulation
- Greedy route-based sorting
- Real-time packing feedback
## 📊 Results

The algorithm was tested on various datasets with different container sizes and box configurations. Below are representative results from real simulations using the GUI-based system.

### 🔢 Example Case

- **Container size**: 600 × 240 × 240 mm
- **Boxes provided**: 75
- **Placed successfully**: 68
- **Unplaced**: 7
- **Volume utilization**: 91.3%
- **Algorithm runtime**: ~2.7 seconds

### 📉 Observations

- Most unplaced boxes were either too large for remaining space or restricted by rotation constraints.
- Boxes placed using greedy priority achieved higher volume efficiency than naive sorting.
- Layer-based placement ensured better vertical packing and less air gaps.

### 🖼️ Visualization Output

- **3D view**: Shows stacked box layers with color-coded identification.
- **2D projections**: Top/side views for verification.
- **Unplaced list**: Logged for user review or retry.

> These results demonstrate that the implemented algorithm can efficiently handle realistic input sets with high packing accuracy and low runtime.


