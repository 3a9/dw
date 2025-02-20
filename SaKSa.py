#!/usr/bin/env python3

import argparse
import requests
import sys
import socket
import ssl
import threading
import os
import time
import json
import csv
from concurrent.futures import ThreadPoolExecutor
green_color = "\033[1;32m"
red_color = "\033[1;31m"
detect_color = "\033[1;34m"
banner_color = "\033[1;33;40m"
end_banner_color = "\33[00m"
print(banner_color+"""

سعد بن جدلان رحمة الله عليه :

      - الملتزم بالصمت مايخطي ولا يخطي عليه
      - انشهد ان الصمت يحفظ للرجال شخصيته 

 ⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀
⠀⠀⠀⣸⣿⣿⣿⣿⡿⠿⠿⢿⣿⠿⠟⠛⠛⠛⠛⠻⣿⣿⣿⣿⣿⣗⠀⠀⠀⠀
⠀⠀⠀⢸⣿⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠹⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣿⣿⣿⣿⣏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠁⠀⠈⠉⣉⠁⠀⠀⠀⠀⠉⠉⠥⠠⠙⠛⢿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⣼⣿⣿⣿⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠒⠃⠀⠀⠀⠀⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⣰⣿⣿⣿⣦⣄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⡿⠛⣻⣷⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⠟⠁⠀⣰⣿⣿⣿⣆⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠶⠾⠿⠿⠛⠁⠀⠀⣰⣿⣿⣿⣿⣿⣿⣶
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿

               0xFaLaH - 0xfff0800 

""")


class Logger:
	"""
	Provides formatting for the custom logger.
	"""

	COLOR_DEFAULT  = "\033[0m"   # White
	COLOR_ERROR    = "\033[91m"  # Red
	COLOR_SUCCESS  = "\033[92m"  # Green
	COLOR_INFO     = "\033[93m"  # Orange

	def __init__(self, enabled=True, color=True):
		"""
		Creates a new logger instance.

		:param enabled: if true, logging is enabled.
		:param color: if true, the logger will output colored text.
		"""
		self.enabled = enabled
		self.color = color

	def log_status(self, msg, color=COLOR_DEFAULT):
		if self.enabled:
			if self.color:
				print("{}[+]{} {}".format(color, self.COLOR_DEFAULT, msg))
			else:
				print("[*] {}".format(msg))

	def success(self, msg):
		"""
		Logs a success message.

		:param msg: the message to log.
		"""
		self.log_status(msg, self.COLOR_SUCCESS)


	def info(self, msg):
		"""
		Logs a information message.

		:param msg: the message to log.
		"""
		self.log_status(msg, self.COLOR_INFO)

	def error(self, msg):
		"""
		Logs a error message.
		"""
		self.log_status(msg, self.COLOR_ERROR)

	def no_status(self, msg):
		"""
		Logs a message with no status icon.

		:param msg: the message to log.
		"""
		if self.enabled:
			print("    " + msg)

class PortInfo:
	"""
	Stores information about a specific port.
	"""

	def __init__(self, port, service_name, service_transport, service_desc):
		"""
		Creates a new PortInfo instance.

		:param port: The port number.
		:param service_name: The name of the service (protocol) running on the port.
		:param service_transport: a list of supported transport layer protocols.
		:param service_desc: A description of the protocol.
		"""

		self.port = port
		self.service_name = service_name
		self.service_transport = service_transport
		self.service_desc = service_desc

