import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置页面标题
st.title("Streamlit 可视化")

# 生成随机数据
data = pd.DataFrame(
    np.random.randn(100, 3),
    columns=['A', 'B', 'C']
)

# 显示数据表格
st.subheader("数据表格")
st.write(data)

# 绘制折线图
st.subheader("折线图")
st.line_chart(data)

# 绘制柱状图
st.subheader("柱状图")
st.bar_chart(data)

# 绘制散点图
st.subheader("散点图")
fig, ax = plt.subplots()
ax.scatter(data['A'], data['B'], c=data['C'], cmap='viridis')
ax.set_xlabel('A')
ax.set_ylabel('B')
ax.set_title('散点图')
st.pyplot(fig)

# 添加交互组件
st.subheader("交互组件")
option = st.selectbox(
    '选择一个选项',
    ['选项 1', '选项 2', '选项 3']
)
st.write('你选择了:', option)

# 显示滑动条
slider_value = st.slider('选择一个值', 0, 100, 50)
st.write('滑动条的值:', slider_value)

# 显示文本输入框
text_input = st.text_input('输入一些文本')
st.write('你输入的文本是:', text_input)
