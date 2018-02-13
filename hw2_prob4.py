# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 14:43:58 2018
Author: Xinyun Cao
"""

import numpy as np
import statistics as stat
import csv
import math

class Customer:
    def __init__(self, arrival_time, service_start_time, service_time):
        self.arrival_time = float("{0:.2f}".format(arrival_time))
        self.service_start_time = float("{0:.2f}".format(service_start_time))
        self.service_time = float("{0:.2f}".format(service_time))  #Ts
        self.service_end_time = self.service_start_time + self.service_time
        self.wait_time = self.service_start_time - self.arrival_time
        self.time_in_system = self.wait_time + service_time


#not a list of Customer objects, just list of IATs
Future_customers = []
#list of total customers serviced
Customers_serviced = []

####
mean_rhos = []
mean_ws = []
mean_qs = []
mean_Tqs = []
mean_Tws = []
#generates exponential variate based on a poisson distribution
#this makes an IAT based on number of requests/time (poisson lambda)
def exp_generator(lambd): 
    return np.random.exponential(1/lambd) 

def mu(Ts):
    return np.random.exponential(Ts)

def initialize_list(n, lambd):
    for i in range(n):
        Future_customers.append(exp_generator(lambd))
    return

#generates the next customer to enter the system, using the list of future_cstomers
def reset():
    Future_customers.clear()
    Customers_serviced.clear()   

def birth(Ts): 
    IAT = Future_customers.pop(0)
    service_time = mu(Ts)
    if len(Customers_serviced) == 0: #first customer
        arrival_time = IAT
        service_start_time = arrival_time
    else: #not the first customer
        arrival_time = IAT + Customers_serviced[-1].arrival_time
        service_start_time = max(Customers_serviced[-1].service_end_time, arrival_time)
    return Customer(arrival_time, service_start_time, service_time)

#customer leaves system; just add customer data to customers_serviced list
        
def death(customer):
    Customers_serviced.append(customer)
    return

def simulate(lambd, Ts, max_time):
    time = 0
    reset()
    while (time < max_time): 
        if len(Future_customers) == 0: # in case simulation runs out of future events
            initialize_list(max_time, lambd)
        customer = birth(Ts)
        death(customer)
        time = customer.arrival_time
        #keep track of all customers in system

    #print("Statistics:\n")
    ##################################################

    total_time = [c.time_in_system for c in Customers_serviced]
    total_mean_time = sum(total_time)/len(total_time)
    service_times = [c.service_time for c in Customers_serviced]
    util = sum(service_times)/time
    wait_times = [c.wait_time for c in Customers_serviced]
    avg_wait = sum(wait_times)/len(wait_times)
    q = util/(1-util)
    w = util**2/(1-util)
    
    mean_rhos.append(util)
    mean_ws.append(w)
    mean_qs.append(q)
    mean_Tqs.append(total_mean_time)
    mean_Tws.append(avg_wait)
    #########################
    #print("ρ: ", util)
    #print("w: ", w)
    #print("q: ", q)
    #print("Tq: ", total_mean_time)
    #print("Tw: ", avg_wait)
    #print("Ts :", avg_service)
    #print()
    

    ##################################################
    """Comment out this part of code if you want to run
    a ton of simulations for CLT purposes"""
    if input("Export data to csv (True/False)?"):
        export_data(lambd, Ts, max_time)
    return

def export_data(lambd, Ts, max_time):
    outfile=open('MM1Q-data-(%s,%s,%s).csv' %(lambd,Ts,max_time),'w')
    output=csv.writer(outfile)
    output.writerow(['Customer', 'arrival_time', 'service_time', 
                     'service_start_time', 'service_end_time', 
                     'wait_time', 'time_in_system'])
    i = 0
    for customer in Customers_serviced:
        i = i + 1
        outrow = []
        outrow.append(i)
        outrow.append(customer.arrival_time)
        outrow.append(customer.service_time)
        outrow.append(customer.service_start_time)
        outrow.append(customer.service_end_time)
        outrow.append(customer.wait_time)
        outrow.append(customer.time_in_system)
        output.writerow(outrow)
    outfile.close()
    return

def statistics(l):
    norm_mean = sum(l)/100
    norm_stdev = stat.stdev(l)
    error = 1.96 * norm_stdev/math.sqrt(100)
    #print("N = 100")
    print("mean: ", norm_mean)
    print("standard deviation: ", norm_stdev)
    print("95% confidence interval: ", 
          float("{0:.3f}".format(norm_mean)), "+-", 
                float("{0:.3f}".format(error)))
    return

simulate(3, 0.20, 2000)

#sim = [simulate(3, 0.20, 2000) for i in range(100)]
#statistics(mean_rhos)
#statistics(mean_ws)
#statistics(mean_qs)
#statistics(mean_Tqs)
#statistics(mean_Tws)
