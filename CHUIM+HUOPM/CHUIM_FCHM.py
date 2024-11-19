import itertools

# Bảng giao dịch 
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
UL = {}
# Nhập các giá trị cần thiết
def get_user_inputs():
    global minUtil
    global minMeasure
    minUtil = float(input("Nhập giá trị minUtil: "))
    minMeasure = float(input("Nhập giá trị minMeasure: "))
    return minUtil, minMeasure

# Tìm các transactions có chứa itemset
def findCoverset(itemset):
    coverset = []
    for key, val in transactions.items():
        count = 0
        for value in val:
            if value[0] in itemset:
                count += 1
        if count == len(itemset):
            coverset.append(key)
    return coverset
# Tính utility của một item trong một giao dịch
def calculate_Item_utility_in_Trans(item, trans):
    util = 0
    for ite in trans:
        if(ite[0] == item):
            util = ite[1]*item_EU[item]
    return int(util)

# Tính utility của một itemset trong một giao dịch
def calculate_Itemset_utility_in_Trans(itemset, trans):
    util = 0
    for ite in trans:
        for i in itemset:
            if(ite[0] == i):
                util += calculate_Item_utility_in_Trans(ite[0], trans)
    return int(util)

# Tính utility của một item trong database
def calculate_Item_utility_in_database(item):
    util = 0
    for trans in transactions:
        util += calculate_Item_utility_in_Trans(item, trans)
    return int(util)

#Tính utility của một itemset trong database
def calculate_Itemset_utility_in_database(itemset):
    util = 0
    for key, val in transactions.item():
        if(key in findCoverset(itemset)):
            util += calculate_Itemset_utility_in_Trans(itemset, val)
    return int(util)

# Tính utility của một giao dịch
def calculate_Trans_utility(trans):
    util = 0
    for item in trans:
        util += calculate_Item_utility_in_Trans(item[0], trans)
    return int(util)

# Tính TWU của một itemset trong database
def calculate_Item_TWU(itemset):
    TWU = 0
    coverset = findCoverset(itemset)
    for trans in coverset:
        TWU += calculate_Trans_utility(transactions[trans])
    return TWU

# Xây dựng mô hình EUCS
def build_eucs(transactions, item_EU):
    items = sorted(item_EU.keys())
    eucs = {item1: {item2: 0 for item2 in items if item2 != item1} for item1 in items}
    for item1 in items:
        for item2 in items:
            if item1 != item2:
                itemset = [item1, item2]
                util = calculate_Item_TWU(itemset)
                eucs[item1][item2] += util
    return eucs
# Hiển thị mô hình EUCS
def print_eucs(eucs):
    items = sorted(eucs.keys())
    # In tiêu đề cột, bao gồm 'a'
    print("    ", "   ".join(item.rjust(1) for item in items))
    for i in range(1, len(items)):
        item1 = items[i]
        row = []
        for j in range(len(items) - 1):
            item2 = items[j]
            if j >= i:
                row.append('-'.rjust(3))  # Đặt "-" cho các mục phía trên và trên đường chéo chính
            else:
                row.append(str(eucs[item1].get(item2, 0)).rjust(3))  # Giá trị thực tế
        print(item1.rjust(3), " ".join(row))

# Xây dựng utility-List
def calculate_remaining_utility(itemset, trans, total_order):
    remaining_util = 0
    max_item = max(itemset, key=lambda x:total_order.index(x))
    for ite in trans:
        if total_order.index(ite[0]) > total_order.index(max_item):
            remaining_util += calculate_Item_utility_in_Trans(ite[0], trans)
    return remaining_util

# Tạo utility-list từ một itemset
def create_utility_list(itemset, total_order):
    utility_list = []
    coverset = findCoverset(itemset)
    for trans_id in coverset:
        trans = transactions[trans_id]
        iutil = calculate_Itemset_utility_in_Trans(itemset, trans)
        rutil = calculate_remaining_utility(itemset, trans, total_order)
        utility_list.append((trans_id, iutil, rutil))
    return utility_list

# Cắt tỉa các item có ul.util < minUtil bằng utility-list
def prune_items_from_UL(minUtil):
    pruned_UL = {}
    for itemset, ul in UL.items():
        total_util = sum(iutil for _, iutil, _ in ul)
        if total_util >= minUtil:
            pruned_UL[itemset] = ul
    return pruned_UL

# Thêm utility-list vào UL
def add_utility_list_to_UL(itemset, total_order):
    ul = create_utility_list(itemset, total_order)
    UL[tuple(itemset)] = ul

# Thêm ul của các item
def add_Item_ul(total_order):
    for item in item_EU.keys():
        add_utility_list_to_UL([item], total_order)

