import panel as pn
import pandas as pd
import numpy as np
import json

pn.extension('deckgl')
import pydeck as pdk
file_input = pn.widgets.FileInput(accept='.csv', name='Upload CSV')
GREEN_RGB = [0, 255, 0, 90]
RED_RGB = [240, 100, 0, 90]
MAPBOX_KEY = "pk.eyJ1IjoicGFuZWxvcmciLCJhIjoiY2s1enA3ejhyMWhmZjNobjM1NXhtbWRrMyJ9.B_frQsAVepGIe-HiOJeqvQ"
# geoview
arc_layer = pdk.Layer(
            "ArcLayer",
            # data=df,
            # get_width="S000 * 60",
            get_width="2",
            # set arc width

            # get_source_position=["origin_lon", "origin_lat"],
            # get_target_position=["dest_lon", "dest_lat"],
            get_tilt=15,
            get_source_color=RED_RGB,
            get_target_color=GREEN_RGB,
            pickable=True,
            auto_highlight=True,
        )
r = pdk.Deck(arc_layer)
json_spec = json.loads(r.to_json())
deck_gl = pn.pane.DeckGL(json_spec, mapbox_api_key=MAPBOX_KEY, 
                         sizing_mode='stretch_width',
                        # sizing_mode='stretch_both',
                        height=666
                        )

def load_csv(data):
    import io
    if data is not None:
        global df
        df = pd.read_csv(io.BytesIO(data))
        return pn.Column("There are %d od pairs that need to be calculated"%df.shape[0])

active_load_csv = pn.bind(load_csv, file_input.param.value)


from bokeh.models import TextInput, Tooltip
from bokeh.models.dom import HTML
html_tooltip = Tooltip(content=HTML("""<p>The input CSV must have at least 4 columns named:</p>
<ul>
<li><code>origin_lon</code></li>
<li><code>origin_lat</code></li>
<li><code>dest_lon</code></li>
<li><code>dest_lat</code> </li>
</ul>
<p>for origin and destination longitude and latitude respectively.</p>
<p>a sample can be found <a href="https://raw.githubusercontent.com/spatial-data-lab/data/main/sample_3.csv">here</a></p>
                                    """), position="right")

# html_tooltip = """<p>The input CSV must have at least 4 columns named <code>origin_lon</code>, <code>origin_lat</code>, <code>dest_lon</code>, <code>dest_lat</code> for origin and destination longitude and latitude respectively, a sample can be found <a href="https://raw.githubusercontent.com/spatial-data-lab/data/main/sample_3.csv">here</a></p>
# """
input_data_tool_tips = pn.widgets.TooltipIcon(value=html_tooltip)


sel_data_desc = pn.pane.Markdown("""## Upload the CSV file""")
data_upload_view = pn.Column(pn.Row(input_data_tool_tips,sel_data_desc),file_input,active_load_csv)




from georouting.routers import OSRMRouter
from panel.widgets import Tqdm
tqdm = Tqdm(width=300)
# create a router object 
router = OSRMRouter(mode="driving",
                    # base_url="http://172.30.232.152:5000"
                    )

