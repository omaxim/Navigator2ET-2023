import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO
import plotly.io as pio
from PIL import Image
from pychartjs.charts import Chart
from pychartjs.datasets import Dataset
from pychartjs.enums import ChartType
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
color_discrete_map = {
    'A02. Doprava': '#d6568c',
    'A03. Budovy': '#274001',
    'A04. Výroba nízkoemisní elektřiny a paliv': '#f29f05',
    'A05. Ukládání energie': '#f25c05',
    'A06. Energetické sítě': '#828a00',
    'E01. Měřící a diagnostické přístroje; Monitoring': '#4d8584',
    'A01. Výroba, nízkoemisní výrobní postupy': '#a62f03',
    'B02. Cirkularita a odpady': '#400d01',

    'A02c. Cyklistika a jednostopá': '#808080',
    'A03a. Snižování energetické náročnosti budov': '#94FFB5',
    'A04f. Jádro': '#8F7C00',
    'A05b. Vodik a čpavek': '#9DCC00',
    'A06a. Distribuce a přenos elektřiny': '#C20088',
    'A04a. Větrná': '#003380',
    'E0f. Měření v energetice a síťových odvětvích (HS9028 - 9030, 903210)': '#FFA405',
    'E01c. Měření okolního prostředí (HS9025)': '#FFA8BB',
    'E01i. Ostatní': '#426600',
    'A02a. Železniční (osobní i nákladní)': '#FF0010',
    'E01h. Surveying / Zeměměřičství (HS 9015)': '#5EF1F2',
    'A01a. Nízkoemisní výroba': '#00998F',
    'A04g. Efektivní využití plynu a vodíku': '#E0FF66',
    'E01e. Chemická analýza (HS9027)': '#740AFF',
    'A04b. Solární': '#990000',
    'A03b. Elektrifikace tepelného hospodářství': '#FFFF80',
    'A05a. Baterie': '#FFE100',
    'E01d. Měření vlastností plynů a tekutnin (HS9026)': '#FF5005',
    'E01a. Optická měření (HS 9000 - 9013, HS 903140)': '#F0A0FF',
    'B02b. Cirkularita, využití odpadu': '#0075DC',
    'A05c. Ostatní ukládání': '#993F00',
    'A01c. Elektrifikace výrobních postupů': '#4C005C',
    'A03b. Elektrifikace domácností': '#191919',

    'Díly a vybavení': '#005C31',
    'Zateplení, izolace': '#2BCE48',
    'Komponenty pro jadernou energetiku': '#FFCC99',
    'Vodík (elektrolyzéry)': '#808080',
    'Transformační stanice a další síťové komponenty': '#94FFB5',
    'Komponenty pro větrnou energetiku': '#8F7C00',
    'Termostaty': '#9DCC00',
    'Termometry': '#C20088',
    'Ostatní': '#003380',
    'Nové lokomotivy a vozy': '#FFA405',
    'Surveying / Zeměměřičství': '#FFA8BB',
    'Nízkoemisní výroby ostatní': '#426600',
    'Komponenty pro výrobu energie z plynů': '#FF0010',
    'Spektrometry': '#5EF1F2',
    'Komponenty pro solární energetiku': '#00998F',
    'Tepelná čerpadla a HVAC': '#E0FF66',
    'Infrastruktura (nové tratě a elektrifikace stávajících)': '#740AFF',
    'Baterie': '#990000',
    'Měření odběru a výroby plynů, tekutin, elektřiny': '#FFFF80',
    'Komponenty pro vodní energetiku': '#FFE100',
    'Měření vlastností plynů a tekutin': '#FF5005',
    'Optická měření': '#F0A0FF',
    'Materiálové využití': '#0075DC',
    'Měření ionizujícího záření': '#993F00',
    'Ostatní ukládání (přečerpávací vodní, ohřátá voda,…)': '#4C005C',
    'Hydrometry': '#191919',
    'Elektrifikace ve výrobě': '#005C31',
    'Domácí elektrické spotřebiče': '#2BCE48',
    'Chromatografy': '#FFCC99',
    'Osciloskopy': '#808080',
}

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
plot_display_names = [
    'Příbuznost CZ '+year_placeholder+'',
    'Výhoda CZ '+year_placeholder+'',
    'Koncentrace světového trhu '+year_placeholder+'',
    'Koncentrace evropského exportu '+year_placeholder+'',
    'Percentil příbuznosti CZ '+year_placeholder+'',
    'Percentil komplexity '+year_placeholder+'',
    'Žebříček exportu CZ '+year_placeholder+'',
    'Žebříček příbuznosti CZ '+year_placeholder+'',
    'Žebříček komplexity '+year_placeholder+'',
    'Komplexita výrobku '+year_placeholder+'',
    'CZ Export '+year_placeholder+' CZK',
    'Světový export '+year_placeholder+' CZK',
    'EU Export '+year_placeholder+' CZK',
    'EU Světový Podíl '+year_placeholder+' %',
    'CZ Světový Podíl '+year_placeholder+' %',
    'CZ-EU Podíl '+year_placeholder+' %',
    'ubiquity',
    'density',
    'cog',
    'CZ 2030 Export CZK',
    'CZ Celkový Export 25-30 CZK',
    'EU 2030 Export CZK',
    'EU Celkový Export 25-30 CZK',
    'CAGR 2022-2030 Předpověď',
    'Stejná Velikost'
]

