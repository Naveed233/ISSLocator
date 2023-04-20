import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "naveed.maqbool2@gmail.com"
MY_PASSWORD = "zcgyjhzzxtourjbp"

MY_LAT = 35.605057
MY_LONG = 138.123306

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    utc_sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    utc_sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    japan_sunrise = utc_sunrise + 9
    japan_sunset = utc_sunset + 9

    if japan_sunrise >=24:
        japan_sunrise -=24

    if japan_sunset >=24:
        japan_sunset -=24

    time_now = datetime.now().hour

    if time_now >= japan_sunset or time_now <= japan_sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg="Subject:Look Up👆\n\nThe ISS is above you in the sky.")