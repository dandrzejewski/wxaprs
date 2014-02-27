# coding=utf-8
"""
wxaprsgen
"""
import ConfigParser
from datetime import datetime
import os
import pytz
import serial
import time

__author__ = 'dave'

OUTPUT_FILE = "/tmp/wxpacket.txt"
SERIAL_DEVICE = "/dev/tty.usbserial-FTH09DY2"
PACKET_COMMENT = "!SN!"
COORDINATES = "4128.26N/08133.43W"
DATA_FILE = "/Users/dave/Google Drive/Weather Data/current.lst"
INTERVAL_IN_SECONDS = 300

USE_SERIAL = False
USE_FILE = True

class WxAprs(object):

    def send_serial_packet(self, packet):
        """
        Sends the data through to the serial port.
        :param packet: The packet to send.
        """
        ser = serial.Serial(SERIAL_DEVICE, 19200, timeout=2)
        print("Using port: {}".format(ser))
        print("Writing packet: {}".format(packet))
        ser.write("{}\n".format(packet))
        # The TinyPack won't send if you close the port too soon.
        time.sleep(5)
        ser.close()

    def parse_and_construct_packet(self):
        """
        Parses the file data and constructs the packet.

        :return: The constructed packet.
        """

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

        return packet


    def write_file(self, packet):
        """
        Writes the packet to a file.
        """
        with open(OUTPUT_FILE, "w") as f:
            f.write("{}{}".format(packet, os.linesep))

    def run(self):
        """
        Main Loop.
        """

        while True:
            packet = self.parse_and_construct_packet()
            if USE_SERIAL:
                self.send_serial_packet(packet)

            if USE_FILE:
                self.write_file(packet)

            time.sleep(INTERVAL_IN_SECONDS)

if __name__ == "__main__":
    wxaprs = WxAprs()
    wxaprs.run()
