transactions = {
    "T1": [("A", 2), ("B", 3), ("C", 1)],
    "T2": [("D", 2), ("F", 2)],
    "T3": [("B", 4), ("G", 2)],
    "T4": [("A", 3), ("C", 4), ("E", 2), ("F", 1)],
    "T5": [("B", 2), ("D", 1), ("E", 1)],
    "T6": [("B", 4), ("C", 1), ("D", 1)],
    "T7": [("F", 1), ("G", 2)],
    "T8": [("A", 3), ("B", 1), ("C", 5)],
    "T9": [("F", 1), ("G", 4)],
    "T10": [("B", 2), ("C", 5), ("D", 2)]
}


item_EU = {
    "A": 3,
    "B": 2,
    "C": 1,
    "D": 6,
    "E": 2,
    "F": 4,
    "G": 3
}

def show_all_item():
    for key,value in transactions.items():
        print(key,value)

def show_all_TU():
    for trans in transactions.items():
        # for transaction in trans[1]:
        print(trans[0], end=" ")
        print(calculate_Total_Util(trans[1]))

def calculate_Total_Util(transaction):
    TU = 0
    for item in transaction:
        TU+= item[1] * item_EU[item[0]]
    return int(TU)

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

def calculate_sup(itemset):
    sup = 0
    for key,val in transactions.items():
        if key in findCoverset(itemset):
            sup+=1
    return sup

def calculate_util(itemset):
    totalutil = 0
    for key,val in transactions.items():
        if(key in findCoverset(itemset)):
            totalutil += calculate_Itemset_util_in_Trans(itemset,val)
    return int(totalutil)

def calculate_Occ(itemset):
    Uo = 0
    for key,val in transactions.items():
        if(key in findCoverset(itemset)):
            Uo+= calculate_Itemset_util_in_Trans(itemset,val)/calculate_Total_Util(val)
    return Uo/calculate_sup(itemset)

def Testing(testingSet):
    coverset = findCoverset(testingSet)
    print("Coverset: ", coverset)

    print("Support: ",  calculate_sup(testingSet))

    print("Utility: ",calculate_util(testingSet))

    print("Occupancy: ",calculate_Occ(testingSet))

def init_I():
    I = dict()
    for key, val in transactions.items():
        for value in val:
            I[value[0]] = calculate_sup(value[0])
    return I
    
def init_RevisedI(minutilThreshold):
    I = init_I()
    todelete = []
    for key,val in I.items():
        if I[key] < minutilThreshold:
            todelete.append(key)
    for key in todelete:
        del I[key]
    RevisedI = dict(sorted(I.items(), key=lambda item: item[1],reverse= False))
    return RevisedI

def init_RevisedI_alphabetical(minutilThreshold):
    I = init_I()
    todelete = []
    for key,val in I.items():
        if I[key] < minutilThreshold:
            todelete.append(key)
    for key in todelete:
        del I[key]
    RevisedI = dict(sorted(I.items()))
    return RevisedI

def calcuate_RUO_trans(itemset,transaction):
    ruo = 0
    index = 0
    i =0
    for key,val in transaction:
        if key == itemset[-1]:
            index = i
        i+=1
    i =0
    for key,val in transaction:
        if (i > index):            
            ruo += calculate_Item_util_in_Trans(key,transaction)/calculate_Total_Util(transaction)
        i+=1

    return ruo

def calculate_RUO(itemset):
    ruo = 0
    for trans in findCoverset(itemset):
        ruo += calcuate_RUO_trans(itemset,transactions[trans])   

    return ruo/len(findCoverset(itemset))

def calculate_ubuo(itemset,minSup):
    vec = []
    for trans in findCoverset(itemset):
        vec.append(calcuate_RUO_trans(itemset,transactions[trans])+calculate_Itemset_util_in_Trans(itemset,transactions[trans])/calculate_Total_Util(transactions[trans]))
    vec = sorted(vec,reverse= True)
    ubuo = 0 
    for number in range(0,int(minSup)):
        ubuo+= vec[number]
    return ubuo/minSup


