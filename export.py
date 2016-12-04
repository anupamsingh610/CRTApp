import MySQLdb
import time
import datetime
import usb

def output_to_file(r,d,s,interval):
  
    db = MySQLdb.connect("localhost","root","password") 							#connect the database
    cursor = db.cursor()
  
    sql= """USE CRT1;"""
    cursor.execute(sql)
	
    outfile = open("testing.text","w") 													#ismei save krenge output || name can preferably be the date!
   	
    outstring1 = "1 "+r+" "+d+" "+s
    outfile.write(outstring1+"\n")  															#Line-1 into the file

    #time1=str(hh1+":"+mm1)
    #time2=str(hh2+":"+mm2)
    intt=int(interval)
    sql = ("""SELECT * FROM TEMPERATURES1;""")		#Retrieving data from whole dbms
    cursor.execute(sql)
    result = cursor.fetchall()
    giveresult(result,intt)
  

def giveresult(result,interval):
  
    num=0																				#To deal with the timeinterval(in minutes)	
    maxtemp = result[0][2]
    mintemp = result[0][2]
	
    absmaxtemp = result[0][2]
    absmintemp = result[0][2]
	
    x=result[0][0]
    y=result[0][1]
	
    mindate =x																				#min ki date
    maxdate	=x																			
	
    absmaxdate =x																		#absolute max ki date
    absmindate =x
	
    mintime=y			
    maxtime=y
	
    absmaxtime=y
    absmintime=y
	
    perdate=x
    
    outstring3="3 " +str(maxdate)+" "+str(maxtime)+" +" + str(maxtemp)+" Deg C HR MAX"
    outstring4="4 " +str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"
	
    for row in result:
        outdate = row[0]
	outtime = row[1]
	outtemp = row[2]
	temptemp=outtemp
	if outtemp>=absmaxtemp:															#changing absolute maximum and minimum(which will be per minute)
            absmaxtemp=outtemp
            absmaxdate=outdate
            absmaxtime=outtime
		                
	if absmintemp>=outtemp:
            absmintemp=outtemp
            absmindate=outdate
            absmintime=outtime

	intt=int(interval)		
	if num%intt==0:  #num%60==0																	for every hour (increasing num at every minute(reading))
            if perdate!=outdate:
                perdate=outdate
                outfile.write(outstring3+"\n")														#Writing the hourly maximum and minimum temperature
                outfile.write(outstring4+"\n")														#Writing Line-3 and Line-4
                mintemp=outtemp
                maxtemp=outtemp
                mindate=outdate
                maxdate=outdate
                mintime=outtime
                maxtime=outtime
                                
            if mintemp>=outtemp:
                mintemp=outtemp
                mindate=outdate
                mintime=outtime
                if(mintemp<0):
                    outstring4 = "4 "+str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"	
                else:
                    outstring4 = "4 "+str(mindate)+" "+str(mintime)+" +" + str(mintemp)+" Deg C HR MIN"
                
            if outtemp>=maxtemp:															
                maxtemp=outtemp
                maxdate=outdate
                maxtime=outtime
                outstring3 = "3 " +str(maxdate)+" "+str(maxtime)+" +" + str(maxtemp)+" Deg C HR MAX"						#hourly max temperature per day
			
            if outtemp>=0 : 																#Line 2 of the output file
                outstring = "2 "+str(outdate)+" "+outtime+" +" +str(outtemp)+" Deg C"
            else :
                outstring = "2 "+str(outdate)+" "+outtime+" -" + str(outtemp)+" Deg C"
        outfile.write(outstring+"\n")
		
        num=num+1
															
    outfile.write(outstring3+"\n")														#Writing the hourly maximum and minimum temperature
    outfile.write(outstring4+"\n")														#Writing Line-3 and Line-4
        
    outstring5 = "5 "+str(absmaxdate)+" "+str(absmaxtime)+" +" + str(absmaxtemp)+" Deg C AB MAX"		#Writing Absolute minimum and maximum ONCE
	
    if(absmintemp<0):
        outstring6 = "6 "+str(absmindate)+" "+str(absmintime)+" -" + str(absmintemp)+" Deg C AB MIN"	
    else:
        outstring6 = "6 "+str(absmindate)+" "+str(absmintime)+" +" + str(absmintemp)+" Deg C AB MIN"
	
    outfile.write(outstring5+"\n")	
    outfile.write(outstring6+"\n")
    usb.usbexport()