def calculate_distance(run):
    if not run:
        # yield "Calculation did not finish yet :("
        return
    # import gevent
    for k,v in tqdm(df.iterrows(), total=df.shape[0],colour='#408558'):
        origin = ( v["origin_lat"],v["origin_lon"])
        destination = ( v["dest_lat"],v["dest_lon"])
        route = router.get_route(origin, destination)
        df.loc[k, 'distance (m)'] = route.get_distance()
        df.loc[k, 'duration (s)'] = route.get_duration()
    
    final_table = pn.pane.DataFrame(df.head(3), 
                                    sizing_mode='stretch_width'
                                    )
    
    import numpy as np
    if df.shape[0] > 10000:
        df_map = df.sample(10000, random_state=36)
    else:
        df_map = df
    v1 = df_map[["origin_lon", "origin_lat"]].values
    v2 = df_map[["dest_lon", "dest_lat"]].values
    v = np.concatenate([v1, v2])
    v_df_map = pd.DataFrame(v, columns=["lon", "lat"])
    data_view = pdk.data_utils.compute_view(v_df_map[["lon", "lat"]])
    view_state = pdk.ViewState(
                    longitude=data_view.longitude, latitude=data_view.latitude, zoom= data_view.zoom, bearing=0, pitch=45
                )
    arc_layer = pdk.Layer(
            "ArcLayer",
            data=df_map,
            # get_width="S000 * 60",
            get_width="2",
            # set arc width

            get_source_position=["origin_lon", "origin_lat"],
            get_target_position=["dest_lon", "dest_lat"],
            get_tilt=15,
            get_source_color=RED_RGB,
            get_target_color=GREEN_RGB,
            pickable=True,
            auto_highlight=True,
        )
    TOOLTIP_TEXT = {"html": "<br /> Source location in red; Destination location in green"}
    r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT,description="<h2>Taxi Trip Type</h2>")

    json_spec = json.loads(r.to_json())
    deck_gl.object = json_spec
    deck_gl.param.trigger('object')


    from io import StringIO
    sio = StringIO()
    df.to_csv(sio)
    sio.seek(0)
    download_view = pn.widgets.FileDownload(sio, 
                                            embed=True, 
                                            filename='results.csv', 
                                            # sizing_mode='stretch_width',
                                            button_type='success',
                                            # text = "Download the result",
                                            # colour='#408558',
                                            # height=34,

                                            )
    results_desc = pn.pane.Markdown("""## Downlaod the result""")


    from bokeh.models import TextInput, Tooltip
    from bokeh.models.dom import HTML
    html_tooltip = Tooltip(content=HTML("""<p>The output is a CSV with added </p>
<ul>
<li><code>distance (m)</code></li>
<li><code>duration (s)</code> </li>
</ul>
<p>columns for route distance in meters and drive time in seconds.</p>
<p>We use <a href="http://project-osrm.org/">OSRM</a> with a Multi-Level Dijkstra algorithm to find the route</p>
<p>The table below shows the first 3 rows of the result</p>

                                        """), position="right")

    # html_tooltip = """<p>The input CSV must have at least 4 columns named <code>origin_lon</code>, <code>origin_lat</code>, <code>dest_lon</code>, <code>dest_lat</code> for origin and destination longitude and latitude respectively, a sample can be found <a href="https://raw.githubusercontent.com/spatial-data-lab/data/main/sample_3.csv">here</a></p>
    # """
    output_data_tool_tips = pn.widgets.TooltipIcon(value=html_tooltip)


    table_download_view = pn.Column(pn.Row(output_data_tool_tips,results_desc),final_table,download_view)
    
    yield table_download_view


run = pn.widgets.Button(name="Calculate",
                        # button_type='primary',
                        # button_type='warning',
                        # button_type='success',
                        button_type='danger',

                        )

run_and_download = pn.Column(run, tqdm, pn.bind(calculate_distance, run))

         
intro = pn.pane.Markdown("""<center>
<img src="https://raw.githubusercontent.com/wybert/routing_app/main/DALL·E%202023-10-21%2010.53.23%20-%20Photo%20logo%20with%20a%20clear%20image%20of%20the%20earth.%20Circling%20the%20globe%20is%20a%20blazing%20comet%2C%20emphasizing%20rapid%20movement.%20Two%20distinct%20points%20on%20the%20globe%20mark%20t.png" alt="drawing" style="width:130px;"/>
                         
This app computes distance and duration between two points.
</center>
""",
sizing_mode='stretch_width'
)



from bokeh.models import TextInput, Tooltip
from bokeh.models.dom import HTML
html_tooltip = Tooltip(content=HTML("""<p>We use <a href="http://project-osrm.org/">OSRM</a> with a Multi-Level Dijkstra algorithm to find the route. </p>
<p>For comparison with other routing engines, like </p>
<ul>
<li>Google Maps</li>
<li>Bing Maps</li>
<li>ESRI Routing service</li>
</ul>
<p>please check <a href="https://isprs-archives.copernicus.org/articles/XLVIII-4-W7-2023/53/2023/">our paper</a> on FOSS4G 2023. </p>
                                        """), position="right")

