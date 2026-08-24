import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components
import extra_streamlit_components as stx

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


# ============================================================
# PREMIUM UI / STYLING  (colored sidebar + white content area)
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --teal: #0f766e;
    --teal-light: #14b8a6;
    --amber: #d97706;
    --amber-soft: #fef3e2;
    --green: #059669;
    --red: #dc2626;
    --ink: #1e2333;
    --muted: #6b7280;
    --line: #e6e8ee;
    --panel: #ffffff;
    --page-bg: #ffffff;
    --sidebar-bg: #0f766e;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ------------------------------------------------------------
   APP BACKGROUND — clean white content area
   ------------------------------------------------------------ */
.stApp {
    background: var(--page-bg);
    color: var(--ink);
}

.block-container {
    max-width: 1460px;
    padding-top: 2.1rem;
    padding-bottom: 3rem;
}

/* ------------------------------------------------------------
   SIDEBAR — solid teal, white text, the colorful anchor of the UI
   ------------------------------------------------------------ */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg);
    border-right: none;
    min-width: 296px;
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding: 1.3rem .95rem 1rem .95rem;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div {
    color: #ffffff;
}

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
    color: rgba(255,255,255,.72) !important;
}

.sidebar-logo {
    font-size: 21px;
    line-height: 1.2;
    font-weight: 800;
    letter-spacing: -.3px;
    color: #ffffff;
    margin-top: .3rem;
}

.sidebar-subtitle {
    font-size: 11.5px;
    color: rgba(255,255,255,.72) !important;
    letter-spacing: .15px;
    margin-top: 4px;
    margin-bottom: 18px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(255,255,255,.18);
}

/* Turn radio into clean, tappable navigation rows */
[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 2px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    width: 100%;
    min-height: 44px;
    display: flex;
    align-items: center;
    border-radius: 9px;
    padding: 10px 12px !important;
    margin: 1px 0;
    background: transparent;
    transition: all .14s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,.10);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: rgba(255,255,255,.88) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    line-height: 1.25 !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #ffffff;
    box-shadow: 0 4px 12px rgba(0,0,0,.12);
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
    color: var(--teal) !important;
    font-weight: 700 !important;
}

/* Hide the native radio-circle indicator across Streamlit DOM variants */
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child:not([data-testid="stMarkdownContainer"]),
[data-testid="stSidebar"] [data-baseweb="radio"] > div:first-child,
[data-testid="stSidebar"] input[type="radio"] {
    display: none !important;
}

/* Sidebar buttons (Logout) */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: rgba(255,255,255,.10) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255,255,255,.28) !important;
    box-shadow: none !important;
    margin-top: 6px;
}

[data-testid="stSidebar"] .stButton > button p,
[data-testid="stSidebar"] .stButton > button span {
    color: #ffffff !important;
    font-weight: 650 !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,.18) !important;
    border-color: rgba(255,255,255,.42) !important;
}

/* ------------------------------------------------------------
   TITLES & TEXT (main content — white background)
   ------------------------------------------------------------ */
.tech-title {
    font-size: clamp(26px, 2.6vw, 36px);
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -.8px;
    color: var(--ink);
    margin-bottom: 4px;
}

.tech-subtitle {
    font-size: 14px;
    color: var(--muted);
    margin-bottom: 22px;
}

.section-title {
    font-size: 17px;
    line-height: 1.2;
    font-weight: 700;
    color: var(--ink);
    letter-spacing: -.2px;
    margin-top: 10px;
    margin-bottom: 12px;
}

.stApp p,
.stApp label,
.stApp li {
    color: #3d4356;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: var(--ink);
}

/* ------------------------------------------------------------
   METRIC CARDS
   ------------------------------------------------------------ */
div[data-testid="stMetric"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-top: 3px solid var(--teal);
    padding: 16px 18px 14px 18px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(30,35,51,.05);
    min-height: 104px;
    transition: box-shadow .15s ease;
}

