"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    converter = {}
    
    with open(codeinfo['codefile'], 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=codeinfo['separator'], quotechar=codeinfo['quote'])
        for row in reader:
            plot_code = row[codeinfo['plot_codes']].strip()
            data_code = row[codeinfo['data_codes']].strip()
            converter[plot_code] = data_code
    
    return converter



def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    converter = build_country_code_converter(codeinfo)
    plot_to_gdp = {}
    not_found = set()
    
    gdp_countries_lower = {key.lower(): key for key in gdp_countries.keys()}
    converter_lower = {key.lower(): value.lower() for key, value in converter.items()}
    
    for plot_code, country_name in plot_countries.items():
        plot_code_lower = plot_code.lower()
        if plot_code_lower in converter_lower:
            data_code_lower = converter_lower[plot_code_lower]
            if data_code_lower in gdp_countries_lower:
                plot_to_gdp[plot_code] = gdp_countries_lower[data_code_lower]
            else:
                not_found.add(plot_code)
        else:
            not_found.add(plot_code)
    
    return plot_to_gdp, not_found


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_map = {}
    not_found_countries = set()
    no_gdp_data_countries = set()
    
    # Load the GDP data
    with open(gdpinfo['gdpfile'], 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=gdpinfo['separator'], quotechar=gdpinfo['quote'])
        gdp_data = {row[gdpinfo['country_code']].strip(): row for row in reader}
    
    # Reconcile countries
    plot_to_gdp, not_found_countries = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data)
    
    # Process the GDP data
    for plot_code, gdp_code in plot_to_gdp.items():
        gdp_value = gdp_data[gdp_code].get(year, '')
        if gdp_value:
            try:
                gdp_map[plot_code] = math.log10(float(gdp_value))
            except ValueError:
                no_gdp_data_countries.add(plot_code)
        else:
            no_gdp_data_countries.add(plot_code)
    
    return gdp_map, not_found_countries, no_gdp_data_countries

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    # Get the GDP data
    gdp_map, not_found_countries, no_gdp_data_countries = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)

    # Create a world map
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = f'World GDP in {year}'

    # Add data to the map
    worldmap_chart.add('GDP (log scale)', gdp_map)
    worldmap_chart.add('Missing from World Bank Data', list(not_found_countries))
    worldmap_chart.add('No GDP Data for Year', list(no_gdp_data_countries))

    # Render the map to a file
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
