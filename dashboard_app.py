import streamlit as st
import pandas as pd

from datetime import datetime, timedelta, time, timezone
from zoneinfo import ZoneInfo
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Techloom Task",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM UI / STYLING
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #071a33;
    --navy-2: #0c2b50;
    --blue: #2563eb;
    --blue-soft: #eaf2ff;
    --cyan: #0ea5e9;
    --green: #10b981;
    --red: #ef4444;
    --amber: #f59e0b;
    --ink: #0f172a;
    --muted: #64748b;
    --line: #e5eaf1;
    --panel: rgba(255,255,255,.92);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
      radial-gradient(circle at 8% 5%, rgba(37,99,235,.08), transparent 28%),
      radial-gradient(circle at 92% 12%, rgba(14,165,233,.08), transparent 24%),
      #f7f9fc;
    color: var(--ink);
}

/* Keep content nicely centred */
.block-container {
    max-width: 1500px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background:
      radial-gradient(circle at 15% 0%, rgba(37,99,235,.30), transparent 28%),
      linear-gradient(180deg, #07162f 0%, #081f3e 58%, #06162d 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding: 1.15rem .85rem 1rem .85rem;
}

[data-testid="stSidebar"] * {
    color: #eef5ff;
}

.sidebar-logo {
    font-size: 23px;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: -.4px;
    margin-top: .35rem;
}

.sidebar-subtitle {
    font-size: 11px;
    color: #9fb4cf !important;
    letter-spacing: .15px;
    margin-top: 5px;
    margin-bottom: 22px;
}

/* Turn radio into navigation pills */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 4px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    width: 100%;
    border-radius: 11px;
    padding: 8px 10px;
    transition: all .16s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,.075);
    transform: translateX(2px);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: linear-gradient(90deg, rgba(37,99,235,.95), rgba(14,165,233,.78));
    box-shadow: 0 8px 22px rgba(0,0,0,.15);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
    display: none;
}

/* Titles */
.tech-title {
    font-size: clamp(30px, 3vw, 44px);
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: var(--ink);
    margin-bottom: 6px;
}

.tech-subtitle {
    font-size: 14px;
    color: var(--muted);
    margin-bottom: 24px;
}

.section-title {
    font-size: 20px;
    line-height: 1.2;
    font-weight: 750;
    color: var(--ink);
    letter-spacing: -.3px;
    margin-top: 12px;
    margin-bottom: 14px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid rgba(226,232,240,.95);
    padding: 18px 18px 16px 18px;
    border-radius: 18px;
    box-shadow: 0 10px 28px rgba(15,23,42,.055);
    min-height: 118px;
    transition: transform .15s ease, box-shadow .15s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 34px rgba(15,23,42,.085);
}

div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: #64748b;
    font-weight: 600;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #0f172a;
    font-weight: 780;
    letter-spacing: -.8px;
}

/* Task cards */
.task-card {
    background: var(--panel);
    padding: 18px 19px;
    border-radius: 16px;
    border: 1px solid var(--line);
    margin-bottom: 11px;
    box-shadow: 0 7px 22px rgba(15,23,42,.045);
}

.task-card-title {
    font-size: 16px;
    font-weight: 750;
    color: var(--ink);
    margin-bottom: 7px;
}

.task-meta {
    color: var(--muted);
    font-size: 12.5px;
    margin-top: 4px;
}

/* Buttons */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 11px !important;
    min-height: 42px;
    font-weight: 650;
    border: 1px solid #dfe6ef;
    box-shadow: none;
    transition: all .15s ease;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(15,23,42,.08);
}

button[kind="primary"] {
    background: linear-gradient(90deg, #2563eb, #0ea5e9) !important;
    border: none !important;
}

/* Inputs */
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div {
    border-radius: 11px !important;
    border-color: #dce3ec !important;
    background: rgba(255,255,255,.96) !important;
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(255,255,255,.92);
    border: 1px solid var(--line);
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(15,23,42,.035);
    margin-bottom: 10px;
}

/* Tables */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background: white;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--line);
}

/* Alerts */
[data-testid="stAlert"] {
    border-radius: 13px;
    border-width: 1px;
}

/* Divider */
hr {
    border-color: rgba(226,232,240,.85) !important;
}

/* Login */
.login-shell {
    min-height: 77vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-hero {
    padding: 34px 6px 20px 6px;
}

.login-kicker {
    display: inline-block;
    padding: 7px 11px;
    border-radius: 999px;
    background: #eaf2ff;
    color: #1d4ed8;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 14px;
}

.login-heading {
    font-size: clamp(36px, 4.8vw, 64px);
    line-height: 1.02;
    font-weight: 850;
    letter-spacing: -2.5px;
    color: #0b1930;
    max-width: 720px;
}

.login-copy {
    font-size: 15px;
    line-height: 1.7;
    color: #667085;
    max-width: 590px;
    margin-top: 18px;
}

.login-card-title {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 3px;
}

.login-card-copy {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 10px;
}

/* ------------------------------------------------------------
   READABILITY + SIDEBAR FIXES
   ------------------------------------------------------------ */

/* Strong, predictable sidebar contrast across Streamlit versions */
[data-testid="stSidebar"] {
    min-width: 300px;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #f8fbff;
}

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: #aebfd5 !important;
}

