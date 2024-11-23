
transactions = {
    "T1": [('a', 1), ('b', 5), ('c', 1), ('d', 3), ('e', 1), ('f', 5)],
    "T2": [('b', 4), ('c', 3), ('d', 3), ('e', 1)],
    "T3": [('a', 1), ('c', 1), ('d', 1)],
    "T4": [('a', 2), ('c', 6), ('e', 2), ('g', 5)],
    "T5": [('b', 2), ('c', 2), ('e', 1), ('g', 2)],
}

# Giá trị hữu ích bên ngoài (External utility values)
item_EU = {
    'a': 5,
    'b': 2,
    'c': 1,
    'd': 2,
    'e': 3,
    'f': 1,
    'g': 1,
}
# item_EU = {

# }
# transactions ={}
def read_data(file_path): 
    """
    Reads a file with item and value pairs, converting it into a transactional database.
    
    Args:
        file_path (str): The path to the input text file.
    
    Returns:
        dict: A transactional database with the format {"TID": [("item", value), ...]}.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for idx, line in enumerate(lines):
            # Parse each line
            tid = f"T{idx + 1}"  # Transaction ID
            items = line.strip().split()  # Split into item:value pairs
            item_pairs = [
                (f"{pair.split(':')[0]}", int(pair.split(':')[1])) for pair in items
            ]
            transactions[tid] = item_pairs

def parse_utility(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    item_id, utility = line.strip().split(", ")
                    item_name = f"{item_id.strip()}"  # Prefix item names
                    item_EU[item_name] = int(utility.strip())  # Convert utility to integer
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error: {e}")

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

def calculateSup(item1,transactions):
    sup = 0
    for key,val in transactions.items():
        for item in val:
            if item[0] == item1:
                sup+=1
    return sup

def calculateItemsetSup(itemset,transactions):
    sup= 0
    for key,val in transactions.items():
        count = 0
        for value in val:
            if value[0] in itemset :
                count +=1
        if count == len(itemset):
            sup+=1
    return sup



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
        if (uI >= minUtil) & (len(i_UtilList)/len(transactions) <1.0):
            HUIs[item] =uI

def normalizeList(list):
    unique_tuples = []
    for t in list: # Sắp xếp các phần tử trong tuple và chuyển đổi thành tuple mới 
        normalized_tuple = tuple(sorted(t)) # Thêm tuple đã chuẩn hóa vào tập hợp 
        if normalized_tuple not in unique_tuples:
            unique_tuples.append(normalized_tuple) # Chuyển đổi tập hợp trở lại danh sách 
    return(unique_tuples)

def MineRemHUIs(minUtil):
    while len(iList) >1 :
        tempList =[]
        for item1 in iList:
            print(" ")
            for item2 in I:
                if ((item1 != item2) & (item2 not in item1) ) :
                    cov1 = iCov[item1]
                    cov2 = iCov[item2]
                    if(len(item1) == 1):
                        S = (item1,item2)
                    else: 
                        S = item1 + tuple(item2)
                    S =  tuple(sorted(S))
                    cov_S = list(set(cov2).intersection(set(cov1)))
                    # print("cov_S =" + str(cov_S))
                    # print(S)
                    if (len(cov_S) > 0) and ( (len(cov_S)/len(transactions) ) >  (len(cov1)/len(transactions)) * (len(cov2)/len(transactions)) ):
                        print (str(S) + " ok")
                        iCov[S] = cov_S 
                        tempList.append(S)
                        if calculate_util(S) >= minUtil:
                            HUIs[S] = calculate_util(S)
                    else: print(str(item1) + " " + str(item2) + " no")
        iList.clear()
        iList.extend(tempList)

def getSubset(HUI):
    subset = []
    for hui in HUIs:
        lenght = 0
        for item in HUI:
            if item in hui:
               lenght+=1
            #    print(hui,end="--- ")
        if lenght == len(HUI) and hui!= HUI:
            subset.append(hui)
            # print(hui , end=" ")
            # print(iCov[hui],end=" ")
    return subset


def createEdom(HUI):
    edom = dict.copy(transactions)
    toremove = []
    for key,val in edom.items():
        check = 0
        for item in val:
            if item[0] in HUI:
                check+=1
        if (check == len(HUI)):
            toremove.append(key)
    for key in toremove:
        edom.pop(key)
    return edom

def isProductiveInEdom(HUI):
    subset = getSubset(HUI)
    if (subset == []):
        corHUI[HUI] = 1
    for set in subset:
        tempCov = iCov[HUI].copy()
        subtract = len(tempCov)
        toremove =[]
        print("------" + str(HUI))
        print(set)
        for trans in tempCov:
            if trans in iCov[set]:
                toremove.append(trans)
        print(tempCov)
        for trans in toremove: 
            tempCov.remove(trans)
        print(tempCov)
        if len(HUI) ==1:
            if(len(tempCov) == 0):
                print("not a Cor HUI! ")  
                return
            else :  corHUI[HUI] = 1
        else: 
            totalsup = 1
            i = 0
            for item in HUI:
                sup = (len(iCov[item])  -subtract)/ (len(transactions) - subtract )
                totalsup*= sup
                print(item+" "+str(sup) +" "+str(iCov[item] ))
                i += 1
            edomSup = len(tempCov)/(len(transactions))
            print(str(edomSup) + " vs " + str(totalsup))
            if edomSup> totalsup:
                corHUI[HUI] = 1
                print("Cor HUI : " + str(HUI))    
            else: print("not a Cor HUI!")  
 
def isProductiveInEdom1(HUI):
    subset = getSubset(HUI)
    if (subset == []):
        corHUI[HUI] = 1
    edom = dict.copy(transactions)
    toremove = []
    for set in subset:
        if set in HUIs:
            print(set)
            edom1 = createEdom(set)
            for key in edom: 
                if key not in edom1: 
                    if (key not in toremove):
                        toremove.append(key) 
    for trans in toremove:
        edom.pop(trans)
    totalsup = 1

    for item in HUI:
        if (len(edom) ==0 ):
            print("not a Cor HUI!")  
            continue
        else:
            print(item,end= " ")
            sup = calculateSup(item,edom) / len(edom)
            print(sup)
            totalsup*=sup
        print(totalsup)
        print(str(calculateItemsetSup(HUI,edom))+ "/ " +str(len(edom)))
        if ((calculateItemsetSup(HUI,edom)/len(edom))>= totalsup) & (totalsup!=0):
            corHUI[HUI] = 1
            print("Cor HUI : " + str(HUI))    
        else: print("not a Cor HUI!")  
               
  
iCov = {}
eUtil = {}
iUtil = {}
iList = []
HUIs= {}
corHUI = {}
I= []

def init_I():
    for key, val in transactions.items():
        for value in val:
            if value[0] not in I:
                I.append(value[0])


def main():
    item_EU.clear()
    transactions.clear()

    read_data('D:\CODING\PYTHON_DA\CHUIM+HUOPM\data\chess_UM_New.txt')
    parse_utility('D:\CODING\PYTHON_DA\CHUIM+HUOPM\data\chess_UM_UtilityTable.txt')

    for key,val in item_EU.items():
        print(key,val)
    init_I()

    eUtil = init_eUtil()
    cLine = 0
    FindUniqueItems(cLine)

    FindLength1HUIs(15)

    # MineRemHUIs(15)
    
    # print("HUIs")
    
    for key,val in HUIs.items():
        print("-")
        print(key,val )
        # isProductiveInEdom1(key)

    # print("________________")
    # for key,val in HUIs.items():
    #     print(key,val)
    # print("________________")

    # for key,val in corHUI.items():
    #     print(key,end = " ")
    print("")
    print(len(HUIs))


    # # print("------")
    # # for key,val in transactions.items():
    # #     print(key, val)

    
if __name__ == "__main__":
    main()

# sup(e) = 4/11
# sup(f) = 3/11