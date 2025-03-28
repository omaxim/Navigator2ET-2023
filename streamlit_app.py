import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import plotly.io as pio
from chartjsbubble import chartjs_plot
from variable_names import get_color_discrete_map, get_plot_and_hover_display_names, get_hover_data
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mapa Příležitostí 2023",
    page_icon="favicon.png"
)
st.logo('logo.svg')
st.error('Toto je pracovní verze. Data s vyjímkou budoucího růstu pochází z CEPII databáze BACI. Projekce 2025-30 berte s velikou rezervou. Krom toho, že jsou odhadem, neberou v potaz inflaci.', icon="⚠️")

# Sidebar for selecting variables
st.sidebar.header("Nastavení Grafu")
year = st.sidebar.pills("Rok",["2022","2023"],default="2023")
def USDtoCZKdefault(year):
    if year=="2022":
        return 23.360
    elif year=="2023":
        return 22.21
USD_to_czk = st.sidebar.number_input("Kurz USD vůči CZK",value=USDtoCZKdefault(year))

# Load data
@st.cache_data
def load_data(datayear,USD_to_czk):
    # Replace with the path to your data file
    #df                          = pd.read_csv('GreenComplexity_CZE_2022.csv')
    url = 'https://docs.google.com/spreadsheets/d/1mhv7sJC5wSqJRXdfyFaWtBuEpX6ENj2c/gviz/tq?tqx=out:csv'
    taxonomy = pd.read_csv(url)
    CZE = pd.read_csv('CZE_'+datayear+'.csv')
    GreenProducts = taxonomy.merge(CZE,how='left',left_on='HS_ID',right_on='prod')
    # Calculate 2030 export value
    GreenProducts['CountryExport2030'] = GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8
    GreenProducts['EUExport2030'] = GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** 8

    # Calculate Total Export Value from 2025 to 2030
    # We calculate for each datayear and sum up
    GreenProducts['CountryExport_25_30'] = sum(GreenProducts['ExportValue'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))
    GreenProducts['EUExport_25_30'] = sum(GreenProducts['EUExport'] * (1 + GreenProducts['CAGR_2022_30_FORECAST']) ** i for i in range(3, 9))

    df = GreenProducts.rename(columns={'ExportValue': 'CZ Export '+datayear+' CZK',
                               'export_Rank':'Žebříček exportu CZ '+datayear+'',
                               'pci': 'Komplexita výrobku '+datayear+'',
                               'relatedness': 'Příbuznost CZ '+datayear+'',
                               'PCI_Rank':'Žebříček komplexity '+datayear+'',
                               'PCI_Percentile':'Percentil komplexity '+datayear+'',
                               'relatedness_Rank':'Žebříček příbuznosti CZ '+datayear+'',
                               'relatedness_Percentile':'Percentil příbuznosti CZ '+datayear+'',
                               'WorldExport':'Světový export '+datayear+' CZK',
                               'EUExport':'EU Export '+datayear+' CZK',
                               'EUWorldMarketShare':'EU Světový Podíl '+datayear+' %',
                               'euhhi':'Koncentrace evropského exportu '+datayear+'',
                               'hhi':'Koncentrace světového trhu '+datayear+'',
                               'CZE_WorldMarketShare':'CZ Světový Podíl '+datayear+' %',
                               'CZE_EUMarketShare':'CZ-EU Podíl '+datayear+' %',
                               'rca':'Výhoda CZ '+datayear+'',
                               'EUTopExporter':'EU Největší Exportér '+datayear+'',
                               'CZ_Nazev':'Název',
                               'CountryExport2030':'CZ 2030 Export CZK',
                               'EUExport2030':'EU 2030 Export CZK',
                               'CountryExport_25_30':'CZ Celkový Export 25-30 CZK',
                               'EUExport_25_30':'EU Celkový Export 25-30 CZK',
                               'CAGR_2022_30_FORECAST':'CAGR 2022-2030 Předpověď'
                               })
    df                          = df[df.Included == "IN"]
    df['stejna velikost']       = 0.02
    df['CZ-EU Podíl '+datayear+' %']      = 100 * df['CZ-EU Podíl '+datayear+' %'] 
    df['EU Světový Podíl '+datayear+' %'] = 100 * df['EU Světový Podíl '+datayear+' %'] 
    df['CZ Světový Podíl '+datayear+' %'] = 100 * df['CZ Světový Podíl '+datayear+' %'] 
    df['CZ Export '+datayear+' CZK']        = USD_to_czk*df['CZ Export '+datayear+' CZK'] 
    df['Světový export '+datayear+' CZK']      = USD_to_czk*df['Světový export '+datayear+' CZK'] 
    df['EU Export '+datayear+' CZK']        = USD_to_czk*df['EU Export '+datayear+' CZK'] 
    df['EU Celkový Export 25-30 CZK'] = USD_to_czk*df['EU Celkový Export 25-30 CZK'] 
    df['CZ Celkový Export 25-30 CZK'] = USD_to_czk*df['CZ Celkový Export 25-30 CZK'] 
    df['EU 2030 Export CZK']        = USD_to_czk*df['EU 2030 Export CZK'] 
    df['CZ 2030 Export CZK']        = USD_to_czk*df['CZ 2030 Export CZK'] 
    df['HS_ID']                 = df['HS_ID'].astype(str)
    df['HS_Lookup']              = df['HS_ID']+" - "+df['Název']
    
    st.info(str(GreenProducts.shape[0]) + " produktů načteno z excelu, z toho " +str(df.shape[0])+" je IN")
    return df

