import calendar
from datetime import timedelta, date, datetime
from dateutil import parser
from itertools import tee
import itertools
from dateutil import rrule
import csv
import re
import os

class budget():
    """Buttcheeks"""
    def __init__(self, bills,start_date, end_date, next_check_date):
        self.bills = bills
        self.start_date = start_date
        self.end_date = end_date
        self.next_check_date = next_check_date
        self.paydate = paydate = []
        self.checks =  checks = []
        self.billsdue = billsdue =[]
        self.cash = cash = []
        self.bymonth = bymonth = []
        self.bbcheq = bbcheq = {}

    def pairwise(self):
        a, b = tee(self.checks)
        next(b, None)
        return zip(a, b)

    def dates(self):
        for n in range(int((start_date - end_date).days)):
            yield self.start_date + timedelta(n)

    def weekendcheck(self,dt):
        if re.match('Saturday', calendar.day_name[dt.weekday()]):
            pay = (dt - timedelta(days=1))
            self.paydate.append(pay.strftime("%Y-%m-%d"))
        if re.match('Sunday', calendar.day_name[dt.weekday()]):
            pay = (dt - timedelta(days=2))
            self.paydate.append(pay.strftime("%Y-%m-%d"))
        else:
            self.paydate.append(dt.strftime("%Y-%m-%d"))
        return self.paydate

    def getpaydays(self):
        for dt in self.dates(start_date,end_date):
            if re.match('(15|30)',str(dt.day)):
                weekendcheck(dt,self.paydate)
            else:
                if dt == x:
                    self.paydate.append(dt.strftime("%Y-%m-%d"))
                else:
                    for dt in rrule.rrule(rrule.WEEKLY, interval=2, dtstart=self.next_check_date, until=self.end_date):
                        weekendcheck(dt,self.paydate)
            self.checks = list(set(self.paydate))
            self.checks.sort()
            self.checks = tuple(self.checks)
        return self.checks


    def getbills(self):
        for month in rrule.rrule(rrule.MONTHLY, interval=1, dtstart=self.start_date, until=self.end_date):
            for bill in self.bills:
                duedate = list([str(month.strftime("%Y-%m-")) + bill[0]])
                duedate.append(bill[1])
                self.billsdue.append(duedate)
        self.billsdue.sort()
        return self.billsdue

    def billcheckdelta(self):
        for month in rrule.rrule(rrule.MONTHLY, interval=1, dtstart=self.start_date, until=self.end_date):
            for bill in self.billsdue:
                for pair in self.pairwise(self.checks):
                    if bill[0] > pair[0] and bill[0] < pair[1]:
                        x = []
                        x.append(pair[0])
                        x.append(bill[1])
                        x = tuple(x)
                        print(X)
                        self.bymonth.append(x)

        return self.bymonth


    def cheques(self):
        for x in self.bymonth:
            for i in range(0, len(x)):
                cheq = x[1]
                bill = x[0]
            if not self.bbcheq.__contains__(bill):
                check_dates = []
                check_dates.append(cheq)
                self.bbcheq[bill] = check_dates
            else:
                self.bbcheq[bill].append(cheq)
        return self.bbcheq

    def billdetail(self):
        with open('/home/joe/Documents/Budget.txt', 'x') as budget:
            distinct = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            header2 = "Checks and bills for Checks until 2019"
            wr = csv.writer(budget, lineterminator='\n')
            wr.writerow([header2])
            wr.writerow([distinct])
        for k, v in self.bbcheq.items():
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

bills =[['01','1.00'],['01','1.00'],['02','1.00'],['07','1.00'],['10','1.00'],['10','1.00'],['10','1.00'],['11','1.00'],['13','1.00'],['14','1.00'],['15','1.00'],['15','1.00'],['05','1.00'],['15','1.00'],['17','1.00'],['17','1.00'],['24','1.00'],['24','1.00'],['06','1.00'],['28','1.00'],['28','1.00']]
datemin = date(2018,9,1)
datemax = date(2018,12,31)
x = '2018-09-14'
x = parser.parse(x)
params = budget(bills, date(2018,9,1), date(2018,12,31),x)
params.getpaydays(),params.getbills(), params.billcheckdelta(), params.cheques(), params.billdetail()