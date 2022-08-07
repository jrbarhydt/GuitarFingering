import streamlit as st
import pandas as pd
import plotly.graph_objects as go

data_filepath = "chord-fingers.csv"


st.title("Guitar Chord Data Explorer")
st.markdown("_Select frets in sidebar on the left._")

with st.sidebar:
    def fret_to_key(fret_option):
        if fret_option in [0, "?"]:
            return 0
        if fret_option in [1, "x"]:
            return 1
        return int(fret_option) + 2
    if st.button("Clear Fret Options"):
        selected_positions = [0] * 6
    else:
        selected_positions = [3, "?", "?", "?", "?", 3]
    st.title("Select frets to explore chords")
    st.markdown("_( **'?'** allows any, **'x'** is muted/unplayed string)_")
    radio_options = ("?", "x", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

    columns = st.columns(6)
    radio_labels = ("E|", "A|", "D|", "G|", "B|", "E|")
    for col_no, column in enumerate(columns):
        with column:
            selected_positions[col_no] = st.radio(label=radio_labels[col_no],
                                                  options=radio_options,
                                                  key=col_no,
                                                  index=fret_to_key(selected_positions[col_no]))
    print("selected", selected_positions)

selected_positions = [element if element != "?" else None for element in selected_positions]

root_chords = ["E", "A", "D", "G", "B", "E"]
cardinal_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_to_fret(note: str, string_no: int):
    # init current note, position in scale, and fret number
    curr = root_chords[string_no]
    pos = cardinal_notes.index(curr)
    fret = 0

    # mute string, note has no index
    if not note:
        return None
    # play open string, sharped note is root
    if cardinal_notes[(pos + len(cardinal_notes) - 1) % len(cardinal_notes)] + "#" == note:
        return 0

    while curr != note[0]:
        curr = cardinal_notes[(pos + 1) % len(cardinal_notes)]
        pos += 1
        fret += 1
    fret -= note.count("b")
    fret += note.count("#")
    return fret


df = pd.read_csv(data_filepath)
positions = df["FINGER_POSITIONS"].str.split(',', expand=True)
note_name = df["NOTE_NAMES"].str.split(',', expand=True)

fret_series = []
for i, record in enumerate(positions.iterrows()):
    notes = list(df.loc[i]["NOTE_NAMES"].split(','))

    for j, val in enumerate(record[1]):
        if val == "x":
            notes.insert(j, '')
    df.loc[i]["NOTE_NAMES"] = notes
    frets = []
    for k, n in enumerate(notes):
        frets.append(note_to_fret(n, k))

    # determine if fret number should be raised by one octave, when highest fret is more than 7 frets away
    depth = max([fret for fret in frets if fret is not None])
    frets = [fret if fret is None else fret+12 if (depth-fret > 7) else fret for fret in frets]

    fret_series.append(frets)


df["FRETS"] = fret_series
df[[f"FRETS_{i}" for i in range(len(root_chords))]] = pd.DataFrame(df.FRETS.tolist(), index=df.index)


query_terms = []
for i in range(len(selected_positions)):
    if selected_positions[i] is not None:
        if selected_positions[i] == "x":
            query_terms.append(f'FRETS_{i}.isnull()')
        else:
            query_terms.append(f'FRETS_{i}=={selected_positions[i]}')
query = ' & '.join(query_terms)
print(query)
df_filtered = df.query(query) if query else df
df_filtered = df_filtered[["FRETS", "CHORD_ROOT", "CHORD_TYPE", "CHORD_STRUCTURE"]]

# cols = st.columns((3, 5))

pie_values = df_filtered["CHORD_ROOT"].value_counts()
pie_colors = ['68ace5', '#cf4520', '#cba052', '#ff9e1b', '#ff6900', '#9e5330']
pie = go.Pie(labels=list(pie_values.index), values=pie_values.values,
             marker=dict(colors=pie_colors, line=dict(color='#000000', width=2)))
fig = go.Figure(data=[pie])
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)

# st.table(df_filtered)

fig = go.Figure(
    data=go.Table(header=dict(values=df_filtered.columns,
                              font_color='white',
                              line_color='darkslategray',
                              fill_color='#002D72',
                              align='center',
                              font_size=20),
                  cells=dict(values=list(df_filtered.transpose().values),
                             font_color='white',
                             line_color='darkslategray',
                             fill_color='#68ace5',
                             align='center',
                             height=30,
                             font_size=18)))
fig.update_layout(height=1000, margin=dict(l=0, r=0, t=0, b=0), template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

import time
print(time.time())
print(df_filtered.CHORD_ROOT.unique())
c = df_filtered["CHORD_ROOT"].value_counts()
print(list(c.index), c.values)
