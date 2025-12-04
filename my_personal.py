import streamlit as st
import datetime
import json
from pathlib import Path

# App Configuration
st.set_page_config(page_title="My Personal PA", page_icon="🤖", layout="wide")

# Initialize session state for data persistence
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'routine' not in st.session_state:
    st.session_state.routine = []

# Header
st.title("My Personal - Your AI Assistant")
st.markdown("*Your personal well-wisher and productivity companion*")

# Sidebar Navigation
menu = st.sidebar.selectbox(
    "Navigate",
    ["🏠 Dashboard", "✅ Tasks", "📝 Notes", "⏰ Daily Routine", "💪 Habits", "⚙️ Settings"]
)

# Dashboard
if menu == "🏠 Dashboard":
    st.header("Good " + ("Morning" if datetime.datetime.now().hour < 12 else "Afternoon" if datetime.datetime.now().hour < 18 else "Evening") + "! 👋")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Tasks Today", len(st.session_state.tasks))
    with col2:
        st.metric("Notes", len(st.session_state.notes))
    with col3:
        st.metric("Routine Items", len(st.session_state.routine))
    
    st.info("💡 **Daily Motivation:** Believe in yourself and all that you are!")

# Tasks Section
elif menu == "✅ Tasks":
    st.header("Task Manager")
    
    # Add new task
    with st.form("add_task"):
        task_name = st.text_input("Task Name")
        task_priority = st.selectbox("Priority", ["High", "Medium", "Low"])
        task_deadline = st.date_input("Deadline")
        submit = st.form_submit_button("Add Task")
        
        if submit and task_name:
            st.session_state.tasks.append({
                "name": task_name,
                "priority": task_priority,
                "deadline": str(task_deadline),
                "completed": False
            })
            st.success(f"✅ Task '{task_name}' added!")
    
    # Display tasks
    st.subheader("Your Tasks")
    for idx, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{task['name']}** - {task['priority']} Priority (Due: {task['deadline']})")
        with col2:
            if st.button("✓ Done", key=f"done_{idx}"):
                st.session_state.tasks[idx]['completed'] = True
        with col3:
            if st.button("🗑️ Delete", key=f"del_{idx}"):
                st.session_state.tasks.pop(idx)
                st.rerun()

# Notes Section
elif menu == "📝 Notes":
    st.header("Quick Notes")
    
    note_content = st.text_area("Write your note here...")
    if st.button("Save Note"):
        if note_content:
            st.session_state.notes.append({
                "content": note_content,
                "timestamp": str(datetime.datetime.now())
            })
            st.success("Note saved!")
    
    st.subheader("Your Notes")
    for idx, note in enumerate(st.session_state.notes):
        with st.expander(f"Note {idx+1} - {note['timestamp'][:16]}"):
            st.write(note['content'])
            if st.button("Delete", key=f"note_del_{idx}"):
                st.session_state.notes.pop(idx)
                st.rerun()

# Daily Routine
elif menu == "⏰ Daily Routine":
    st.header("Daily Routine Manager")
    
    with st.form("add_routine"):
        routine_time = st.time_input("Time")
        routine_activity = st.text_input("Activity")
        submit = st.form_submit_button("Add to Routine")
        
        if submit and routine_activity:
            st.session_state.routine.append({
                "time": str(routine_time),
                "activity": routine_activity
            })
            st.success(f"Added: {routine_activity} at {routine_time}")
    
    st.subheader("Your Daily Schedule")
    sorted_routine = sorted(st.session_state.routine, key=lambda x: x['time'])
    for item in sorted_routine:
        st.write(f"⏰ **{item['time']}** - {item['activity']}")

# Habits Tracker
elif menu == "💪 Habits":
    st.header("Habit Tracker")
    st.info("🚧 Coming soon! Track your daily habits and build streaks.")

# Settings
elif menu == "⚙️ Settings":
    st.header("Settings")
    st.subheader("Your Profile")
    user_name = st.text_input("Your Name", "User")
    st.write(f"Hello, {user_name}!")
    
    if st.button("Clear All Data"):
        st.session_state.tasks = []
        st.session_state.notes = []
        st.session_state.routine = []
        st.success("All data cleared!")

# Footer
st.sidebar.markdown("---")