import calendar
from datetime import timedelta, date, datetime
from dateutil import parser
from itertools import tee
import itertools
from dateutil import rrule
import csv
import re
import os
bills =[['01','1500.00'],['01','190.00'],['02','87.00'],['07','15.00'],['10','220.00'],['10','256.00'],['10','11.99'],['11','210.00'],['13','34.00'],['14','118.00'],['15','5.00'],['15','290.00'],['05','15.99'],['15','140.00'],['17','290.00'],['17','120.00'],['24','300.00'],['24','52.00'],['06','155.00'],['28','70.00'],['28','50.00']]


datemin = date(2018,9,1)
datemax = date(2018,12,31)



x = '2018-09-14'
x = parser.parse(x)


paydate = []
checks = []
billsdue =[]
cash = []
bymonth = []
bbcheq = {}

def pairwise(checks):
    a, b = tee(checks)
    next(b, None)
    return zip(a, b)

def dates(datemin,datemax):
    for n in range(int ((datemax - datemin).days)):
        yield datemin + timedelta(n)

def weekendcheck(dt,paydate):
    if re.match('Saturday', calendar.day_name[dt.weekday()]):
        pay = (dt - timedelta(days=1))
        paydate.append(pay.strftime("%Y-%m-%d"))
    if re.match('Sunday', calendar.day_name[dt.weekday()]):
        pay = (dt - timedelta(days=2))
        paydate.append(pay.strftime("%Y-%m-%d"))
    else:
        paydate.append(dt.strftime("%Y-%m-%d"))
    return paydate

def getpaydays(datemin,datemax,x,checks,paydate):
    for dt in dates(datemin,datemax):
        if re.match('(15|30)',str(dt.day)):
            weekendcheck(dt,paydate)
        else:
            if dt == x:
                paydate.append(dt.strftime("%Y-%m-%d"))
            else:
                for dt in rrule.rrule(rrule.WEEKLY, interval=2, dtstart=x, until=datemax):
                    weekendcheck(dt,paydate)
        checks = list(set(paydate))
    checks.sort()
    checks = tuple(checks)
    return checks


def getbills(datemin,datemax,bills):
    for month in rrule.rrule(rrule.MONTHLY, interval=1, dtstart=datemin, until=datemax):
        for bill in bills:
            duedate = list([str(month.strftime("%Y-%m-")) + bill[0]])
            duedate.append(bill[1])
            billsdue.append(duedate)
    billsdue.sort()
    return billsdue

def billcheckdelta(billsdue,checks,bymonth):
    for month in rrule.rrule(rrule.MONTHLY, interval=1, dtstart=datemin, until=datemax):
        for bill in billsdue:
            for pair in pairwise(checks):
                if bill[0] > pair[0] and bill[0] < pair[1]:
                    x = []
                    x.append(pair[0])
                    x.append(bill[1])
                    x = tuple(x)
                    bymonth.append(x)

    return bymonth


def cheques(bymonth,bbcheq):
    for x in bymonth:
        for i in range(0, len(x)):
            cheq = x[1]
            bill = x[0]
        if not bbcheq.__contains__(bill):
            URLlist = []
            URLlist.append(cheq)
            bbcheq[bill] = URLlist
        else:
            bbcheq[bill].append(cheq)
    return bbcheq

def billdetail(bbcheq):

    with open('/home/joe/Documents/Budget.txt', 'x') as budget:
        distinct = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        header2 = "Checks and bills for Checks until 2019"
        wr = csv.writer(budget, lineterminator='\n')
        wr.writerow([header2])
        wr.writerow([distinct])
    for k, v in bbcheq.items():
        with open('/home/joe/Documents/Budget.txt', 'a') as budget:
            breakup = '--------------------------------------'
            distinct = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            header = "Check Date"
            x = set(v)
            totes = sum(map(float, list(x)))
            print(k)
            print(x)
            print(totes)
            header1 = "Bills Detail"
            header3 = "Sum Total"
            wr = csv.writer(budget, lineterminator='\n')
            wr.writerow([header])
            wr.writerow([k])
            wr.writerow([breakup])
            wr.writerow([header1])
            wr.writerow([x])
            wr.writerow([header3])
            wr.writerow([breakup])
            wr.writerow([float(totes)])
            wr.writerow([distinct])






checks = getpaydays(datemin,datemax,x,checks,paydate)
billsdue = getbills(datemin,datemax,bills)
bymonth = billcheckdelta(billsdue,checks,bymonth)
bbcheq = cheques(bymonth,bbcheq)
print (bbcheq)
billdetail(bbcheq)