/* Navigation labels */
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    min-height: 42px;
    display: flex;
    align-items: center;
    padding: 9px 12px !important;
    margin: 2px 0;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #f8fbff !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    line-height: 1.25 !important;
}

/* Hide the native radio-circle indicator in multiple Streamlit DOM variants */
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child:not([data-testid="stMarkdownContainer"]),
[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child,
[data-testid="stSidebar"] input[type="radio"] {
    display: none !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
    color: #ffffff !important;
}

/* Logout must never become white-on-white */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: rgba(255,255,255,.075) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,.18) !important;
    box-shadow: none !important;
}

[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] .stButton > button span {
    color: #ffffff !important;
    font-weight: 650 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,.14) !important;
    border-color: rgba(255,255,255,.30) !important;
}

/* Better text contrast everywhere */
.stApp p,
.stApp label,
.stApp li {
    color: #334155;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #0f172a;
}

/* Inputs: dark typed text on white background */
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] input,
[data-baseweb="select"] div {
    color: #0f172a !important;
}

/* Ensure metric labels and values stay readable */
div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
    color: #53657a !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #0b1930 !important;
}

/* Cleaner alerts with stronger text */
[data-testid="stAlert"] p {
    color: #16324f !important;
    font-weight: 500;
}

/* Quick-overview info panels */
[data-testid="stAlert"] {
    box-shadow: 0 4px 16px rgba(15,23,42,.03);
}

/* Tables */
[data-testid="stDataFrame"] * {
    color: #24364b;
}

/* Small-screen refinement */
@media (max-width: 900px) {
    .block-container {
        padding-top: 1.25rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .tech-title {
        font-size: 30px;
    }
}

/* Hide Streamlit footer */
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SUPABASE
# ============================================================

@st.cache_resource
def get_supabase():

    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )


supabase = get_supabase()


# ============================================================
# SESSION
# ============================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "profile" not in st.session_state:
    st.session_state.profile = None


# ============================================================
# LOGIN
# ============================================================

def login(email, password):

    try:

        auth_result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_result.user

        profile_result = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", user.id)
            .execute()
        )

        if not profile_result.data:

            st.error(
                "Login succeeded, but no Techloom profile "
                "was found for this account."
            )

            return False

        st.session_state.user = user
        st.session_state.profile = profile_result.data[0]

        return True

    except Exception as error:

        st.error("Login failed.")

        st.write(error)

        return False


# ============================================================
# LOGOUT
# ============================================================

def logout():

    try:
        supabase.auth.sign_out()

    except Exception:
        pass

    st.session_state.user = None
    st.session_state.profile = None

    st.rerun()


# ============================================================
# LOGIN PAGE
# ============================================================

