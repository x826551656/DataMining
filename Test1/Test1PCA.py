from sklearn.datasets import load_iris
import numpy as np
iris = load_iris()

X = iris.data
target = iris.target

print("原始数据:\n", X)
# print("Target:\n",target)
X_mean=np.mean(X,axis=0)
print("均值:\n",X_mean)
X_centered=X-X_mean
print("去均值前五行：\n",X_centered[:5])
n=X_centered.shape[0]
cov_matrix=np.cov(X_centered,rowvar=False)
print("协方差矩阵：\n",cov_matrix)