def construct_GUO(I):
    GUO = {}
    i =0
    # print(I)
    for key,val in transactions.items():
        filtered_val = [x for x in val if x[0] in I] # bỏ qua giá trị không có trong I     
        revised_T = sorted(filtered_val, key=lambda x: (I[x[0]], x[0]),reverse=True) # sắp xếp transaction theo I & đảo ngược
        revised_T_1 = sorted(filtered_val, key=lambda x: (I[x[0]], x[0]),reverse=False) # sắp xếp transaction theo I
        ruo = 0
        N_Item = None
        N_Idx = None
        # print(str(key) + " " + str(revised_T_1))
        # Duyệt qua từng item i trong tập I và trong T'
        for item in revised_T:
            if item[0] not in I:
                continue
            # # Nếu item không tồn tại trong GUO, tạo mới
            if item[0] not in GUO:
                GUO[item[0]] = {
                    "sumUO": 0,
                    "sumRUO": 0,
                    "entries": []  # Danh sách các entry
                }
            #  Tính toán các giá trị tiện ích
            uo =calculate_Item_util_in_Trans(item[0],transactions[key])/calculate_Total_Util(transactions[key])  # Lấy tiện ích từ bảng EU
            ruo = calcuate_RUO_trans(item[0],revised_T_1)

            e = {"N_Item": N_Item, "uo": uo, "ruo": ruo, "N_Idx": N_Idx}
            GUO[item[0]]["entries"].append(e)

            # Cập nhật ruo và các giá trị khác

            N_Item = item[0]
            N_Idx = len(GUO[item[0]]["entries"])

            # # Cập nhật sumUO và sumRUO của item trong GUO
            GUO[item[0]]["sumUO"] += uo
            GUO[item[0]]["sumRUO"] += ruo
            # print("----" + item[0])
            # print(GUO[item[0]]["entries"])  
            # print("----------")
            # print(GUO[item[0]])
        i+= 1
        if(i == 10):
            return GUO
    return GUO

def calculate_lubuo(itemset,minsup):
    lubuo = 0 
    for trans in findCoverset(itemset):
        # print(calculate_Itemset_util_in_Trans(itemset,transactions[trans])/calculate_Total_Util(transactions[trans]) , end = " ")
        # print(str(calcuate_RUO_trans(itemset,transactions[trans])) + "= " +str((calculate_Itemset_util_in_Trans(itemset,transactions[trans])/calculate_Total_Util(transactions[trans]))+calcuate_RUO_trans(itemset,transactions[trans])))
        lubuo = calculate_Itemset_util_in_Trans(itemset,transactions[trans])/calculate_Total_Util(transactions[trans])+calcuate_RUO_trans(itemset,transactions[trans])
    return lubuo / minsup

