import urllib2
import sys
import json
import pprint

METSERVICE_BASE = 'http://metservice.com/publicData/'
# It's a little bit ugly, but it allows me to iterate over them later
API_OPTIONS = {
    'LOCAL_FORECAST': 'localForecast',
    'SUN_PROTECTION_URL': 'sunProtectionAlert',
    'ONE_MIN_OBS': 'oneMinObs_',
    'HOURLY_OBS_AND_FORCAST': 'hourlyObsAndForecast_',
    'LOCAL_OBS': 'localObs_',
    'TIDES': 'tides_',
    'WARNINGS': 'warningsForRegion3_urban.',  # Only works on cities
    'RISE_TIMES': 'riseSet_',
    'POLLEN_LEVELS': 'pollen_town_',
    'DAILY_FORECAST': 'climateDataDailyTown_{0}_32',
}


def get_response(url):
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError:
        return None
    return json.loads(response.read())

if __name__ == '__main__':
    try:
        city = sys.argv[1]
    except IndexError:
        city = 'christchurch'

    for key in API_OPTIONS.iterkeys():
        if key == 'DAILY_FORECAST':
            url = ''.join([METSERVICE_BASE, API_OPTIONS[key].format(city)])
        else:
            url = ''.join([METSERVICE_BASE, API_OPTIONS[key], city])
        print url
        pprint.pprint(get_response(url))