df = load_data(year,USD_to_czk)
st.title("Mapa Příležitostí "+year)

# Create lists of display names for the sidebar
ji_display_names = ['Skupina', 'Podskupina', 'Kategorie výrobku']
year_placeholder = " ‎"
plot_display_names, hover_display_data = get_plot_and_hover_display_names(year_placeholder)
# Sidebar selection boxes using display names
x_axis      = st.sidebar.selectbox("Vyber osu X:", plot_display_names, index=4)
y_axis      = st.sidebar.selectbox("Vyber osu Y:", plot_display_names, index=5)
markersize  = st.sidebar.selectbox("Velikost dle:", plot_display_names, index=9)


# Apply filters to dataframe
filtered_df = df.copy()

filtrovat_dle_skupin = st.sidebar.toggle("Filtrovat dle skupin",value=False)

if filtrovat_dle_skupin:
    color       = st.sidebar.selectbox("Barva dle:", ji_display_names,index = 1)
    skupiny = df['Skupina'].unique()
    Skupina = st.sidebar.multiselect('Skupina',skupiny,default=skupiny[0])
    podskupiny = df['Podskupina'][df['Skupina'].isin(Skupina)].unique()
    Podskupina = st.sidebar.multiselect('Podskupina',podskupiny,default=podskupiny)
    filtered_df = filtered_df[filtered_df['Skupina'].isin(Skupina)]
    filtered_df = filtered_df[filtered_df['Podskupina'].isin(Podskupina)]
else:
    color       = 'Skupina'


hover_info  = st.sidebar.multiselect("Co se zobrazí při najetí myší:", hover_display_data, default=['Název',x_axis,y_axis])
st.sidebar.divider()
# Filter section
if 'filters' not in st.session_state:
    st.session_state.filters = []

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Číselný filtr"):
        st.session_state.filters.append({'column': None, 'range': None})
with col2:
    if st.button("Odstranit filtry"):
        st.session_state.filters = []

# Display existing filters using display names
for i, filter in enumerate(st.session_state.filters):
    filter_col= st.sidebar.selectbox(f"Filtr {i+1}", plot_display_names, key=f"filter_col_{i}")
    filter_min, filter_max = df[filter_col.replace(year_placeholder,year)].min(), df[filter_col.replace(year_placeholder,year)].max()
    filter_range = st.sidebar.slider(f"Filtr {i+1}", float(filter_min), float(filter_max), (float(filter_min), float(filter_max)), key=f"filter_range_{i}")
    st.session_state.filters[i]['column'] = filter_col
    st.session_state.filters[i]['range'] = filter_range

# Apply numerical filters
for filter in st.session_state.filters:
    if filter['column'] is not None and filter['range'] is not None:
        filtered_df = filtered_df[
            (filtered_df[filter['column'].replace(year_placeholder,year)] >= filter['range'][0]) &
            (filtered_df[filter['column'].replace(year_placeholder,year)] <= filter['range'][1])
        ]

markersize = markersize.replace(year_placeholder,year)
x_axis = x_axis.replace(year_placeholder,year)
y_axis = y_axis.replace(year_placeholder,year)