hover_display_data = [
    'HS_ID',
    'Skupina',
    'Podskupina',
    'Název',
    'CZ Celkový Export 25-30 CZK',
    'Příbuznost CZ '+year_placeholder+'',
    'Výhoda CZ '+year_placeholder+'',
    'Koncentrace světového trhu '+year_placeholder+'',
    'Koncentrace evropského exportu '+year_placeholder+'',
    'EU Největší Exportér '+year_placeholder+'',
    'Komplexita výrobku '+year_placeholder+'',
    'CZ Export '+year_placeholder+' CZK',
    'Žebříček exportu CZ '+year_placeholder+'',
    'Světový export '+year_placeholder+' CZK',
    'EU Export '+year_placeholder+' CZK',
    'EU Světový Podíl '+year_placeholder+' %',
    'CZ Světový Podíl '+year_placeholder+' %',
    'CZ-EU Podíl '+year_placeholder+' %',
    'CZ 2030 Export CZK',
    'CZ Celkový Export 25-30 CZK',
    'EU 2030 Export',
    'ubiquity',
    'EU Celkový Export 25-30 CZK',
    'Percentil příbuznosti CZ '+year_placeholder+'',
    'Percentil komplexity '+year_placeholder+'',
    'Žebříček příbuznosti CZ '+year_placeholder+'',
    'Žebříček komplexity '+year_placeholder+'',
]

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
    filter_min, filter_max = df[filter_col].min(), df[filter_col].max()
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
plotlystyle = st.sidebar.selectbox("Styl grafu:",["plotly_dark","plotly","ggplot2","seaborn","simple_white","none"])
background_color = st.sidebar.selectbox('Barva pozadí',[None,'#0D1A27','#112841'])
# Create a button in the sidebar that clears the cache
if st.sidebar.button('Obnovit Data'):
    load_data.clear()  # This will clear the cache for the load_data function
    st.sidebar.write("Sušenky vyčištěny!")
debug = st.sidebar.toggle('Debug')
pio.templates.default = plotlystyle
# Initialize the hover_data dictionary with default values of False for x, y, and markersize
#hover_data = {col: True for col in hover_info}
hover_data = {}

