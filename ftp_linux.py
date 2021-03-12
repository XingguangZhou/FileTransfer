import ftplib
import threading
import socket
import time
import sys

# Create a object to manage the file transfer between
# the client and the server.
class MyFTP(object):

	# !DEBUG! A private class-domain parameter used to record the file transfer count.
	__file_cnt = 0
	# A private class-domain parameter used to record the state of the upload file.
	__upload_file_ready = True

	# Initial settings.
	def __init__(self, ip, port):
		self.ftp = ftplib.FTP()
		self.ftp.connect(ip, port)
		self.ftp.set_debuglevel(2)
		self.ftp.login('******', '******')

	# Begin to download the file from the server
	def download(self, filename):
		self.file_handle = open(filename, 'wb').write
		self.ftp.retrbinary('retr '+filename, self.file_handle, 0x2000)
		print('Client has downloaded the file!')

	# Begin to upload the file from client to server
	def upload(self, filename):
		self.file_handle = open(filename, 'rb')
		self.ftp.storbinary('stor '+filename, self.file_handle, 0x2000)
		print('Client has uploaded the target file to server!')
    
	# FLAG to judge which time to download and upload.
	# Ubuntu is the client, and the Windows is server.
	def management(self, ip, port, download_filename, upload_filename):
		self.ip = ip
		self.port = port
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		# try to connect the windows server.
		try:
			self.client.connect((self.ip, self.port))
		except Exception as e:
			print('[*] Ubuntu : Server not found or not open!')
			self.ftp.close()
			sys.exit()  
        # begin to recieve the data.
		while True:
			send_message = self.client.sendall(input('Please input some message:').encode())
			request_code = self.client.recv(1024).decode()
			print("[*] request_code is : ", request_code)
			if request_code == '1':
				self.download(download_filename)
				# TODO: download and read file here!
				
			# Check the upload file state, and if it was ready, then,
			# send the message to TCP-SERVER and upload the file.
			# When OpenFAOM has done the calculation, then set the '__upload_file_ready'property into True.
			if MyFTP.__upload_file_ready == True:
				# upload the target file first!
				self.upload(upload_filename)
				# then, send the remind message second!
				self.client.sendall('1'.encode())
				# reset the '_upload_file_ready' property into False.
				MyFTP.__upload_file_ready = False

			# if the server recv the 'q' or 'quit' string, then break the cycle
			if request_code.lower() in ['q', 'quit']:
				break

    # !DEBUG_TEST!
	def debug(self):
		print('hello world!')

	# redefine the '__del__' magic method
	def __del__(self):
		# Close the connection from the client, unilaterally. 
		self.ftp.close()
		self.client.close()

if __name__ == '__main__':
	your_ip = ******
	your_port1 = *****
	your_port2 = *****
	ftp = MyFTP(your_ip, your_port1)
	ftp.management(your_ip, your_port2, 'ADSNJI.ZIP', 'ftp_linux.py')

