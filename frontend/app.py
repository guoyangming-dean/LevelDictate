"""
Streamlit 前端入口
英语学习 - 词汇抽取与听写练习系统
"""
import streamlit as st
import api_client as api

# 页面配置
st.set_page_config(
    page_title="LevelDictate - 英语听写练习",
    page_icon="📚",
    layout="wide"
)


def main():
    """主函数"""

    # 标题
    st.title("📚 LevelDictate - 英语听写练习")
    st.markdown("上传英文材料，生成个性化听写练习")

    # 侧边栏 - 设置
    st.sidebar.title("⚙️ 设置")

    # 选择英语水平
    level_options = {
        "A1": "A1 - 入门级",
        "A2": "A2 - 初级",
        "B1": "B1 - 中级",
        "B2": "B2 - 中高级",
        "C1": "C1 - 高级",
    }
    user_level = st.sidebar.selectbox(
        "选择你的英语水平",
        options=list(level_options.keys()),
        format_func=lambda x: level_options[x],
        index=2  # 默认 B1
    )

    # 选择每轮练习数量
    question_count = st.sidebar.radio(
        "每轮练习数量",
        options=[10, 20, 30],
        index=0,
        horizontal=True
    )

    # 初始化 session state
    if 'full_text' not in st.session_state:
        st.session_state.full_text = ""
    if 'candidate_words' not in st.session_state:
        st.session_state.candidate_words = []
    if 'dictation_items' not in st.session_state:
        st.session_state.dictation_items = []
    if 'recommended_words' not in st.session_state:
        st.session_state.recommended_words = []
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False

    # 主界面 - 文件上传
    st.header("📤 第一步：上传学习材料")

    uploaded_file = st.file_uploader(
        "上传英文材料 (支持 TXT 和 PDF)",
        type=['txt', 'pdf']
    )

    if uploaded_file is not None:
        # 上传文件
        with st.spinner("正在解析文件..."):
            try:
                result = api.upload_file_content(
                    uploaded_file.getvalue(),
                    uploaded_file.name
                )

                if result.get('success'):
                    st.session_state.full_text = result.get('full_text', '')
                    st.session_state.candidate_words = []

                    st.success(f"✅ 文件解析成功！")

                    # 显示文本预览
                    with st.expander("📄 查看解析后的文本预览", expanded=True):
                        st.text(result.get('text_preview', ''))

                    # 提取单词
                    if st.button("🔍 第二步：提取候选词汇", type="primary"):
                        with st.spinner("正在提取词汇..."):
                            extract_result = api.extract_words(st.session_state.full_text)

                            if extract_result.get('success'):
                                st.session_state.candidate_words = extract_result.get('candidate_words', [])

                                st.success(
                                    f"✅ 提取到 {len(st.session_state.candidate_words)} 个候选词汇"
                                )

                                # 显示候选词统计
                                with st.expander(f"📋 查看候选词汇 (共 {len(st.session_state.candidate_words)} 个)"):
                                    # 每行显示 10 个词
                                    cols = st.columns(5)
                                    for i, word in enumerate(st.session_state.candidate_words):
                                        col = cols[i % 5]
                                        col.markdown(f"- {word}")

                                    if len(st.session_state.candidate_words) > 50:
                                        st.caption(f"...还有 {len(st.session_state.candidate_words) - 50} 个词汇")

                else:
                    st.error(f"❌ 文件解析失败：{result.get('message', '未知错误')}")

            except Exception as e:
                st.error(f"❌ 请求失败：{str(e)}")

    # 候选词列表
    if st.session_state.candidate_words:
        st.header("📖 第三步：生成听写练习")

        # 显示当前设置
        st.info(
            f"📌 当前设置：{level_options[user_level]} | "
            f"每轮 {question_count} 个单词"
        )

        # 生成听写
        if st.button("🎯 生成听写任务", type="primary"):
            with st.spinner("正在生成听写任务..."):
                try:
                    result = api.generate_dictation(
                        candidate_words=st.session_state.candidate_words,
                        user_level=user_level,
                        question_count=question_count
                    )

                    if result.get('success'):
                        st.session_state.dictation_items = result.get('dictation_items', [])
                        st.session_state.recommended_words = result.get('recommended_words', [])
                        st.session_state.show_results = False

                        st.success(
                            f"✅ 生成 {len(st.session_state.dictation_items)} 道听写题！"
                        )

                        # 显示推荐词汇
                        with st.expander(
                            f"⭐ 推荐词汇 (共 {len(st.session_state.recommended_words)} 个)"
                        ):
                            cols = st.columns(5)
                            for i, word in enumerate(st.session_state.recommended_words):
                                col = cols[i % 5]
                                col.markdown(f"- **{word}**")

                    else:
                        st.error("❌ 生成听写任务失败")

                except Exception as e:
                    st.error(f"❌ 请求失败：{str(e)}")

    # 听写练习界面
    if st.session_state.dictation_items and not st.session_state.show_results:
        st.header("✍️ 第四步：开始听写")

        st.markdown("请根据显示的单词含义或提示，输入正确的拼写：")

        # 存储用户答案
        user_answers = []

        # 随机打乱显示顺序
        items = st.session_state.dictation_items

        # 显示题目
        with st.form("dictation_form"):
            for i, item in enumerate(items):
                st.markdown(f"**{i+1}.** {item['display_word']}")
                answer = st.text_input(
                    f"请输入第 {i+1} 题的拼写",
                    key=f"answer_{i}",
                    placeholder="输入单词拼写..."
                )
                user_answers.append(answer)
                st.markdown("---")

            # 提交答案
            submitted = st.form_submit_button("📝 提交答案", type="primary")

            if submitted:
                # 检查答案
                with st.spinner("正在判分..."):
                    try:
                        result = api.check_answer(
                            dictation_items=items,
                            user_answers=user_answers
                        )

                        if result.get('success'):
                            st.session_state.show_results = True
                            st.session_state.check_result = result

                            # 显示结果
                            st.header("📊 答题结果")

                            # 正确率
                            accuracy = result.get('accuracy', 0)
                            correct_count = result.get('correct_count', 0)
                            total_count = result.get('total_count', 0)

                            # 正确率颜色
                            if accuracy >= 90:
                                st.balloons()
                                st.success(f"🎉 太棒了！正确率：{accuracy}% ({correct_count}/{total_count})")
                            elif accuracy >= 70:
                                st.info(f"👍 不错！正确率：{accuracy}% ({correct_count}/{total_count})")
                            elif accuracy >= 50:
                                st.warning(f"💪 继续加油！正确率：{accuracy}% ({correct_count}/{total_count})")
                            else:
                                st.error(f"📚 需要多加练习！正确率：{accuracy}% ({correct_count}/{total_count})")

                            # 显示每题结果
                            results = result.get('results', [])
                            for i, r in enumerate(results):
                                with st.expander(f"第 {i+1} 题：{r['correct_answer']}", expanded=True):
                                    if r['is_correct']:
                                        st.markdown(f"✅ **正确！**")
                                    else:
                                        st.markdown(f"❌ **错误**")
                                        st.markdown(f"正确拼写：{r['correct_answer']}")
                                        st.markdown(f"你的答案：{r['user_answer'] or '(未作答)'}")

                            # 重新练习按钮
                            if st.button("🔄 重新练习"):
                                st.session_state.show_results = False
                                st.session_state.dictation_items = []
                                st.session_state.recommended_words = []
                                st.rerun()

                        else:
                            st.error("❌ 判分失败")

                    except Exception as e:
                        st.error(f"❌ 请求失败：{str(e)}")

    # 使用说明
    st.sidebar.markdown("---")
    st.sidebar.title("📖 使用说明")
    st.sidebar.markdown("""
    **使用流程：**

    1. 📤 上传 TXT 或 PDF 文件
    2. 🔍 点击提取词汇按钮
    3. 🎯 设置水平并生成听写
    4. ✍️ 输入拼写并提交
    5. 📊 查看得分和答案

    **提示：**
    - PDF 必须是可复文本的
    - 第一次使用建议选择 B1
    """)

    # 底部信息
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "LevelDictate v1.0.0 - 英语听写练习系统"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
