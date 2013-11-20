#!/usr/bin/env python
#coding:utf-8

import MySQLdb
import sys,os
import time
import getopt
from dnspod.apicn import *




def usage():

        print """

              -h,-H, --help         帮助页面 
              -d , --domain       需要解析的域名
	          -i , --ipaddress    域名对应的IP地址
		
	ex:
	python  dns_mamange.py -d test.testoa.com  -i 192.168.1.1
"""

 
def add_records(domain_id,records,ipaddress):
        try:
                tmp_sub=[]
                for i in range(len(rec_list)):
                        tmp_sub.append(rec_list[i].get("name"))
                if sub_dom in tmp_sub:
               		update_record(rec_list,sub_dom,domain_id,'.'.join(records.split('.')[-2:]),ipaddress)
               	else:
               		add_record=RecordCreate(sub_dom,"A",u'默认'.encode("utf8"),ipaddress,600,domain_id=domain_id,email=login_email,password=password)
                        add_record()
	                print "\033[31m成功添加域名记录:[ %s.%s ==> %s ]！\033[0m"%(sub_dom,dom,ipaddress)
        except Exception,e:
                print e

def update_record(rec_list,sub_dom,domain_id,dom,ipaddress):
			if record_value == ipaddress:
				print "\033[31m域名记录:[ %s.%s ==> %s ]已经存在！\033[0m"%(sub_dom,dom,ipaddress)
			else:
	                	try:
	                		update_dom=RecordDdns(record_id=record_id,sub_domain=sub_dom,record_line="默认",domain_id=domain_id,value=ipaddress,record_type=record_type,ttl=600,email=login_email,password=password)
	                    		update_dom()
	                    		print "\033[32m域名 [ %s.%s ] IP地址成功更新为 [ %s ] \033[0m" % (sub_dom,dom,ipaddress)
	
	                	except Exception,e:
	                		print "[Error]: %s" % e
	                    		print "\033[31m域名 [ %s.%s ] IP地址更改失败！ [ %s ] \033[0m" % (sub_dom,dom,ipaddress)



def namedmanager(sub_dom,record_value):
	try:
		conn=MySQLdb.connect(host='192.168.250.138',user='namedmanager',passwd='namedmanager',db='namedmanager',port=3306,charset='utf8')
	    	cursor=conn.cursor()
	    	cursor.execute('select id,name,content from dns_records where type = "A";')
	    	result=cursor.fetchall()
		cursor.close()

		instert_dns="INSERT INTO `namedmanager`.`dns_records`(`id`,`id_domain`,`name`,`type`,`content`,`ttl`,`prio`) VALUES ( NULL,'1','%s','A','%s','86400','0'); "%(sub_dom,record_value)
		update_name_dns="UPDATE `namedmanager`.`dns_records` SET `name`='%s' WHERE content='%s';"%(sub_dom,record_value)
		update_ip_dns="UPDATE `namedmanager`.`dns_records` SET `content`='%s' WHERE name='%s' ;"%(record_value,sub_dom)
                ip_exist_dns_not_exist = []
                dns_exist_ip_not_exist = []
                ip_not_exist_dns_not_exist = []
		#print result
                for item in result:
			if record_value in item and item[1] == sub_dom:
                               	print '\033[31m [%s.testoa.com ==> %s ] 记录已经存在！\033[0m'%(sub_dom,record_value)
				sys.exit()
			elif record_value in item and item[1] != sub_dom:
				ip_exist_dns_not_exist.append(item)
			if sub_dom in item and item[2] != record_value:
				dns_exist_ip_not_exist.append(item)
				if sub_dom in item and item[2] == record_value:
					pass
			if sub_dom not in item:
				if record_value not in item:
					pass

		#print ip_exist_dns_not_exist,dns_exist_ip_not_exist,ip_not_exist_dns_not_exist
		if ip_exist_dns_not_exist:
			cursor=conn.cursor()
			cursor.execute(update_name_dns)
			print '\033[32m [%s.testoa.com ==> %s ] IP不变，更改域名成功！\033[0m'%(sub_dom,record_value)
			cursor.close()
			conn.commit()
			sys.exit()
		if  dns_exist_ip_not_exist:
			cursor=conn.cursor()
			cursor.execute(update_ip_dns)
			print '\033[32m [%s.testoa.com ==> %s ] 域名不变，更改IP成功！\033[0m'%(sub_dom,record_value)	
			cursor.close()
			conn.commit()
			sys.exit()
		if not ip_not_exist_dns_not_exist:
			cursor=conn.cursor()
			cursor.execute(instert_dns)
			print '\033[32m [%s.testoa.com ==> %s ] 记录添加成功！\033[0m'%(sub_dom,record_value)
			cursor.close()
			conn.commit()
			sys.exit()
   		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
	try:
        	opts, args = getopt.getopt(sys.argv[1:], "(hH)d:i:", ["help","domain=","ipaddress="])
                if   len(sys.argv) == 1 :
                        usage()
			print "\033[041m参数为空，请重新输入！\033[0m"
                        sys.exit()
                if sys.argv[1] in ("-h","-H","--help"):
                        usage()
                        sys.exit()
		elif sys.argv[1] in ("-d","--domain"):
                        for opt,arg in opts:
                                if opt in ("-d","--domain="):
                                        records=arg
                                if opt in ("-i","--ipaddress="):
					ipaddress=arg
		else:
			print "\033[041m参数输入有误，请重新输入！\033[0m"
			usage()
			sys.exit()

		login_email = "login_email"
		password = "password"
		domain_id='domain'	
		sub_dom='.'.join(records.split('.')[:-2])
        	api_subdom=RecordList(domain_id,email=login_email,password=password)
        	rec_list=api_subdom().get("records")
		dom='.'.join(records.split('.')[-2:])
		for nu in range(0,len(rec_list)):
        		if sub_dom == rec_list[nu].get("name"):
				record_value=rec_list[nu].get("value")
            			record_id=rec_list[nu].get("id")
				record_type=rec_list[nu].get("type")			

		#更新dnspod域名
		print "\nDNSPOD域名变更.......\n"
        	add_records(domain_id,records,ipaddress)
		#更新内部域名
		print "\n内部域名变更.......\n"
		namedmanager(sub_dom,ipaddress)
		time.sleep(1)
		os.system('/usr/sbin/rndc reload')
	
        except Exception,ex:
                print ex
