# EDL-Time_Sum: Precise Source Material Usage Analysis
# Python script for accurate source material usage reporting from an EDL.
# Author: Johannes Glaw | License: GNU AGPL-3.0

# Requirements:
# - Python 3.6+
# - Standard libraries only: re, collections

# Usage:
# 1. Duplicate your sequence in your editor (Premiere, DaVinci, Avid)
# 2. Consolidate all video cuts onto a single video track (V1)
# 3. Export as CMX 3600 EDL

# ---------------- CONFIGURATION ----------------
# Path to your EDL file
EDL_FILE_PATH="ADD/YOUR/PATH/TO/EDL_FILE.edl"  # <--- ENTER YOUR PATH HERE
# Frame rate of your source clips (e.g., 24, 25, 30)
SOURCE_FRAMERATE=25  # <--- ENTER YOUR SOURCE CLIP FRAMERATE HERE

# ---------------- RUN ----------------
# Open terminal, navigate to script folder, and run:
# $ python edl-time-sum.py

# ---------------- OUTPUT ----------------
# - Debug log for merged/ignored overlaps
# - Total Additive Length (inflated)
# - Total Unique Length (accurate billing)
# - Difference between totals

# Enjoy precise reporting! 🥳

# Support the Author: https://buymeacoffee.com/ReflexLabFlow
