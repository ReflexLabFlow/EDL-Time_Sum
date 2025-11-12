# EDL-Time_Sum: Precise Source Material Usage Analysis

# This Python script is designed for video editors, post-production supervisors, 
# and media professionals who need accurate reporting on source material usage 
# within an Edit Decision List (EDL).

# Accurately calculates the unique, non-redundant usage time of source clips from an EDL,
# ignoring overlaps and multi-use for precise billing (Meldung rechnen) and royalty reports.

# ============================================================================

# 📋 Metadata
# Author: Johannes Glaw
# License: GNU Affero General Public License v3.0 (AGPL-3.0)

# ============================================================================

# 🛠️ Requirements & Setup
# - Only standard Python libraries are used (re, collections)
# - Minimal Requirement: Python 3.6 or newer
# - No external dependencies required

# ============================================================================

# 🎬 How to Use

# Step 1: Prepare Your Edit Decision List (EDL)
# 1. Duplicate your sequence in your editing program (Premiere, DaVinci Resolve, Avid).
# 2. Consolidate all video cuts onto a single video track (V1) to ensure clean EDL.
# 3. Export the sequence as a standard CMX 3600 EDL file.

# Step 2: Configure the Script
# 1. Open the `edl-time-sum.py` script.
# 2. Locate the `--- CONFIGURATION ---` section.
# 3. Replace the placeholder text with the full path to your exported EDL file.

# --- CONFIGURATION ---
EDL_FILE_PATH="ADD/YOUR/PATH/TO/EDL_FILE.edl"  # <--- ENTER YOUR PATH HERE

# Step 3: Run the Analysis
# Open terminal and navigate to the script directory:
# $ python edl-time-sum.py

# Step 4: Review Results
# The script outputs:
# - Debug log showing merged or ignored overlaps
# - Total Additive Length of all source clips (inflated)
# - Total Unique Length (accurate billing time)
# - Difference between the totals

# Finished! Enjoy your precise usage report! 🥳

# ============================================================================

# ☕ Support the Author
# If this tool saves you time and ensures accurate reporting, consider supporting development:
# https://buymeacoffee.com/ReflexLabFlow