# html_tooltip = """<p>The input CSV must have at least 4 columns named <code>origin_lon</code>, <code>origin_lat</code>, <code>dest_lon</code>, <code>dest_lat</code> for origin and destination longitude and latitude respectively, a sample can be found <a href="https://raw.githubusercontent.com/spatial-data-lab/data/main/sample_3.csv">here</a></p>
# """
cite_tool_tips = pn.widgets.TooltipIcon(value=html_tooltip)


cite_text = pn.pane.Markdown("""## Cite [this](https://isprs-archives.copernicus.org/articles/XLVIII-4-W7-2023/53/2023/) if you use this app
""", 
sizing_mode='stretch_width'
)

cite = pn.Row(cite_tool_tips,cite_text)

acknowledge = pn.pane.Markdown("""Acknowledgment: this app is built with [OSRM](http://project-osrm.org/), [Panel](https://panel.holoviz.org/), [Georouting](https://github.com/wybert/georouting), [Pydeck.gl](https://pydeck.gl/) and hosted in [New England Research Cloud (NERC)](https://nerc.mghpcc.org/). The road network data is from [OpenStreetMap](https://www.openstreetmap.org/). """)


green = pn.Spacer(styles=dict(background='#408558'),width=33,height=16,align='center')
red = pn.Spacer(styles=dict(background='#CB444A'),width=33,height=16,align='center')
map_legend = pn.Column(
    # pn.pane.Markdown("### The arc map of the source and destination points, The map can only show 10000 rows at most",align='end'),
    pn.Row(red,"Source locations",
           green,"Destination locations"),
        #    pn.pane.Markdown("The arc map of the source and destination points, The map can only show 10000 rows at most",align='end'),
        align='end'
           )


contribute_contacts = pn.Row(pn.pane.Markdown("""©️ This app is developed by [X.F.](https://gis.harvard.edu/people/xiaokang-fu) and [D.K.](https://gis.harvard.edu/people/devika-kakkar) from Harvard CGA. Please contact [Harvard CGA](mailto:kakkar@fas.harvard.edu) for any questions.""")
                                )



app = pn.Column(
       intro,
        data_upload_view,
        run_and_download,
        # cite
        )


cga_logo = pn.pane.PNG(
    'https://dssg.fas.harvard.edu/wp-content/uploads/2017/12/CGA_logo_globe_400x400.jpg',
    link_url='https://gis.harvard.edu/', height=43, align='center'
)

iqss_logo = pn.pane.PNG(
    'https://www.iq.harvard.edu/files/harvard-iqss/files/iq-logo-white_alt.png',
    link_url='https://www.iq.harvard.edu/', height=33, align='center'
)

# theme_switcher = pn.widgets.Switch(name='theme')
logos = pn.Row(pn.layout.HSpacer(),cga_logo)

main_view = pn.Column(
    # pn.Row(pn.layout.HSpacer(),pn.pane.Markdown("## The arc map of the source and destination points, it only show 10000 rows at most"),pn.layout.HSpacer()),
    # deck_gl,
    pn.Row(pn.pane.Markdown("The arc map of the source and destination points. It shows 10000 rows at most"), pn.layout.HSpacer(),map_legend),
    deck_gl,
    # pn.layout.Divider(),
    contribute_contacts
    
    # sizing_mode='stretch_height'
)
# Instantiate the template with widgets displayed in the sidebar
# template = pn.template.GoldenTemplate(
# template = pn.template.FastListTemplate(
# template = pn.template.ReactTemplate(
# template = pn.template.BootstrapTemplate(
# template = pn.template.SlidesTemplate(
# template = pn.template.VanillaTemplate(
template = pn.template.MaterialTemplate(
    title='RapidRoute (RR)',
    # logo='https://dssg.fas.harvard.edu/wp-content/uploads/2017/12/CGA_logo_globe_400x400.jpg',
    favicon = 'https://dssg.fas.harvard.edu/wp-content/uploads/2017/12/CGA_logo_globe_400x400.jpg',
    header_background = '#212121',
    header_color = '#2F6DAA',
    # header_color = '#408558',
    # neutral_color = '#408558',
    # accent_base_color = '#408558',
    header=[logos],
    sidebar=[app,cite,acknowledge],
    main=main_view,
    theme="dark"
    # sidebar_footer = """Xiao""",
    # busy_indicator=pn.indicators.BooleanStatus(value=False)

)

template.servable()