# Replace negative values in markersize column with zero
filtered_df[markersize] = filtered_df[markersize].clip(lower=0)

# Remove NA values
filtered_df = filtered_df.dropna(subset=[x_axis, y_axis, color, markersize])


HS_select = st.multiselect("Filtrovat HS6 kódy",filtered_df['HS_Lookup'])
plotly_or_chartjs = st.sidebar.radio("Plotly nebo Chart.js",["Plotly","Chart.js"],1)
if plotly_or_chartjs=="Plotly":
    plotlystyle = st.sidebar.selectbox("Styl grafu:",["plotly_dark","plotly","ggplot2","seaborn","simple_white","none"])
    pio.templates.default = plotlystyle


background_color = st.sidebar.selectbox('Barva pozadí',[None,'#0D1A27','#112841'])
# Create a button in the sidebar that clears the cache
if st.sidebar.button('Obnovit Data'):
    load_data.clear()  # This will clear the cache for the load_data function
    st.sidebar.write("Sušenky vyčištěny!")
debug = st.sidebar.toggle('Debug')
# Initialize the hover_data dictionary with default values of False for x, y, and markersize
#hover_data = {col: True for col in hover_info}
hover_data = get_hover_data(year,year_placeholder,hover_info,x_axis,y_axis,markersize)

if HS_select == []:
    fig = px.scatter(filtered_df,
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=get_color_discrete_map(),  # Hard-code the colors
                     labels={x_axis: x_axis, y_axis: y_axis},
                     hover_data=hover_data,
                     opacity=0.7,
                     size=markersize,
                     size_max=40)
    chart_js = chartjs_plot(filtered_df,markersize,hover_data,color,x_axis,y_axis,year)

    

else:
    fig = px.scatter(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)],
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=get_color_discrete_map(),  # Hard-code the colors
                     labels={x_axis: x_axis, y_axis: y_axis},
                     hover_data=hover_data,
                     opacity=0.7,
                     size=markersize,
                     size_max=40
                     )
    chart_js = chartjs_plot(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)],markersize,hover_data,color,x_axis,y_axis,year)


fig.update_layout(
    hoverlabel=dict(
        font_family="verdana",
        bgcolor="#008C00"
    ),
        legend=dict(
        orientation="h",  # Horizontal legend
        yanchor="top",    # Align the legend's top with the graph's bottom
        y=-0.3,           # Push the legend further below (negative moves it below the plot)
        xanchor="center", # Center the legend horizontally
        x=0.5             # Position it at the center of the graph
    ),
    plot_bgcolor=background_color,
    paper_bgcolor = background_color          
)

if plotly_or_chartjs=="Plotly":
    st.plotly_chart(fig)
    mybuff = StringIO()
    fig.write_html(mybuff, include_plotlyjs='cdn')
    html_bytes = mybuff.getvalue().encode()
else:
    # Render the chart in Streamlit
    components.html(chart_js, height=800)
    html_bytes=chart_js

col1, col2, col3 = st.columns(3)
if HS_select == []:
    col1.metric("Vybraný český export za rok "+year+"", "{:,.0f}".format(sum(filtered_df['CZ Export '+year+' CZK'])/1000000000),'miliard CZK' )
    col2.metric("Vybraný český export 2025 až 2030", "{:,.0f}".format(sum(filtered_df['CZ Celkový Export 25-30 CZK'])/1000000000), "miliard CZK")
    col3.metric("Vybraný evropský export 2025 až 2030", "{:,.0f}".format(sum(filtered_df['EU Celkový Export 25-30 CZK'])/1000000000), "miliard CZK")
    if debug:
        st.dataframe(filtered_df)
else:
    col1.metric("Vybraný český export za rok "+year+"", "{:,.0f}".format(sum(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)]['CZ Export '+year+' CZK'])/1000000),'milionů CZK' )
    col2.metric("Vybraný český export 2025 až 2030", "{:,.0f}".format(sum(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)]['CZ Celkový Export 25-30 CZK'])/1000000), "milionů CZK")
    col3.metric("Vybraný evropský export 2025 až 2030", "{:,.0f}".format(sum(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)]['EU Celkový Export 25-30 CZK'])/1000000), "milionů CZK")
    if debug:
        st.dataframe(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)])




st.download_button(
    label = "Stáhnout HTML",
    data = html_bytes,
    file_name = "plot.html",
    mime="text/html"
)

