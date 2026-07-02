import streamlit as st

# Guitar Root Notes, second "B" is Flat
notes_parser = {
    'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11
}

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

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

def diatonic_gen(scale_notes, scale_choice, sf):
    diatonic_degree = {
    'Major': ['Maj', 'min', 'min', 'Maj', 'Maj', 'min', ' Dim'],
    'Minor': ['min', ' Dim', 'Maj', 'min', 'min', 'Maj', 'Maj']
}
    
    chord_dia = diatonic_degree[scale_choice]
    chord_progression = []

    for i in range(7):
        chord_root_val = scale_notes[i]
        chord_root = sf[chord_root_val]
        full_chord = f"{chord_root}{chord_dia[i]}"
        chord_progression.append(full_chord)
    return chord_progression

#Triad created based on root_note and its derived diatonic scale
def triad_gen(scale_notes):
    triads = []
    for i in range(7):
        triad = [
            scale_notes[i],
            scale_notes[(i + 2) % 7],
            scale_notes[(i + 4) % 7]
        ]
        triads.append(triad)
    return triads

#Triad inversion, over number 12 interval means one octave higher than scale_notes
def triad_inv(triad):
    inv = [triad]
    inv.append([triad[1], triad[2], triad[0] + 12])
    inv.append([triad[2], triad[0] + 12, triad[1] + 12])
    return inv

#Transfer resulted notes in number back to display notes
def label_to_note(triad, user):
    return [user[note % 12] for note in triad]

def fretboard(target_notes, user, active_strings=None):
    strings = [4, 11, 7, 2, 9, 4]
    string_names = ['E', 'B', 'G', 'D', 'A', 'E']
    display_notes = [n % 12 for n in target_notes]
    
    # Default to all strings if no subset is passed
    if active_strings is None:
        active_strings = list(range(6))
    
    output = ""
    header = "   " + "  ".join(f"{fret:<4}" for fret in range(13))
    output += header + "\n"
    output += "  " + "=" * 78 + "\n"
    
    for i, open_note in enumerate(strings):
        # If the string isn't selected, skip it or print empty space
        if i not in active_strings:
            continue
            
        string_line = f"{string_names[i]} |"
        for fret in range(13):
            current_fret = (open_note + fret) % 12
            if current_fret in display_notes:
                string_line += f"{user[current_fret]:<3} | "
            else:
                string_line += "--  | "
        output += string_line + "\n"
    output += "  " + "=" * 78 + "\n"
    return output
    
st.set_page_config(page_title="Guitar Triad Master", page_icon="🎸", layout="centered")

st.title("🎸 GUITAR TRIAD MASTER")
st.markdown("---")

st.sidebar.header("⏣ Configuration")
user_note = st.sidebar.selectbox("Select Root Note:", list(notes_parser.keys()))
scale_choice = st.sidebar.selectbox("Select Scale Type:", ["Major", "Minor"])
mode_choice = st.sidebar.radio("Select Fretboard View Mode:", ["Full Fretboard", "3-String Mode (Triads)", "Single String Mode (Linear)"])
user_note_val = notes_parser[user_note]
scale_notes = scale_gen(user_note_val, scale_choice)
result_notes = notes
triads = triad_gen(scale_notes)
invs = triad_inv(triads[0])

# Fretboard Computing Section
active_strings = None
display_notes = invs[0] + invs[1] + invs[2]

if mode_choice == "3-String Mode (Triads)":
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
    st.subheader(f"𝄞 Practicing Triads for {user_note} {scale_choice.upper()}")

elif mode_choice == "Single String Mode (Linear)":
    string_choice = st.sidebar.slider("Select String (1=High E, 6=Low E):", 1, 6, 1)
    active_strings = [string_choice - 1]
    st.subheader(f"{user_note} {scale_choice} Scale — String {string_choice}")

else:
    st.subheader(f"Full Fretboard Mapping: {user_note} {scale_choice}")

fretboard_string = fretboard(display_notes, result_notes, active_strings)
st.code(fretboard_string, language="text")

# Inversion Section
st.subheader("🎶 Triad Inversions")
inv_cols = st.columns(3)

labels = ["Root Position", "1st Position", "2nd Position"]
for i, inv in enumerate(invs):
    with inv_cols[i]:
        result_triad = label_to_note(inv, result_notes)
        formatted_notes = " | ".join(f"{note:<2}" for note in result_triad)
        st.write(f"{labels[i]}")
        st.markdown(f"### `{formatted_notes}`")

# Diatonic Scale Section
st.subheader("🎼 Diatonic Scale Harmonization Sequence")
chords_progression = diatonic_gen(scale_notes, scale_choice, result_notes)

degree_roman = {
    'Major': ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°'],
    'Minor': ['i', 'ii°', 'III', 'iv', 'v', 'VI', 'VII']
}
degree_roman_choice = degree_roman[scale_choice]
cols = st.columns(7)
for i, col in enumerate(cols):
    with col:
        st.markdown(f"##### {degree_roman_choice[i]}")
        st.markdown(f"**{chords_progression[i]}**")
