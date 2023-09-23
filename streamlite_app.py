import streamlit as st
import pandas as pd
import numpy as np

from stqdm import stqdm

st.title('Routing Calculator')
st.write("""This app is used to calculate the distance and duration between two points. This app is developed by [Xiaokang Fu](https://gis.harvard.edu/people/xiaokang-fu) and [Devika Kakkar](https://gis.harvard.edu/people/devika-kakkar).
Please contact [Devika Kakkar](mailto:kakkar@fas.harvard.edu) for any questions.""")


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)

    st.write('Please select the columns for origin and destination longitude and latitude.')
# orignal longitude  selection
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        orig_lon = st.selectbox(
            'Origin Longitude',
            # set default value 
            (df.columns),
            index=4)
    
    with col2:
        orig_lat = st.selectbox(
            'Origin Latitude',
            (df.columns),
            index=5
            )
    
    with col3:
        dest_lon = st.selectbox(
            'Destination Longitude',
            (df.columns),
            index=2)
    with col4:
        dest_lat = st.selectbox(
            'Destination Latitude',
            (df.columns),
            index=3)

    st.write('You selected:', orig_lon, orig_lat, dest_lon, dest_lat)


    from georouting.routers import OSRMRouter


    router = OSRMRouter(mode="driving")
    for k,v in stqdm(df.iterrows(), total=df.shape[0]):
        origin = (v[orig_lat], v[orig_lon])
        destination = (v[dest_lat], v[dest_lon])
        route = router.get_route(origin, destination)
        df.loc[k, 'distance (m)'] = route.get_distance()
        df.loc[k, 'duration (s)'] = route.get_duration()
    
    st.balloons()

    st.write('Done!')
    # download df as csv
    st.download_button(
        label="Download data as CSV",
        data=df.to_csv().encode("utf-8"),
        file_name='routing.csv',
        mime='text/csv'
    )

    st.write(df)