div[data-testid="stMetric"]:hover {
    box-shadow: 0 6px 16px rgba(30,35,51,.08);
}

div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {
    color: var(--muted) !important;
    font-weight: 600;
    font-size: 12.5px;
    text-transform: uppercase;
    letter-spacing: .3px;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--ink) !important;
    font-weight: 780;
    letter-spacing: -.6px;
}

/* ------------------------------------------------------------
   TASK CARDS — left accent bar in amber for contrast against teal nav
   ------------------------------------------------------------ */
.task-card {
    background: var(--panel);
    padding: 14px 18px 14px 16px;
    border-radius: 10px;
    border: 1px solid var(--line);
    border-left: 4px solid var(--amber);
    margin-bottom: 9px;
    box-shadow: 0 1px 3px rgba(30,35,51,.04);
    transition: box-shadow .15s ease;
}

.task-card:hover {
    box-shadow: 0 6px 16px rgba(30,35,51,.07);
}

.task-card-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 5px;
}

.task-meta {
    color: var(--muted);
    font-size: 12.5px;
    margin-top: 3px;
}

/* ------------------------------------------------------------
   BUTTONS
   ------------------------------------------------------------ */
.stButton > button, .stFormSubmitButton > button {
    border-radius: 8px !important;
    min-height: 42px;
    font-weight: 650;
    border: 1px solid #dfe2ea;
    box-shadow: none;
    transition: all .14s ease;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    border-color: #c7cbdb;
    box-shadow: 0 4px 12px rgba(30,35,51,.06);
}

button[kind="primary"] {
    background: var(--teal) !important;
    border: none !important;
}

button[kind="primary"]:hover {
    background: #0c5f58 !important;
}

/* ------------------------------------------------------------
   INPUTS
   ------------------------------------------------------------ */
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div {
    border-radius: 8px !important;
    border-color: #dde0e8 !important;
    background: #ffffff !important;
}

[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] input,
[data-baseweb="select"] div {
    color: var(--ink) !important;
}

[data-baseweb="input"] > div:focus-within,
[data-baseweb="textarea"] > div:focus-within,
[data-baseweb="select"] > div:focus-within {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(15,118,110,.14) !important;
}

/* ------------------------------------------------------------
   EXPANDERS
   ------------------------------------------------------------ */
[data-testid="stExpander"] {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(30,35,51,.03);
    margin-bottom: 10px;
}

/* ------------------------------------------------------------
   TABLES
   ------------------------------------------------------------ */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background: #ffffff;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--line);
}

[data-testid="stDataFrame"] * {
    color: #2c3142;
}

/* ------------------------------------------------------------
   ALERTS
   ------------------------------------------------------------ */
[data-testid="stAlert"] {
    border-radius: 10px;
    border-width: 1px;
    box-shadow: 0 1px 3px rgba(30,35,51,.03);
}

[data-testid="stAlert"] p {
    color: #1e2333 !important;
    font-weight: 500;
}

/* ------------------------------------------------------------
   TABS (if used)
   ------------------------------------------------------------ */
button[data-baseweb="tab"] {
    font-weight: 600;
    color: var(--muted);
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--teal) !important;
}

[data-baseweb="tab-highlight"] {
    background-color: var(--teal) !important;
}

/* ------------------------------------------------------------
   MISC
   ------------------------------------------------------------ */
hr {
    border-color: var(--line) !important;
}

