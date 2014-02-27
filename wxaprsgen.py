import ConfigParser
from datetime import datetime
import pytz
import serial
import time

__author__ = 'dave'

SERIAL_DEVICE = "/dev/tty.usbserial-FTH09DY2"
PACKET_COMMENT = "!SN!"
COORDINATES = "4128.26N/08133.43W"
DATA_FILE = "/Users/dave/Google Drive/Weather Data/current.lst"

#@DDHHMM/DDMM.hhN/DDDMM.hhW_CSE/SPDgXXXtXXXrXXXpXXXPXXXhXXbXXXXXdU2k
#    r is in hundredths of an inch of rain in the LAST HOUR
#    p is in hundredths of an inch of rain in the LAST 24 HOURS
#    s is INCHES of snow in the last 24 hours
#    b is in tenths of millibars
#    h is percent humidity (00=100%)
#    dU2k is Ultimeter 2000, /U5 is the 500 and /Dvs is Davis
#         The "d" means it is running DOS


def send_serial_packet(packet):
    ser = serial.Serial(SERIAL_DEVICE, 19200, timeout=2)
    print("Using port: {}".format(ser))
    ser.write("{}\n".format(packet))
    # The TinyPack won't send if you close the port too soon.
    time.sleep(5)
    ser.close()

if __name__ == "__main__":

    config = ConfigParser.ConfigParser()
    config.readfp(open(DATA_FILE))

    d = datetime.now(pytz.timezone("UTC"))
    timestamp = d.strftime("%d%H%Mz")

    wind_direction_raw = config.get('wind_direction', 'deg')

    wind_speed_raw = config.get('wind_speed', 'mph')

    wind_gust_raw = config.get('wind_gust', 'mph')

    temperature_raw = config.get('outdoor_temperature', 'deg_F')

    rain_1h_raw = config.get('rain_1h', 'inch')

    rain_24h_raw = config.get('rain_24h', 'inch')

    rain_since_midnight_raw = "0.00"

    # TODO Fix this
    snow_24h_raw = "0.00"

    humidity_raw = config.get('humidity_levels', 'outdoor_percent_int')

    barometer_raw = config.get('pressure_relative', 'hpa')

    software = "KD8TWG WXAPRSGEN 1.0"

    # Now format all the raw data
    wind_dir = "%.3d" % float(wind_direction_raw.replace('"', ''))
    wind_speed = "%.3d" % float(wind_speed_raw.replace('"', ''))
    wind_gust = "%.3d" % float(wind_gust_raw.replace('"', ''))
    temperature = "%.3d" % float(temperature_raw.replace('"', ''))
    rain_1h = "%.3d" % (float(rain_1h_raw.replace('"', '')) * 100)
    rain_24h = "%.3d" % (float(rain_24h_raw.replace('"', '')) * 100)
    rain_since_midnight = "%.3d" % (float(rain_since_midnight_raw.replace('"', '')) * 100)
    humidity = "%.2d" % float(humidity_raw.replace('"', ''))
    barometer = "%.5d" % (float(barometer_raw.replace('"', '')) * 10)

    packet = "@" + timestamp + COORDINATES + "_" + wind_dir + "/" + wind_speed + "g" + wind_gust + "t" + temperature + "r" + rain_1h + "p" + rain_24h + "P" + rain_since_midnight \
             + "h" + humidity + "b" + barometer + "e" + software + " " + PACKET_COMMENT



    print("Packet: " + packet)

    send_serial_packet(packet)