# Lấy item mở rộng của itemset hiện tại
def get_extension_set(itemset, total_order):
    last_item_index = total_order.index(itemset[-1]) 
    extension_set = total_order[last_item_index + 1:] 
    return extension_set

#Tìm tập mở rộng 
def find_Extension(pruned_UL):
    extension_set = list(pruned_UL.keys())
    return extension_set

# Kết hợp item với tập mở rộng của chúng
def connect_Item_with_extension(pruned_UL, total_order):
    extension_set = find_Extension(pruned_UL)
    new_combinations = []
    for item in extension_set:
        ext_set = get_extension_set([item], total_order)
        for ext_item in ext_set:
            new_combination = tuple(sorted([item, ext_item]))
            if new_combination not in new_combinations:
                new_combinations.append(new_combination)
    return new_combinations

# Tạo tổ hợp các item từ danh sách các item đã được cắt tỉa
def generate_combinations(pruned_items):
    combinations = []
    for r in range(2, len(pruned_items) + 1):
        combinations.extend(itertools.combinations(pruned_items, r))
    return combinations

# Tính utility-list cho các itemset vừa kết hợp
def add_combinations_to_UL(combinations, total_order):
    for comb in combinations:
        utility_list = create_utility_list(comb, total_order)
        UL[comb] = utility_list


# Hàm kiểm tra các itemset đó có thỏa >= minUtil không
def filter_combinations_by_util(minUtil):
    filtered_combinations = {}
    for comb, ul in UL.items():
        total_util = sum(iutil for _, iutil, _ in ul)
        if total_util >= minUtil:
            filtered_combinations[comb] = ul
    return filtered_combinations

# def calculate_all_confidence(itemset, transactions):
#     min_support = min([transactions.count(item) for item in itemset])
#     all_confidence = transactions.count(itemset) / min_support
#     return all_confidence

# def calculate_bond(itemset, transactions):
#     support_itemset = transactions.count(itemset)
#     total_support = sum([transactions.count(item) for item in itemset])
#     bond = support_itemset / total_support
#     return bond

#def main():
    # # Xác định ngưỡng utility tối thiểu
    # MIN_UTILITY = 5

    # high_utility_itemsets = []

    # for itemset in itertools.chain.from_iterable(itertools.combinations(external_utility.keys(), r) for r in range(1, len(external_utility)+1)):
    #     utility = calculate_utility(itemset, transactions)
    #     if utility >= MIN_UTILITY:
    #         high_utility_itemsets.append(itemset)

    # correlated_itemsets = []

    # THRESHOLD = 0.5  # Điều chỉnh ngưỡng theo yêu cầu

    # for itemset in high_utility_itemsets:
    #     all_confidence = calculate_all_confidence(itemset, transactions)
    #     bond = calculate_bond(itemset, transactions)
        
    #     if all_confidence > THRESHOLD and bond > THRESHOLD:
    #         correlated_itemsets.append(itemset)


    # transactions_Utility = []
    # for tran in transactions :
        #transactions_Utility.append(calculate_utility(tran))


    # for ulti in transactions_Utility:
        # print( "Trasaction ulti của ni là "+ str(ulti)); 

#if __name__ == "__main__":
    #main()
# Tạo tổ hợp các item từ danh sách các item đã được cắt tỉa
def main():
    get_user_inputs()
    total_order = sorted(item_EU.keys())
    
    # Bước 1: Thêm utility-list của các item ban đầu vào UL
    add_Item_ul(total_order)
    
    # Bước 2: Cắt tỉa các item có utility nhỏ hơn minUtil
    pruned_UL = prune_items_from_UL(minUtil)
    print("Pruned Utility List:", pruned_UL)
    
    # Bước 3: Tạo các tổ hợp các item từ danh sách các item đã cắt tỉa
    pruned_items = [item[0] for item in pruned_UL.keys()]  # Extracting single items from tuples
    print("Pruned Items:", pruned_items)
    combinations = generate_combinations(pruned_items)
    print("Generated Combinations:", combinations)
    
    # Bước 4: Thêm các tổ hợp vào UL và in ra utility list của từng tổ hợp
    add_combinations_to_UL(combinations, total_order)
    
    for comb in combinations:
        print(f"Utility List for {comb}: {UL.get(comb)}")

    # Bước 5: Lọc các tổ hợp có utility lớn hơn minUtil
    filtered_combinations = filter_combinations_by_util(minUtil)
    print("Filtered Combinations by Utility:", filtered_combinations)
    
    # Hiển thị các tổ hợp có utility lớn hơn minUtil
    for comb, ul in filtered_combinations.items():
        print("Combination:", comb, "Utility List:", ul)

if __name__ == "__main__":
    main()
