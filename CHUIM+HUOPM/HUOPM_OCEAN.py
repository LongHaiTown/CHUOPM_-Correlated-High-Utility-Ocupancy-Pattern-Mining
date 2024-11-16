item_EU = {
    'A': 1,
    'B': 1,
    'C': 4,
    'D': 5,
    'E': 2,
    'F': 3,
    'G': 3
}

# Bảng giao dịch (Transaction table)
transactions = {
    "T1": [('A', 1), ('B', 1), ('C', 1), ('E', 1)],
    "T2": [('A', 9), ('C', 3), ('D', 2), ('E', 1),('F', 1), ('G', 2)],
    "T3": [('D', 1), ('G', 1)],
    "T4": [('A', 1),('B', 1),('E', 1)],
    "T5": [('B', 8), ('C', 2), ('D', 2), ('F', 1), ('G', 1)],
    "T6": [('A', 1),('B', 2), ('C', 1)],
    "T7": [('E', 3),('F', 3),('G', 1)],
    "T8": [('C', 1),('F', 3)],

}

UL = {}
I = {}

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


def calculate_Item_Util_in_Trans(item,trans):
    util = 0
    for ite in trans:
        if (ite[0] == item):
            util = ite[1]*item_EU[item]
    return int(util)

def calculate_Itemset_util_in_Trans(itemset,transaction):
    util = 0
    for ite in transaction:
        for i in itemset:
            if (ite[0] == i):
                util += calculate_Item_Util_in_Trans(ite[0],transaction) 
    return int(util)

def calculate_util(itemset):
    totalutil = 0
    for key,val in transactions.items():
        if(key in findCoverset(itemset)):
            totalutil += calculate_Itemset_util_in_Trans(itemset,val)
    return int(totalutil) 

def total_Util(transaction):
    total_Util =0
    for item in transaction:
        total_Util += item[1] * item_EU[item[0]]
    return total_Util

def calculate_uo_in_Trans(itemset,trans):
    total_Occ = 0
    for item in itemset:
        for ite in trans:
            if (ite[0] == item):
                total_Occ+= calculate_Item_Util_in_Trans(ite[0],trans) / total_Util(trans)
    return total_Occ    

def calculate_Uo(itemset):
    if(len(findCoverset(itemset))!= 0):
        total_Occ=0
        for trans in findCoverset(itemset):
            total_Occ += calculate_uo_in_Trans(itemset,transactions[trans])
        return total_Occ/len(findCoverset(itemset))
    return 0

def calculate_TWU(itemset):
    TWU = 0
    for trans in findCoverset(itemset):
        TWU += total_Util(transactions[trans])
    return TWU

def Init_UL():
    global UL
    for key, val in transactions.items():
        for value in val:
            if value[0] not in UL:
                UL[value[0]] = {
                "transactions_Id" : [],
                "UtX": [],
                "UtE": None,
            }
    for key,val in UL.items():
        for trans in findCoverset(key):
            UL[key]["transactions_Id"].append(int(trans[1:]))
            UL[key]["UtX"].append(calculate_Itemset_util_in_Trans(key,transactions[trans]))
            
    return UL

def init_I():
    global I
    for key, val in transactions.items():
        for value in val:
            if value[0] not in I:
                I[value[0]] = calculate_TWU(value[0])    
    return sorted(I.items(), key=lambda x: x[1])

def get_extension_set(itemset, total_order): 
    last_item_index = total_order.index(itemset[-1]) 
    extension_set = total_order[last_item_index + 1:] 
    return extension_set

def calculate_ute(itemset ,total_order):
    extension_set = get_extension_set(itemset, total_order)
    UtE = []
    for trans in UL[itemset]["transactions_Id"]:
        sum =0
        for item in transactions["T"+str(trans)]:
            if(item[0] in extension_set):
                sum += item[1]*item_EU[item[0]]
                # print(str(item), end =" ")
        # print("= "+str(sum))
        UtE.append(sum)

    return UtE

def merge_utility_lists(UL_PX, UL_y):
    merged_UL = {'transactions_Id': [], 'UtX': [], 'UtE': []}
    merged_UL['transactions_Id'] = []
    for trans in UL_y["transactions_Id"]:
        if trans in UL_PX["transactions_Id"]:
            merged_UL['transactions_Id'].append(trans)
            merged_UL['UtX'].append(UL_PX["UtX"][UL_PX["transactions_Id"].index(trans)] + UL_y["UtX"][UL_y["transactions_Id"].index(trans)]) 
            merged_UL['UtE'].append(UL_y["UtX"][UL_y["transactions_Id"].index(trans)])  

    # print(merged_UL['transactions_Id'])
    # print(merged_UL['UtX'])
    # print(merged_UL['UtE'])
    return merged_UL


def calculateUpperBound(Px, minSUP):
    V = []
    i =0
    for trans in UL[Px]["transactions_Id"]:
        if len(UL[Px]["UtE"]) ==0 :
            UtEvalue = 0
        else: 
            UtEvalue = UL[Px]["UtE"][i]
        V.append((UL[Px]["UtX"][i] + UtEvalue)/total_Util(transactions[str("T"+str(trans))]) )
        i+=1

    V = sorted(V,reverse=True)
    V_top = []
    if(len(V) > int(minSUP*len(transactions))):
        for num in range(0,int(minSUP*len(transactions))):
            V_top.append(V[num])
        sum_top = sum(V_top)
        occu = sum_top / int(len(transactions)*minSUP)  
        return occu
    return 0

def Prune(P,exP,minOcc,minSUP):
    for Px in exP:
        if((calculate_Uo(Px) > minOcc) & (len(UL[Px]['transactions_Id']) > int(len(transactions))*minSUP)):
            ResultSet.append(Px)
        maxOcc = calculateUpperBound(Px,minSUP)
        if((maxOcc >= minOcc) & (len(UL[Px]['transactions_Id']) > int(len(transactions))*minSUP) ):
            exPx = []
            for item in get_extension_set(Px,I):
                Pxy  = Px + item
                UL[Pxy]= merge_utility_lists(UL[Px],UL[item])
                exPx.append(Pxy)
                # print(str(Pxy)+" "+str(UL[Pxy]))
            Prune([],exPx,minOcc,minSUP)

ResultSet = []                   
def main():
    global UL, I , ResultSet
    I = init_I()
    UL = Init_UL()


    I = [item[0] for item in I ]
    UL = {key: UL[key] for key in I}

    print(I)

    for item in UL:
        UL[item]['UtE'] =(calculate_ute(item,I))
        print(item+" "+ str(UL[item]))
    
    Prune([],I,0.1,0.2)
    for key,val in UL.items():
        print(key + " " + str(val))
    # print(calculateUpperBound("GAC", 0.2))
    # print(int(len(transactions)*0.1))

    print(UL["B"])
    print(UL["A"])
    print(merge_utility_lists(UL["B"],UL["A"]))
    print(UL["G"])
    print(merge_utility_lists(merge_utility_lists(UL["B"],UL["A"]),UL["G"]))
    
    for item in ResultSet:
        print(item)
    # print(calculateUpperBound("G",0.25))



if __name__ == "__main__":
    main()