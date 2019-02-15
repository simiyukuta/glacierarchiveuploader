# glacierarchiveuploader
Python script to compress,uploads archives on amazon glacier and the log details of the archive in a mysql table  

amazon  

https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html  
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html#Glacier.Client.upload_archive  
apt install awscli  
aws configure  
python3  
apt install python3-pip  
pip3 install boto3  
pip3 install mysql-connector-python  
mkdir /home/james/uploaded  

mysql  
CREATE DATABASE glacier;  
USE glacier;  
CREATE TABLE `archive` (  
  `id` int(11) NOT NULL AUTO_INCREMENT,  
  `archiveId` text,  
  `location` text,  
  `checksum` text,  
  `file_name` varchar(50) DEFAULT NULL,  
  `created_date` datetime DEFAULT CURRENT_TIMESTAMP,  
  `modified_date` datetime DEFAULT CURRENT_TIMESTAMP,  
  `created_by` int(11) NOT NULL DEFAULT '1',  
  `is_deleted` int(11) NOT NULL DEFAULT '0',  
  PRIMARY KEY (`id`)  
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;  
