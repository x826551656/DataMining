# 从sklearn.decomposition模块导入PCA类
from sklearn.decomposition import PCA

# 从sklearn.datasets导入load_iris函数
from sklearn.datasets import load_iris

# 加载iris数据集
iris = load_iris()

# 取出特征数据
X = iris.data

# 创建PCA对象，n_components=2表示要降到2维
pca = PCA(n_components=2)

# 用fit_transform方法对X进行降维
# fit表示计算主成分方向，transform表示把数据投影到主成分上
# 返回降维后的数据，赋值给X_pca
X_pca = pca.fit_transform(X)

# 打印降维后的前五行数据
print("sklearn PCA降维后前五行数据：")
print(X_pca[:5])

# 打印每个主成分的解释方差比
print("解释方差比：")
print(pca.explained_variance_ratio_)