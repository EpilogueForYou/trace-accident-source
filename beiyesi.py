import pandas as pd
import numpy as np
from scipy.stats import multivariate_normal

file_path = 'C:/Users/dadada/Desktop/暂时/临时/data2.xlsx'

# 加载数据
data = pd.read_excel(file_path)
# 分割已分组和未分组的数据
grouped_data = data.dropna(subset=['Group'])
unclassified_data = data[data['Group'].isnull()]

# 计算已分组数据的统计量
mean_I = grouped_data[grouped_data['Group'] == 1].iloc[:, :-1].mean().to_numpy()
cov_I = grouped_data[grouped_data['Group'] == 1].iloc[:, :-1].cov().to_numpy()
mean_II = grouped_data[grouped_data['Group'] == 2].iloc[:, :-1].mean().to_numpy()
cov_II = grouped_data[grouped_data['Group'] == 2].iloc[:, :-1].cov().to_numpy()
# 先验概率
p_I = 0.8
p_II = 0.2
# 贝叶斯判别函数
def bayes_discriminant(x, mean_I, cov_I, mean_II, cov_II, p_I, p_II):
    # 计算后验概率
    pdf_I = multivariate_normal.pdf(x, mean=mean_I, cov=cov_I)
    pdf_II = multivariate_normal.pdf(x, mean=mean_II, cov=cov_II)
    
    post_prob_I = pdf_I * p_I / (pdf_I * p_I + pdf_II * p_II)
    post_prob_II = pdf_II * p_II / (pdf_I * p_I + pdf_II * p_II)
    
    # 根据后验概率判定归属
    return 'I' if post_prob_I > post_prob_II else 'II'

# 对未定级运动员进行判别
unclassified_data['Predicted_Group'] = unclassified_data.apply(lambda row: bayes_discriminant(row[:-1].to_numpy(), mean_I, cov_I, mean_II, cov_II, p_I, p_II), axis=1)
# 输出判别结果
print(unclassified_data[['Predicted_Group']])
