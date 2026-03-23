import streamlit as st
from datetime import date

st.set_page_config(page_title="To-Do App", page_icon="📝", layout="centered")

st.title("📝 Smart To-Do List")

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Sidebar
username = st.sidebar.text_input("👤 Enter your name")
st.sidebar.write(f"Welcome, {username} 👋")

menu = st.sidebar.radio(
    "📌 Choose Option",
    ["Add Task", "Manage Tasks"]
)

# ---------------- ADD TASK ----------------
if menu == "Add Task":
    st.subheader("Add New Task")

    task = st.text_input("Enter your task:")
    
    # NEW FEATURES 👇
    deadline = st.date_input("📅 Select deadline", min_value=date.today())
    priority = st.selectbox("⚡ Select Priority", ["Low", "Medium", "High"])

    if st.button("Add Task"):
        if task.strip() != "":
            st.session_state.tasks.append({
                "task": task,
                "done": False,
                "deadline": deadline,
                "priority": priority
            })
            st.success("✅ Task Added Successfully!")
        else:
            st.warning("⚠️ Please enter a task")

# ---------------- MANAGE TASK ----------------
elif menu == "Manage Tasks":
    st.subheader("📋 Your Tasks")

    if len(st.session_state.tasks) == 0:
        st.info("No tasks yet! Add some tasks first 😊")
    else:
        completed = 0

        for i, item in enumerate(st.session_state.tasks):
            
            # 🎨 CARD STYLE USING CONTAINER
            with st.container():
                col1, col2, col3 = st.columns([5,1,1])

                # Task Info + Checkbox
                with col1:
                    done = st.checkbox(
                        f"{item['task']}  \n📅 {item['deadline']} | ⚡ {item['priority']}",
                        value=item["done"],
                        key=f"check_{i}"
                    )
                    st.session_state.tasks[i]["done"] = done

                    if done:
                        completed += 1

                # ❌ Delete
                with col2:
                    if st.button("❌", key=f"del_{i}"):
                        st.session_state.tasks.pop(i)
                        st.rerun()

                # ✏️ Edit
                with col3:
                    if st.button("✏️", key=f"edit_{i}"):
                        st.session_state.edit_index = i

                st.divider()  # clean separation

        # 📊 Progress
        total = len(st.session_state.tasks)
        st.write(f"### 📊 Progress: {completed}/{total}")

        if total > 0:
            st.progress(completed / total)

# ---------------- EDIT TASK ----------------
if "edit_index" in st.session_state:
    st.subheader("✏️ Edit Task")

    idx = st.session_state.edit_index
    task_data = st.session_state.tasks[idx]

    new_task = st.text_input("Update task:", value=task_data["task"])
    new_deadline = st.date_input("📅 Update deadline", value=task_data["deadline"])
    new_priority = st.selectbox(
        "⚡ Update Priority",
        ["Low", "Medium", "High"],
        index=["Low", "Medium", "High"].index(task_data["priority"])
    )

    if st.button("Update Task"):
        st.session_state.tasks[idx] = {
            "task": new_task,
            "done": task_data["done"],
            "deadline": new_deadline,
            "priority": new_priority
        }
        del st.session_state.edit_index
        st.success("✅ Task Updated!")
        st.rerun()