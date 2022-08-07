# GuitarFingering.py

This application launches a Streamlit dashboard to explore a guitar chord database by selecting fingerings based on fret locations.

_hosted by Streamlit.io at_<br>
https://jrbarhydt-guitarfingering-guitarfingering-zljmbo.streamlitapp.com/


---

## Data Source:

chord-fingers.csv from:<br>
https://archive.ics.uci.edu/ml/datasets/Guitar+Chords+finger+positions <br/>
original data source:<br>
https://wwww.fachords.com/guitar-chord/

---

## To Run:

    - streamlit run GuitarFingering.py

---

## Requirements:

    - python 3.9
    - streamlit
    - pandas
    - plotly

---

## Data Preparation:
    
    - All Data was semicolon delimited
    - FINGER_POSITIONS was comma delimited, and split into 6 columns
    - NOTE_NAMES was comma delimited, had null values filled with blank spaces, and split into 6 columns
