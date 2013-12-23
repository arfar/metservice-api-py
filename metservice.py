import ghost
import re

# Match numbers and literal '.' (i.e. decimals/floats)
RE_FLOAT = re.compile('[^0-9.]+')


def wind_direction_to_string(wind_direction, wind_speed):
    """
    Inspired by the actual javascript.
    Find it here http://metservice.com/_/js/main-3.0.136.js
    """
    wind_abbreviations = {
        'n': ('N', 'North'),
        'ne': ('NE', 'Northeast'),
        'e': ('E', 'East'),
        'se': ('SE', 'Southeast'),
        's': ('S', 'South'),
        'sw': ('SW', 'Southwest'),
        'w': ('W', 'West'),
        'nw': ('NW', 'Norwest'),
        'calm': ('Calm'),
    }

    try:
        wind_int = int(wind_direction)
        if wind_int <= 23 or wind_direction >= 337:
            return wind_abbreviations['n']
        elif wind_int < 67:
            return wind_abbreviations['ne']
        elif wind_int <= 113:
            return wind_abbreviations['e']
        elif wind_int < 167:
            return wind_abbreviations['se']
        elif wind_int <= 203:
            return wind_abbreviations['s']
        elif wind_int < 247:
            return wind_abbreviations['sw']
        elif wind_int <= 293:
            return wind_abbreviations['w']
        elif wind_int < 337:
            return wind_abbreviations['nw']
    except ValueError:
        # Wasn't an integer and should be a string
        if int(wind_speed) > 0 and wind_direction == 'calm':
            return wind_abbreviations['n']
        return wind_abbreviations.get(wind_direction, 'None')
    return 'n/a'


def get_current_info(city='christchurch'):
    """
    This function returns a dictionary containing current information about
    city/area given. It might be worth double checking the website is correct
    before using this function.

    Example dictionary:
    {'cur_temp': 11.4,
     'humidity': 61.0,
     'pressure': 1017.0,
     'rainfall': 0.0,
     'wind_description': 'Light winds',
     'wind_dir': 116.0,
     'wind_dir_str': ('SE', 'Southeast'),
     'wind_speed': 7.0}
    """

    weather_info = {}
    metservice_url = ''.join(['http://metservice.com/towns-cities/', city])
    gh = ghost.Ghost(wait_timeout=600)
    try:
        gh.open(metservice_url)
    except:
        # FIXME: USUALLY BREAKS TIMEOUT ISSUES,
        # CAN'T REMEMBER EXACTLY WHAT THE EXCEPTION IS
        print 'Something went wrong with connecting to metservice'
        return None

    wind_description, _ = gh.evaluate('data.windSpeedDesc')
    weather_info['wind_description'] = str(wind_description)
    weather_info['wind_speed'], _ = gh.evaluate('data.windSpeed')
    weather_info['cur_temp'], _ = gh.evaluate('data.temperature')
    weather_info['wind_dir'], _ = gh.evaluate('data.windDirection')
    weather_info['wind_dir_str'] = wind_direction_to_string(
        weather_info['wind_dir'], weather_info['wind_speed']
    )

    rainfall_in_mm, _ = gh.evaluate(
        "document.getElementById('obs-rainfall').textContent"
    )
    weather_info['rainfall'] = float(RE_FLOAT.sub('', str(rainfall_in_mm)))
    humidity, _ = gh.evaluate(
        "document.getElementById('obs-humidity').textContent"
    )
    weather_info['humidity'] = float(RE_FLOAT.sub('', str(humidity)))
    pressure, _ = gh.evaluate(
        "document.getElementById('obs-pressure').textContent"
    )
    weather_info['pressure'] = float(RE_FLOAT.sub('', str(pressure)))
    return weather_info


if __name__ == '__main__':
    import pprint
    import sys
    weather_info = get_current_info(sys.argv[1])
    pprint.pprint(weather_info)
