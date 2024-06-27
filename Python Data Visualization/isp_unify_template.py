"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    country_code_to_name = {}
    not_found_codes = set()
    
    for code, name in plot_countries.items():
        if name in gdp_countries:
            country_code_to_name[code] = name
        else:
            not_found_codes.add(code)
    
    return country_code_to_name, not_found_codes


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

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
    
    try:
        with open(gdpinfo['gdpfile'], 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=gdpinfo['separator'], quotechar=gdpinfo['quote'])
            gdp_countries = {row[gdpinfo['country_name']].strip(): row for row in reader}
    except KeyError as e:
        raise KeyError(f"CSV file does not contain the column: {e}")

    plot_to_gdp_country, not_found_countries = reconcile_countries_by_name(plot_countries, gdp_countries)
    
    for code, country_name in plot_to_gdp_country.items():
        gdp_value = gdp_countries[country_name].get(year, '')
        if gdp_value:
            try:
                gdp_map[code] = math.log10(float(gdp_value))
            except ValueError:
                no_gdp_data_countries.add(code)
        else:
            no_gdp_data_countries.add(code)
    
    return gdp_map, not_found_countries, no_gdp_data_countries


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    # Get the GDP data
    gdp_map, not_found_countries, no_gdp_data_countries = build_map_dict_by_name(gdpinfo, plot_countries, year)

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
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
