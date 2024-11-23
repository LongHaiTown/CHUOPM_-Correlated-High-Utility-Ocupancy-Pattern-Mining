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

def read_data(file_path): 
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for idx, line in enumerate(lines):
            # Parse each line
            tid = f"T{idx + 1}"  # Transaction ID
            items = line.strip().split()  # Split into item:value pairs
            item_pairs = [
                (int(pair.split(':')[0]), int(pair.split(':')[1])) for pair in items
            ]
            transactions[tid] = item_pairs

def parse_utility(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    item_id, utility = line.strip().split(", ")
                    item_name = int(item_id.strip())  # Prefix item names
                    item_EU[item_name] = int(utility.strip())  # Convert utility to integer
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error: {e}")

UL = {}
I = {}
iCov ={}
iUtil ={}

def FindUniqueItems(cLine):
    for key,val in transactions.items():
        cLine+=1 
        for item in val :
            if item[0] not in iCov:
                iCov[item[0]] = [cLine]
                iUtil[item[0]] = [item[1]]
            else:
                iCov[item[0]].append(cLine)
                iUtil[item[0]].append(item[1])

def total_iUtil(transaction):
    total_iUtil =0
    for item in transaction:
        total_iUtil += item[1] 
    return total_iUtil


# def calculate_Item_Util_in_Trans(item,trans):
#     util = 0
#     for ite in trans:
#         if (ite[0] == item):
#             util = ite[1]*item_EU[item]
#     return int(util)

# def calculate_Itemset_util_in_Trans(itemset,transaction):
#     util = 0
#     for ite in transaction:
#         for i in itemset:
#             if (ite[0] == i):
#                 util += calculate_Item_Util_in_Trans(ite[0],transaction) 
#     return int(util)


def calculate_Item_util_in_Trans(itemset,transaction):
    return iUtil[itemset][iCov[itemset].index(transaction)] * item_EU[itemset]

def calculate_util(item):
    i_UtilList = iUtil[item]
    uI =0
    for util in i_UtilList:
        # print(str(item_EU[item])+ " + "+ str(util) + " = " + str(item_EU[item]*util))
        uI+= item_EU[item]*util
    return int(uI) 

def total_Util(transaction):
    total_Util =0
    for item in transaction:
        total_Util += item[1] * item_EU[item[0]]
    return total_Util

# def calculate_uo_in_Trans(itemset,trans):
#     total_Occ = 0
#     for item in itemset:
#         for ite in trans:
#             if (ite[0] == item):
#                 total_Occ+= calculate_Item_Util_in_Trans(ite[0],trans) / total_Util(trans)
#     return total_Occ    

def calculate_Uo(item):
    uO = 0
    if isinstance(item, tuple): 
        for sub_item in item: 
            i_UtilList = UL[sub_item]['UtX']
            i_Cover = iCov[sub_item] 
            for i, util in enumerate(i_UtilList): 
                uO += util / total_Util(transactions["T" + str(i_Cover[i])]) 
            uO /= sum(len(iCov[sub_item]) for sub_item in item) 
    else: 
        i_UtilList = iUtil[item] 
        i_Cover = iCov[item] 
        for i, util in enumerate(i_UtilList): 
            uO += util / total_Util(transactions["T" + str(i_Cover[i])]) 
        uO /= len(iCov[item]) 
    return uO

def calculate_TWU(itemset):
    TWU = 0
    for trans in iCov[itemset]:
        TWU += total_Util(transactions["T"+str(trans)])
    return TWU

def Init_UL():
    global UL
    for key, val in transactions.items():
        for value in val:
            if value[0] not in UL:
                UL[value[0]] = {
                "transactions_Id" : iCov[value[0]],
                "UtX": [],
                "UtE": None,
                }
                
    for key,val in UL.items():
        for trans in val['transactions_Id']:
            UL[key]['UtX'].append(calculate_Item_util_in_Trans(key,trans))      
    return UL

def init_I():
    global I
    for key, val in transactions.items():
        for value in val:
            if value[0] not in I:
                I[value[0]] = calculate_TWU(value[0])
    return sorted(I.items(), key=lambda x: x[1])


def get_extension_set(itemset, total_order):
    if isinstance(itemset, tuple): # Lấy phần tử cuối cùng từ tuple 
        item = itemset[-1] 
    else:
        item = itemset # Nếu không phải là tuple, lấy trực tiếp itemset item = itemset 
    last_item_index = total_order.index(item) 
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
                # print(str(item[0]), end =" ")
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

def Prune(P,exP,minOcc,minSUP,Ix):
    for Px in exP:
        if((calculate_Uo(Px) > minOcc) & (len(UL[Px]['transactions_Id']) > int(len(transactions))*minSUP)):
            ResultSet.append(Px)
            print("_")
            print(Px)
        maxOcc = calculateUpperBound(Px,minSUP)
        if((maxOcc >= minOcc) & (len(UL[Px]['transactions_Id']) > int(len(transactions))*minSUP) ):
            exPx = []
            for item in get_extension_set(Px,Ix):
                Pxy  = (Px,item)
                UL[Pxy]= merge_utility_lists(UL[Px],UL[item])
                iCov[Pxy] = list(set(iCov[Px]).intersection(set(iCov[Px])))
                exPx.append(Pxy)
                print(str(Pxy))
            Prune([],exPx,minOcc,minSUP,Ix)

ResultSet = []   

def update_globals(): 
    global I

def main():

    item_EU.clear()
    transactions.clear()

    read_data(r'D:\CODING\PYTHON_DA\CHUIM+HUOPM\data\chess_UM_New.txt')
    parse_utility(r'D:\CODING\PYTHON_DA\CHUIM+HUOPM\data\chess_UM_UtilityTable.txt')

    FindUniqueItems(0)

    # for key,val in transactions.items():
    #     print(key,val)
    # print(calculate_util(53))

    # print(iCov[53])
    # print(iUtil[53])

    I = init_I()
    UL = Init_UL()

    # # print(I)

    I = [item[0] for item in I]

    print(I)

    for item in UL:
        UL[item]['UtE'] =(calculate_ute(item,I))

    Prune([],I,0.1,0.2,I)
    
    # for key,val in UL.items():
    #     print(key + " " + str(val))
    # # print(calculateUpperBound("GAC", 0.2))
    # # print(int(len(transactions)*0.1))

    # print(UL["B"])
    # print(UL["A"])
    # print(merge_utility_lists(UL["B"],UL["A"]))
    # print(UL["G"])
    # print(merge_utility_lists(merge_utility_lists(UL["B"],UL["A"]),UL["G"]))
    
    # for item in ResultSet:
    #     print(item)
    # print(calculateUpperBound("G",0.25))



if __name__ == "__main__":
    main()