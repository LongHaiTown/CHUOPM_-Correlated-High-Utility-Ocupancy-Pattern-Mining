transactions = {
    "T1": [("b", 4), ("p", 2)],
    "T2": [("c", 1), ("e", 1)],
    "T3": [("e", 1), ("t", 1), ("ts", 1)],
    "T4": [("b", 1), ("p", 3)],
    "T5": [("t", 1)],
    "T6": [("e", 1), ("p", 1), ("t", 1)],
    "T7": [("b", 1), ("c", 2), ("p", 4)],
    "T8": [("p", 2), ("t", 1)],
    "T9": [("p", 3), ("t", 1), ("ts", 1)],
    "T10": [("b", 1),("c", 2), ("p", 4)],
    "T11": [("e", 1),("ts", 1)]
}
item_EU = {
    "b": 2,
    "c": 2,
    "e": 4,
    "p": 2,
    "t": 10,
    "ts": 10
}
## [ ['ts'] , ['b'] ...]
# def findCoverset(itemset):
#     coverset= []
#     for key,val in transactions.items():
#         print(key)
#         count = 0
#         for value in val:
#             print(value[0],end=" ")
#             for item in itemset:
#                 if value[0] == item[0]:
#                     count +=1
#         if count == len(itemset):
#             coverset.append(key)
#             print("yes" ,end= "")

#         print("")
#     return coverset

def findCoverset(itemset):
    coverset= []
    for key,val in transactions.items():
        count = 0
        for value in val:
            if value[0] in itemset :
                count +=1
        if count == len(itemset):
            coverset.append(key)
    return coverset


def calculate_Item_util_in_Trans(item,transaction):
    util = 0
    for ite in transaction:
        if (ite[0] == item):
            util = ite[1]*item_EU[item]
    return int(util)

def calculate_Itemset_util_in_Trans(itemset,transaction):
    util = 0
    for ite in transaction:
        for i in itemset:
            if (ite[0] == i):
                util += calculate_Item_util_in_Trans(ite[0],transaction) 
    return int(util)

def calculate_util(itemset):
    totalutil = 0
    for key,val in transactions.items():
        if(key in findCoverset(itemset)):
            totalutil += calculate_Itemset_util_in_Trans(itemset,val)
    return int(totalutil) 

def total_iUtil(transaction):
    total_iUtil =0
    for item in transaction:
        total_iUtil += item[1] 
    return total_iUtil

# def init_iUtil():
#     for key, val in transactions.items():
#         for value in val:
#             if value[0] not in iUtil:
#                 items= [value[0]]
#                 sumIU = 0
#                 for trans in findCoverset(items):
#                     for item in transactions[trans]:
#                         if item[0] == value[0]:  
#                             sumIU+= item[1]
#                 iUtil[value[0]] = sumIU
#     return sorted(iUtil.items(), key=lambda x: x[0])
# def init_iCov():
#     for key, val in transactions.items():
#         for value in val:
#             if value[0] not in iCov:
#                 items= [value[0]]
#                 iCov[value[0]] = findCoverset(items)
#     return sorted(iCov.items(), key=lambda x: x[0])
def init_eUtil():
    for key, val in transactions.items():
        for value in val:
            if value[0] not in eUtil:
                eUtil[value[0]] = item_EU[value[0]]
    return sorted(eUtil.items(), key=lambda x: x[0])

def FindUniqueItems(cLine):
    for key,val in transactions.items():
        cLine+=1 
        for item in val :
            if item[0] not in iCov:
                iCov[item[0]] = [cLine]
                iUtil[item[0]] = [item[1]]
                iList.append(item[0])
            else:
                iCov[item[0]].append(cLine)
                iUtil[item[0]].append(item[1])

def FindLength1HUIs(minUtil):
    for item in iList:
        i_exUtil = eUtil[item]
        i_UtilList = iUtil[item]
        uI =0
        for util in i_UtilList:
            uI+= i_exUtil*util
        if (uI > minUtil) & (len(i_UtilList)/len(transactions) <1.0):
            HUIs[item] =uI

def normalizeList(list):
    unique_tuples = []
    for t in list: # Sắp xếp các phần tử trong tuple và chuyển đổi thành tuple mới 
        normalized_tuple = tuple(sorted(t)) # Thêm tuple đã chuẩn hóa vào tập hợp 
        if normalized_tuple not in unique_tuples:
            unique_tuples.append(normalized_tuple) # Chuyển đổi tập hợp trở lại danh sách 
    return(unique_tuples)

def MineRemHUIs(minUtil):
    i = 0
    while len(iList) >1 :
        tempList =[]
        for item1 in iList:
            print(" ")
            for item2 in iList:
                ## apriori herer
                if (item1 != item2) and (tuple(sorted((item1, item2))) not in HUIs):
                    cov1 = iCov[item1]
                    cov2 = iCov[item2]
                    S = (item1,item2)
                    print("S =" + str(S))
                    cov_S = list(set(cov2).intersection(set(cov1)))
                    print("cov_S =" + str(cov_S))
                    if (len(cov_S) > 0) and ( (len(cov_S)/len(transactions) ) >  (len(cov1)/len(transactions)) * (len(cov2)/len(transactions)) ):
                        print (str(S) + " ok")
                        iCov[S] = cov_S 
                        tempList.append(S)
                        if calculate_util(S) >= minUtil:
                            HUIs[S] = calculate_util(S)
                    else: print(str(item1) + " " + str(item2) + " no")
        if i==2:
            break
        else : i+=1
        tempList= (normalizeList(tempList))
        iList.clear()
        iList.extend(tempList)
iCov = {}
eUtil = {}
iUtil = {}
iList = []
HUIs= {}
corHUI = {}

def main():
 
    eUtil = init_eUtil()
    cLine = 0
    FindUniqueItems(cLine)

    # print("iCov")
    # for key,val in iCov.items():
    #     print(key,val)
    # print("________________")

    # print("iUtil")
    # for key,val in iUtil.items():
    #     print(key,val)
    # print("________________")
    # for item in iList:
    #     print(item, end = " ")
    
    FindLength1HUIs(0.5)

    # iCov[("c","ts")] = [1,2,3]
    # print(iCov)
    # print(calculate_util(["e","t","ts"]))
    MineRemHUIs(0.5)
    
    print("HUIs")
    for key,val in HUIs.items():
        print(key,val)
    print("________________")







if __name__ == "__main__":
    main()
