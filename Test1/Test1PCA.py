from sklearn.datasets import load_iris
import numpy as np
iris = load_iris()

X = iris.data

print("原始数据:\n", X)
# print("Target:\n",target)
X_mean=np.mean(X,axis=0)
print("均值:\n",X_mean)
X_centered=X-X_mean
print("去均值前五行：\n",X_centered[:5])
cov_matrix=np.cov(X_centered,rowvar=False)
print("协方差矩阵：\n",cov_matrix)
eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)
# [::-1]表示把索引反转，变成从大到小
idx = np.argsort(eig_vals)[::-1]
# 按照从大到小的索引重新排列特征值
eig_vals = eig_vals[idx]
# 按照同样的索引重新排列特征向量
eig_vecs = eig_vecs[:, idx]
# 特征向量的方向可以整体取反，不影响结果，但为了和sklearn结果比较，统一一下
# 对每一列，找到绝对值最大的那个元素，如果它是负数，就把整列取反
for i in range(eig_vecs.shape[1]):
    if eig_vecs[np.argmax(np.abs(eig_vecs[:, i])), i] < 0:
        eig_vecs[:, i] = -eig_vecs[:, i]

print("特征值（降序）：")
print(eig_vals)
print("特征向量（列对应特征值）：")
print(eig_vecs)

k = 2
# 取特征向量的前k列，组成投影矩阵W
# eig_vecs是4行4列，取前2列，变成4行2列
W = eig_vecs[:, :k]

# 把去均值后的数据投影到新的坐标方向上
# X_centered是150行4列，W是4行2列
# 矩阵乘法后得到150行2列的数据，就是降维后的结果
X_pca_manual = X_centered.dot(W)

print("手动PCA降维后前五行数据：")
print(X_pca_manual[:5])

# 计算每个主成分的解释方差比
# 特征值除以所有特征值之和，得到每个主成分占的总信息比例
print("各主成分解释方差比：")
print(eig_vals / np.sum(eig_vals))