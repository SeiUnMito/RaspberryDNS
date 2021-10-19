from os import system
import os
from time import sleep
import shutil

class RaspberryDNS:
	def __init__(self):
		if os.name=="nt":
			print("This program does not work on Microsoft Windows.\nPlease run this on the GNU/Linux System.")
			exit()
		self.home=os.path.expanduser("~")+"/"
		permission=os.getuid()
		if permission!=0:
			print("This program should be run as root.\nPlease consider to run with sudo option.")
			exit()
		else:
			print("Root check verified. continue to the section.")
	def installDependencies(self):
		system("sudo apt -y install dnsmasq")
		print("If you failed to install software, please install dnsmasq manually.")
		print("Some of the distribution is not shipped with or unavailable repository.")
		print("If failed to install, Please check your distribution's package lists.")
	
	def backupConf(self):
		with open ("/etc/dnsmasq.conf","r") as f:
			lines=f.read()
			print("Preparing for back up...")
			if "#RaspberryDNS#" in lines:
				print("This one was created by RaspberryDNS. ")
				print("Backup is not needed.")
			else:
				print("It seems like this is original one.\nCreating back up")
				try:
					shutil.copy("/etc/dnsmasq.conf","/etc/dnsmasq.conf.bak")
					print("Backed up successfully.")
				except:
					print("Failed to create an backup. Please run this program with appropriate privilege.")

	def getHosts(self,path):
		with open(path,"r") as f:
			lines=f.read()
			lines=lines.split("\n")
			hosts=[]
			for a in lines:
				el=False
				for b in a:
					if b==" ":
						el=True
					else:
						el=False
				
				if a.startswith("#")!=True and el==False and a!="":
					hosts.append(a)
				
			return hosts

	def setPrefer(self,domainName="internal"):
			try:
				with open("/etc/dnsmasq.conf","w") as f:
					f.write("#RaspberryDNS#\n")
					f.write("# You can restore original configuration at any time. The original one has been stored at /etc/dnsmasq.conf.bak ")
					f.write("# This will send DNS query to the main DNS server only for domain name.\n")
					f.write("domain-needed\n")
					f.write("# If IP is local one, it will not send DNS query to the main DNS server\n")
					f.write("bogus-priv\n")
					f.write("# This will be useful later to add a fake domain name to your local devices.\n")
					f.write("expand-hosts\n")
					f.write("# This is your domain name. You can change  whatever you want\n")
					f.write("domain="+domainName)
					print("Settled preferred config. Please configure a local host.")
			except:
				print("Failed to write lines. Please check you have appropriate permissions.")
	def restore(self):
		try:
			print("Overwriting existing config and restoreing default...")
			shutil.copy("/etc/dnsmasq.conf.bak","/etc/dnsmasq.conf")
			print("Configuration has been restored.")
		except:
			print("Failed to restore configuration. Please consider to check you have appropriate permission.")
	
	def reinstall(self):
		system("sudo apt -y purge dnsmasq")	
		if os.path.isfile("/etc/dnsmasq.conf"):
			try:
				os.remove("/etc/dnsmasq.conf")
			except:
				print("Failed to delete a configuration file. Please check your permission.")
				system("sudo apt -y install dnsmasq")
				print("Re installation command issued. Checking default file.")
		self.installDependencies()
		if os.path.isfile("/etc/dnsmasq.conf"):
			with open("/etc/dnsmasq.conf","r") as f:
				data=f.read().split("\n")
				print("**** This is the preview of Re-installed configuration file ****")
			c=0
			while c<=20:
				if len(data) > c:
					print(data[c])
				c+=1
			print("**** Re installation Successfully done ****")
		else:
			print("Unfortunately, default configuration could not restored...\n Please install dnsmasq manually or check your distribution's default package.")

RaspberryDNS=RaspberryDNS()

if __name__=="__main__":
	print("RaspberryDNS: Easy DNS Builder for home users")
	print("* Please  use this software for small scale networking, not for bigger one! *\n")
	yes=["y","yes"]
	no=["no","n"]
	prefer=input("Is this your first time to setup? [Y/n] >>> ")
	if prefer.lower() in yes:
		RaspberryDNS.installDependencies()
		RaspberryDNS.backupConf()
		rasp=input("If you do not know about DNS server so much, RaspberryDNS can make a very basic configuration for just work.\nWould you like to use preferred configuration? [Y/n] >>> ")
		if rasp.lower() in yes:
			name=input("What domain name would you like to use? (For example, you can use example.com or local.rasp) >>> ")
			RaspberryDNS.setPrefer(name)
	else:
		funcList=["Try to install dependencies","Restore default configuration","Set preferred configuration","Manage hosts","Hanged up and I do not know what to do..."]
		c=0
		for f in funcList:
			print(str(c)+"."+f)
			c+=1
		wtd=input("What do you want to do? [0~{0}] >>> ".format(c-1))
		if wtd=="0":
			RaspberryDNS.installDependencies()
		elif wtd=="1":
			RaspberryDNS.restore()
		elif wtd=="2":
			name=input("What domain name would you like to use? (For example, you can use example.com or local.rasp) >>> ")
			RaspberryDNS.setPrefer(name)
		elif wtd=="3":
			print("Now you can edit your hosts table. Type dl:(number) to delete entry from table or type ip __ name to add an entry to the table. You can quit as #")
			print("*** Examples ***")
			print("dl:0    <- This means delete number 0 from the table")
			print("192.168.0.102  media_centre    <- This means add 192.168.0.102 as named media_centre")
			hosts=RaspberryDNS.getHosts(path="/etc/hosts")
			origin=hosts.copy()
			while True:
				print("\n**** These are hosts entry ****")
				en=0
				for f in hosts:
					print(str(en)+"  --- >  {0}".format(f))
					en+=1


				wtd=input(">>> ")
				if wtd.startswith("dl:"):
					wtd=wtd[wtd.find(":")+1:]
					del hosts[int(wtd)]
				elif wtd=="#":
					print("Quit manage mode.")
					if origin!=hosts:
						save=input("The configuration has been changed. Are you sure you save the buffer? [Y/n] >>> ")
						if save.lower() in yes:
							try:
								with open ("/etc/hosts","w")  as f:
									for a in hosts:
										f.write(a+"\n")
								print("Successfly Updated. Please restart service as sudo service dnsmasq restart")
							except:
								print("Failed to save to the file. Please check your permission.")
						else:
							print("Canceled.")
					break
				else:
					hosts.append(wtd)
		elif wtd=="4":
			reins=input("Stay calm. Maybe you can restore your default configuration by reinstalling dnsmasq package.\nMay I reinstall the dnsmasq package right now? [Y/n] >>> ")
			if reins.lower() in yes:
				RaspberryDNS.reinstall()
			else:
				print("Ok. You can re-install dnsmasq with sudo apt purge dmsmasq && sudo apt install dnsmasq")
				

