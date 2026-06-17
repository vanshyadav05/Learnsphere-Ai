
import streamlit as st
import urllib.parse
import json
import os
from ai import ask_ai
from pdf_reader import extract_pdf_text
from memory import add, get, remove
from voice import speak

SAVE_FILE = "data.json"

def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data():
    data = {
        "tasks": st.session_state.tasks,
        "saved_projects": st.session_state.saved_projects,
        "favorite": st.session_state.favorite,
        "theme": st.session_state.theme,
        "mobile": st.session_state.mobile,
        "compact": st.session_state.compact,
        "accent": st.session_state.accent,
        "daily_goal": st.session_state.daily_goal,
        "study_done": st.session_state.study_done,
        "recent_activity": st.session_state.recent_activity,
        "memory_enabled": st.session_state.memory_enabled
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def stop_speaking():
   return 

st.set_page_config(
    page_title="LearnSphere AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

saved = load_data()

defaults = {
    "theme": saved.get("theme", "Dark"),
    "mobile": saved.get("mobile", False),
    "compact": saved.get("compact", False),
    "accent": saved.get("accent", "Blue"),
    "pdf_text": "",
    "chat": "Chat 1",
    "search_answer": "",
    "pdf_answer": "",
    "study_answer": "",
    "quiz": "",
    "tasks": saved.get("tasks", []),
    "notes": "",
    "resume_answer": "",
    "saved_projects": saved.get("saved_projects", []),
    "favorite": saved.get("favorite", ""),
    "logged_in": False,
    "user": "",
    "export_text": "",
    "image_url": "",
    "daily_goal": saved.get("daily_goal", 5),
    "study_done": saved.get("study_done", 0),
    "recent_activity": saved.get("recent_activity", []),
    "memory_enabled": saved.get("memory_enabled", True)
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

theme_bg = "#0d1117"
theme_side = "#161b22"
text_color = "#ffffff"

if st.session_state.theme == "Light":
    theme_bg = "#ffffff"
    theme_side = "#f3f3f3"
    text_color = "#111111"

accent_colors = {
    "Blue": "#58a6ff",
    "Purple": "#a855f7",
    "Green": "#22c55e",
    "Red": "#ef4444"
}

accent = accent_colors.get(st.session_state.accent, "#58a6ff")
padding = "0.5rem" if st.session_state.compact else "1rem"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {theme_bg};
        color: {text_color};
    }}

    [data-testid="stSidebar"] {{
        background: {theme_side};
    }}

    .block-container {{
        padding-top: {padding};
        max-width: {"900px" if st.session_state.mobile else "1200px"};
    }}

    div[data-testid="metric-container"] {{
        background: {theme_side};
        padding: 20px;
        border-radius: 20px;
    }}

    h1, h2, h3 {{
        color: {accent};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

PAGES = {
    "🏠 Dashboard": "dashboard",
    "💬 AI Chat": "chat",
    "🌐 Web Search": "search",
    "📄 PDF Q&A": "pdf",
    "📚 Study Helper": "study",
    "🧪 Quiz Generator": "quiz",
    "📝 Planner": "planner",
    "📝 Notes Maker": "notes",
    "💼 Resume Helper": "resume",
    "🚀 Workspace": "workspace",
    "📥 Export Center": "export",
    "🖼️ AI Image Generator": "image",
    "🔔 Notifications": "notify",
    "📈 Analytics": "analytics",
    "☁️ Backup": "backup",
    "👤 Profile": "profile",
    "⚙ Settings": "settings"
}

with st.sidebar:
    st.title("🧠 AI OS")

    st.session_state.chat = st.text_input("Chat Name", st.session_state.chat)

    if st.button("🗑 Delete Chat"):
        remove(st.session_state.chat)
        st.rerun()

    st.markdown("---")

    section = st.selectbox(
        "Section",
        [
            "Core",
            "Study",
            "Tools",
            "Account"
        ]
    )

    if section == "Core":
        page = st.radio(
            "Go to",
            [
                "🏠 Dashboard",
                "💬 AI Chat",
                "🌐 Web Search"
            ]
        )

    elif section == "Study":
        page = st.radio(
            "Go to",
            [
                "📄 PDF Q&A",
                "📚 Study Helper",
                "🧪 Quiz Generator",
                "📝 Planner",
                "📝 Notes Maker"
            ]
        )

    elif section == "Tools":
        page = st.radio(
            "Go to",
            [
                "💼 Resume Helper",
                "🚀 Workspace",
                "📥 Export Center",
                "🖼️ AI Image Generator",
                "🔔 Notifications",
                "☁️ Backup",
                "📈 Analytics"
            ]
        )

    else:
        page = st.radio(
            "Go to",
            [
                "👤 Profile",
                "⚙ Settings"
            ]
        )

    st.markdown("---")

    if st.session_state.logged_in:
        st.success("User: " + st.session_state.user)
    else:
        st.warning("Guest Mode")

    st.write("Built by Vansh")

selected = PAGES[page]

if selected == "dashboard":

    st.title("🧠 LearnSphere AI")
    st.caption(
        f"Welcome {st.session_state.user if st.session_state.logged_in else 'Guest'}"
    )

    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for task in st.session_state.tasks if task["done"])
    total_projects = len(st.session_state.saved_projects)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pages", len(PAGES))

    with col2:
        st.metric("Tasks", total_tasks)

    with col3:
        st.metric("Completed", completed_tasks)

    with col4:
        st.metric("Projects", total_projects)

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("📌 Today Overview")

        if total_tasks == 0:
            st.info("No tasks added yet.")
        else:
            st.write(f"Tasks completed: {completed_tasks}/{total_tasks}")
            st.progress(completed_tasks / total_tasks if total_tasks > 0 else 0)

        st.subheader("⭐ Favorite Project")

        if st.session_state.favorite:
            st.success(st.session_state.favorite)
        else:
            st.warning("No favorite project selected.")

    with right:
        st.subheader("💬 Current Chat")
        st.info(st.session_state.chat)

        st.subheader("🔔 Daily Goal")
        st.write(f"{st.session_state.study_done}/{st.session_state.daily_goal} hours completed")
        st.progress(
            st.session_state.study_done / st.session_state.daily_goal
            if st.session_state.daily_goal > 0 else 0
        )

    st.markdown("---")
    st.subheader("🧠 Recent Activity")

    if st.session_state.memory_enabled:
        if st.session_state.recent_activity:
            for activity in st.session_state.recent_activity[:5]:
                st.info(activity)
        else:
            st.write("No activity yet.")
    else:
        st.warning("Memory disabled.")

elif selected == "chat":

    st.title("💬 AI Chat")
    st.caption("Current chat: " + st.session_state.chat)

    history = get(st.session_state.chat)

    for msg in history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask your AI...")

    if question:
        add(st.session_state.chat, "user", question)

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("🧠 AI is thinking..."):
                answer = ask_ai(question)
            st.write(answer)

        add(st.session_state.chat, "assistant", answer)

        if st.session_state.memory_enabled:
            st.session_state.recent_activity.insert(
                0,
                f"Asked: {question[:40]}"
            )
            st.session_state.recent_activity = st.session_state.recent_activity[:10]
            save_data()

        st.rerun()

    last_answer = ""

    for msg in reversed(history):
        if msg["role"] == "assistant":
            last_answer = msg["content"]
            break

    if last_answer:
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔊 Speak last answer"):
                speak(last_answer)

        with col2:
            if st.button("⏹ Stop speaking"):
                stop_speaking()

elif selected == "search":

    st.title("🌐 Web Search")

    question = st.text_input("Search anything")

    if st.button("Search"):
        with st.spinner("Searching..."):
            st.session_state.search_answer = ask_ai(
                "latest current web search: " + question
            )

    if st.session_state.search_answer:
        st.write(st.session_state.search_answer)

elif selected == "pdf":

    st.title("📄 PDF Q&A")

    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_pdf:
        st.session_state.pdf_text = extract_pdf_text(uploaded_pdf)
        st.success("PDF uploaded successfully")

    question = st.text_input("Ask question from PDF")

    if st.button("Ask PDF"):

        if st.session_state.pdf_text == "":
            st.warning("Please upload a PDF first.")

        else:
            final_question = f"""
Answer the question using this PDF text.

PDF text:
{st.session_state.pdf_text[:8000]}

Question:
{question}
"""

            with st.spinner("Reading PDF..."):
                st.session_state.pdf_answer = ask_ai(final_question)

    if st.session_state.pdf_answer:
        st.write(st.session_state.pdf_answer)

elif selected == "study":

    st.title("📚 Study Helper")

    topic = st.text_input("Enter topic")

    if st.button("Explain"):

        final_question = f"""
Explain this like a teacher.
Use simple language.
Give examples.
Then give 5 viva questions.

Topic:
{topic}
"""

        with st.spinner("Preparing answer..."):
            st.session_state.study_answer = ask_ai(final_question)

    if st.session_state.study_answer:
        st.write(st.session_state.study_answer)

elif selected == "quiz":

    st.title("🧪 Quiz Generator")

    topic = st.text_input("Enter quiz topic")

    level = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

    if st.button("Generate Quiz"):

        prompt = f"""
Create a {level} level quiz on this topic:

{topic}

Make exactly 5 MCQ questions.

Format:
Q1. question
A. option
B. option
C. option
D. option
Answer: correct option
Short explanation:
"""

        with st.spinner("Creating quiz..."):
            st.session_state.quiz = ask_ai(prompt)

    if st.session_state.quiz:
        st.write(st.session_state.quiz)

        st.markdown("---")
        st.subheader("Self Score")

        score = st.slider("How many did you get correct?", 0, 5, 0)

        st.metric("Your Score", f"{score}/5")

        if score >= 4:
            st.success("Excellent performance 🔥")
        elif score >= 2:
            st.warning("Good, but revise more.")
        else:
            st.error("Revise this topic again.")

elif selected == "planner":

    st.title("📝 Study Planner")

    task = st.text_input("Add a task")

    if st.button("Add Task"):
        if task.strip():
            st.session_state.tasks.append(
                {
                    "task": task,
                    "done": False
                }
            )
            save_data()
            st.rerun()

    st.markdown("---")
    st.subheader("Your Tasks")

    for i, item in enumerate(st.session_state.tasks):

        col1, col2 = st.columns([4, 1])

        with col1:
            done = st.checkbox(
                item["task"],
                value=item["done"],
                key=f"task_{i}"
            )

            if done != st.session_state.tasks[i]["done"]:
                st.session_state.tasks[i]["done"] = done
                save_data()

        with col2:
            if st.button("Delete", key=f"del_{i}"):
                st.session_state.tasks.pop(i)
                save_data()
                st.rerun()

    total = len(st.session_state.tasks)
    completed = sum(1 for t in st.session_state.tasks if t["done"])

    st.markdown("---")
    st.metric("Progress", f"{completed}/{total}")
    st.progress(completed / total if total > 0 else 0)

    st.markdown("---")
    st.subheader("AI Study Plan")

    subject = st.text_input("Subject")

    hours = st.number_input(
        "Available hours today",
        min_value=1,
        max_value=12,
        value=2
    )

    if st.button("Generate Study Plan"):

        prompt = f"""
Create a study plan for this subject:

Subject: {subject}
Available time: {hours} hours

Make it practical.
Break it into time blocks.
Add revision and practice.
"""

        with st.spinner("Creating plan..."):
            plan = ask_ai(prompt)

        st.write(plan)

elif selected == "notes":

    st.title("📝 Notes Maker")

    topic = st.text_input("Enter topic for notes")

    note_type = st.selectbox(
        "Choose notes type",
        [
            "Short Notes",
            "Detailed Notes",
            "Exam Notes",
            "Viva Notes"
        ]
    )

    if st.button("Generate Notes"):

        prompt = f"""
Create {note_type} on this topic:

Topic: {topic}

Format:
1. Simple explanation
2. Important points
3. Example
4. Common mistakes
5. 5 viva questions

Use beginner-friendly language.
"""

        with st.spinner("Making notes..."):
            st.session_state.notes = ask_ai(prompt)

    if st.session_state.notes:
        st.write(st.session_state.notes)

elif selected == "resume":

    st.title("💼 Resume Project Helper")

    project_name = st.text_input("Project name")

    tech_stack = st.text_input(
        "Tech stack",
        placeholder="Python, Streamlit, Ollama, SQLite"
    )

    features = st.text_area(
        "Main features",
        placeholder="AI chat, PDF Q&A, quiz generator, planner..."
    )

    if st.button("Generate Resume Content"):

        prompt = f"""
Create professional resume content for this project.

Project name: {project_name}
Tech stack: {tech_stack}
Features: {features}

Give:
1. 3 resume bullet points
2. 2-line project explanation
3. Interview explanation
4. GitHub README description

Keep it impressive but realistic.
"""

        with st.spinner("Creating resume content..."):
            st.session_state.resume_answer = ask_ai(prompt)

    if st.session_state.resume_answer:
        st.write(st.session_state.resume_answer)

elif selected == "workspace":

    st.title("🚀 Workspace")

    st.subheader("Saved Projects")

    name = st.text_input("Project Name")

    if st.button("Save Project"):
        if name.strip():
            st.session_state.saved_projects.append(name)

            if st.session_state.memory_enabled:
                st.session_state.recent_activity.insert(
                    0,
                    f"Saved project: {name}"
                )
                st.session_state.recent_activity = st.session_state.recent_activity[:10]

            save_data()
            st.rerun()

    st.markdown("---")

    for i, project in enumerate(st.session_state.saved_projects):

        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            st.success(project)

        with col2:
            if st.button("⭐", key=f"fav_{i}"):
                st.session_state.favorite = project
                save_data()
                st.rerun()

        with col3:
            if st.button("Delete", key=f"project_del_{i}"):
                st.session_state.saved_projects.pop(i)
                save_data()
                st.rerun()

    st.markdown("---")

    st.subheader("Favorite")

    if st.session_state.favorite:
        st.info(st.session_state.favorite)
    else:
        st.write("No favorite selected")

elif selected == "profile":

    st.title("👤 Profile")

    if not st.session_state.logged_in:

        user = st.text_input("Username")

        if st.button("Login"):
            if user.strip():
                st.session_state.user = user
                st.session_state.logged_in = True
                st.rerun()

    else:

        st.success(f"Welcome {st.session_state.user}")

        st.subheader("Profile")
        st.write("Status: Active")
        st.write("Workspace Enabled")

        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.rerun()

elif selected == "export":

    st.title("📥 Export Center")

    topic = st.text_input("Enter topic to generate export content")

    export_type = st.selectbox(
        "Choose export type",
        [
            "Short Notes",
            "Detailed Explanation",
            "Resume Points",
            "Study Plan",
            "Project Summary"
        ]
    )

    if st.button("Generate Export Content"):

        prompt = f"""
Create {export_type} for this topic:

{topic}

Make it clean and well structured.
"""

        with st.spinner("Generating content..."):
            st.session_state.export_text = ask_ai(prompt)

    if st.session_state.export_text:

        st.write(st.session_state.export_text)

        st.download_button(
            label="⬇️ Download as TXT",
            data=st.session_state.export_text,
            file_name="ai_output.txt",
            mime="text/plain"
        )

elif selected == "image":

    st.title("🖼 AI Image Generator")

    prompt = st.text_input("Describe image")

    style = st.selectbox(
        "Choose style",
        [
            "Realistic",
            "Anime"
        ]
    )

    size = st.selectbox(
        "Image Size",
        [
            "512×512",
            "768×768",
            "1024×1024"
        ]
    )

    if st.button("Generate Image"):

        if prompt.strip() == "":
            st.warning("Enter prompt first")

        else:

            if style == "Anime":
                final_prompt = prompt + ", anime style"
            else:
                final_prompt = prompt + ", ultra realistic photo"

            if size == "512×512":
                w = 512
                h = 512
            elif size == "768×768":
                w = 768
                h = 768
            else:
                w = 1024
                h = 1024

            encoded = urllib.parse.quote(final_prompt)

            st.session_state.image_url = (
                f"https://image.pollinations.ai/prompt/{encoded}"
                f"?width={w}&height={h}"
            )

    if st.session_state.image_url:
        st.image(
            st.session_state.image_url,
            use_container_width=True
        )

elif selected == "notify":

    st.title("🔔 Daily Goal")

    goal = st.number_input(
        "Daily Goal in hours",
        min_value=1,
        max_value=20,
        value=st.session_state.daily_goal
    )

    if st.button("Save Goal"):
        st.session_state.daily_goal = goal
        save_data()
        st.success("Goal Updated")

    st.markdown("---")

    st.subheader("Today's Progress")

    progress = st.slider(
        "Hours Completed",
        0,
        st.session_state.daily_goal,
        st.session_state.study_done
    )

    if progress != st.session_state.study_done:
        st.session_state.study_done = progress
        save_data()

    percent = progress / st.session_state.daily_goal

    st.progress(percent)

    st.write(f"{progress}/{st.session_state.daily_goal} hours completed")

    st.markdown("---")

    if percent >= 1:
        st.success("Goal achieved 🎉")
    elif percent >= 0.7:
        st.info("Almost done 🚀")
    else:
        st.warning("Keep going 💪")

elif selected == "analytics":

    st.title("📈 Analytics")

    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(
        1 for task in st.session_state.tasks if task["done"]
    )
    pending_tasks = total_tasks - completed_tasks
    total_projects = len(st.session_state.saved_projects)
    activity_count = len(st.session_state.recent_activity)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Tasks", total_tasks)

    with col2:
        st.metric("Completed", completed_tasks)

    with col3:
        st.metric("Pending", pending_tasks)

    with col4:
        st.metric("Projects", total_projects)

    st.markdown("---")

    st.subheader("Task Completion")

    if total_tasks > 0:
        completion_rate = completed_tasks / total_tasks
        st.progress(completion_rate)
        st.write(f"{int(completion_rate * 100)}% completed")
    else:
        st.info("No tasks yet.")

    st.markdown("---")

    st.subheader("Daily Goal Progress")

    if st.session_state.daily_goal > 0:
        goal_progress = st.session_state.study_done / st.session_state.daily_goal
        st.progress(goal_progress)
        st.write(
            f"{st.session_state.study_done}/{st.session_state.daily_goal} hours completed"
        )

    st.markdown("---")

    st.subheader("Recent Activity")

    if st.session_state.memory_enabled:

        if activity_count > 0:
            for activity in st.session_state.recent_activity[:5]:
                st.info(activity)
        else:
            st.write("No recent activity yet.")

    else:
        st.warning("Memory is disabled.")
elif selected == "backup":

    st.title("☁️ Backup & Restore")

    st.subheader("Export Backup")

    backup_data = {
        "tasks": st.session_state.tasks,
        "saved_projects": st.session_state.saved_projects,
        "favorite": st.session_state.favorite,
        "theme": st.session_state.theme,
        "mobile": st.session_state.mobile,
        "compact": st.session_state.compact,
        "accent": st.session_state.accent,
        "daily_goal": st.session_state.daily_goal,
        "study_done": st.session_state.study_done,
        "recent_activity": st.session_state.recent_activity,
        "memory_enabled": st.session_state.memory_enabled
    }

    backup_json = json.dumps(
        backup_data,
        indent=4
    )

    st.download_button(
        "⬇️ Download Backup",
        data=backup_json,
        file_name="ai_os_backup.json",
        mime="application/json"
    )

    st.markdown("---")

    st.subheader("Restore Backup")

    uploaded_backup = st.file_uploader(
        "Upload backup JSON",
        type=["json"]
    )

    if uploaded_backup is not None:

        try:
            restored = json.load(uploaded_backup)

            if st.button("Restore Data"):

                st.session_state.tasks = restored.get("tasks", [])
                st.session_state.saved_projects = restored.get("saved_projects", [])
                st.session_state.favorite = restored.get("favorite", "")
                st.session_state.theme = restored.get("theme", "Dark")
                st.session_state.mobile = restored.get("mobile", False)
                st.session_state.compact = restored.get("compact", False)
                st.session_state.accent = restored.get("accent", "Blue")
                st.session_state.daily_goal = restored.get("daily_goal", 5)
                st.session_state.study_done = restored.get("study_done", 0)
                st.session_state.recent_activity = restored.get("recent_activity", [])
                st.session_state.memory_enabled = restored.get("memory_enabled", True)

                save_data()

                st.success("Backup restored successfully.")
                st.rerun()

        except:
            st.error("Invalid backup file.")

elif selected == "settings":

    st.title("⚙ Settings")

    theme = st.selectbox(
        "Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1
    )

    mobile = st.toggle(
        "📱 Mobile Mode",
        value=st.session_state.mobile
    )

    compact = st.toggle(
        "🧠 Compact Layout",
        value=st.session_state.compact
    )

    color = st.selectbox(
        "Accent",
        ["Blue", "Purple", "Green", "Red"],
        index=["Blue", "Purple", "Green", "Red"].index(st.session_state.accent)
    )

    memory = st.toggle(
        "Enable Memory",
        value=st.session_state.memory_enabled
    )

    if st.button("Apply Settings"):
        st.session_state.theme = theme
        st.session_state.mobile = mobile
        st.session_state.compact = compact
        st.session_state.accent = color
        st.session_state.memory_enabled = memory
        save_data()
        st.success("Settings Applied")
        st.rerun()

    st.markdown("---")
    st.write("Current Theme:", st.session_state.theme)
    st.write("Mobile Mode:", st.session_state.mobile)
    st.write("Compact Mode:", st.session_state.compact)
    st.write("Accent:", st.session_state.accent)
    st.write("Memory:", st.session_state.memory_enabled)

st.markdown("---")


st.caption(
"LearnSphere AI • Version 1.0 • Built with Streamlit"
)
