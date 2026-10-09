from sklearn.datasets import load_iris
iris = load_iris()

# 获取数据和目标
data = iris.data
target = iris.target

print(iris.DESCR)

# 打印前五个样本的数据和目标
print("Data:\n", iris.data[:5])
print("Target:\n", iris.target[:5])