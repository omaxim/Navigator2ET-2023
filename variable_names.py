def get_color_discrete_map():
    colormap = {
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
    return colormap

def get_plot_and_hover_display_names(year_placeholder):
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
        'EU 2030 Export CZK',
        'ubiquity',
        'EU Celkový Export 25-30 CZK',
        'Percentil příbuznosti CZ '+year_placeholder+'',
        'Percentil komplexity '+year_placeholder+'',
        'Žebříček příbuznosti CZ '+year_placeholder+'',
        'Žebříček komplexity '+year_placeholder+'',
    ]
    return plot_display_names, hover_display_data


def get_hover_formatting(year):
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
    return no_decimal,two_sigfig,percentage,texthover

def get_hover_data(year,year_placeholder,hover_info,x_axis,y_axis,markersize):
    hover_data = {}
    no_decimal,two_sigfig,percentage,texthover = get_hover_formatting(year)
    
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

    return hover_data
