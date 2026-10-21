def create_C1(dataset):
    C1 = []
    for transaction in dataset:
        for item in transaction:
            if [item] not in C1:      # 用列表[item]表示一个项集
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))   # 转成frozenset，可作字典key

def scan_D(D, Ck, min_support):
    ssCnt = {}                        # 记录每个候选项集出现的次数
    for tid in D:                     # 遍历每条交易
        for can in Ck:                # 遍历每个候选集
            if can.issubset(tid):     # 候选集是否是交易的子集
                ssCnt[can] = ssCnt.get(can, 0) + 1
    numItems = float(len(D))
    retList = []                      # 存频繁项集
    supportData = {}                  # 存所有候选集的支持度
    for key in ssCnt:
        support = ssCnt[key] / numItems
        supportData[key] = support
        if support >= min_support:    # 达到阈值就是频繁的
            retList.append(key)
    return retList, supportData

def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            # 前 k-2 项相同才合并（合并后是 k 项，Python下标从0开始）
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])   # 集合并集
    return retList

def apriori(dataset, min_support=0.5):
    C1 = create_C1(dataset)
    D = list(map(set, dataset))                 # 每条交易转成set
    L1, supportData = scan_D(D, C1, min_support)
    L = [L1]                                    # L[0]是频繁1项集
    k = 2
    while len(L[k-2]) > 0:                      # 上一轮还有频繁项集才继续
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scan_D(D, Ck, min_support)
        supportData.update(supK)
        if len(Lk) == 0:
            break
        L.append(Lk)
        k += 1
    return L, supportData

if __name__ == "__main__":
    dataset = [
    ['苹果', '香蕉', '牛奶'],
    ['苹果', '香蕉', '面包'],
    ['苹果', '牛奶', '鸡蛋'],
    ['香蕉', '面包', '牛奶'],
    ['苹果', '香蕉', '牛奶', '面包'],
    ['香蕉', '牛奶', '鸡蛋'],
    ['苹果', '面包', '鸡蛋'],
    ['苹果', '香蕉', '面包', '鸡蛋'],
    ['牛奶', '面包', '鸡蛋'],
    ['苹果', '香蕉', '牛奶', '鸡蛋'],
]
    L, supportData = apriori(dataset, min_support=0.3)

    print("频繁项集结果：")
    for i, Lk in enumerate(L):
        print(f"--- 频繁{i+1}项集 ---")
        for itemset in Lk:
            print(sorted(itemset), "支持度=%.2f" % supportData[itemset])
def generate_rules(L, supportData, min_conf=0.6):
    rules = []
    for i in range(1, len(L)):            # 从频繁2项集开始
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            calcConf(freqSet, H1, supportData, rules, min_conf)
    return rules

def calcConf(freqSet, H, supportData, rules, min_conf):
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= min_conf:
            lift = conf / supportData[conseq]     # 提升度
            rules.append((freqSet - conseq, conseq, conf, lift))

# 调用：
rules = generate_rules(L, supportData, min_conf=0.6)
print("\n强关联规则（置信度>=0.6）：")
for ant, con, conf, lift in rules:
    print(sorted(ant), "->", sorted(con), "置信度=%.2f 提升度=%.2f" % (conf, lift))