class Dumper:
	"""
	Gathers information via APIs and portscanning about a given IP Address, Web Address or Domain.
	"""

	def __init__(self, target):
		"""
		Creates a new Dumper instance.

		:param target: the target host.
		"""

		self.target = target
		self.logger = Logger(enabled=False, color=True)
		self.service_map = {}
		self.service_map_loaded = False

	def attach_logger(self, logger):
		"""
		Attaches a logger to the dumper. This directly outputs to stdout.

		:param logger: the logger to attach to the dumper.
		"""
		self.logger = logger

	def load_service_map(self, filename="services.csv"):
		"""
		Loads and parses the given csv file mapping port numbers to service information.

		:param filename: the name of the csv file.
		"""

		service_map = {}
		try:
			with open(filename) as csvfile:
				reader = csv.reader(csvfile, delimiter=',', quotechar='"')
				next(reader) # skip the headings
				for row in reader:

					# If the port number is empty, skip
					if row[1] == "":
						continue

					port_numbers = []

					if '-' in row[1]:
						parts = row[1].split('-')
						port_numbers = [int(x) for x in range(int(parts[1]), int(parts[1]) + 1)] 
					else:
						port_numbers = [int(row[1])]


					for port_no in port_numbers:

						# Most protocols support multiple transport methods
						if port_no in service_map:
							entry = service_map[port_no]
							new_transport = entry.service_transport
							new_transport.add(row[2])
							service_map[port_no] = PortInfo(
								entry.port, 
								entry.service_name, 
								new_transport, 
								entry.service_desc
							) 
						else:
							service_map[port_no] = PortInfo(
								port_no, row[0], set([row[2]]), row[3]
							)

			self.service_map_loaded = True

		except Exception as e:
			self.logger.log_status(
				"Unable to load or parse service map. Service information will not be available when portscanning (Reason: {})".format(e), Logger.COLOR_INFO)

			self.service_map_loaded = False

		return service_map

	def get_ip_info(self):
		"""
		Retrieve the information about the IP address from ip-api.com.
		"""

		base_url = "http://ip-api.com/json/"
		url_params = "?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,currency,isp,org,as,asname,reverse,mobile,proxy,query"
		self.logger.info("Requesting information from {}".format(base_url))
		response = requests.get(base_url + str(self.target) + url_params)
		if response.status_code != 200:
			self.logger.error("Unable to connect to {} (Code {})".format(base_url, response.status_code))
		else:
			response_json = response.json()
			if response_json["status"] == "success":
				self.logger.success("Response from {}:".format(base_url))
				return response.json()
			else:
				self.logger.error("Unable to fetch information from {} (Reason: {})".format(base_url, response_json["message"]))
		return dict()

	def get_ssl_info(self, timeout=5):
		"""
		Retrieve the SSL certificate from the host.

		:param timeout: the timeout for the SSL connection.
		"""

		ctx = ssl.create_default_context()
		s = ctx.wrap_socket(socket.socket(), server_hostname=str(self.target))
		s.settimeout(timeout)
		try:
			s.connect((str(self.target), 443))
		except Exception as e:
			self.logger.error("Unable to connect to {} (Reason: {})".format(str(self.target), e))
			return dict()

		cert = s.getpeercert()
		s.close()
		self.logger.success("Certificate: ")
		return dict(cert)

	def get_whois_info(self, timeout=5):
		"""
		Retrieve the whois information for the targetfrom whois.arin.net.

		:param timout: the timeout for the WHOIS request.
		"""

		base_url = "whois.arin.net"
		self.logger.info("Sending whois query to {}".format(base_url))
		s = None
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((base_url, 43))
		except Exception as e:
			self.logger.error("Unable to connect to {} (Reason: {})".format(str(self.target), e))
			s.close()
			return ""
		
		host_address = ""
		try:
			host_address = socket.gethostbyname(self.target)
		except Exception as e:
			self.logger.error("Unable to connect to {} (Reason: {})".format(str(self.target), e))
			s.close()
			return ""

		s.send((host_address + "\r\n").encode())
		response = b""
		while True:
			data = s.recv(4096)
			response += data
			if not data:
				break

		s.close()
		self.logger.success("Response from {}:".format(base_url))
		return response.decode()

	def __check_port(self, port_no, callback, timeout=5):
		"""
		Tests if the given port is open on the target, if it is, the callback function is executed with one argument of type PortInfo.
		
		:param port_no: the port number to check.
		:param callback: the function to call upon completion.
		:param timeout: the time to wait for a response.
		"""

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(timeout)
		try:
			con = s.connect((self.target, port_no))
			try:
				service_info = self.find_service(port_no)
				callback(service_info)
			except Exception as e1:
				self.logger.error("Unable to scan port {} (Reason: {})".format(port_no, e1))
			con.close()
		except Exception:
			pass # port is probably closed

	def get_open_ports(self, callback, workers=100, start=1, end=1000, timeout=5):
		"""
		Gets the open ports running on the target and prints them as a table.

		:param callback: the function to call upon completion.
		:param workers: the number of workers (threads) to use.
		:param start: the start port number.
		:param end: the end port number.
		:param timeout: the time to wait for a response.
		"""

		# If the service map is not loaded yet, then try to load it
		if self.service_map_loaded == False:
			self.service_map = self.load_service_map()
			

		self.logger.info("Portscanning {} for open ports in the range {}-{}".format(self.target, start, end))
		self.logger.no_status("+----------+------------------------------+-------------------------+{}+".format("-" * 50))
		self.logger.no_status("| {} | {} | {} | {} |".format("Port No".ljust(8), "Protocol".ljust(28), "Transport".ljust(23), "Description".ljust(48)))
		self.logger.no_status("+----------+------------------------------+-------------------------+{}+".format("-" * 50))
		with ThreadPoolExecutor(max_workers=workers) as executor:
			for port in range(start, end+1):
				executor.submit(self.__check_port, port, callback, timeout)

		self.logger.no_status("+----------+------------------------------+-------------------------+{}+" .format("-" * 50))
		self.logger.success("Portscan finished")

	
	def find_service(self, port_no):
		"""
		Retrieves information about the service running on the given port.
		This information is read from services.csv.

		:param port_no: the port number to find the service / protocol for.
		"""

		try:
			if self.service_map_loaded:
				return self.service_map[port_no]
		except Exception:
			pass

		return PortInfo(port_no, "Unknown", "Unknown", "Unknown")


def print_dict(d):
	"""
	Prints the given dictionary in key-value pairs.

	:param d: the dictionary to print
	"""

	for k, v in d.items():
		print("{}: {}".format(k.ljust(20), v))