if st.session_state.user is None:

    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    hero, form_col = st.columns([1.55, 0.9], gap="large")

    with hero:
        st.markdown(
            """
            <div class="login-hero">
                <div class="login-kicker">TECHLOOM WORKSPACE</div>
                <div class="login-heading">One place to run the workday.</div>
                <div class="login-copy">
                    Manage tasks, approvals, marketplace operations and attendance
                    from one focused workspace built for the Techloom team.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        b1, b2, b3 = st.columns(3)
        b1.metric("Workspace", "Centralised")
        b2.metric("Team", "Connected")
        b3.metric("Access", "Secure")

    with form_col:
        st.markdown('<div class="login-card-title">Welcome back</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-card-copy">Sign in with your Techloom account.</div>', unsafe_allow_html=True)

        email = st.text_input("Email", placeholder="name@company.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Sign In →", type="primary", use_container_width=True):
            if not email or not password:
                st.warning("Please enter your email and password.")
            else:
                if login(email, password):
                    st.rerun()

        st.caption("🔒 Internal Techloom workspace")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()


# ============================================================
# CURRENT USER
# ============================================================

profile = st.session_state.profile

name = profile["name"]
role = profile["role"]
department = profile["department"]

current_user_id = st.session_state.user.id

PK_TZ = ZoneInfo("Asia/Karachi")


# ============================================================
# HELPERS
# ============================================================

def is_manager():

    return role in [
        "Admin",
        "Team Lead"
    ]


def load_all_tasks():

    try:

        result = (
            supabase
            .table("tasks")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data or []

    except Exception as error:

        st.error("Could not load tasks.")
        st.write(error)

        return []


def load_my_tasks():

    try:

        result = (
            supabase
            .table("tasks")
            .select("*")
            .eq(
                "assigned_to",
                name
            )
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return result.data or []

    except Exception as error:

        st.error("Could not load your tasks.")
        st.write(error)

        return []


def tasks_for_current_user():

    if is_manager():
        return load_all_tasks()

    return load_my_tasks()


def add_activity(
    task_id,
    action,
    details=""
):

    try:

        supabase.table(
            "task_activity"
        ).insert({
            "task_id": task_id,
            "user_id": current_user_id,
            "user_name": name,
            "action": action,
            "details": details
        }).execute()

    except Exception:
        # We don't want an activity-log problem
        # to stop the whole dashboard.
        pass


def update_task_status(
    task_id,
    status
):

    data = {
        "status": status,
        "updated_at": datetime.utcnow().isoformat()
    }

    if status == "Submitted for Review":

        data["submitted_at"] = (
            datetime.utcnow().isoformat()
        )

    if status == "Completed":

        data["completed_at"] = (
            datetime.utcnow().isoformat()
        )

    try:

        supabase.table(
            "tasks"
        ).update(
            data
        ).eq(
            "id",
            task_id
        ).execute()

        add_activity(
            task_id,
            "Status Updated",
            f"Changed status to {status}"
        )

        return True

    except Exception as error:

        st.error("Could not update task.")

        st.write(error)

        return False


# ============================================================
# ATTENDANCE HELPERS
# ============================================================

def pakistan_today():
    return datetime.now(PK_TZ).date().isoformat()


def parse_timestamp(value):
    if not value:
        return None

    try:
        parsed = datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        )

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed

    except Exception:
        return None


def format_pk_time(value):
    parsed = parse_timestamp(value)

    if parsed is None:
        return "--"

    return parsed.astimezone(PK_TZ).strftime("%I:%M %p")


def working_time(check_in, check_out=None):
    start = parse_timestamp(check_in)

    if start is None:
        return "--"

    if check_out:
        end = parse_timestamp(check_out)
    else:
        end = datetime.now(timezone.utc)

    if end is None:
        return "--"

    total_seconds = max(
        0,
        int((end - start).total_seconds())
    )

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60

    return f"{hours}h {minutes}m"


def get_today_attendance():
    try:
        result = (
            supabase
            .table("attendance")
            .select("*")
            .eq("user_id", current_user_id)
            .eq("attendance_date", pakistan_today())
            .limit(1)
            .execute()
        )

        if result.data:
            return result.data[0]

        return None

    except Exception as error:
        st.error("Could not load today's attendance.")
        st.write(error)
        return None


def check_in_employee():
    try:
        existing = get_today_attendance()

        if existing:
            return True

        supabase.table("attendance").insert({
            "user_id": current_user_id,
            "employee_name": name,
            "attendance_date": pakistan_today(),
            "check_in": datetime.now(timezone.utc).isoformat(),
            "status": "Present"
        }).execute()

        return True

    except Exception as error:
        st.error("Check-in failed.")
        st.write(error)
        return False


def check_out_employee():
    try:
        existing = get_today_attendance()

        if not existing:
            st.warning("Please check in first.")
            return False

        if existing.get("check_out"):
            return True

        supabase.table("attendance").update({
            "check_out": datetime.now(timezone.utc).isoformat()
        }).eq(
            "id",
            existing["id"]
        ).execute()

        return True

    except Exception as error:
        st.error("Check-out failed.")
        st.write(error)
        return False


def render_today_attendance():
    attendance = get_today_attendance()

    if attendance is None:
        st.info("You have not checked in today.")

        if st.button(
            "🟢 Check In Now",
            type="primary",
            use_container_width=True,
            key="dashboard_attendance_checkin"
        ):
            if check_in_employee():
                st.success("Check-in recorded successfully.")
                st.rerun()

        return

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Check In",
        format_pk_time(attendance.get("check_in"))
    )

    c2.metric(
        "Check Out",
        format_pk_time(attendance.get("check_out"))
    )

    c3.metric(
        "Working Time",
        working_time(
            attendance.get("check_in"),
            attendance.get("check_out")
        )
    )

    if not attendance.get("check_out"):
        if st.button(
            "🚪 Check Out",
            type="primary",
            use_container_width=True,
            key="dashboard_attendance_checkout"
        ):
            if check_out_employee():
                st.success("Check-out recorded successfully.")
                st.rerun()
    else:
        st.success("Attendance completed for today.")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">'
        '◈ TECHLOOM TASK'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Work Smart. Stay Organized.'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(f"### {name}")

    st.caption(role)
    st.caption(department)

    st.divider()

    # ----------------------------
    # AIFA / MANAGEMENT
    # ----------------------------

    if is_manager():

        menu_options = [
            "🏠 Dashboard",
            "📋 Team Tasks",
            "➕ Create Task",
            "✅ Approvals",
            "👥 Team Overview",
            "⏱ Attendance",
            "📅 Attendance Report",
            "🛡 Compliance",
            "📜 Activity"
        ]

    # ----------------------------
    # TALHA
    # ----------------------------

    elif name == "Talha":

        menu_options = [
            "🏠 Dashboard",
            "📋 My Tasks",
            "⏱ Attendance",
            "🟠 Temu",
            "🛡 Compliance",
            "📨 Appeals",
            "💬 Seller Support",
            "📜 Activity"
        ]

    # ----------------------------
    # JUNAID
    # ----------------------------

    elif name == "Junaid":

        menu_options = [
            "🏠 Dashboard",
            "📋 My Tasks",
            "⏱ Attendance",
            "🛒 Amazon",
            "🛍 eBay",
            "📦 Listing Uploads",
            "📜 Activity"
        ]

    # ----------------------------
    # NABIHA
    # ----------------------------

    elif name == "Nabiha":

        menu_options = [
            "🏠 Dashboard",
            "📋 My Tasks",
            "⏱ Attendance",
            "📜 Activity"
        ]

    else:

        menu_options = [
            "🏠 Dashboard",
            "📋 My Tasks",
            "⏱ Attendance"
        ]

    page = st.radio(
        "Navigation",
        menu_options,
        label_visibility="collapsed"
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        f'<div class="tech-title">'
        f'Welcome, {name} 👋'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="tech-subtitle">'
        f'{department} • {role}'
        f'</div>',
        unsafe_allow_html=True
    )

    tasks = tasks_for_current_user()

    total_count = len(tasks)

    new_count = 0
    progress_count = 0
    review_count = 0
    changes_count = 0
    completed_count = 0

    for task in tasks:

        status = task.get(
            "status",
            ""
        )

        if status == "New":
            new_count += 1

        elif status == "In Progress":
            progress_count += 1

        elif status == "Submitted for Review":
            review_count += 1

        elif status == "Changes Requested":
            changes_count += 1

        elif status in [
            "Completed",
            "Approved"
        ]:
            completed_count += 1

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    c1.metric(
        "📋 Total Tasks",
        total_count
    )

    c2.metric(
        "🆕 New",
        new_count
    )

    c3.metric(
        "🕒 In Progress",
        progress_count
    )

    c4.metric(
        "📤 For Review",
        review_count
    )

    c5.metric(
        "🔄 Changes",
        changes_count
    )

    c6.metric(
        "✅ Done",
        completed_count
    )

    st.write("")

    st.markdown(
        '<div class="section-title">'
        'Today\'s Attendance'
        '</div>',
        unsafe_allow_html=True
    )

    render_today_attendance()

    st.write("")

    left, right = st.columns(
        [2.7, 1]
    )

    # --------------------------------------------------------
    # RECENT TASKS
    # --------------------------------------------------------

    with left:

        st.markdown(
            '<div class="section-title">'
            'Recent Tasks'
            '</div>',
            unsafe_allow_html=True
        )

        if not tasks:

            st.info(
                "No tasks available."
            )

        else:

            for task in tasks[:7]:

                title = task.get(
                    "title",
                    "Untitled Task"
                )

                platform = task.get(
                    "platform",
                    "N/A"
                )

                task_type = task.get(
                    "task_type",
                    "Task"
                )

                assigned_to = task.get(
                    "assigned_to",
                    "N/A"
                )

                priority = task.get(
                    "priority",
                    "Normal"
                )

                status = task.get(
                    "status",
                    "New"
                )

                task_html = (
                    '<div class="task-card">'
                    f'<div class="task-card-title">{title}</div>'
                    f'<div class="task-meta">{platform} &nbsp; • &nbsp; '
                    f'{task_type} &nbsp; • &nbsp; Assigned to: {assigned_to}</div>'
                    f'<div class="task-meta">Priority: <b>{priority}</b> '
                    f'&nbsp; • &nbsp; Status: <b>{status}</b></div>'
                    '</div>'
                )

                st.markdown(
                    task_html,
                    unsafe_allow_html=True
                )

    # --------------------------------------------------------
    # QUICK OVERVIEW
    # --------------------------------------------------------

    with right:

        st.markdown(
            '<div class="section-title">'
            'Quick Overview'
            '</div>',
            unsafe_allow_html=True
        )

        st.info(
            f"🕒 Active tasks: "
            f"{new_count + progress_count}"
        )

        st.info(
            f"📤 Waiting review: "
            f"{review_count}"
        )

        st.info(
            f"🔄 Changes requested: "
            f"{changes_count}"
        )

        st.success(
            f"✅ Completed / Approved: "
            f"{completed_count}"
        )


# ============================================================
# MY TASKS / TEAM TASKS
# ============================================================

elif page in [
    "📋 My Tasks",
    "📋 Team Tasks"
]:

    if page == "📋 Team Tasks":

        st.markdown(
            '<div class="tech-title">'
            'Team Tasks'
            '</div>',
            unsafe_allow_html=True
        )

        tasks = load_all_tasks()

    else:

        st.markdown(
            '<div class="tech-title">'
            'My Tasks'
            '</div>',
            unsafe_allow_html=True
        )

        tasks = load_my_tasks()

    st.markdown(
        '<div class="tech-subtitle">'
        'Search, review and update assigned work.'
        '</div>',
        unsafe_allow_html=True
    )

    if not tasks:

        st.info("No tasks found.")
        st.stop()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    f1, f2, f3, f4 = st.columns(4)

    with f1:

        search = st.text_input(
            "Search",
            placeholder="Title, SKU, Goods ID..."
        )

    with f2:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "New",
                "In Progress",
                "Waiting on Information",
                "Waiting on Platform",
                "Submitted for Review",
                "Changes Requested",
                "Approved",
                "Completed"
            ]
        )

    with f3:

        platform_filter = st.selectbox(
            "Platform",
            [
                "All",
                "Temu",
                "Amazon",
                "eBay",
                "TikTok",
                "Multiple"
            ]
        )

    with f4:

        priority_filter = st.selectbox(
            "Priority",
            [
                "All",
                "Low",
                "Normal",
                "High",
                "Urgent"
            ]
        )

    # --------------------------------------------------------
    # TASK CARDS
    # --------------------------------------------------------

    visible_tasks = []

    for task in tasks:

        searchable = " ".join([
            str(task.get("title", "")),
            str(task.get("goods_id", "")),
            str(task.get("platform", "")),
            str(task.get("task_type", "")),
            str(task.get("assigned_to", ""))
        ]).lower()

        if (
            search
            and search.lower() not in searchable
        ):
            continue

        if (
            status_filter != "All"
            and task.get("status")
            != status_filter
        ):
            continue

        if (
            platform_filter != "All"
            and task.get("platform")
            != platform_filter
        ):
            continue

        if (
            priority_filter != "All"
            and task.get("priority")
            != priority_filter
        ):
            continue

        visible_tasks.append(task)

    st.caption(
        f"{len(visible_tasks)} task(s) shown"
    )

    for task in visible_tasks:

        task_id = task["id"]

        title = task.get(
            "title",
            "Untitled Task"
        )

        status = task.get(
            "status",
            "New"
        )

        priority = task.get(
            "priority",
            "Normal"
        )

        with st.expander(
            f"{title}  •  {status}  •  {priority}"
        ):

            left, right = st.columns(
                [2, 1]
            )

            with left:

                st.write(
                    "**Platform:**",
                    task.get(
                        "platform",
                        ""
                    )
                )

                st.write(
                    "**Task Type:**",
                    task.get(
                        "task_type",
                        ""
                    )
                )

                st.write(
                    "**Assigned To:**",
                    task.get(
                        "assigned_to",
                        ""
                    )
                )

                st.write(
                    "**Assigned By:**",
                    task.get(
                        "assigned_by",
                        ""
                    )
                )

                st.write(
                    "**Priority:**",
                    priority
                )

                st.write(
                    "**Goods ID / ASIN / SKU:**",
                    task.get(
                        "goods_id",
                        ""
                    )
                )

                supplier_link = task.get(
                    "supplier_link",
                    ""
                )

                if supplier_link:

                    st.write(
                        "**Supplier Link:**"
                    )

                    st.write(
                        supplier_link
                    )

                listing_url = task.get(
                    "listing_url",
                    ""
                )

                if listing_url:

                    st.write(
                        "**Listing URL:**"
                    )

                    st.write(
                        listing_url
                    )

                st.write(
                    "**Instructions:**"
                )

                st.write(
                    task.get(
                        "description",
                        ""
                    )
                )

                review_notes = task.get(
                    "review_notes",
                    ""
                )

                if review_notes:

                    st.warning(
                        f"Review Notes: "
                        f"{review_notes}"
                    )

            # ------------------------------------------------
            # STATUS CONTROLS
            # ------------------------------------------------

            with right:

                st.write(
                    f"**Current Status:** "
                    f"{status}"
                )

                allowed_statuses = [
                    "New",
                    "In Progress",
                    "Waiting on Information",
                    "Waiting on Platform",
                    "Submitted for Review",
                    "Completed"
                ]

                if is_manager():

                    allowed_statuses.extend([
                        "Changes Requested",
                        "Approved"
                    ])

                if (
                    status in allowed_statuses
                ):

                    status_index = (
                        allowed_statuses.index(
                            status
                        )
                    )

                else:

                    status_index = 0

                new_status = st.selectbox(
                    "Update Status",
                    allowed_statuses,
                    index=status_index,
                    key=f"status_{task_id}"
                )

                if st.button(
                    "Save Status",
                    key=f"save_{task_id}",
                    use_container_width=True
                ):

                    if update_task_status(
                        task_id,
                        new_status
                    ):

                        st.success(
                            "Task status updated."
                        )

                        st.rerun()

                if (
                    not is_manager()
                    and status
                    != "Submitted for Review"
                ):

                    if st.button(
                        "📤 Submit for Review",
                        key=f"submit_{task_id}",
                        use_container_width=True
                    ):

                        if update_task_status(
                            task_id,
                            "Submitted for Review"
                        ):

                            st.success(
                                "Submitted for review."
                            )

                            st.rerun()


# ============================================================
# CREATE TASK
# ============================================================

elif page == "➕ Create Task":

    if not is_manager():

        st.error(
            "You do not have permission "
            "to create tasks."
        )

        st.stop()

    st.markdown(
        '<div class="tech-title">'
        'Create New Task'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tech-subtitle">'
        'Assign work to a team member.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form(
        "create_task_form"
    ):

        task_title = st.text_input(
            "Task Title"
        )

        c1, c2 = st.columns(2)

        with c1:

            task_type = st.selectbox(
                "Task Type",
                [
                    "New Listing",
                    "Listing Upload",
                    "Listing Update",
                    "Image Generation",
                    "Compliance",
                    "Appeal",
                    "Seller Support Case",
                    "Product Research",
                    "Other"
                ]
            )

            platform = st.selectbox(
                "Platform",
                [
                    "Temu",
                    "Amazon",
                    "eBay",
                    "TikTok",
                    "Multiple"
                ]
            )

            assigned_to = st.selectbox(
                "Assign To",
                [
                    "Talha",
                    "Junaid",
                    "Nabiha",
                    "AIFA"
                ]
            )

            priority = st.selectbox(
                "Priority",
                [
                    "Low",
                    "Normal",
                    "High",
                    "Urgent"
                ]
            )

        with c2:

            supplier_price = st.number_input(
                "Supplier Price",
                min_value=0.0,
                step=0.10
            )

            selling_price = st.number_input(
                "Selling Price",
                min_value=0.0,
                step=0.10
            )

            due_date = st.date_input(
                "Due Date",
                value=(
                    datetime.today()
                    + timedelta(days=1)
                )
            )

        supplier_link = st.text_input(
            "Supplier Link"
        )

        goods_id = st.text_input(
            "Goods ID / ASIN / SKU"
        )

        instructions = st.text_area(
            "Task Instructions",
            height=140
        )

        submit_task = st.form_submit_button(
            "Assign Task",
            type="primary",
            use_container_width=True
        )

        if submit_task:

            if not task_title:

                st.error(
                    "Please enter a task title."
                )

            else:

                due_datetime = datetime.combine(
                    due_date,
                    time(
                        hour=17,
                        minute=0
                    )
                )

                task_data = {
                    "title": task_title,
                    "description": instructions,
                    "task_type": task_type,
                    "platform": platform,
                    "priority": priority,
                    "status": "New",
                    "assigned_to": assigned_to,
                    "assigned_by": name,
                    "supplier_link": supplier_link,
                    "supplier_price": supplier_price,
                    "selling_price": selling_price,
                    "goods_id": goods_id,
                    "due_date":
                    due_datetime.isoformat(),
                    "updated_at":
                    datetime.utcnow().isoformat()
                }

                try:

                    result = (
                        supabase
                        .table("tasks")
                        .insert(
                            task_data
                        )
                        .execute()
                    )

                    if result.data:

                        new_task_id = (
                            result.data[0]["id"]
                        )

                        add_activity(
                            new_task_id,
                            "Task Created",
                            f"Assigned to "
                            f"{assigned_to}"
                        )

                    st.success(
                        f"Task assigned to "
                        f"{assigned_to}."
                    )

                    st.rerun()

                except Exception as error:

                    st.error(
                        "Could not create task."
                    )

                    st.write(error)


# ============================================================
# APPROVALS
# ============================================================

elif page == "✅ Approvals":

    if not is_manager():

        st.error(
            "Management access only."
        )

        st.stop()

    st.markdown(
        '<div class="tech-title">'
        'Approvals'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tech-subtitle">'
        'Review work submitted by the team.'
        '</div>',
        unsafe_allow_html=True
    )

    try:

        result = (
            supabase
            .table("tasks")
            .select("*")
            .eq(
                "status",
                "Submitted for Review"
            )
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        approval_tasks = (
            result.data or []
        )

    except Exception as error:

        st.error(error)

        approval_tasks = []

    if not approval_tasks:

        st.info(
            "No tasks are currently "
            "waiting for approval."
        )

    for task in approval_tasks:

        task_id = task["id"]

        with st.expander(
            f"{task.get('title', '')} "
            f"• {task.get('assigned_to', '')}"
        ):

            st.write(
                "**Platform:**",
                task.get(
                    "platform",
                    ""
                )
            )

            st.write(
                "**Task Type:**",
                task.get(
                    "task_type",
                    ""
                )
            )

            st.write(
                "**Instructions:**"
            )

            st.write(
                task.get(
                    "description",
                    ""
                )
            )

            notes = st.text_area(
                "Review Notes",
                key=f"review_{task_id}"
            )

            approve_col, changes_col = (
                st.columns(2)
            )

            with approve_col:

                if st.button(
                    "✅ Approve",
                    key=f"approve_{task_id}",
                    use_container_width=True
                ):

                    try:

                        supabase.table(
                            "tasks"
                        ).update({
                            "status": "Approved",
                            "review_notes": notes,
                            "updated_at":
                            datetime.utcnow()
                            .isoformat()
                        }).eq(
                            "id",
                            task_id
                        ).execute()

                        add_activity(
                            task_id,
                            "Task Approved",
                            notes
                        )

                        st.success(
                            "Task approved."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(error)

            with changes_col:

                if st.button(
                    "🔄 Request Changes",
                    key=f"changes_{task_id}",
                    use_container_width=True
                ):

                    try:

                        supabase.table(
                            "tasks"
                        ).update({
                            "status":
                            "Changes Requested",
                            "review_notes":
                            notes,
                            "updated_at":
                            datetime.utcnow()
                            .isoformat()
                        }).eq(
                            "id",
                            task_id
                        ).execute()

                        add_activity(
                            task_id,
                            "Changes Requested",
                            notes
                        )

                        st.success(
                            "Changes requested."
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(error)


# ============================================================
# ATTENDANCE
# ============================================================

elif page == "⏱ Attendance":

    st.markdown(
        '<div class="tech-title">'
        'Attendance'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tech-subtitle">'
        'Check in when you arrive and check out when you leave.'
        '</div>',
        unsafe_allow_html=True
    )

    attendance = get_today_attendance()

    if attendance is None:

        st.info("You have not checked in today.")

        if st.button(
            "🟢 CHECK IN",
            type="primary",
            use_container_width=True,
            key="attendance_page_checkin"
        ):

            if check_in_employee():
                st.success("Check-in recorded successfully.")
                st.rerun()

    else:

        a1, a2, a3 = st.columns(3)

        a1.metric(
            "🟢 Check In",
            format_pk_time(
                attendance.get("check_in")
            )
        )

        a2.metric(
            "🔴 Check Out",
            format_pk_time(
                attendance.get("check_out")
            )
        )

        a3.metric(
            "⏱ Working Time",
            working_time(
                attendance.get("check_in"),
                attendance.get("check_out")
            )
        )

        if not attendance.get("check_out"):

            if st.button(
                "🚪 CHECK OUT",
                type="primary",
                use_container_width=True,
                key="attendance_page_checkout"
            ):

                if check_out_employee():
                    st.success("Check-out recorded successfully.")
                    st.rerun()

        else:

            st.success(
                "Today's attendance is complete."
            )

    st.write("")
    st.subheader("My Attendance History")

    try:

        history_result = (
            supabase
            .table("attendance")
            .select("*")
            .eq("user_id", current_user_id)
            .order(
                "attendance_date",
                desc=True
            )
            .limit(60)
            .execute()
        )

        history = history_result.data or []

        history_rows = []

        for record in history:

            history_rows.append({
                "Date":
                    record.get("attendance_date"),

                "Check In":
                    format_pk_time(
                        record.get("check_in")
                    ),

                "Check Out":
                    format_pk_time(
                        record.get("check_out")
                    ),

                "Working Time":
                    working_time(
                        record.get("check_in"),
                        record.get("check_out")
                    ),

                "Status":
                    record.get(
                        "status",
                        "Present"
                    )
            })

        if history_rows:

            st.dataframe(
                pd.DataFrame(history_rows),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No attendance history yet."
            )

    except Exception as error:

        st.error(
            "Could not load attendance history."
        )

        st.write(error)


# ============================================================
# ATTENDANCE REPORT
# ============================================================

elif page == "📅 Attendance Report":

    if not is_manager():

        st.error(
            "Management access only."
        )

        st.stop()

    st.markdown(
        '<div class="tech-title">'
        'Attendance Report'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tech-subtitle">'
        'View daily attendance for the Techloom team.'
        '</div>',
        unsafe_allow_html=True
    )

    selected_date = st.date_input(
        "Attendance Date",
        value=datetime.now(PK_TZ).date()
    )

    try:

        result = (
            supabase
            .table("attendance")
            .select("*")
            .eq(
                "attendance_date",
                selected_date.isoformat()
            )
            .order("employee_name")
            .execute()
        )

        records = result.data or []

        present_count = len(records)

        working_now_count = sum(
            1
            for record in records
            if record.get("check_in")
            and not record.get("check_out")
        )

        checked_out_count = sum(
            1
            for record in records
            if record.get("check_out")
        )

        r1, r2, r3 = st.columns(3)

        r1.metric(
            "🟢 Present",
            present_count
        )

        r2.metric(
            "🕒 Working Now",
            working_now_count
        )

        r3.metric(
            "🚪 Checked Out",
            checked_out_count
        )

        report_rows = []

        for record in records:

            report_rows.append({
                "Employee":
                    record.get("employee_name"),

                "Date":
                    record.get("attendance_date"),

                "Check In":
                    format_pk_time(
                        record.get("check_in")
                    ),

                "Check Out":
                    format_pk_time(
                        record.get("check_out")
                    ),

                "Working Time":
                    working_time(
                        record.get("check_in"),
                        record.get("check_out")
                    ),

                "Status":
                    record.get(
                        "status",
                        "Present"
                    )
            })

        if report_rows:

            st.dataframe(
                pd.DataFrame(report_rows),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No attendance records for this date."
            )

    except Exception as error:

        st.error(
            "Could not load attendance report."
        )

        st.write(error)


# ============================================================
# TEAM OVERVIEW
# ============================================================

elif page == "👥 Team Overview":

    if not is_manager():

        st.error(
            "Management access only."
        )

        st.stop()

    st.markdown(
        '<div class="tech-title">'
        'Team Overview'
        '</div>',
        unsafe_allow_html=True
    )

    tasks = load_all_tasks()

    members = [
        "Talha",
        "Junaid",
        "Nabiha",
        "AIFA"
    ]

    member_columns = st.columns(
        len(members)
    )

    for index, member in enumerate(
        members
    ):

        member_tasks = [
            task
            for task in tasks
            if task.get("assigned_to")
            == member
        ]

        active_tasks = [
            task
            for task in member_tasks
            if task.get("status")
            not in [
                "Completed",
                "Approved"
            ]
        ]

        with member_columns[index]:

            st.metric(
                member,
                len(active_tasks),
                f"{len(member_tasks)} total"
            )

    st.write("")

    if tasks:

        team_df = pd.DataFrame(tasks)

        if (
            "assigned_to"
            in team_df.columns
            and "status"
            in team_df.columns
        ):

            summary = (
                team_df
                .groupby([
                    "assigned_to",
                    "status"
                ])
                .size()
                .reset_index(
                    name="Tasks"
                )
            )

            st.subheader(
                "Workload by Status"
            )

            st.dataframe(
                summary,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# PLATFORM FILTER PAGES
# ============================================================

elif page in [
    "🟠 Temu",
    "🛒 Amazon",
    "🛍 eBay"
]:

    platform_name = (
        page.split(
            " ",
            1
        )[1]
    )

    st.markdown(
        f'<div class="tech-title">'
        f'{platform_name}'
        f'</div>',
        unsafe_allow_html=True
    )

    tasks = load_my_tasks()

    platform_tasks = [
        task
        for task in tasks
        if task.get("platform")
        == platform_name
    ]

    if not platform_tasks:

        st.info(
            f"No {platform_name} "
            f"tasks assigned."
        )

    else:

        for task in platform_tasks:

            st.markdown(
                f"""
                <div class="task-card">

                    <div class="task-card-title">
                        {task.get("title", "")}
                    </div>

                    <div class="task-meta">
                        {task.get("task_type", "")}
                        &nbsp; • &nbsp;
                        {task.get("priority", "")}
                    </div>

                    <div class="task-meta">
                        Status:
                        <b>
                            {task.get("status", "")}
                        </b>
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# LISTING UPLOADS
# ============================================================

elif page == "📦 Listing Uploads":

    st.markdown(
        '<div class="tech-title">'
        'Listing Uploads'
        '</div>',
        unsafe_allow_html=True
    )

    tasks = load_my_tasks()

    listing_tasks = [
        task
        for task in tasks
        if task.get("task_type")
        in [
            "New Listing",
            "Listing Upload",
            "Listing Update"
        ]
    ]

    if not listing_tasks:

        st.info(
            "No listing upload tasks."
        )

    else:

        for task in listing_tasks:

            st.markdown(
                f"""
                <div class="task-card">

                    <div class="task-card-title">
                        {task.get("title", "")}
                    </div>

                    <div class="task-meta">
                        {task.get("platform", "")}
                        &nbsp; • &nbsp;
                        {task.get("status", "")}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# COMPLIANCE
# ============================================================

elif page in [
    "🛡 Compliance",
    "🛡 Compliance Overview"
]:

    st.markdown(
        '<div class="tech-title">'
        'Compliance'
        '</div>',
        unsafe_allow_html=True
    )

    if is_manager():
        source_tasks = load_all_tasks()

    else:
        source_tasks = load_my_tasks()

    compliance_tasks = [
        task
        for task in source_tasks
        if task.get("task_type")
        in [
            "Compliance",
            "Appeal",
            "Seller Support Case"
        ]
    ]

    if not compliance_tasks:

        st.info(
            "No compliance tasks."
        )

    else:

        compliance_df = pd.DataFrame(
            compliance_tasks
        )

        st.dataframe(
            compliance_df,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# APPEALS
# ============================================================

elif page == "📨 Appeals":

    st.markdown(
        '<div class="tech-title">'
        'Appeals'
        '</div>',
        unsafe_allow_html=True
    )

    tasks = load_my_tasks()

    appeal_tasks = [
        task
        for task in tasks
        if task.get("task_type")
        == "Appeal"
    ]

    if not appeal_tasks:

        st.info(
            "No appeal tasks."
        )

    else:

        for task in appeal_tasks:

            st.markdown(
                f"""
                <div class="task-card">

                    <div class="task-card-title">
                        {task.get("title", "")}
                    </div>

                    <div class="task-meta">
                        Goods ID:
                        {task.get("goods_id", "")}
                    </div>

                    <div class="task-meta">
                        Status:
                        {task.get("status", "")}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# SELLER SUPPORT
# ============================================================

elif page == "💬 Seller Support":

    st.markdown(
        '<div class="tech-title">'
        'Seller Support'
        '</div>',
        unsafe_allow_html=True
    )

    tasks = load_my_tasks()

    support_tasks = [
        task
        for task in tasks
        if task.get("task_type")
        == "Seller Support Case"
    ]

    if not support_tasks:

        st.info(
            "No Seller Support cases."
        )

    else:

        for task in support_tasks:

            st.markdown(
                f"""
                <div class="task-card">

                    <div class="task-card-title">
                        {task.get("title", "")}
                    </div>

                    <div class="task-meta">
                        Case ID:
                        {task.get("case_id", "")}
                    </div>

                    <div class="task-meta">
                        Status:
                        {task.get("status", "")}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# ACTIVITY
# ============================================================

elif page == "📜 Activity":

    st.markdown(
        '<div class="tech-title">'
        'Recent Activity'
        '</div>',
        unsafe_allow_html=True
    )

    try:

        result = (
            supabase
            .table("task_activity")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .limit(100)
            .execute()
        )

        activities = (
            result.data or []
        )

    except Exception as error:

        st.error(
            "Could not load activity."
        )

        st.write(error)

        activities = []

    if not activities:

        st.info(
            "No activity recorded yet."
        )

    else:

        for activity in activities:

            st.markdown(
                f"""
                <div class="task-card">

                    <div class="task-card-title">
                        {activity.get(
                            "user_name",
                            "User"
                        )}
                        —
                        {activity.get(
                            "action",
                            ""
                        )}
                    </div>

                    <div class="task-meta">
                        {activity.get(
                            "details",
                            ""
                        )}
                    </div>

                    <div class="task-meta">
                        {activity.get(
                            "created_at",
                            ""
                        )}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )
