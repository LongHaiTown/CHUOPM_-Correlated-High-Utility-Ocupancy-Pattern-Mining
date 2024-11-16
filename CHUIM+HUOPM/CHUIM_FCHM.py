import itertools

# Ví dụ về external utility của các item
external_utility = {
    'a': 5,
    'b': 3,
    'c': 2,
    'd': 4
}
transactions = [
        ('a', 'b', 'c'),
        ('a', 'b'),
        ('a', 'c'),
        ('b', 'c'),
        ('a', 'b', 'c', 'd'),
        # Thêm các giao dịch khác
    ]

# Tính utility của một itemset
def calculate_utility(itemset):
    utility = sum(external_utility[item] for item in itemset)
    return utility

# def calculate_all_confidence(itemset, transactions):
#     min_support = min([transactions.count(item) for item in itemset])
#     all_confidence = transactions.count(itemset) / min_support
#     return all_confidence

# def calculate_bond(itemset, transactions):
#     support_itemset = transactions.count(itemset)
#     total_support = sum([transactions.count(item) for item in itemset])
#     bond = support_itemset / total_support
#     return bond

def main():
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


    transactions_Utility = []
    for tran in transactions :
        transactions_Utility.append(calculate_utility(tran))


    for ulti in transactions_Utility:
        print( "Trasaction ulti của ni là "+ str(ulti)); 

if __name__ == "__main__":
    main()