def Mine(prefix,CUOILs,minOcc,minSUP):
    for key,val in CUOILs.items():
        print(key ,end=" ")
    print("all above is checking")
    I = init_RevisedI(3)
    ResultSet = []
    CUO_k_ = {}
    CUOILs = {key: CUOILs[key] for key in I if key in CUOILs}

    for key,val in CUOILs.items():
        if(key in prefix):
            continue
        print("- "+key + " is checking", end= " ")
        if (CUOILs[key]["sumUO"] / calculate_sup(key) >= minOcc) & (key != prefix):
            ResultSet.append(prefix + [key])
        if (calculate_lubuo(key,minSUP) < minOcc): # first casting
            print( key + " is eliminated")          
        else: 
            print(key + " pass 1", end = " ")
            ubuo = calculate_ubuo(key,minSUP)
            if ubuo < minOcc:
                print("but "+key + " is eliminated because ubuo")
            else:
                print(key + " pass 2",end= " ")
                new_prefix = prefix + [key]
                print("new_prefix is " + str(new_prefix))
                for entry in CUOILs[key]["entries"]:
                    print(entry["N_Item"])
                    base_list = []
                    base_entry = {
                        "prefix": new_prefix,
                        "N_Idx": entry["N_Idx"],
                        "uo": entry["uo"]
                    }
                    base_list.append(base_entry)
                    print(base_list)
                    if entry["N_Item"] in CUOILs:
                        for ce in CUOILs[entry["N_Item"]]["entries"]:
                            if ce["N_Idx"] is not None and base_entry["N_Idx"] is not None:
                                if ce["N_Idx"] == base_entry["N_Idx"]:
                                    print("Legal ", end=" ")
                                    print(ce)
                                    
                                    if ce["N_Item"] not in CUO_k_:
                                        CUO_k_[ce["N_Item"]] = {
                                        "sumUO": 0,
                                        "sumRUO": 0,
                                        "entries": []
                                    }
                                    new_entry = {
                                        "N_Item": ce["N_Item"],
                                        "uo": entry["uo"] + calculate_util(ce["N_Item"])/calculate_sup(ce["N_Item"]) - base_list[0]["uo"],
                                        "ruo": ce["ruo"],
                                        "N_Idx": ce["N_Idx"]
                                    }
                                    CUO_k_[ce["N_Item"]]["entries"].append(new_entry)
                                    CUO_k_[ce["N_Item"]]["sumUO"] += new_entry["uo"]
                                    CUO_k_[ce["N_Item"]]["sumRUO"] += new_entry["ruo"]
                                    print()
                                    print( ce["N_Item"] + " is put into CUO_K")
                    if CUO_k_:
                        ResultSet.append(Mine(prefix, CUO_k_, minSUP, minOcc))
        print("____")

    return ResultSet

def create_base_list(prefix, CUO):
    """
    Create a Base-list for a given prefix based on entries in CUO.
    """
    base_list = []
    for entry in CUO["entries"]:
        base_entry = {
            "prefix": prefix,
            "N_Idx": entry["N_Idx"],
            "uo": entry["uo"]
        }
        base_list.append(base_entry)
    return base_list
def update_CUO_IL_next(CUO_IL_next, base_entry, CUO):
    """
    Update CUO-IL_next structure based on the base entry and existing CUO entries.
    """
    for e in CUO["entries"]:
        if e["N_Idx"] is not None and base_entry["N_Idx"] is not None:
            if e["N_Idx"] == base_entry["N_Idx"]:
                if e["N_Item"] not in CUO_IL_next:
                    CUO_IL_next[e["N_Item"]] = {
                    "sumUO": 0,
                    "sumRUO": 0,
                    "entries": []
                }
                new_entry = {
                    "N_Item": e["N_Item"],
                    "uo": e["uo"] - base_entry["uo"],
                    "ruo": e["ruo"],
                    "N_Idx": e["N_Idx"]
                }
                CUO_IL_next[e["N_Item"]]["entries"].append(new_entry)
                CUO_IL_next[e["N_Item"]]["sumUO"] += new_entry["uo"]
                CUO_IL_next[e["N_Item"]]["sumRUO"] += new_entry["ruo"]
    return 1
def main():
    all = list(transactions.values())
    # Testing(['A','B'])
    
    # print(all[9])
    # print(calcuate_RUO_trans(["B","C","D"],all[9]))
    # print(calculate_RUO(["B"]))
    # print((calculate_ubuo(["A","B"])[0] + calculate_ubuo(["A","B"])[1] + calculate_ubuo(["A","B"])[2])/3)
    # print(calculate_ubuo(["B","C"]))

    # print(init_RevisedI(3))
    GUO_ILS = construct_GUO(init_RevisedI(3))
    # print(construct_GUO(init_RevisedI(3)))
    # for item in construct_GUO(init_RevisedI(3)).items():
    #     print(item)
    print("Mine")
    # print(Mine([],GUO_ILS,0.3,3))
    for itemset in Mine([],GUO_ILS,0.3,3):
        print(itemset)



if __name__ == "__main__":
    main()