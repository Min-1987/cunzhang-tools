import streamlit as st
import re

st.title("数字工具应用")

st.header("数字配对")
st.write("输入两组数字（用空格或逗号分隔），应用将自动配对它们。")

group1_input = st.text_input("第一组数字（例如：18 19 20 30 21）", value="18 19 20 30 21")
group2_input = st.text_input("第二组数字（例如：21 17 15 16 14）", value="21 17 15 16 14")

if st.button("生成配对"):
    # 解析输入
    group1 = [int(x.strip()) for x in group1_input.replace(',', ' ').split() if x.strip()]
    group2 = [int(x.strip()) for x in group2_input.replace(',', ' ').split() if x.strip()]
    
    if len(group1) != len(group2):
        st.error("两组数字的数量必须相同！")
    else:
        pairs = [f"{a}={b}" for a, b in zip(group1, group2)]
        st.write("配对结果：")
        st.write(", ".join(pairs))

st.header("字符串解析数字")
st.write("输入包含数字和符号的字符串，应用将提取数字并格式化。")

string_input = st.text_input("输入字符串（例如：18-30*+16+40+28-31-43-14-38-26-34*10*12-24-36+48-32-8-44-各5）", value="18-30*+16+40+28-31-43-14-38-26-34*10*12-24-36+48-32-8-44-各5")

if st.button("解析数字"):
    # 如果包含“各5”，先移除它再提取数字
    temp_input = string_input.replace("各5", "")
    numbers = re.findall(r'\d+', temp_input)
    result = " ".join(numbers)
    if "各5" in string_input:
        result += "各5"
    st.write("解析结果：")
    st.write(result)

st.header("生肖包数计算")
st.write("输入生肖名称或别称和包数，应用将计算各份数（马年5份，其他4份）。")

zodiac_input = st.text_input("生肖或别称（例如：马 或 子）", value="马")
amount_input = st.number_input("包数（例如：100）", value=100, min_value=1)

if st.button("计算份数"):
    zodiac = zodiac_input.strip()
    zodiac_mapping = {'子': '鼠'}
    zodiac = zodiac_mapping.get(zodiac, zodiac)
    amount = int(amount_input)
    if zodiac == "马":
        per_share = amount // 5
    else:
        per_share = amount // 4
    result = f"{zodiac}各{per_share}"
    st.write("计算结果：")
    st.write(result)

st.write("或输入多个生肖和数字（例如：龙虎免猪冬5 或 子各20），排除非生肖。")

multi_input = st.text_input("输入字符串（例如：龙虎免猪冬5）", value="龙虎免猪冬5")

if st.button("解析生肖"):
    # 定义生肖列表
    zodiacs = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
    # 映射特殊字符
    mapping = {'免': '兔', '子': '鼠'}
    
    # 提取数字
    numbers = re.findall(r'\d+', multi_input)
    if not numbers:
        st.error("未找到数字！")
    else:
        amount = int(numbers[0])
        # 提取非数字部分
        non_digits = re.sub(r'\d+', '', multi_input)
        # 分割成字符
        chars = list(non_digits)
        # 过滤生肖
        valid_zodiacs = []
        for char in chars:
            if char in mapping:
                char = mapping[char]
            if char in zodiacs:
                valid_zodiacs.append(char)
        if not valid_zodiacs:
            st.error("未找到有效生肖！")
        else:
            result = "".join(valid_zodiacs) + f"各{amount}"
            st.write("解析结果：")
            st.write(result)