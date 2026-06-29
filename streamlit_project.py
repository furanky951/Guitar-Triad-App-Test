import streamlit as st

# Guitar Root Notes, second "B" is Flat
notes_parser = {
    'C': 0, 'C#': 1, 'DB': 1, 'D': 2, 'D#': 3, 'EB': 3, 'D#/EB': 3, 'E': 4, 'F': 5, 'F#': 6, 'GB': 6, 'F#/GB': 6,
    'G': 7, 'G#': 8, 'AB': 8, 'G#/AB': 8, 'A': 9, 'A#': 10, 'BB': 10, 'A#/BB': 10, 'B': 11
}

sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
flats  = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

#Major and Minor Scale : [Interval]
scale = {
    'Major': [0, 2, 4, 5, 7, 9, 11],
    'Minor': [0, 2, 3, 5, 7, 8, 10]
}

#Scale notes generated based on the chosen notes(AKA root_note) and scale (Major or Minor)
def scale_gen(root_note,scale_choice):
    interval = scale[scale_choice]
    scale_notes = [(root_note + i) % 12 for i in interval]
    return scale_notes

#Triad created based on root_note and its derived diatonic scale
def diatonic_triads(scale_notes):
    triads = []
    for i in range(7):
        triad = [
            scale_notes[i],
            scale_notes[(i + 2) % 7],
            scale_notes[(i + 4) % 7]
        ]
        triads.append(triad)
    return triads

#Triad inversion, >12th interval means one octave higher than scale_notes
def triad_inv(triad):
    inv = [triad]
    inv.append([triad[1], triad[2], triad[0] + 12])
    inv.append([triad[2], triad[0] + 12, triad[1] + 12])
    return inv

#Transfer resulted notes in number back to display notes
def label_to_note(triad, user):
    return [user[note % 12] for note in triad]

def fretboard(display_notes, user, active_strings=None):
    strings = [4, 11, 7, 2, 9, 4]
    string_names = ['E', 'B', 'G', 'D', 'A', 'E']
    target_notes_mod = [n % 12 for n in display_notes]
    
    # Default to all strings if no subset is passed
    if active_strings is None:
        active_strings = list(range(6))
    
    output = ""
    header = "    " + "  ".join(f"{fret:<4}" for fret in range(13))
    output += header + "\n"
    output += "    " + "=" * 80 + "\n"
    
    for i, open_note in enumerate(strings):
        # If the string isn't selected, skip it or print empty space
        if i not in active_strings:
            continue
            
        string_line = f"{string_names[i]} |"
        for fret in range(13):
            current_note_val = (open_note + fret) % 12
            if current_note_val in target_notes_mod:
                string_line += f"{user[current_note_val]:<3} | "
            else:
                string_line += "--  | "
        output += string_line + "\n"
    output += "    " + "=" * 80 + "\n"
    return output
    
st.set_page_config(page_title="Guitar Triad Visualizer", page_icon="🎸", layout="centered")

st.title("🎸 GUITAR TRIAD MASTER")
st.write("PRACTICE YOUR TRIAD")
st.markdown("---")

# 1. Inputs via Sidebar
st.sidebar.header("🎯 Configuration")
root_selection = st.sidebar.selectbox("Select Root Note:", list(notes_parser.keys()))
scale_selection = st.sidebar.selectbox("Select Scale Type:", ["Major", "Minor"])
mode_selection = st.sidebar.radio("Select Fretboard View Mode:", ["Full Fretboard", "3-String Set (Triads)", "Single String (Linear)"])

# 2. Process Core Logic Instantly
user_note_val = notes_parser[root_selection]
scale_notes = scale_gen(user_note_val, scale_selection)

# Accidental Detector
if "b" in root_selection or ("B" in root_selection and root_selection != "B"):
    result_nomenclature = flats
else:
    result_nomenclature = sharps

triads = diatonic_triads(scale_notes)
invs = triad_inv(triads[0])

# 3. Handle Interactive View Layouts
active_strings = None

if mode_selection == "3-String Set (Triads)":
    string_set_choice = st.sidebar.selectbox("Choose String Set:", [
        "E, B, G (Strings 1, 2, 3)", 
        "B, G, D (Strings 2, 3, 4)", 
        "G, D, A (Strings 3, 4, 5)", 
        "D, A, E (Strings 4, 5, 6)"
    ])
    set_mapping = {
        "E, B, G (Strings 1, 2, 3)": [0, 1, 2],
        "B, G, D (Strings 2, 3, 4)": [1, 2, 3],
        "G, D, A (Strings 3, 4, 5)": [2, 3, 4],
        "D, A, E (Strings 4, 5, 6)": [3, 4, 5]
    }
    active_strings = set_mapping[string_set_choice]
    # Merge all inversion note values to map them out together
    display_notes = invs[0] + invs[1] + invs[2]
    st.subheader(f"Practicing Triads for {root_selection} {scale_selection.upper()}")

elif mode_selection == "Single String (Linear)":
    string_choice = st.sidebar.slider("Select String (1=High E, 6=Low E):", 1, 6, 1)
    active_strings = [string_choice - 1]
    display_notes = scale_notes
    st.subheader(f"{root_selection} {scale_selection} Scale — String {string_choice}")

else:  # Full Fretboard
    display_notes = scale_notes
    st.subheader(f"Full Fretboard Mapping: {root_selection} {scale_selection}")

# 4. Render the Monospaced Fretboard
fretboard_string = fretboard(display_notes, result_nomenclature, active_strings)
st.code(fretboard_string, language="text")

# 5. Render Aligned Text Inversions Bottom Sheet
st.markdown("### 🎼 Triad Inversions Breakdown")
for i, inv in enumerate(invs):
    note_names = label_to_note(inv, result_nomenclature)
    alignment = [f"{note:<2}" for note in note_names]
    st.markdown(f"**Inversion {i}**: `{' | '.join(alignment)}`")
