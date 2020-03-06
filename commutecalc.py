import googlemaps
import pendulum
import json

def weekly_travel(destinations):
    #Parse Input
    home = destinations['home']
    work = destinations['work']
    wkly_dests = destinations['wkly_dests']

    # Load API Key
    f = open("googlemapskey.txt","r")
    gmaps = googlemaps.Client(key=f.read())
    f.close()

    # Commute Times
    now = pendulum.now(tz='America/New_York')
    morning = now.next(pendulum.WEDNESDAY).add(hours=9)
    evening = now.next(pendulum.WEDNESDAY).add(hours=17)
    night = now.next(pendulum.WEDNESDAY).add(hours=20)

    # Weekly Travel Time in Seconds
    time = 0

    # Daily Outbound Trips
    daily_to = gmaps.distance_matrix(
        home, work, mode = 'transit', arrival_time = morning
        )
    time += 5*daily_to['rows'][0]['elements'][0]['duration']['value']

    # Daily Return Trips
    daily_from = gmaps.distance_matrix(
        work, home, mode = 'transit', departure_time = evening
        )
    time += 5*daily_from['rows'][0]['elements'][0]['duration']['value']

    # Weekly Outbound Trips
    wkly_to = gmaps.distance_matrix(
        home, wkly_dests, mode = 'transit', departure_time = night
        )
    for i in wkly_to['rows']:
        for j in i['elements']:
            time += j['duration']['value']

    # Weekly Return Trips
    wkly_from = gmaps.distance_matrix(
        wkly_dests, home, mode = 'transit', departure_time = night
        )
    for i in wkly_from['rows']:
        for j in i['elements']:
            time += j['duration']['value']

    return(time)

if __name__ == "__main__":
    with open('destinations.json') as json_file:
        data = json.load(json_file)

    commute = weekly_travel(data)

    print(str(commute/3600)[:4]+' hours of travel per week')