/* Login */
.login-shell {
    min-height: 77vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-hero {
    padding: 30px 6px 20px 6px;
}

.login-kicker {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    background: var(--amber-soft);
    color: var(--amber);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .3px;
    margin-bottom: 14px;
}

.login-heading {
    font-size: clamp(32px, 4.2vw, 54px);
    line-height: 1.08;
    font-weight: 800;
    letter-spacing: -1.6px;
    color: var(--ink);
    max-width: 720px;
}

.login-copy {
    font-size: 15px;
    line-height: 1.7;
    color: var(--muted);
    max-width: 590px;
    margin-top: 16px;
}

.login-card-title {
    font-size: 21px;
    font-weight: 800;
    color: var(--ink);
    margin-bottom: 3px;
}

.login-card-copy {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 10px;
}

/* Small-screen refinement */
@media (max-width: 900px) {
    .block-container {
        padding-top: 1.2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .tech-title {
        font-size: 26px;
    }
}

/* Notification badge / workspace cards */
.workspace-hero {
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 20px 22px;
    background: linear-gradient(135deg, #f0fdfa 0%, #ffffff 55%, #fff7ed 100%);
    margin-bottom: 18px;
}
.workspace-hero-title {
    font-size: 15px;
    font-weight: 750;
    color: var(--ink);
}
.workspace-hero-copy {
    color: var(--muted);
    font-size: 13px;
    margin-top: 4px;
}
.status-pill {
    display: inline-block;
    padding: 4px 9px;
    border-radius: 999px;
    background: #ecfdf5;
    color: #047857;
    font-size: 11px;
    font-weight: 700;
}
.chat-bubble {
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 10px 12px;
    margin: 6px 0;
    background: #fff;
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

# Browser cookie manager for persistent login across refreshes.
cookie_manager = stx.CookieManager()


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

def load_profile_for_user(user):
    profile_result = (
        supabase
        .table("profiles")
        .select("*")
        .eq("id", user.id)
        .execute()
    )

    if not profile_result.data:
        return None

    return profile_result.data[0]


def remember_session(auth_result):
    """Store Supabase tokens in browser cookies so refresh does not log the user out."""
    try:
        if auth_result.session:
            cookie_manager.set(
                "techloom_access_token",
                auth_result.session.access_token,
                key="techloom_set_access"
            )
            cookie_manager.set(
                "techloom_refresh_token",
                auth_result.session.refresh_token,
                key="techloom_set_refresh"
            )
    except Exception:
        # Login should still work even if a browser blocks cookies.
        pass


def restore_login_from_cookie():
    """Restore a Supabase session after a full page refresh."""
    if st.session_state.user is not None:
        return True

    try:
        access_token = cookie_manager.get("techloom_access_token")
        refresh_token = cookie_manager.get("techloom_refresh_token")

        if not access_token or not refresh_token:
            return False

        auth_result = supabase.auth.set_session(
            access_token,
            refresh_token
        )

        user = auth_result.user
        if not user:
            return False

        profile = load_profile_for_user(user)
        if not profile:
            return False

        st.session_state.user = user
        st.session_state.profile = profile

        # Supabase may rotate the refresh token.
        remember_session(auth_result)
        return True

    except Exception:
        return False


def login(email, password):

    try:

        auth_result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        user = auth_result.user
        profile = load_profile_for_user(user)

        if not profile:

            st.error(
                "Login succeeded, but no Techloom profile "
                "was found for this account."
            )

            return False

        st.session_state.user = user
        st.session_state.profile = profile
        remember_session(auth_result)

        return True

    except Exception as error:

        st.error("Login failed.")
        st.write(error)

        return False


# Attempt session restoration before showing the login page.
if st.session_state.user is None:
    restore_login_from_cookie()


# ============================================================
# LOGOUT
# ============================================================

def logout():

    try:
        supabase.auth.sign_out()
    except Exception:
        pass

    try:
        cookie_manager.delete(
            "techloom_access_token",
            key="techloom_delete_access"
        )
        cookie_manager.delete(
            "techloom_refresh_token",
            key="techloom_delete_refresh"
        )
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

        # Route a notification to the other side of the workflow.
        try:
            task_result = (
                supabase.table("tasks")
                .select("title,assigned_to")
                .eq("id", task_id)
                .limit(1)
                .execute()
            )
            task_row = task_result.data[0] if task_result.data else {}
            task_title = task_row.get("title", "Task")
            assigned_employee = task_row.get("assigned_to")

            if is_manager() and assigned_employee:
                notify_employee(
                    assigned_employee,
                    "Task status updated",
                    f"{name} changed '{task_title}' to {status}.",
                    "status",
                    task_id
                )
            elif not is_manager():
                notify_managers(
                    "Task status updated",
                    f"{name} changed '{task_title}' to {status}.",
                    "status",
                    task_id
                )
        except Exception:
            pass

        return True

    except Exception as error:

        st.error("Could not update task.")

        st.write(error)

        return False



# ============================================================
# TEAM / NOTIFICATION / CHAT HELPERS
# ============================================================

def load_team_profiles():
    """Return basic team directory data through a controlled Supabase RPC."""
    try:
        result = supabase.rpc("get_team_profiles").execute()
        return result.data or []
    except Exception:
        return []


def find_profile_by_name(employee_name):
    for profile_record in load_team_profiles():
        if profile_record.get("name") == employee_name:
            return profile_record
    return None


def manager_profiles():
    return [
        profile_record
        for profile_record in load_team_profiles()
        if profile_record.get("role") in ["Admin", "Team Lead"]
    ]


def create_notification(target_user_id, title, message, notification_type="activity", task_id=None):
    if not target_user_id:
        return
    try:
        supabase.table("notifications").insert({
            "user_id": target_user_id,
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "related_task_id": task_id,
            "is_read": False
        }).execute()
    except Exception:
        # Notification problems must never break normal task work.
        pass


def notify_employee(employee_name, title, message, notification_type="activity", task_id=None):
    profile_record = find_profile_by_name(employee_name)
    if profile_record:
        create_notification(
            profile_record.get("id"),
            title,
            message,
            notification_type,
            task_id
        )


def notify_managers(title, message, notification_type="activity", task_id=None):
    for manager in manager_profiles():
        if manager.get("id") != current_user_id:
            create_notification(
                manager.get("id"),
                title,
                message,
                notification_type,
                task_id
            )


def play_notification_tone():
    """Short two-note browser tone. Browser autoplay rules may require one prior user interaction."""
    components.html(
        """
        <script>
        (() => {
          try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            const ctx = new AudioCtx();
            const now = ctx.currentTime;
            [[740, 0.00], [980, 0.12]].forEach(([freq, delay]) => {
              const osc = ctx.createOscillator();
              const gain = ctx.createGain();
              osc.type = "sine";
              osc.frequency.value = freq;
              gain.gain.setValueAtTime(0.0001, now + delay);
              gain.gain.exponentialRampToValueAtTime(0.12, now + delay + 0.015);
              gain.gain.exponentialRampToValueAtTime(0.0001, now + delay + 0.14);
              osc.connect(gain);
              gain.connect(ctx.destination);
              osc.start(now + delay);
              osc.stop(now + delay + 0.16);
            });
          } catch (e) {}
        })();
        </script>
        """,
        height=0,
        width=0
    )


def get_unread_notifications(limit=25):
    try:
        result = (
            supabase
            .table("notifications")
            .select("*")
            .eq("user_id", current_user_id)
            .eq("is_read", False)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
    except Exception:
        return []


def mark_all_notifications_read():
    try:
        supabase.table("notifications").update({
            "is_read": True
        }).eq(
            "user_id", current_user_id
        ).eq(
            "is_read", False
        ).execute()
        return True
    except Exception:
        return False


@st.fragment(run_every=5)
def render_notification_monitor():
    unread = get_unread_notifications()
    unread_count = len(unread)

    latest_id = unread[0]["id"] if unread else 0
    previous_id = st.session_state.get("latest_notification_seen")

    # First poll establishes the baseline. Later genuinely new IDs make a sound.
    if previous_id is None:
        st.session_state.latest_notification_seen = latest_id
    elif latest_id and latest_id != previous_id:
        play_notification_tone()
        st.session_state.latest_notification_seen = latest_id

    if unread_count:
        st.caption(f"🔔 {unread_count} unread notification(s)")
    else:
        st.caption("🔔 No unread notifications")


def submit_task_for_review(task_id, submission_link="", submission_notes=""):
    try:
        supabase.table("tasks").update({
            "status": "Submitted for Review",
            "submission_link": submission_link.strip(),
            "submission_notes": submission_notes.strip(),
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }).eq("id", task_id).execute()

        add_activity(
            task_id,
            "Submitted for Review",
            submission_link.strip() or submission_notes.strip() or "Task submitted for review"
        )
        notify_managers(
            "Task submitted for review",
            f"{name} submitted a task for review.",
            "review",
            task_id
        )
        return True
    except Exception as error:
        st.error("Could not submit the task for review.")
        st.write(error)
        return False


def send_chat_message(message):
    message = (message or "").strip()
    if not message:
        return False
    try:
        supabase.table("chat_messages").insert({
            "user_id": current_user_id,
            "user_name": name,
            "message": message
        }).execute()

        # Notify every other visible teammate.
        for teammate in load_team_profiles():
            teammate_id = teammate.get("id")
            if teammate_id and teammate_id != current_user_id:
                create_notification(
                    teammate_id,
                    f"New message from {name}",
                    message[:180],
                    "chat"
                )
        return True
    except Exception as error:
        st.error("Message could not be sent.")
        st.write(error)
        return False


@st.fragment(run_every=3)
def render_group_chat_messages():
    try:
        result = (
            supabase
            .table("chat_messages")
            .select("*")
            .order("created_at", desc=False)
            .limit(150)
            .execute()
        )
        messages = result.data or []
    except Exception as error:
        st.error("Could not load group chat.")
        st.write(error)
        return

    if not messages:
        st.info("No messages yet. Start the Techloom group conversation.")
        return

    for message in messages:
        sender = message.get("user_name", "Team member")
        created = message.get("created_at")
        display_stamp = ""
        parsed = parse_timestamp(created)
        if parsed:
            display_stamp = parsed.astimezone(PK_TZ).strftime("%d %b • %I:%M %p")

        with st.chat_message("user" if sender == name else "assistant"):
            st.markdown(f"**{sender}**")
            st.write(message.get("message", ""))
            if display_stamp:
                st.caption(display_stamp)


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
            "💬 Group Chat",
            "🔔 Notifications",
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
            "💬 Group Chat",
            "🔔 Notifications",
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
            "💬 Group Chat",
            "🔔 Notifications",
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
            "💬 Group Chat",
            "🔔 Notifications",
            "📜 Activity"
        ]

    else:

        menu_options = [
            "🏠 Dashboard",
            "📋 My Tasks",
            "⏱ Attendance",
            "💬 Group Chat",
            "🔔 Notifications"
        ]

    page = st.radio(
        "Navigation",
        menu_options,
        label_visibility="collapsed"
    )

    st.divider()
    render_notification_monitor()

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

    today_date = datetime.now(PK_TZ).date()
    due_today_count = 0
    overdue_count = 0

    for task_item in tasks:
        due_value = task_item.get("due_date")
        if due_value and task_item.get("status") not in ["Completed", "Approved"]:
            try:
                due_dt = datetime.fromisoformat(str(due_value).replace("Z", "+00:00"))
                due_day = due_dt.date()
                if due_day == today_date:
                    due_today_count += 1
                elif due_day < today_date:
                    overdue_count += 1
            except Exception:
                pass

    unread_dashboard = len(get_unread_notifications(limit=100))

    st.markdown(
        '<div class="workspace-hero">'
        f'<div class="workspace-hero-title">Today at Techloom</div>'
        f'<div class="workspace-hero-copy">'
        f'{due_today_count} due today • {overdue_count} overdue • '
        f'{unread_dashboard} unread notification(s)'
        f'</div></div>',
        unsafe_allow_html=True
    )

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
                    and status != "Submitted for Review"
                ):
                    st.divider()
                    submission_link = st.text_input(
                        "Return / submission link",
                        value=task.get("submission_link", "") or "",
                        placeholder="Paste listing, case, document or work link",
                        key=f"submission_link_{task_id}"
                    )

                    submission_notes = st.text_area(
                        "Submission note",
                        value=task.get("submission_notes", "") or "",
                        placeholder="Briefly tell AIFA what was completed.",
                        height=90,
                        key=f"submission_notes_{task_id}"
                    )

                    if st.button(
                        "📤 Send Back for Review",
                        key=f"submit_{task_id}",
                        use_container_width=True,
                        type="primary"
                    ):
                        if submit_task_for_review(
                            task_id,
                            submission_link,
                            submission_notes
                        ):
                            st.success("Task sent back for review.")
                            st.rerun()


# ============================================================
# CREATE TASK
# ============================================================

elif page == "➕ Create Task":

    if not is_manager():
        st.error("You do not have permission to create tasks.")
        st.stop()

    st.markdown('<div class="tech-title">Assign a New Task</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tech-subtitle">'
        'Create a clear brief, choose the owner and set the delivery details.'
        '</div>',
        unsafe_allow_html=True
    )

    team_profiles = load_team_profiles()
    team_names = [
        p.get("name")
        for p in team_profiles
        if p.get("name")
    ]
    if not team_names:
        team_names = ["Talha", "Junaid", "Nabiha", "AIFA"]

    st.markdown(
        '<div class="workspace-hero">'
        '<div class="workspace-hero-title">📌 Assignment brief</div>'
        '<div class="workspace-hero-copy">'
        'A good task should tell the assignee what needs doing, where it belongs, '
        'when it is due and what evidence/link should be returned.'
        '</div></div>',
        unsafe_allow_html=True
    )

    with st.form("create_task_form"):
        task_title = st.text_input(
            "Task title",
            placeholder="e.g. Upload Amazon listing for new explorer hat"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            assigned_to = st.selectbox(
                "Assign to",
                team_names
            )

            priority = st.selectbox(
                "Priority",
                ["Normal", "High", "Urgent", "Low"]
            )

        with c2:
            task_type = st.selectbox(
                "Task type",
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
                ["Temu", "Amazon", "eBay", "TikTok", "Multiple"]
            )

        with c3:
            due_date = st.date_input(
                "Due date",
                value=datetime.now(PK_TZ).date() + timedelta(days=1)
            )
            due_time = st.time_input(
                "Due time",
                value=time(hour=17, minute=0)
            )

        l1, l2 = st.columns(2)

        with l1:
            supplier_link = st.text_input(
                "Supplier / reference link",
                placeholder="https://..."
            )
            goods_id = st.text_input(
                "Goods ID / ASIN / SKU",
                placeholder="Optional"
            )

        with l2:
            supplier_price = st.number_input(
                "Supplier price",
                min_value=0.0,
                step=0.10
            )
            selling_price = st.number_input(
                "Selling price",
                min_value=0.0,
                step=0.10
            )

        instructions = st.text_area(
            "Instructions",
            height=170,
            placeholder=(
                "Explain exactly what needs to be done, important checks, "
                "required output and anything the assignee must return."
            )
        )

        submit_task = st.form_submit_button(
            "Assign Task →",
            type="primary",
            use_container_width=True
        )

        if submit_task:
            if not task_title.strip():
                st.error("Please enter a task title.")
            else:
                due_datetime = datetime.combine(
                    due_date,
                    due_time
                )

                task_data = {
                    "title": task_title.strip(),
                    "description": instructions.strip(),
                    "task_type": task_type,
                    "platform": platform,
                    "priority": priority,
                    "status": "New",
                    "assigned_to": assigned_to,
                    "assigned_by": name,
                    "supplier_link": supplier_link.strip(),
                    "supplier_price": supplier_price,
                    "selling_price": selling_price,
                    "goods_id": goods_id.strip(),
                    "due_date": due_datetime.isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat()
                }

                try:
                    result = (
                        supabase
                        .table("tasks")
                        .insert(task_data)
                        .execute()
                    )

                    new_task_id = result.data[0]["id"] if result.data else None

                    if new_task_id:
                        add_activity(
                            new_task_id,
                            "Task Created",
                            f"{name} assigned '{task_title.strip()}' to {assigned_to}"
                        )

                    notify_employee(
                        assigned_to,
                        "New task assigned",
                        f"{name} assigned you: {task_title.strip()}",
                        "task",
                        new_task_id
                    )

                    st.success(f"Task assigned to {assigned_to}.")
                    st.rerun()

                except Exception as error:
                    st.error("Could not create task.")
                    st.write(error)


# ============================================================
# APPROVALS
# ============================================================

elif page == "✅ Approvals":

    if not is_manager():
        st.error("Management access only.")
        st.stop()

    st.markdown('<div class="tech-title">Approvals</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tech-subtitle">'
        'Review returned work, open the supplied link and approve or request changes.'
        '</div>',
        unsafe_allow_html=True
    )

    try:
        result = (
            supabase
            .table("tasks")
            .select("*")
            .eq("status", "Submitted for Review")
            .order("created_at", desc=True)
            .execute()
        )
        approval_tasks = result.data or []
    except Exception as error:
        st.error(error)
        approval_tasks = []

    if not approval_tasks:
        st.info("No tasks are currently waiting for approval.")

    for task in approval_tasks:
        task_id = task["id"]
        title = task.get("title", "")
        assignee = task.get("assigned_to", "")
        submission_link = task.get("submission_link", "") or ""
        submission_notes = task.get("submission_notes", "") or ""

        with st.expander(f"{title} • {assignee}", expanded=True):

            info1, info2, info3 = st.columns(3)
            info1.write(f"**Platform:** {task.get('platform', '')}")
            info2.write(f"**Task Type:** {task.get('task_type', '')}")
            info3.write(f"**Priority:** {task.get('priority', '')}")

            st.write("**Original instructions**")
            st.write(task.get("description", ""))

            st.divider()

            st.markdown("#### 📦 Returned work")

            if submission_link:
                st.write("**Submission link**")
                st.link_button(
                    "Open returned work ↗",
                    submission_link,
                    use_container_width=False
                )
                st.caption(submission_link)
            else:
                st.warning("The assignee did not provide a return link.")

            if submission_notes:
                st.info(f"Submission note: {submission_notes}")

            review_notes = st.text_area(
                "Manager review note",
                key=f"review_{task_id}",
                placeholder="Optional note for the assignee."
            )

            review_link = st.text_input(
                "Reference / correction link",
                key=f"review_link_{task_id}",
                placeholder="Optional link to an example, correction, document or reference"
            )

            approve_col, changes_col = st.columns(2)

            with approve_col:
                if st.button(
                    "✅ Approve",
                    key=f"approve_{task_id}",
                    use_container_width=True,
                    type="primary"
                ):
                    try:
                        supabase.table("tasks").update({
                            "status": "Approved",
                            "review_notes": review_notes,
                            "review_link": review_link.strip(),
                            "updated_at": datetime.now(timezone.utc).isoformat()
                        }).eq("id", task_id).execute()

                        add_activity(
                            task_id,
                            "Task Approved",
                            review_notes or "Approved"
                        )
                        notify_employee(
                            assignee,
                            "Task approved",
                            f"{name} approved: {title}",
                            "approval",
                            task_id
                        )

                        st.success("Task approved.")
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
                        supabase.table("tasks").update({
                            "status": "Changes Requested",
                            "review_notes": review_notes,
                            "review_link": review_link.strip(),
                            "updated_at": datetime.now(timezone.utc).isoformat()
                        }).eq("id", task_id).execute()

                        add_activity(
                            task_id,
                            "Changes Requested",
                            review_notes or review_link.strip() or "Changes requested"
                        )
                        notify_employee(
                            assignee,
                            "Changes requested",
                            f"{name} requested changes on: {title}",
                            "changes",
                            task_id
                        )

                        st.success("Changes requested.")
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
        st.error("Management access only.")
        st.stop()

    st.markdown('<div class="tech-title">Attendance Report</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tech-subtitle">'
        'Full team attendance, including employees who have not checked in.'
        '</div>',
        unsafe_allow_html=True
    )

    selected_date = st.date_input(
        "Attendance Date",
        value=datetime.now(PK_TZ).date()
    )

    try:
        # SECURITY DEFINER RPC from the SQL upgrade. It returns the whole team
        # and avoids the old RLS issue where AIFA could see only one person.
        result = supabase.rpc(
            "get_team_attendance",
            {"report_date": selected_date.isoformat()}
        ).execute()

        records = result.data or []

        present_count = sum(
            1 for r in records if r.get("check_in")
        )
        absent_count = sum(
            1 for r in records if not r.get("check_in")
        )
        working_now_count = sum(
            1 for r in records
            if r.get("check_in") and not r.get("check_out")
        )
        checked_out_count = sum(
            1 for r in records if r.get("check_out")
        )

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("🟢 Present", present_count)
        r2.metric("⚪ Not Checked In", absent_count)
        r3.metric("🕒 Working Now", working_now_count)
        r4.metric("🚪 Checked Out", checked_out_count)

        st.write("")

        report_rows = []

        for record in records:
            is_present = bool(record.get("check_in"))
            report_rows.append({
                "Employee": record.get("employee_name"),
                "Role": record.get("employee_role"),
                "Department": record.get("employee_department"),
                "Date": selected_date.isoformat(),
                "Check In": (
                    format_pk_time(record.get("check_in"))
                    if is_present else "--"
                ),
                "Check Out": (
                    format_pk_time(record.get("check_out"))
                    if record.get("check_out") else "--"
                ),
                "Working Time": (
                    working_time(
                        record.get("check_in"),
                        record.get("check_out")
                    )
                    if is_present else "--"
                ),
                "Status": (
                    record.get("attendance_status") or "Present"
                    if is_present else "Not Checked In"
                )
            })

        if report_rows:
            st.dataframe(
                pd.DataFrame(report_rows),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No team profiles are available.")

    except Exception as error:
        st.error(
            "Could not load the full team report. "
            "Please run the supplied Supabase SQL upgrade first."
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
# GROUP CHAT
# ============================================================

elif page == "💬 Group Chat":

    st.markdown('<div class="tech-title">Techloom Group Chat</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tech-subtitle">'
        'Shared team conversation for quick updates, questions and coordination.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="workspace-hero">'
        '<div class="workspace-hero-title">💬 Team channel</div>'
        '<div class="workspace-hero-copy">'
        'Messages refresh automatically. New messages also create an unread notification '
        'for the rest of the team.'
        '</div></div>',
        unsafe_allow_html=True
    )

    render_group_chat_messages()

    chat_text = st.chat_input("Message the Techloom team…")

    if chat_text:
        if send_chat_message(chat_text):
            st.rerun()


# ============================================================
# NOTIFICATIONS
# ============================================================

elif page == "🔔 Notifications":

    st.markdown('<div class="tech-title">Notifications</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tech-subtitle">'
        'Task assignments, approvals, changes, submissions and team chat alerts.'
        '</div>',
        unsafe_allow_html=True
    )

    unread = get_unread_notifications(limit=100)

    n1, n2 = st.columns([1, 4])
    n1.metric("Unread", len(unread))

    with n2:
        if unread and st.button(
            "Mark all as read",
            use_container_width=False
        ):
            if mark_all_notifications_read():
                st.session_state.latest_notification_seen = 0
                st.rerun()

    if not unread:
        st.success("You're all caught up.")
    else:
        for notification in unread:
            created = parse_timestamp(notification.get("created_at"))
            stamp = (
                created.astimezone(PK_TZ).strftime("%d %b %Y • %I:%M %p")
                if created else ""
            )

            with st.container(border=True):
                st.markdown(f"**{notification.get('title', 'Notification')}**")
                st.write(notification.get("message", ""))
                if stamp:
                    st.caption(stamp)


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