def print_port_info(portinfo):
	"""
	Prints the information of a port formatted to match the table in Dumper.get_open_ports.
	
	:param portinfo: a PortInfo object to display as a table.
	"""

	service_transport_joined = ','.join(portinfo.service_transport)

	port = str(portinfo.port).ljust(8)
	service_name = (portinfo.service_name[:25] + "..." if len(portinfo.service_name) >= 28 else portinfo.service_name).ljust(28)
	service_transport = (service_transport_joined[:20] + "..." if len(service_transport_joined) >= 23 else service_transport_joined).ljust(23)
	service_desc = (portinfo.service_desc[:45] + "..." if len(portinfo.service_desc) >= 48 else portinfo.service_desc).ljust(48)
	print("    | {} | {} | {} | {} |".format(port, service_name, service_transport, service_desc))

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("host", help="The hostname/IP Address, URL or Domain of the target", type=str)
	parser.add_argument("-l", "--no-logging", help="Disable logging", action="count")
	parser.add_argument("-c", "--no-color", help="Disable colored logging", action="count")
	parser.add_argument("-a", "--all", help="Run all tools on the given target", action="count")
	parser.add_argument("-p", "--port-scan", help="Enable portscanning on the target", action="count")
	parser.add_argument("-i", "--ip-info", help="Fetch information from api-ip.com (contains geographical info)", action="count")
	parser.add_argument("-s", "--ssl-cert", help="Retrieves the SSL Certificate of the host", action="count")
	parser.add_argument("-w", "--whois", help="Fetch whois information from arin.net (contains domain ownership info)", action="count")
	parser.add_argument("-n", "--workers", help="Number of workers for portscanning", type=int, default=256)
	parser.add_argument("-r", "--range", help="Range of ports to scan formatted as START-END", type=str, default="1-1024")
	parser.add_argument("-t", "--timeout", help="Timeout for SSL and WHOIS fetching and portscanning", type=int, default=5)
	args = parser.parse_args()
	
	logger = Logger(enabled=args.no_logging == None, color=args.no_color == None)
	dumper = Dumper(args.host)
	
	dumper.attach_logger(logger)

	logger.info("WARNING: By using this software you agree that you are liable for any damage (including criminal charges) which may arise from use of this software." \
		" For more information see the LICENSE file included with this software.")

	done_action = False
	if args.all != None or args.ip_info != None:
		print_dict(dumper.get_ip_info())
		done_action = True
	if args.all != None or args.ssl_cert != None:
		done_action = True
		print_dict(dumper.get_ssl_info(timeout=args.timeout))
	if args.all != None or args.whois != None:
		done_action = True
		print(dumper.get_whois_info(timeout=args.timeout))
	if args.all != None or args.port_scan != None:
		done_action = True
		dumper.get_open_ports(workers=args.workers, 
			start=int(args.range.split("-")[0]), 
			end=int(args.range.split("-")[1]), 
			callback=print_port_info, 
			timeout=args.timeout)

	if not done_action:
		logger.info("No actions specified for {}".format(args.host))
	else:
		logger.info("Report for {} completed".format(args.host))
		
		print("تريد الابلاغ عن الموقع اكتب الرابط هنا 👇")
		domain= input("domain ScamBot : ")


print (red_color+time.asctime( time.localtime(time.time()) ))
def print_progressbar(total, current, barsize=60):
    progress = int(current*barsize/total)
    completed = str(int(current*100/total)) + '%'
    print('[', chr(9608)*progress, ' ', completed, '.'*(barsize-progress), '] ', sep='', end='\r', flush=True)

total = 1
time.sleep(7)
barsize = 40
print_frequency = max(min(total//barsize, 100), 1)
print("Start Task..", flush=True)
for i in range(1, total+1):
  if i%print_frequency == 0 or i == 1:
    print_progressbar(total, i, barsize)
    print("")


os.system("curl -I "+domain+"")

total = 1
time.sleep(7)
barsize = 40
print_frequency = max(min(total//barsize, 100), 1)
print("Start Task..", flush=True)
for i in range(1, total+1):
  if i%print_frequency == 0 or i == 1:
    print_progressbar(total, i, barsize)
    print(banner_color+"")


data = {
    "client": {
      "clientId": "ScamBot",
      "clientVersion": "1.0"
    },
    "threatInfo": {
      "threatTypes":      ["MALWARE", "SOCIAL_ENGINEERING"],
      "platformTypes":    ["WINDOWS"],
      "threatEntryTypes": ["URL"],
      "threatEntries": [
{"url": domain},
      ]
    }
    }
json_data = json.dumps(data)
r = requests.post(f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key=AIzaSyBotIdgGswdWZ5yIUvX0bAkS_XejlHpyok', data = json_data)
response = r.json()
print(response,"" + domain + " تم البلاغ  ",)



api_url=f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_5IQnufTGIStbfGfKu0IoyWMD5jU6q&domainName='+domain
headers = {
        "Host": "www.whoisxmlapi.com"
    }
response = requests.request ("GET", api_url, headers=headers)
with open (''+domain+'.xml', 'a') as x:
    x.write (''+ response.text + '')
    print(response.text)





