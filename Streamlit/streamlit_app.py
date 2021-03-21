import numpy as np
import pandas as pd
import streamlit as st
import pickle
import streamlit.components.v1 as components

st.title('Predicting the Next TikTok Hit')
st.markdown('_Data courtesy of Spotify_')

#read-in data that was collected from collegefootballdata.com
#cache this function so that streamlit doesn't rerun it everytime a user input is changed
st.cache(allow_output_mutation=True)
def getData():
    #read in
    results = pd.read_csv(r'https://raw.githubusercontent.com/andrewdouglassmith1/Temp/main/kaggle_results_knn.csv')
    return results

#download csv function from https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
st.cache(allow_output_mutation=True)
def get_table_download_link(df, titleString):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="{titleString}.csv">Download {titleString} as CSV</a>'
    return href

results = getData()

#user input for date range
st.cache(allow_output_mutation=True)
years = st.slider("Release Year", min_value=1920, max_value=2021, value=(2015, 2020))

#user input for probability a success
success = st.slider("Probaility a Hit", min_value=0.0, max_value=1.0, value=(0.6, 1.0))

#user input for popularity
popularity = st.slider("Popularity", min_value=0, max_value=100, value=(40, 100))

#user input for danceability
danceability = st.slider("Danceability", min_value=0.0, max_value=1.0, value=(0.7, 1.0))

#user input for energy
energy = st.slider("Energy", min_value=0.0, max_value=1.0, value=(0.7, 1.0))

#user input for energy
valence = st.slider("Valence", min_value=0.0, max_value=1.0, value=(0.0, 1.0))

#filter recruits dataframe to match user selections
results = results[results['year'].between(years[0],years[1])]
results = results[results['prob a success'].between(success[0],success[1])]
results = results[results['popularity'].between(popularity[0],popularity[1])]
results = results[results['danceability'].between(danceability[0],danceability[1])]
results = results[results['energy'].between(energy[0],energy[1])]
results = results[results['valence'].between(valence[0],valence[1])]

# Reduce results dataframe to the top 100

top_results = results[0:100]

st.markdown('_Displaying the top 200_')


for index, row in top_results.iterrows():
    # Song name
    song_name = row['name']
    st.title(f'{song_name}')
    # Probaility of success
    prob_hit = row['prob a success']
    st.write("Probability a hit: {:6.0f}%".format(100*(prob_hit)))
    # Song link and embedding
    link = row['link']
    link_button = f'[Having trouble viewing the song - click here]({link})'
    components.iframe(link)
    st.markdown(link_button,unsafe_allow_html=True)
