import sys, getopt
from datetime import datetime
import requests,json

def main(argv):
    help_message = 'fetch_temperature.py -k [dark_sky_api_key] -u [url]'
    url = None
    key = None
    try:
        opts, args = getopt.getopt(argv,"hk:u:",["key=", "url="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    for opt, arg in opts:
        print(f'== {opt}|{arg}')
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-k", "--key"):
            key = arg
    
    print('Using Key [{0}]'.format(key))
    print('Using Url [{0}]'.format(url))
    r = requests.get('https://api.darksky.net/forecast/{0}/53.544,-113.4909?units=ca'.format(key))
    reading = r.json()["currently"]["temperature"]

    result = requests.post('{0}/sensorreadings'.format(url), json.dumps({
        "name": "darksky",
        "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f'),
        "value": reading,
        "uom": "c"    
    }))


if __name__ == "__main__":
    main(sys.argv[1:])