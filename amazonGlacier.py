import boto3
import os
import zipfile
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime

class amazonGlacier():
	def __init__(self,base_path,vault_name,host,username,password,database,uploaded_path):
		self.base_path=base_path
		self.vault_name=vault_name
		self.host=host
		self.username=username
		self.password=password
		self.database=database
		self.uploaded_path=uploaded_path
	def addArchive(self,file_name,archiveId,location,checksum):
		try:
			connection = mysql.connector.connect(host=host,
								 database=self.database,
								 user=self.username,
								 password=self.password,use_pure=True)
			cursor = connection.cursor(prepared=True)
			query = """ INSERT INTO `archive`
							  (file_name,archiveId,location,checksum) 
							  VALUES (%s,%s,%s,%s)"""
			query_tuple = (file_name,archiveId,location,checksum)
			result  = cursor.execute(query, query_tuple)
			connection.commit()
			#print ("Record inserted successfully into archive table")
		except mysql.connector.Error as error:
			connection.rollback()
			#print("Failed to insert into MySQL table {}".format(error))
		finally:
			#closing database connection.
			if(connection.is_connected()):
				cursor.close()
				connection.close()
				#print("MySQL connection is closed")
	def compressFile(self,file_name):
		name=file_name.split(".")
		zipper=zipfile.ZipFile(base_path+name[0]+".zip",'w')
		zipper.write(base_path+file_name,file_name)
		zipper.close()
	def archiveUpload(self,file_name):
		client=boto3.client('glacier')
		response=client.upload_archive(vaultName=vault_name,archiveDescription=file_name,body=base_path+file_name)
		#self.addArchive("zero","one","two","three")	
		self.addArchive(file_name,response['archiveId'],response['location'],response['checksum'])		
	def compressFiles(self):
		files=os.listdir(base_path)
		for i in range(len(files)):
			self.compressFile(files[i])
		print(str(len(files))+" files compressed ")	
	def removeFiles(self):
		files=os.listdir(base_path)
		for i in range(len(files)):
			if(files[i].split(".")[1]=="sql"):
				os.remove(base_path+files[i])	
		print(str(len(files))+" files removed ")
	def uploadFiles(self):
		files=os.listdir(base_path)
		for i in range(len(files)):
			self.archiveUpload(files[i])
			os.rename(base_path+files[i],uploaded_path+files[i])
		print(str(len(files))+" files uploaded and moved ")		
base_path="/home/james/archive/"
uploaded_path="/home/james/uploaded/"
vault_name="xxx"
host="xxx"
username="xxx"
password="xxx"
database="xxx"
amazon=amazonGlacier(base_path,vault_name,host,username,password,database,uploaded_path)
amazon.compressFiles()
amazon.removeFiles()
amazon.uploadFiles()

"""
filepath=input("Enter path: ")
action=input("Enter action to be done: ")
base_path="/home/james/archives/"+filepath+"/"
amazon=amazonGlacier(base_path)

if action=="compress":
	amazon.compressFiles()
	#remove the non compressed files before this process
elif action=="upload":
	amazon.uploadFiles()
elif action=="remove":
	amazon.removeFiles()
"""

		



