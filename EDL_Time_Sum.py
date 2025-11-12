# CODE-ASSISTENT: EDL-Time_Sum

# --- METADATEN & LIZENZ ---
__author__ = "Johannes Glaw"
__license__ = "The GNU Affero General Public License v3.0 (AGPL-3.0)"

# --- CONFIGURATION ---
# Defines the frame rate for timecode calculation.
FRAMERATE = 25 # change it, if it's different
# Define the path to the EDL file.
EDL_FILE_PATH = "" #add path to your EDL file here


import re
from collections import defaultdict

# --- HELPER FUNCTIONS ---

def timecode_to_frames(timecode_str, framerate=FRAMERATE):
    """Converts a timecode string (HH:MM:SS:FF) into the total number of frames."""
    try:
        parts = timecode_str.split(':')
        if len(parts) != 4:
            raise ValueError("Invalid timecode format.")
            
        h, m, s, f = map(int, parts)
        total_frames = (h * 3600 + m * 60 + s) * framerate + f
        return total_frames
    except Exception as e:
        return 0

def frames_to_timecode(total_frames, framerate=FRAMERATE):
    """Converts the total number of frames back into a timecode string (HH:MM:SS:FF)."""
    h = int(total_frames // (3600 * framerate))
    remaining_frames = total_frames % (3600 * framerate)
    m = int(remaining_frames // (60 * framerate))
    remaining_frames %= (60 * framerate)
    s = int(remaining_frames // framerate)
    f = int(remaining_frames % framerate)
    return f"{h:02}:{m:02}:{s:02}:{f:02}"


def analyze_edl_material_lengths(file_path):
    # Regex for extracting timecodes and clip names
    edl_entry_pattern = re.compile(
        r'^\s*\d{3}\s+AX\s+V\s+C\s+(\d{2}:\d{2}:\d{2}:\d{2})\s+(\d{2}:\d{2}:\d{2}:\d{2})\s'
    )
    clip_name_pattern = re.compile(r'^\* FROM CLIP NAME:\s*(.*)$')
    
    unique_segments = defaultdict(list)    # For Unique/Merged Length
    total_usage_frames = defaultdict(int)  # For Additive Length
    
    current_clip_name = None
    
    if file_path == "ADD YOUR PATH TO EDL FILE HERE":
        print("ERROR: Please update 'EDL_FILE_PATH' in the CONFIGURATION section with your actual file path.")
        return

    try:
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"ERROR: File not found at '{file_path}'")
        return
    except Exception as e:
        print(f"ERROR reading file: {e}")
        return

    print("--- 🎬 EDL File Analysis Started ---")
    print(f"Using path: {file_path}")

    # 1. Data Acquisition
    for line in lines:
        clip_match = clip_name_pattern.search(line)
        if clip_match:
            current_clip_name = clip_match.group(1).strip()
            continue
        
        entry_match = edl_entry_pattern.search(line)
        if entry_match and current_clip_name:
            sc_in_str = entry_match.group(1)
            sc_out_str = entry_match.group(2)
            
            sc_in_frames = timecode_to_frames(sc_in_str)
            sc_out_frames = timecode_to_frames(sc_out_str)
            
            duration_frames = sc_out_frames - sc_in_frames
            
            if duration_frames > 0:
                unique_segments[current_clip_name].append((sc_in_frames, sc_out_frames))
                total_usage_frames[current_clip_name] += duration_frames
            
            current_clip_name = None

    # 2. Calculating Unique/Merged Length (Length 2)
    grand_unique_frames = 0
    unique_results = {} # Stores the Unique results per clip
    
    # --- Debug Logging (Only Actions) ---
    print("\n--- 📣 Debug Log: Timecode Segment Merging (Overlap/Extension) ---")
    
    sorted_unique_segments = sorted(unique_segments.items())

    for clip_name, segments in sorted_unique_segments:
        if not segments:
            continue
            
        segments.sort(key=lambda x: x[0])
        
        print(f"\n> **CLIP: {clip_name}** ({len(segments)} Cuts)")
        
        merged_segments = []
        current_start, current_end = segments[0]
        
        # Iterate through all cuts starting from the second segment
        for next_start, next_end in segments[1:]:
            
            if next_start < current_end: 
                # Overlap or adjacent
                
                old_end_tc = frames_to_timecode(current_end)
                current_end = max(current_end, next_end)
                new_end_tc = frames_to_timecode(current_end)
                
                if old_end_tc != new_end_tc:
                    # ACTION: EXTENDED (If the end was actually prolonged)
                    print(f">   - **ACTION: EXTENDED** -> Merge from {frames_to_timecode(next_start)} to {new_end_tc}")
                else:
                    # ACTION: OVERLAP (If the cut is fully inside the current segment)
                    print(f">   - **ACTION: OVERLAP** -> Segment {frames_to_timecode(next_start)} ignored")
            else:
                # ACTION: SEGMENT CLOSED (Not logged)
                merged_segments.append((current_start, current_end))
                current_start, current_end = next_start, next_end
        
        # Add the last/current segment
        merged_segments.append((current_start, current_end))

        # Sum the lengths of the merged segments
        unique_frames_for_clip = sum(end - start for start, end in merged_segments)
        grand_unique_frames += unique_frames_for_clip
        unique_results[clip_name] = unique_frames_for_clip
        
        # Closing line per clip
        print(f">   - **END**: {len(merged_segments)} unique segments. Duration: **{frames_to_timecode(unique_frames_for_clip)}**")
        print("-" * 50)
            
    # 3. Final Result Output: Direct Comparison
    
    print("\n## 📊 Final Result Overview and Direct Comparison 🚀")
    
    grand_total_usage_frames = sum(total_usage_frames.values())
    
    # --- Individual Values (Additive Usage) ---
    print("\n### 1. Total Source Material Length (Incl. Multiple Uses/Additive) ⏱️")
    sorted_total_usage = sorted(total_usage_frames.items())
    for clip_name, frames in sorted_total_usage:
        print(f"* **{clip_name}**: {frames_to_timecode(frames)}")
    
    # --- Individual Values (Unique Usage) ---
    print("\n### 2. Total Source Material Length (Multiple Uses Counted Only Once!) 🧩")
    sorted_unique_results = sorted(unique_results.items())
    for clip_name, frames in sorted_unique_results:
        print(f"* **{clip_name}**: {frames_to_timecode(frames)}")


    # --- Comparison and Final Totals ---
    total_difference_frames = grand_total_usage_frames - grand_unique_frames
    
    print("\n---")
    print("\n### 🥇 Final Totals and Difference")
    print(f"| **Total Length (Additive)** | **{frames_to_timecode(grand_total_usage_frames)}** |")
    print(f"| **Total Length (Unique/Counted Once)** | **{frames_to_timecode(grand_unique_frames)}** |")
    print(f"| **Difference (Multiple Use Overlap)** | **{frames_to_timecode(total_difference_frames)}** |")

    print("\n--- ✅ Analysis Complete ---")


# --- IMPLEMENTATION ---

# Execute the analysis using the configured path
analyze_edl_material_lengths(EDL_FILE_PATH)