# Columns without decimals, which should also have thousands separators
no_decimal = [
    'HS_ID',
    'CZ Celkový Export 25-30 CZK',
    'CZ Export '+year+' CZK',
    'Světový export '+year+' CZK',
    'EU Export '+year+' CZK',
    'CZ 2030 Export CZK',
    'CZ Celkový Export 25-30 CZK',
    'EU 2030 Export',
    'EU Celkový Export 25-30 CZK',
    'Žebříček příbuznosti CZ '+year+'',
    'Žebříček komplexity '+year+'',
    'ubiquity',
    'Percentil příbuznosti CZ '+year+'',
    'Percentil komplexity '+year+'',
    'Žebříček exportu CZ '+year+''
]

# Columns requiring three significant figures and percentage formatting
two_sigfig = [
    'Příbuznost CZ '+year+'',
    'Výhoda CZ '+year+'',
    'Koncentrace světového trhu '+year+'',
    'Koncentrace evropského exportu '+year+'',
    'Komplexita výrobku '+year+'',
    'CAGR 2022-2030 Předpověď',
]

# Columns that should show as percentages
percentage = [
    'EU Světový Podíl '+year+' %',
    'CZ Světový Podíl '+year+' %',
    'CZ-EU Podíl '+year+' %',
]

texthover = [
    'Skupina',
    'Podskupina',
    'Název',
    'EU Největší Exportér '+year+''
]

# Iterate over the columns in hover_info
hover_info_year = [text.replace(year_placeholder,year) for text in hover_info]
for col in hover_info_year:
    # If the column is in no_decimal, format with no decimals and thousands separator
    if col in no_decimal:
        hover_data[col] = ':,.0f'  # No decimals, thousands separator
    # If the column is in three_sigfig, format with 3 decimal places
    elif col in two_sigfig:
        hover_data[col] = ':.2f'
    elif col in percentage:
        hover_data[col] = ':.1f'  # Three decimal places, with percentage symbol
    elif col in texthover:
        hover_data[col] = True
    else:
        hover_data[col] = False  # No formatting needed, just show the column
    
# Ensure x_axis, y_axis, and markersize default to False if not explicitly provided in hover_info
hover_data.setdefault(markersize, False)
hover_data.setdefault(x_axis, False)
hover_data.setdefault(y_axis, False)
hover_data.setdefault('Skupina', False)
hover_data.setdefault('Podskupina', False)
hover_data.setdefault('Název', True)


if HS_select == []:
    fig = px.scatter(filtered_df,
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=color_discrete_map,  # Hard-code the colors
                     labels={x_axis: x_axis, y_axis: y_axis},
                     hover_data=hover_data,
                     opacity=0.7,
                     size=markersize,
                     size_max=40)
    

else:
    fig = px.scatter(filtered_df[filtered_df['HS_Lookup'].isin(HS_select)],
                     x=x_axis,
                     y=y_axis,
                     color=color,
                     color_discrete_map=color_discrete_map,  # Hard-code the colors
                     labels={x_axis: x_axis, y_axis: y_axis},
                     hover_data=hover_data,
                     opacity=0.7,
                     size=markersize,
                     size_max=40
                     )

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

st.plotly_chart(fig)
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


mybuff = StringIO()
fig.write_html(mybuff, include_plotlyjs='cdn')
html_bytes = mybuff.getvalue().encode()
st.download_button(
    label = "Stáhnout HTML",
    data = html_bytes,
    file_name = "plot.html",
    mime="text/html"
)
dataset = Dataset(
    label="Sales Data",
    data=[10, 20, 30, 40, 50],
    backgroundColor="rgba(75, 192, 192, 0.2)",
    borderColor="rgba(75, 192, 192, 1)",
    borderWidth=1,
)

chart = Chart(
    chart_type=ChartType.BUBBLE,
    datasets=[dataset],
    labels=["January", "February", "March", "April", "May"]
)

# Render the chart as HTML
chart_html = chart.render()
st.text(chart_html)
components.html(f"""
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    {chart_html}
""", height=300)