import urllib2
import json
import math

import numpy as np

np.random.seed(123)

class Stock:
    SD=0
    average_return=0
    
    def __init__(self, selected_stock):
        self.selected_stock = selected_stock
        self.SD = 0
        self.average_return = 0
        
    def stockName(self):
        return self.selected_stock
        
    def stockReturn(self):
        endpoint = 'https://api.iextrading.com/1.0/stock/'
        url = endpoint + self.selected_stock + '/chart/5y'
        json_obj = urllib2.urlopen(url)
        data = json.load(json_obj)
        
        float_return = 0
        float_sum = 0
        num_entries = 0
        for item in data:
            float_sum += float(item['close'])
            float_return += float(item['changePercent'])
            num_entries += 1
        self.average_return = 100 * (float_return / num_entries)
        return self.average_return
        
    def stockSD(self):
        endpoint = 'https://api.iextrading.com/1.0/stock/'
        url = endpoint + self.selected_stock + '/chart/5y'
        json_obj = urllib2.urlopen(url)
        data = json.load(json_obj)
        
        float_return = 0
        float_sum = 0
        num_entries = 0
        for item in data:
            float_sum += float(item['close'])
            # print item['date']
            # print item['close']
            num_entries += 1
        mean = float_sum / num_entries

        variance = 0
        for item in data:
            variance += ((mean - item['close']) * (mean - item['close']))
        variance = variance / num_entries
        variance = math.sqrt(variance)
        
        self.SD = variance
        return self.SD
        
def rand_weights(n):
    k = np.random.rand(n)
    return k / sum(k)
    
def main():
    
    riskFree = 2
    
    num_entries = int(raw_input("Enter num of Stocks: "))
    if ((num_entries<1) or (num_entries>4)):
        return
    
    stock_list = []
    stds = []
    means = []
    
    num_entries_iter = num_entries
    while (num_entries_iter > 0):
        inputString = raw_input("Enter a stock name: ")
        stock1 = Stock(inputString)
        stock_list.append(stock1)
        stds.append(stock1.stockSD())
        means.append(stock1.stockReturn())
        num_entries_iter -= 1
   
    ## NUMBER OF ASSETS
    n_assets = num_entries
    
    ## NUMBER OF OBSERVATIONS
    n_obs = 25
    
    weight_array = []
    
    # print "FInished )AS)D "
    
    n_obs_iter = n_obs
    port_weights = rand_weights(n_assets)
    port_weights_list = []
    maxSharp = 0
    maxSharp_loc = 0
    
    while n_obs_iter > 0:
        
        port_weights = rand_weights(n_assets)
        port_weights_list.append(port_weights)
        
        portSD = 0
        portReturn = 0
        num_entries_iter=0
        while num_entries_iter < num_entries:
            portReturn += port_weights.item(num_entries_iter) * stock_list[num_entries_iter].stockReturn()
            portSD += port_weights.item(num_entries_iter) * stock_list[num_entries_iter].stockSD()
            num_entries_iter += 1
        portReturn = float(portReturn) / float(num_entries)
        portSD = float(portSD) / float(num_entries)
        
        sharp = (portReturn - riskFree) / portSD
        # print(str(sharp) + " Iter: " + str(n_obs_iter))
        if(sharp > maxSharp):
            maxSharp = sharp
            maxSharp_loc = int(n_obs_iter)
        
        n_obs_iter -= 1
    # print(maxSharp_loc)
    print
    print "Optimal portfolio is made up of"
    num_entries_iter=0
    while num_entries_iter < num_entries:
        print(str(stock_list[num_entries_iter].stockName()) + ": " + str(100 * port_weights_list[maxSharp_loc-1].item(num_entries_iter)) + "%")
        num_entries_iter += 1
    
    return
    
main()