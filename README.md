# Project Title: Guitar Triad Master
#### Video Demo: URL
#### Description: A small project built using Python to help guitarists map out triad inversions dynamically across the fingerboard.

This tool primarily uses modulo 12 to calculate and output scale intervals and notes relationship, then display on a simple computer ASCII style fingerboard.
The tool functions as below:
* User picks a root note and a scale
* scale_gen(): Return the diatonic scale based on user's chosen note and scale
* diatonic_gen(): Create the diatonic scale according to chosen note and scale
* triad_gen(): Return the according triad based on scale_gen() output
* triad_inv(): Create 3 version of the triad by rotating the sequence of notes
* label_to_note(): Return the notes from numerical value back to alphabets
* fretboard(): Output and display the notes on a ASCII style fretboard in 3 modes
** Full fretboard mode - Show the whole fretboard
** 3-string set mode - Show only 3 strings
** Single string mode - Show only 1 string

Additional: Streamlit cloud version of the code is included and deployed primarily for people who doesn't have Python installed on PC.
* Streamlit URL: https://guitar-triad-app-aeze6comfjgdjlpemf5y97.streamlit.app/
* OR pip install Streamlit and enter "streamlit run streamlit_project.py" in the terminal for local deploy

Future Addition:
* Diatonic Triad
* Metronome
* Chord backtrack
