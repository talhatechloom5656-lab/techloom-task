import streamlit as st
import pandas as pd
import uuid
import re
import io
import json
import calendar
import streamlit.components.v1 as components
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

:root{
  --bg:#ffffff;
  --sidebar:#f7f7f5;
  --line:#e8e8e4;
  --text:#252524;
  --muted:#7b7b75;
  --soft:#efefec;
  --blue:#2383e2;
  --blue-soft:#edf5fc;
  --green:#2f7a48;
  --green-soft:#eef8f0;
  --amber:#996b20;
  --amber-soft:#fbf3df;
  --red:#b54a4a;
  --red-soft:#fff0f0;
}

html,body,[class*="css"]{
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}

.stApp{
  background:var(--bg);
  color:var(--text);
}

/* Main content tighter and more app-like */
.block-container{
  max-width:1280px;
  padding:1.15rem 1.55rem 3rem 1.55rem;
}

/* Hide Streamlit chrome as much as possible */
header[data-testid="stHeader"]{
  background:transparent;
}
[data-testid="stToolbar"]{
  visibility:hidden;
  height:0;
}
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}

/* ============================================================
   SIDEBAR
   ============================================================ */
[data-testid="stSidebar"]{
  background:var(--sidebar);
  border-right:1px solid var(--line);
  width:230px !important;
  min-width:230px !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarContent"]{
  padding:.7rem .65rem .7rem .65rem;
}
.side-brand{
  display:flex;
  align-items:center;
  gap:9px;
  height:38px;
  padding:0 6px;
  margin-bottom:5px;
}
.brand-mark{
  width:24px;
  height:24px;
  border-radius:7px;
  background:#252524;
  color:#fff;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-size:10px;
  font-weight:800;
}
.side-brand strong{
  font-size:13px;
  font-weight:750;
  color:#252524;
}
.side-user{
  padding:8px 9px;
  margin:6px 0 8px;
  border:1px solid var(--line);
  border-radius:8px;
  background:#fff;
}
.side-user b{
  display:block;
  font-size:11px;
  color:#252524;
}
.side-user small{
  display:block;
  margin-top:3px;
  font-size:9.5px;
  color:#8c8c86;
}

/* radio circles completely gone */
[data-testid="stSidebar"] [role="radiogroup"]{
  gap:1px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label{
  width:100%;
  min-height:31px;
  padding:5px 7px !important;
  margin:0;
  border-radius:6px;
  display:flex;
  align-items:center;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{
  background:#ecece9;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){
  background:#e9e9e6;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{
  color:#50504c !important;
  font-size:11.3px !important;
  font-weight:520 !important;
  margin:0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p{
  color:#252524 !important;
  font-weight:700 !important;
}
[data-testid="stSidebar"] [data-baseweb="radio"],
[data-testid="stSidebar"] input[type="radio"],
[data-testid="stSidebar"] [role="radio"] > div:first-child{
  display:none !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child{
  display:none !important;
}
[data-testid="stSidebar"] .stButton > button{
  width:100%;
  min-height:31px;
  padding:5px 8px;
  border-radius:6px !important;
  border:1px solid #deded9 !important;
  background:#fff !important;
  color:#444 !important;
  box-shadow:none !important;
  font-size:10.5px !important;
}
[data-testid="stSidebar"] .stButton > button:hover{
  background:#efefec !important;
}
.sidebar-section{
  padding:11px 7px 4px;
  color:#9a9a94;
  font-size:8.5px;
  font-weight:750;
  letter-spacing:.08em;
}

/* ============================================================
   TOPBAR
   ============================================================ */
.portal-topbar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  min-height:43px;
  margin:0 0 18px 0;
  padding:0 1px 10px 1px;
  border-bottom:1px solid #efefec;
}
.crumb{
  display:flex;
  align-items:center;
  gap:7px;
  color:#5a5a56;
  font-size:11px;
  font-weight:620;
}
.crumb-mark{
  font-size:9px;
  color:#75756f;
}
.top-user{
  display:flex;
  align-items:center;
  gap:7px;
  color:#666660;
  font-size:10.5px;
}
.top-avatar{
  width:25px;
  height:25px;
  border-radius:50%;
  background:#2f80ed;
  color:#fff;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-size:9px;
  font-weight:800;
}
.notify-dot{
  width:25px;
  height:25px;
  border-radius:6px;
  border:1px solid #e6e6e2;
  background:#f7f7f5;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-size:10px;
  color:#666;
}

/* ============================================================
   TYPOGRAPHY / PAGE HEADERS
   ============================================================ */
.eyebrow{
  display:block;
  margin-bottom:8px;
  color:#94948e;
  font-size:8.5px;
  font-weight:750;
  letter-spacing:.1em;
}
.page-head-new{
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  gap:20px;
  margin-bottom:16px;
}
.page-head-new h1{
  margin:0 0 4px;
  color:#252524;
  font-size:29px;
  line-height:1.05;
  letter-spacing:-.045em;
  font-weight:760;
}
.page-head-new p{
  margin:0;
  color:#7e7e78;
  font-size:11px;
}
.tech-title,.page-title{
  color:#252524;
  font-size:29px;
  font-weight:760;
  letter-spacing:-.045em;
  line-height:1.05;
}
.tech-subtitle,.page-subtitle{
  color:#7e7e78;
  font-size:10.8px;
  margin-top:5px;
  margin-bottom:16px;
}
.section-title{
  font-size:12px;
  font-weight:700;
  color:#343432;
  margin:8px 0 8px;
}

/* ============================================================
   DASHBOARD
   ============================================================ */
.dashboard-hero{
  border:0;
  padding:0;
  margin-bottom:14px;
  background:transparent;
}
.dashboard-hero-title{
  font-size:29px;
  line-height:1.05;
  letter-spacing:-.045em;
  font-weight:760;
  color:#252524;
}
.dashboard-hero-copy{
  font-size:11px;
  color:#7e7e78;
  margin-top:5px;
}
.hero-date{
  text-align:right;
  font-size:10px;
  color:#85857f;
  line-height:1.45;
}
.today-strip{
  border:1px solid var(--line);
  border-radius:9px;
  background:#fafaf8;
  padding:10px 12px;
  margin:0 0 12px;
  font-size:10.5px;
  color:#696963;
}
.today-strip b{
  color:#30302e;
  font-size:11px;
}
.announcement-mini{
  border:1px solid #f1d6d6;
  background:#fff7f7;
  color:#8e4a4a;
  border-radius:8px;
  padding:9px 11px;
  font-size:10.5px;
  margin-bottom:12px;
}

/* Compact KPI cards */
div[data-testid="stMetric"]{
  border:1px solid var(--line);
  border-radius:9px;
  background:#fff;
  min-height:78px;
  padding:11px 12px 9px;
  box-shadow:none;
}
div[data-testid="stMetric"] [data-testid="stMetricLabel"] p{
  font-size:9px !important;
  font-weight:650 !important;
  color:#7f7f79 !important;
  margin-bottom:2px !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{
  font-size:24px !important;
  color:#252524 !important;
  font-weight:720 !important;
  letter-spacing:-.04em;
}

/* ============================================================
   PANELS / CARDS
   ============================================================ */
.panel,.workspace-hero,.task-board-header{
  border:1px solid var(--line);
  border-radius:9px;
  background:#fff;
  padding:14px;
  box-shadow:none;
}
.attention-card,.work-card,.task-card{
  border:1px solid #e6e6e2;
  border-radius:7px;
  background:#fff;
  padding:9px 10px;
  margin-bottom:6px;
  box-shadow:0 1px 1px rgba(0,0,0,.02);
}
.attention-card:hover,.work-card:hover,.task-card:hover{
  border-color:#d5d5d0;
  background:#fdfdfc;
}
.attention-card-title,.work-card-title,.task-card-title{
  color:#2b2b29;
  font-size:11.5px;
  line-height:1.35;
  font-weight:650;
}
.attention-card-meta,.work-meta,.task-meta{
  color:#8b8b85;
  font-size:9.3px;
  line-height:1.5;
  margin-top:3px;
}
.status-chip,.status-pill{
  display:inline-flex;
  align-items:center;
  padding:2px 5px;
  border-radius:4px;
  font-size:8.5px;
  font-weight:650;
  margin-right:3px;
  border:0;
  background:#eee;
  color:#555;
}
.priority-urgent{background:#ffe6e6;color:#a63d3d}
.priority-high{background:#fff0d7;color:#986814}
.priority-normal{background:#e8f2fb;color:#3475aa}
.priority-low{background:#f0f0ed;color:#777}

/* ============================================================
   BOARD
   ============================================================ */
.kanban-column-title{
  font-size:9.5px;
  font-weight:700;
  color:#6e6e68;
  margin-bottom:6px;
}
.kanban-count{
  float:right;
  color:#aaa;
}
[data-testid="column"]{
  min-width:0;
}

/* ============================================================
   FORMS / INPUTS / BUTTONS
   ============================================================ */
[data-baseweb="input"]>div,
[data-baseweb="textarea"]>div,
[data-baseweb="select"]>div{
  min-height:36px;
  background:#fff !important;
  border:1px solid #deded9 !important;
  border-radius:7px !important;
}
[data-baseweb="input"]>div:focus-within,
[data-baseweb="textarea"]>div:focus-within,
[data-baseweb="select"]>div:focus-within{
  border-color:#8db9e8 !important;
  box-shadow:0 0 0 3px rgba(35,131,226,.09) !important;
}
.stTextInput label p,.stTextArea label p,.stSelectbox label p,.stDateInput label p,
.stNumberInput label p,.stFileUploader label p,.stMultiSelect label p{
  font-size:9.5px !important;
  color:#696963 !important;
  font-weight:600 !important;
}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button,.stLinkButton>a{
  min-height:33px;
  border-radius:7px !important;
  border:1px solid #deded9;
  background:#fff;
  font-size:10px;
  font-weight:600;
  box-shadow:none;
}
button[kind="primary"],.stFormSubmitButton button[kind="primary"]{
  background:var(--blue) !important;
  border-color:var(--blue) !important;
  color:#fff !important;
}

/* ============================================================
   TABLES / TABS / EXPANDERS
   ============================================================ */
button[data-baseweb="tab"]{
  padding:6px 8px !important;
  font-size:10px !important;
  color:#797973 !important;
}
button[data-baseweb="tab"][aria-selected="true"]{
  color:#252524 !important;
  font-weight:700 !important;
}
[data-baseweb="tab-highlight"]{
  height:1.5px !important;
  background:#252524 !important;
}
[data-testid="stDataFrame"],[data-testid="stTable"]{
  border:1px solid var(--line);
  border-radius:8px;
  overflow:hidden;
  background:#fff;
}
[data-testid="stExpander"]{
  border:1px solid var(--line);
  border-radius:8px;
  background:#fff;
  margin-bottom:6px;
}
[data-testid="stAlert"]{
  border-radius:8px;
  padding-top:.55rem !important;
  padding-bottom:.55rem !important;
}

/* ============================================================
   ATTENDANCE
   ============================================================ */
.attendance-hero{
  border:1px solid var(--line);
  border-radius:9px;
  background:#fafaf8;
  padding:14px;
  margin-bottom:10px;
}
.attendance-eyebrow{
  color:#92928c;
  font-size:8.5px;
  font-weight:750;
  letter-spacing:.08em;
  text-transform:uppercase;
}
.attendance-date{
  color:#252524;
  font-size:24px;
  font-weight:730;
  letter-spacing:-.04em;
  margin-top:4px;
}
.attendance-day,.attendance-note{
  color:#85857f;
  font-size:9.5px;
}
.attendance-status-card{
  border:1px solid var(--line);
  border-radius:8px;
  background:#fff;
  padding:11px;
  min-height:90px;
}
.attendance-label{
  color:#85857f;
  font-size:8.5px;
  font-weight:750;
  text-transform:uppercase;
  letter-spacing:.04em;
}
.attendance-value{
  color:#252524;
  font-size:17px;
  font-weight:700;
  margin-top:5px;
}
.attendance-rules{
  border:1px solid var(--line);
  border-radius:8px;
  background:#fafaf8;
  padding:9px 10px;
  color:#666660;
  font-size:9.5px;
}

/* ============================================================
   MOBILE
   ============================================================ */
@media(max-width:900px){
  .block-container{padding:1rem .8rem 2.5rem}
  .page-head-new{align-items:flex-start;flex-direction:column}
  .page-head-new h1,.tech-title,.page-title,.dashboard-hero-title{font-size:26px}
  [data-testid="stSidebar"]{width:220px!important;min-width:220px!important}
}

/* ===== TECHLOOM ENHANCED STABLE V5 ===== */
.block-container{max-width:1320px!important;padding-top:.8rem!important;padding-left:1.35rem!important;padding-right:1.35rem!important}
.portal-topbar{margin-top:0!important;margin-bottom:10px!important;min-height:38px!important;padding-bottom:8px!important}
[data-testid="stSidebar"]{width:232px!important;min-width:232px!important}
[data-testid="stSidebar"] [data-testid="stSidebarContent"]{padding:.72rem .62rem!important}
.side-brand{height:36px!important;margin-bottom:3px!important}
.side-user{padding:8px 9px!important;margin:5px 0 8px!important}
.side-user b{font-size:11px!important}.side-user small{font-size:9px!important}
[data-testid="stSidebar"] input[type="radio"]{position:absolute!important;opacity:0!important;pointer-events:none!important}
[data-testid="stSidebar"] [data-baseweb="radio"]{display:none!important}
[data-testid="stSidebar"] [role="radio"]>div:first-child{display:none!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label>div:first-child{display:none!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label{display:block!important;width:100%!important;min-height:30px!important;padding:5px 8px!important;border-radius:6px!important;margin:0 0 1px 0!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{margin:0!important;font-size:10.8px!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#ededeb!important}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){background:#e8e8e5!important}
[data-testid="stSidebar"] .stRadio>label{display:none!important}
.dashboard-hero-title,.tech-title,.page-title{font-size:28px!important;line-height:1.05!important;letter-spacing:-.045em!important}
.dashboard-hero-copy,.tech-subtitle,.page-subtitle{font-size:10.5px!important}
.today-strip{padding:8px 10px!important;margin-bottom:9px!important;border-radius:8px!important;font-size:9.8px!important}
.today-strip b{font-size:10.5px!important}
.announcement-mini{padding:7px 10px!important;font-size:9.7px!important;margin-bottom:10px!important;border-radius:8px!important}
div[data-testid="stMetric"]{min-height:70px!important;padding:9px 11px 8px!important;border-radius:9px!important}
div[data-testid="stMetric"] [data-testid="stMetricLabel"] p{font-size:8.8px!important}
div[data-testid="stMetric"] [data-testid="stMetricValue"]{font-size:22px!important}
.section-title{font-size:11.5px!important;margin-top:7px!important;margin-bottom:7px!important}
.attention-card{padding:9px 10px!important;border-radius:7px!important;margin-bottom:6px!important}
.attention-card-title{font-size:11px!important}.attention-card-meta{font-size:9px!important}
.tl-chip{display:inline-flex;align-items:center;padding:2px 6px;border-radius:999px;font-size:8px;line-height:1.35;font-weight:700;margin-right:4px}
.tl-chip-platform{background:#eef3f7;color:#5d6b76}.tl-chip-status{background:#f1f1ef;color:#65615d}
.tl-chip-urgent{background:#ffe8e8;color:#a74343}.tl-chip-high{background:#fff0d7;color:#936116}
.tl-chip-normal{background:#e8f2fb;color:#3475aa}.tl-chip-low{background:#efefec;color:#777}
.tl-dot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:6px;vertical-align:middle}
.tl-dot-good{background:#36a269}.tl-dot-warn{background:#df9a2d}.tl-dot-bad{background:#d9534f}.tl-dot-neutral{background:#b7b7b1}
.stButton>button,.stFormSubmitButton>button{min-height:33px!important;border-radius:7px!important;font-size:10px!important}


/* ===== DASHBOARD CHAT SHORTCUT ===== */
.chat-shortcut-card{
    border:1px solid #e6e6e2;
    border-radius:10px;
    background:#fff;
    padding:10px 11px;
    display:flex;
    align-items:center;
    gap:9px;
    min-height:55px;
}
.chat-shortcut-icon{
    position:relative;
    width:34px;
    height:34px;
    border-radius:10px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:#eef6fd;
    font-size:17px;
    flex:none;
}
.chat-unread-badge{
    position:absolute;
    right:-5px;
    top:-6px;
    min-width:17px;
    height:17px;
    padding:0 4px;
    border-radius:999px;
    background:#e5484d;
    color:#fff;
    border:2px solid #fff;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:8px;
    font-weight:800;
}
.chat-shortcut-title{
    color:#2b2b29;
    font-size:10.5px;
    font-weight:700;
}
.chat-shortcut-copy{
    color:#8a8a84;
    font-size:8.8px;
    margin-top:2px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# SUPABASE
# ============================================================

def get_supabase():
    """
    Create one Supabase client per Streamlit user session.

    IMPORTANT:
    Do not use st.cache_resource here because the Supabase client carries
    authentication state. A globally cached client can mix auth sessions
    between different employees and make RLS see the wrong auth.uid().
    """
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    return st.session_state.supabase_client


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
    """Store Supabase tokens in session_state and browser cookies."""
    try:
        if auth_result.session:
            access_token = auth_result.session.access_token
            refresh_token = auth_result.session.refresh_token

            # Keep tokens in this Streamlit session so every rerun can
            # re-attach the authenticated JWT to the Supabase client.
            st.session_state.techloom_access_token = access_token
            st.session_state.techloom_refresh_token = refresh_token

            cookie_manager.set(
                "techloom_access_token",
                access_token,
                key="techloom_set_access"
            )
            cookie_manager.set(
                "techloom_refresh_token",
                refresh_token,
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


def ensure_supabase_auth():
    """
    Make sure the Supabase/PostgREST client is actually authenticated as
    the same employee shown in Streamlit session_state.

    This fixes cases where Streamlit keeps the visible login state across a
    rerun/redeploy but the Supabase client's JWT was lost, causing RLS
    errors such as 42501 on chat_messages.
    """
    expected_user = st.session_state.get("user")
    if expected_user is None:
        return False

    expected_id = str(expected_user.id)

    # First check whether the client already has the correct authenticated user.
    try:
        auth_user_result = supabase.auth.get_user()
        auth_user = getattr(auth_user_result, "user", None)
        if auth_user and str(auth_user.id) == expected_id:
            return True
    except Exception:
        pass

    # Re-attach tokens from Streamlit session state first.
    access_token = st.session_state.get("techloom_access_token")
    refresh_token = st.session_state.get("techloom_refresh_token")

    # Fall back to browser cookies after a full page refresh.
    if not access_token or not refresh_token:
        try:
            access_token = cookie_manager.get("techloom_access_token")
            refresh_token = cookie_manager.get("techloom_refresh_token")
        except Exception:
            access_token = None
            refresh_token = None

    if not access_token or not refresh_token:
        return False

    try:
        auth_result = supabase.auth.set_session(
            access_token,
            refresh_token
        )

        auth_user = auth_result.user
        if not auth_user or str(auth_user.id) != expected_id:
            return False

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
    st.session_state.pop("techloom_access_token", None)
    st.session_state.pop("techloom_refresh_token", None)

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

# Re-sync the JWT before any RLS-protected table operations.
if not ensure_supabase_auth():
    st.warning(
        "Your secure session needs to be refreshed. "
        "Please log out and sign in again once."
    )

PK_TZ = ZoneInfo("Asia/Karachi")
ATTENDANCE_START_DATE = datetime(2026, 8, 25).date()  # Official first attendance day


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
            .eq("archived", False)
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
            .eq("archived", False)
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
    """
    Play a short notification chime using a native HTML audio element.

    Chrome/Edge may block sound until the employee has clicked
    "Enable Notification Sound" once in the sidebar.
    """
    st.markdown(
        """
        <audio autoplay style="display:none">
            <source src="data:audio/wav;base64,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" type="audio/wav">
        </audio>
        """,
        unsafe_allow_html=True
    )


def enable_notification_sound():
    """User-initiated sound test. This helps browsers allow later notification audio."""
    st.session_state.notification_sound_enabled = True
    play_notification_tone()


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
        if st.session_state.get("notification_sound_enabled", False):
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



def get_unread_chat_count():
    """Return unread chat-notification count for the current employee."""
    try:
        result = (
            supabase
            .table("notifications")
            .select("id")
            .eq("user_id", current_user_id)
            .eq("is_read", False)
            .eq("notification_type", "chat")
            .execute()
        )
        return len(result.data or [])
    except Exception:
        return 0


def mark_chat_notifications_read():
    """Clear only chat notifications when the employee opens Group Chat."""
    try:
        (
            supabase
            .table("notifications")
            .update({"is_read": True})
            .eq("user_id", current_user_id)
            .eq("is_read", False)
            .eq("notification_type", "chat")
            .execute()
        )
        return True
    except Exception:
        return False


def safe_chat_filename(filename):
    filename = filename or "attachment"
    filename = re.sub(r"[^A-Za-z0-9._-]+", "_", filename)
    return filename[:120] or "attachment"


def upload_chat_attachment(uploaded_file):
    """
    Upload an image/document to the private Supabase chat-files bucket.
    Returns attachment metadata for chat_messages.
    """
    if uploaded_file is None:
        return None

    if not ensure_supabase_auth():
        st.error("Your secure login session needs to be refreshed.")
        return None

    try:
        file_bytes = uploaded_file.getvalue()
        if len(file_bytes) > 10 * 1024 * 1024:
            st.error("File is too large. Maximum chat upload size is 10 MB.")
            return None

        original_name = safe_chat_filename(uploaded_file.name)
        mime_type = uploaded_file.type or "application/octet-stream"
        object_path = (
            f"{current_user_id}/"
            f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_"
            f"{uuid.uuid4().hex[:10]}_{original_name}"
        )

        supabase.storage.from_("chat-files").upload(
            object_path,
            file_bytes,
            {
                "content-type": mime_type,
                "upsert": "false"
            }
        )

        return {
            "attachment_path": object_path,
            "attachment_name": original_name,
            "attachment_type": mime_type,
            "attachment_size": len(file_bytes)
        }

    except Exception as error:
        st.error("Attachment could not be uploaded.")
        st.write(error)
        return None


def get_chat_attachment_url(path):
    """Create a temporary signed URL for a private chat attachment."""
    if not path:
        return None

    try:
        result = (
            supabase
            .storage
            .from_("chat-files")
            .create_signed_url(path, 3600)
        )

        if isinstance(result, str):
            return result

        if isinstance(result, dict):
            return (
                result.get("signedURL")
                or result.get("signedUrl")
                or result.get("signed_url")
            )

        return None

    except Exception:
        return None


def human_file_size(size):
    try:
        size = int(size or 0)
    except Exception:
        size = 0

    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.1f} MB"
    if size >= 1024:
        return f"{size / 1024:.0f} KB"
    return f"{size} B"


def send_chat_attachment(uploaded_file, caption=""):
    """Upload an attachment and create a group-chat message for it."""
    attachment = upload_chat_attachment(uploaded_file)
    if not attachment:
        return False

    caption = (caption or "").strip()
    message_text = caption or f"📎 {attachment['attachment_name']}"

    return send_chat_message(
        message_text,
        attachment=attachment
    )

def send_chat_message(message, attachment=None):
    message = (message or "").strip()
    if not message and not attachment:
        return False

    if not ensure_supabase_auth():
        st.error(
            "Your Supabase login token is not attached to this browser session. "
            "Please log out and sign in again."
        )
        return False

    try:
        row = {
            "user_id": current_user_id,
            "user_name": name,
            "message": message or "Attachment"
        }

        if attachment:
            row.update({
                "attachment_path": attachment.get("attachment_path"),
                "attachment_name": attachment.get("attachment_name"),
                "attachment_type": attachment.get("attachment_type"),
                "attachment_size": attachment.get("attachment_size")
            })

        supabase.table("chat_messages").insert(row).execute()

        preview = message[:180] if message else "Sent an attachment"

        # Notify every other visible teammate.
        for teammate in load_team_profiles():
            teammate_id = teammate.get("id")
            if teammate_id and str(teammate_id) != str(current_user_id):
                create_notification(
                    teammate_id,
                    f"New message from {name}",
                    preview,
                    "chat"
                )
        return True

    except Exception as error:
        st.error("Message could not be sent.")
        st.write(error)
        return False


@st.fragment(run_every=2)
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

    # Chat-specific sound detection. This is separate from the general
    # notification monitor so incoming chat messages can chime quickly.
    latest_message = messages[-1]
    latest_message_id = latest_message.get("id")
    latest_sender_id = latest_message.get("user_id")
    previous_chat_id = st.session_state.get("latest_chat_message_seen")

    if previous_chat_id is None:
        st.session_state.latest_chat_message_seen = latest_message_id
    elif latest_message_id != previous_chat_id:
        if (
            str(latest_sender_id) != str(current_user_id)
            and st.session_state.get("notification_sound_enabled", False)
        ):
            play_notification_tone()
        st.session_state.latest_chat_message_seen = latest_message_id

    for message in messages:
        sender = message.get("user_name", "Team member")
        created = message.get("created_at")
        display_stamp = ""
        parsed = parse_timestamp(created)
        if parsed:
            display_stamp = parsed.astimezone(PK_TZ).strftime("%d %b • %I:%M %p")

        with st.chat_message("user" if sender == name else "assistant"):
            st.markdown(f"**{sender}**")

            body = message.get("message", "")
            if body:
                st.write(body)

            attachment_path = message.get("attachment_path")
            attachment_name = message.get("attachment_name")
            attachment_type = message.get("attachment_type") or ""
            attachment_size = message.get("attachment_size")

            if attachment_path:
                attachment_url = get_chat_attachment_url(attachment_path)

                if attachment_url:
                    if attachment_type.startswith("image/"):
                        st.image(
                            attachment_url,
                            caption=attachment_name or "Image",
                            width="stretch"
                        )
                    else:
                        st.link_button(
                            f"📎 {attachment_name or 'Open attachment'} "
                            f"({human_file_size(attachment_size)})",
                            attachment_url
                        )
                else:
                    st.caption(
                        f"📎 {attachment_name or 'Attachment'} "
                        "(temporary link unavailable)"
                    )

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
# ADVANCED WORKSPACE HELPERS
# ============================================================

def audit(action, entity_type="", entity_id=None, details=""):
    try:
        supabase.table("audit_logs").insert({
            "user_id": current_user_id,
            "user_name": name,
            "action": action,
            "entity_type": entity_type,
            "entity_id": str(entity_id) if entity_id is not None else None,
            "details": details
        }).execute()
    except Exception:
        pass


def get_profile_by_name(person_name):
    for person in load_team_profiles():
        if person.get("name") == person_name:
            return person
    return None


def get_profile_id_by_name(person_name):
    profile_row = get_profile_by_name(person_name)
    return profile_row.get("id") if profile_row else None


def update_presence():
    status = st.session_state.get("presence_status", "Working")
    try:
        supabase.table("presence").upsert({
            "user_id": current_user_id,
            "user_name": name,
            "status": status,
            "last_seen": datetime.now(timezone.utc).isoformat()
        }, on_conflict="user_id").execute()
    except Exception:
        pass


def load_presence():
    try:
        result = (
            supabase.table("presence")
            .select("*")
            .order("user_name")
            .execute()
        )
        return result.data or []
    except Exception:
        return []


def process_due_recurring_tasks():
    """Materialize recurring tasks that are due. Safe to call on normal app visits."""
    if not is_manager():
        return
    try:
        result = (
            supabase.table("recurring_tasks")
            .select("*")
            .eq("active", True)
            .lte("next_run", datetime.now(timezone.utc).isoformat())
            .execute()
        )
        rows = result.data or []
        for row in rows:
            task_data = {
                "title": row.get("title"),
                "description": row.get("description", ""),
                "task_type": row.get("task_type", "Other"),
                "platform": row.get("platform", "Multiple"),
                "priority": row.get("priority", "Normal"),
                "status": "New",
                "assigned_to": row.get("assigned_to"),
                "assigned_by": name,
                "supplier_link": row.get("supplier_link", ""),
                "goods_id": row.get("goods_id", ""),
                "due_date": (
                    datetime.now(PK_TZ)
                    + timedelta(hours=int(row.get("due_after_hours") or 24))
                ).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "archived": False
            }
            created = supabase.table("tasks").insert(task_data).execute()
            task_id = created.data[0]["id"] if created.data else None
            if task_id:
                target_id = get_profile_id_by_name(row.get("assigned_to"))
                create_notification(
                    target_id,
                    "Recurring task assigned",
                    row.get("title", "New recurring task"),
                    "task",
                    task_id
                )
                add_activity(task_id, "Recurring Task Created", row.get("title", ""))

            cadence = row.get("cadence", "Daily")
            now_utc = datetime.now(timezone.utc)
            if cadence == "Weekly":
                next_run = now_utc + timedelta(days=7)
            elif cadence == "Monthly":
                next_run = now_utc + timedelta(days=30)
            else:
                next_run = now_utc + timedelta(days=1)

            supabase.table("recurring_tasks").update({
                "last_run": now_utc.isoformat(),
                "next_run": next_run.isoformat()
            }).eq("id", row.get("id")).execute()
    except Exception:
        pass


def escalate_unopened_urgent_tasks():
    """Notify management when an urgent task has not been opened within 60 minutes."""
    if not is_manager():
        return
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=60)
        urgent = (
            supabase.table("tasks")
            .select("*")
            .eq("priority", "Urgent")
            .eq("archived", False)
            .in_("status", ["New", "In Progress"])
            .lt("created_at", cutoff.isoformat())
            .execute()
        ).data or []

        for task in urgent:
            views = (
                supabase.table("task_views")
                .select("id")
                .eq("task_id", task["id"])
                .limit(1)
                .execute()
            ).data or []
            if not views:
                existing = (
                    supabase.table("notifications")
                    .select("id")
                    .eq("related_task_id", task["id"])
                    .eq("notification_type", "escalation")
                    .limit(1)
                    .execute()
                ).data or []
                if not existing:
                    for person in load_team_profiles():
                        if person.get("role") in ["Admin", "Team Lead"]:
                            create_notification(
                                person.get("id"),
                                "Urgent task not opened",
                                f'{task.get("title", "Urgent task")} has not been opened within 60 minutes.',
                                "escalation",
                                task["id"]
                            )
    except Exception:
        pass


def register_task_view(task_id):
    try:
        supabase.table("task_views").upsert({
            "task_id": task_id,
            "user_id": current_user_id,
            "user_name": name,
            "viewed_at": datetime.now(timezone.utc).isoformat()
        }, on_conflict="task_id,user_id").execute()
    except Exception:
        pass


def task_comments(task_id):
    try:
        result = (
            supabase.table("task_comments")
            .select("*")
            .eq("task_id", task_id)
            .order("created_at")
            .execute()
        )
        return result.data or []
    except Exception:
        return []


def add_task_comment(task_id, comment):
    comment = (comment or "").strip()
    if not comment:
        return False
    try:
        supabase.table("task_comments").insert({
            "task_id": task_id,
            "user_id": current_user_id,
            "user_name": name,
            "comment": comment
        }).execute()
        add_activity(task_id, "Comment Added", comment[:180])
        audit("Task comment added", "task", task_id, comment[:180])
        return True
    except Exception as error:
        st.error(error)
        return False


def task_subtasks(task_id):
    try:
        return (
            supabase.table("task_subtasks")
            .select("*")
            .eq("task_id", task_id)
            .order("created_at")
            .execute()
        ).data or []
    except Exception:
        return []


def add_subtask(task_id, title):
    title = (title or "").strip()
    if not title:
        return False
    try:
        supabase.table("task_subtasks").insert({
            "task_id": task_id,
            "title": title,
            "created_by": current_user_id
        }).execute()
        audit("Subtask created", "task", task_id, title)
        return True
    except Exception as error:
        st.error(error)
        return False


def toggle_subtask(subtask_id, completed):
    try:
        supabase.table("task_subtasks").update({
            "completed": completed,
            "completed_by": current_user_id if completed else None,
            "completed_at": datetime.now(timezone.utc).isoformat() if completed else None
        }).eq("id", subtask_id).execute()
        return True
    except Exception:
        return False


def upload_private_file(bucket, uploaded_file, prefix):
    if uploaded_file is None:
        return None
    try:
        data = uploaded_file.getvalue()
        if len(data) > 15 * 1024 * 1024:
            st.error("Maximum file size is 15 MB.")
            return None
        filename = safe_chat_filename(uploaded_file.name)
        object_path = (
            f"{current_user_id}/{prefix}/"
            f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_"
            f"{uuid.uuid4().hex[:10]}_{filename}"
        )
        supabase.storage.from_(bucket).upload(
            object_path,
            data,
            {"content-type": uploaded_file.type or "application/octet-stream", "upsert": "false"}
        )
        return {
            "path": object_path,
            "name": filename,
            "type": uploaded_file.type or "application/octet-stream",
            "size": len(data)
        }
    except Exception as error:
        st.error("Upload failed.")
        st.write(error)
        return None


def signed_file_url(bucket, path, seconds=3600):
    if not path:
        return None
    try:
        result = supabase.storage.from_(bucket).create_signed_url(path, seconds)
        if isinstance(result, str):
            return result
        if isinstance(result, dict):
            return result.get("signedURL") or result.get("signedUrl") or result.get("signed_url")
    except Exception:
        return None
    return None


def attach_file_to_task(task_id, uploaded_file):
    meta = upload_private_file("task-files", uploaded_file, f"task_{task_id}")
    if not meta:
        return False
    try:
        supabase.table("task_attachments").insert({
            "task_id": task_id,
            "user_id": current_user_id,
            "user_name": name,
            "file_path": meta["path"],
            "file_name": meta["name"],
            "file_type": meta["type"],
            "file_size": meta["size"]
        }).execute()
        add_activity(task_id, "Attachment Added", meta["name"])
        return True
    except Exception as error:
        st.error(error)
        return False


def load_task_attachments(task_id):
    try:
        return (
            supabase.table("task_attachments")
            .select("*")
            .eq("task_id", task_id)
            .order("created_at")
            .execute()
        ).data or []
    except Exception:
        return []


def load_task_templates():
    try:
        return (
            supabase.table("task_templates")
            .select("*")
            .eq("active", True)
            .order("name")
            .execute()
        ).data or []
    except Exception:
        return []


def create_task_from_template(template, assigned_to, due_date):
    try:
        due_dt = datetime.combine(due_date, time(hour=17))
        result = supabase.table("tasks").insert({
            "title": template.get("title_template") or template.get("name"),
            "description": template.get("description_template", ""),
            "task_type": template.get("task_type", "Other"),
            "platform": template.get("platform", "Multiple"),
            "priority": template.get("priority", "Normal"),
            "status": "New",
            "assigned_to": assigned_to,
            "assigned_by": name,
            "due_date": due_dt.isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "archived": False
        }).execute()
        task_id = result.data[0]["id"] if result.data else None
        if task_id:
            target_id = get_profile_id_by_name(assigned_to)
            create_notification(target_id, "New task assigned", template.get("name", "Task"), "task", task_id)
            audit("Task created from template", "task", task_id, template.get("name", ""))
        return True
    except Exception as error:
        st.error(error)
        return False


def send_direct_message(target_user_id, target_name, message):
    message = (message or "").strip()
    if not message:
        return False
    try:
        supabase.table("direct_messages").insert({
            "sender_id": current_user_id,
            "sender_name": name,
            "recipient_id": target_user_id,
            "recipient_name": target_name,
            "message": message
        }).execute()
        create_notification(
            target_user_id,
            f"Private message from {name}",
            message[:160],
            "direct_message"
        )
        return True
    except Exception as error:
        st.error(error)
        return False


def load_direct_messages(other_user_id):
    try:
        result = supabase.rpc(
            "get_direct_conversation",
            {"other_user": str(other_user_id)}
        ).execute()
        return result.data or []
    except Exception:
        return []


def browser_notification(title, body):
    """Best-effort desktop notification. Browser permission is required."""
    safe_title = json.dumps(str(title))
    safe_body = json.dumps(str(body))
    components.html(
        f"""
        <script>
        if ("Notification" in window) {{
            if (Notification.permission === "granted") {{
                new Notification({safe_title}, {{body: {safe_body}}});
            }}
        }}
        </script>
        """,
        height=0,
    )


def request_browser_notification_permission():
    components.html(
        """
        <button onclick="
            if ('Notification' in window) {
                Notification.requestPermission().then(function(permission) {
                    document.getElementById('result').innerText =
                        'Browser notification permission: ' + permission;
                });
            }
        ">Enable browser desktop notifications</button>
        <div id="result" style="font-family:Arial;font-size:12px;margin-top:8px"></div>
        """,
        height=70,
    )


def to_excel_bytes(sheets):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for sheet_name, dataframe in sheets.items():
            dataframe.to_excel(writer, sheet_name=sheet_name[:31], index=False)
    return output.getvalue()


def load_announcements(active_only=True):
    try:
        q = supabase.table("announcements").select("*")
        if active_only:
            q = q.eq("active", True)
        return q.order("pinned", desc=True).order("created_at", desc=True).execute().data or []
    except Exception:
        return []


def load_knowledge_items():
    try:
        return (
            supabase.table("knowledge_items")
            .select("*")
            .eq("active", True)
            .order("category")
            .order("title")
            .execute()
        ).data or []
    except Exception:
        return []


def get_user_preferences():
    try:
        rows = (
            supabase.table("user_preferences")
            .select("*")
            .eq("user_id", current_user_id)
            .limit(1)
            .execute()
        ).data or []
        return rows[0] if rows else {}
    except Exception:
        return {}


def save_user_preferences(values):
    try:
        values = dict(values)
        values["user_id"] = current_user_id
        values["updated_at"] = datetime.now(timezone.utc).isoformat()
        supabase.table("user_preferences").upsert(values, on_conflict="user_id").execute()
        return True
    except Exception as error:
        st.error(error)
        return False


def mark_break_start():
    try:
        open_break = (
            supabase.table("attendance_breaks")
            .select("*")
            .eq("user_id", current_user_id)
            .is_("break_end", "null")
            .limit(1)
            .execute()
        ).data or []
        if open_break:
            return True
        supabase.table("attendance_breaks").insert({
            "user_id": current_user_id,
            "user_name": name,
            "attendance_date": pakistan_today(),
            "break_start": datetime.now(timezone.utc).isoformat()
        }).execute()
        st.session_state.presence_status = "On Break"
        update_presence()
        return True
    except Exception as error:
        st.error(error)
        return False


def mark_break_end():
    try:
        open_break = (
            supabase.table("attendance_breaks")
            .select("*")
            .eq("user_id", current_user_id)
            .is_("break_end", "null")
            .order("break_start", desc=True)
            .limit(1)
            .execute()
        ).data or []
        if open_break:
            supabase.table("attendance_breaks").update({
                "break_end": datetime.now(timezone.utc).isoformat()
            }).eq("id", open_break[0]["id"]).execute()
        st.session_state.presence_status = "Working"
        update_presence()
        return True
    except Exception:
        return False


def current_break():
    try:
        rows = (
            supabase.table("attendance_breaks")
            .select("*")
            .eq("user_id", current_user_id)
            .is_("break_end", "null")
            .order("break_start", desc=True)
            .limit(1)
            .execute()
        ).data or []
        return rows[0] if rows else None
    except Exception:
        return None


def late_status(check_in_value):
    """
    Official TECHLOOM arrival grading:
    - Up to 10:15 AM: On Time
    - 10:16–10:30 AM: Late
    - 10:31–10:45 AM: Very Late
    - After 10:45 AM: Extremely Late
    """
    check_dt = parse_timestamp(check_in_value)
    if not check_dt:
        return "--"

    local = check_dt.astimezone(PK_TZ)
    arrival = local.time()

    if arrival <= time(hour=10, minute=15):
        return "On Time"
    if arrival <= time(hour=10, minute=30):
        return "Late"
    if arrival <= time(hour=10, minute=45):
        return "Very Late"
    return "Extremely Late"


def early_departure_status(check_out_value):
    out_dt = parse_timestamp(check_out_value)
    if not out_dt:
        return "--"
    local = out_dt.astimezone(PK_TZ)
    office_end = time(hour=18, minute=0)
    return "Early Departure" if local.time() < office_end else "Full Day"


def archive_task(task_id):
    try:
        supabase.table("tasks").update({
            "archived": True,
            "archived_at": datetime.now(timezone.utc).isoformat(),
            "archived_by": name
        }).eq("id", task_id).execute()
        add_activity(task_id, "Task Archived", f"Archived by {name}")
        audit("Task archived", "task", task_id)
        return True
    except Exception as error:
        st.error(error)
        return False


def handover_task(task_id, new_owner, reason):
    try:
        task_rows = (
            supabase.table("tasks")
            .select("*")
            .eq("id", task_id)
            .limit(1)
            .execute()
        ).data or []
        old_owner = task_rows[0].get("assigned_to") if task_rows else ""
        supabase.table("tasks").update({
            "assigned_to": new_owner,
            "handover_reason": reason,
            "handover_from": old_owner,
            "handover_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }).eq("id", task_id).execute()
        add_activity(task_id, "Task Handed Over", f"{old_owner} → {new_owner}. {reason}")
        target_id = get_profile_id_by_name(new_owner)
        create_notification(target_id, "Task handed over to you", task_rows[0].get("title", "Task") if task_rows else "Task", "task", task_id)
        audit("Task handover", "task", task_id, f"{old_owner} -> {new_owner}")
        return True
    except Exception as error:
        st.error(error)
        return False


def task_status_badge(status):
    icons = {
        "New": "🆕",
        "In Progress": "🟡",
        "Waiting on Information": "🟠",
        "Waiting on Platform": "🟣",
        "Submitted for Review": "🔵",
        "Changes Requested": "🔄",
        "Approved": "✅",
        "Completed": "✅"
    }
    return f"{icons.get(status, '⚪')} {status}"


def priority_badge(priority):
    icons = {"Urgent": "🔴", "High": "🟠", "Normal": "🔵", "Low": "⚪"}
    return f"{icons.get(priority, '⚪')} {priority}"


# Heartbeat / automation checks
update_presence()
process_due_recurring_tasks()
escalate_unopened_urgent_tasks()



def task_due_bucket(task):
    due = parse_timestamp(task.get("due_date")) if task.get("due_date") else None
    if not due:
        return "No Due Date"
    local_due = due.astimezone(PK_TZ)
    today = datetime.now(PK_TZ).date()
    if local_due.date() < today and task.get("status") not in ["Completed","Approved"]:
        return "Overdue"
    if local_due.date() == today:
        return "Due Today"
    if local_due.date() == today + timedelta(days=1):
        return "Due Tomorrow"
    return local_due.strftime("%d %b")


def task_priority_class(priority):
    return {
        "Urgent": "priority-urgent",
        "High": "priority-high",
        "Normal": "priority-normal",
        "Low": "priority-low"
    }.get(priority, "priority-normal")


def open_task_detail(task):
    st.session_state.selected_task_id = task["id"]
    st.session_state.selected_task_title = task.get("title", "Task")


def find_task_by_id(task_id, source_tasks):
    for row in source_tasks:
        if str(row.get("id")) == str(task_id):
            return row
    return None


def render_task_card(task, key_prefix):
    task_id = task["id"]
    title = task.get("title", "Untitled Task")
    platform = task.get("platform", "N/A")
    task_type = task.get("task_type", "Task")
    priority = task.get("priority", "Normal")
    status = task.get("status", "New")
    due_text = task_due_bucket(task)
    assigned_by = task.get("assigned_by", "")
    goods_id = task.get("goods_id", "")

    st.markdown(
        (
            '<div class="work-card">'
            f'<div class="work-card-title">{title}</div>'
            f'<span class="status-chip">{platform}</span>'
            f'<span class="status-chip {task_priority_class(priority)}">{priority}</span>'
            f'<span class="status-chip">{status}</span>'
            f'<div class="work-meta">Due: {due_text} • Type: {task_type}</div>'
            f'<div class="work-meta">Assigned by: {assigned_by}'
            + (f' • ID: {goods_id}' if goods_id else '') +
            '</div></div>'
        ),
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        if status == "New" and not is_manager():
            if st.button("▶ Start", key=f"{key_prefix}_start_{task_id}", use_container_width=True):
                if update_task_status(task_id, "In Progress"):
                    st.rerun()
        else:
            if st.button("Open", key=f"{key_prefix}_open_{task_id}", use_container_width=True):
                open_task_detail(task)
                st.rerun()
    with c2:
        if not is_manager() and status in ["In Progress","Changes Requested","Waiting on Information","Waiting on Platform","New"]:
            if st.button("📤 Review", key=f"{key_prefix}_review_{task_id}", use_container_width=True):
                open_task_detail(task)
                st.session_state.task_detail_tab = "Submission"
                st.rerun()
        else:
            if st.button("Details", key=f"{key_prefix}_details_{task_id}", use_container_width=True):
                open_task_detail(task)
                st.rerun()


def render_task_detail_panel(task):
    task_id = task["id"]
    register_task_view(task_id)

    st.markdown("---")
    st.markdown(f"## {task.get('title','Untitled Task')}")
    st.caption(
        f"{task.get('platform','')} • {task.get('task_type','')} • "
        f"{priority_badge(task.get('priority','Normal'))} • "
        f"{task_status_badge(task.get('status','New'))}"
    )

    top1, top2, top3, top4 = st.columns(4)
    top1.metric("Owner", task.get("assigned_to",""))
    top2.metric("Assigned By", task.get("assigned_by",""))
    top3.metric("Due", task_due_bucket(task))
    top4.metric("Goods / ASIN / SKU", task.get("goods_id","") or "—")

    tabs = st.tabs(["Overview","Checklist","Comments","Files","Activity","Submission","History"])

    with tabs[0]:
        st.write("### Instructions")
        st.write(task.get("description","") or "No instructions provided.")

        l1, l2 = st.columns(2)
        with l1:
            if task.get("supplier_link"):
                st.link_button("🔗 Supplier Link", task.get("supplier_link"))
            if task.get("listing_url"):
                st.link_button("🛍 Listing URL", task.get("listing_url"))
        with l2:
            if task.get("submission_link"):
                st.link_button("📤 Submitted Work", task.get("submission_link"))
            if task.get("review_reference_link"):
                st.link_button("🧭 Reviewer Reference", task.get("review_reference_link"))

        if task.get("review_notes"):
            st.warning(f"Review Notes: {task.get('review_notes')}")

    with tabs[1]:
        subtasks = task_subtasks(task_id)
        completed = sum(1 for s in subtasks if s.get("completed"))
        total = len(subtasks)
        st.caption(f"{completed}/{total} checklist items completed")
        for sub in subtasks:
            checked = st.checkbox(
                sub.get("title","Subtask"),
                value=bool(sub.get("completed")),
                key=f"detail_sub_{sub['id']}"
            )
            if checked != bool(sub.get("completed")):
                if toggle_subtask(sub["id"], checked):
                    st.rerun()
        new_sub = st.text_input("New checklist item", key=f"detail_new_sub_{task_id}")
        if st.button("Add item", key=f"detail_add_sub_{task_id}"):
            if add_subtask(task_id, new_sub):
                st.rerun()

    with tabs[2]:
        for row in task_comments(task_id):
            with st.container(border=True):
                st.markdown(f"**{row.get('user_name','User')}**")
                st.write(row.get("comment",""))
                st.caption(row.get("created_at",""))
        new_comment = st.text_area("Comment", key=f"detail_comment_{task_id}")
        if st.button("Post comment", key=f"detail_post_comment_{task_id}"):
            if add_task_comment(task_id, new_comment):
                st.rerun()

    with tabs[3]:
        task_file = st.file_uploader(
            "Attach file",
            type=["png","jpg","jpeg","webp","pdf","doc","docx","xls","xlsx","csv","txt","zip"],
            key=f"detail_file_{task_id}"
        )
        if task_file and st.button("Upload", key=f"detail_upload_{task_id}"):
            if attach_file_to_task(task_id, task_file):
                st.rerun()
        for att in load_task_attachments(task_id):
            url = signed_file_url("task-files", att.get("file_path"))
            if url:
                st.link_button(
                    f"📎 {att.get('file_name','Attachment')} ({human_file_size(att.get('file_size'))})",
                    url
                )

    with tabs[4]:
        try:
            timeline = (
                supabase.table("task_activity")
                .select("*")
                .eq("task_id", task_id)
                .order("created_at", desc=True)
                .execute()
            ).data or []
        except Exception:
            timeline = []
        for event in timeline:
            with st.container(border=True):
                st.markdown(f"**{event.get('action','Activity')}**")
                st.write(event.get("details",""))
                st.caption(f"{event.get('user_name','')} • {event.get('created_at','')}")

    with tabs[5]:
        if is_manager():
            st.info("Review employee submission from the Approvals page.")
            if task.get("submission_link"):
                st.link_button("Open submitted link", task.get("submission_link"))
        else:
            st.write("### Send Back for Review")
            submission_link = st.text_input(
                "Work / listing / case link",
                value=task.get("submission_link","") or "",
                key=f"detail_submission_link_{task_id}"
            )
            submission_note = st.text_area(
                "Submission note",
                value=task.get("submission_note","") or "",
                key=f"detail_submission_note_{task_id}"
            )
            if st.button("📤 Send to AIFA for Review", type="primary", key=f"detail_submit_{task_id}", use_container_width=True):
                try:
                    supabase.table("tasks").update({
                        "status":"Submitted for Review",
                        "submission_link":submission_link.strip(),
                        "submission_note":submission_note.strip(),
                        "submitted_at":datetime.now(timezone.utc).isoformat(),
                        "updated_at":datetime.now(timezone.utc).isoformat()
                    }).eq("id",task_id).execute()
                    for person in load_team_profiles():
                        if person.get("role") in ["Admin","Team Lead"]:
                            create_notification(
                                person.get("id"),
                                f"{name} submitted a task",
                                task.get("title","Task"),
                                "review",
                                task_id
                            )
                    add_activity(task_id,"Submitted for Review",submission_note[:180])
                    st.success("Task sent for review.")
                    st.rerun()
                except Exception as error:
                    st.error(error)

    with tabs[6]:
        try:
            history = (
                supabase.table("task_activity")
                .select("*")
                .eq("task_id", task_id)
                .order("created_at")
                .execute()
            ).data or []
        except Exception:
            history = []
        for event in history:
            st.write(
                f"**{event.get('created_at','')}** — "
                f"{event.get('user_name','')} — "
                f"{event.get('action','')} — "
                f"{event.get('details','')}"
            )

    if st.button("✕ Close Task", key=f"close_task_{task_id}"):
        st.session_state.selected_task_id = None
        st.rerun()


def get_attendance_scope_rows(start_date, end_date):
    """
    Build a complete attendance matrix for all active team members.
    Missing attendance = Absent, but only from the official first attendance day.
    """
    start_date = max(start_date, ATTENDANCE_START_DATE)
    if end_date < ATTENDANCE_START_DATE:
        return []

    profiles = [p for p in load_team_profiles() if p.get("name")]
    try:
        attendance_rows = (
            supabase.table("attendance")
            .select("*")
            .gte("attendance_date", start_date.isoformat())
            .lte("attendance_date", end_date.isoformat())
            .order("attendance_date")
            .execute()
        ).data or []
    except Exception:
        attendance_rows = []

    by_key = {
        (str(r.get("user_id")), str(r.get("attendance_date"))): r
        for r in attendance_rows
    }

    results = []
    current = start_date
    while current <= end_date:
        for person in profiles:
            user_id = person.get("id")
            row = by_key.get((str(user_id), current.isoformat()))
            if row:
                status = row.get("status") or "Present"
                check_in = row.get("check_in")
                check_out = row.get("check_out")
                arrival = late_status(check_in)
                departure = early_departure_status(check_out)
            else:
                status = "Absent"
                check_in = None
                check_out = None
                arrival = "--"
                departure = "--"

            results.append({
                "Date": current.isoformat(),
                "Employee": person.get("name"),
                "Department": person.get("department", ""),
                "Role": person.get("role", ""),
                "Status": status,
                "Check In": format_pk_time(check_in) if check_in else "--",
                "Check Out": format_pk_time(check_out) if check_out else "--",
                "Arrival": arrival,
                "Departure": departure
            })
        current += timedelta(days=1)

    return results


def attendance_period_dates(period_type, anchor_date):
    if period_type == "Weekly":
        start = anchor_date - timedelta(days=anchor_date.weekday())
        end = start + timedelta(days=6)
    else:
        start = anchor_date.replace(day=1)
        end = anchor_date.replace(
            day=calendar.monthrange(anchor_date.year, anchor_date.month)[1]
        )
    return start, end


def attendance_summary_dataframe(rows):
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame()

    summary = []
    for employee, group in df.groupby("Employee"):
        present = int((group["Status"].str.lower() == "present").sum())
        absent = int((group["Status"].str.lower() == "absent").sum())
        late = int((group["Arrival"] == "Late").sum())
        very_late = int((group["Arrival"] == "Very Late").sum())
        extremely_late = int((group["Arrival"] == "Extremely Late").sum())
        on_time = int((group["Arrival"] == "On Time").sum())

        summary.append({
            "Employee": employee,
            "Present Days": present,
            "Absent Days": absent,
            "On Time Days": on_time,
            "Late Days": late,
            "Very Late Days": very_late,
            "Extremely Late Days": extremely_late,
            "Total Days": len(group)
        })
    return pd.DataFrame(summary)


def attendance_excel_bytes(detail_df, summary_df, title):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
        detail_df.to_excel(writer, sheet_name="Attendance", index=False)
    return output.getvalue()


def today_team_attendance():
    try:
        return (
            supabase.table("attendance")
            .select("*")
            .eq("attendance_date", pakistan_today().isoformat())
            .execute()
        ).data or []
    except Exception:
        return []


def today_activity_counts():
    """Count meaningful task activity today by employee."""
    try:
        start_local = datetime.combine(
            pakistan_today(),
            time.min,
            tzinfo=PK_TZ
        ).astimezone(timezone.utc)

        rows = (
            supabase.table("task_activity")
            .select("*")
            .gte("created_at", start_local.isoformat())
            .execute()
        ).data or []
    except Exception:
        rows = []

    counts = {}
    for row in rows:
        person = row.get("user_name")
        if person:
            counts[person] = counts.get(person, 0) + 1
    return counts


def today_completed_task_counts():
    try:
        start_local = datetime.combine(
            pakistan_today(),
            time.min,
            tzinfo=PK_TZ
        ).astimezone(timezone.utc)

        rows = (
            supabase.table("tasks")
            .select("assigned_to,status,completed_at,updated_at")
            .in_("status", ["Completed", "Approved"])
            .gte("updated_at", start_local.isoformat())
            .execute()
        ).data or []
    except Exception:
        rows = []

    counts = {}
    for row in rows:
        person = row.get("assigned_to")
        if person:
            counts[person] = counts.get(person, 0) + 1
    return counts


def build_team_shoutout():
    """
    Pick one positive, useful message for the top notification bar.
    Priority:
    1. On-time attendance shout-out
    2. Strong completion activity
    3. Strong overall task activity
    4. Office timing reminder
    """
    attendance = today_team_attendance()

    on_time_people = []
    for row in attendance:
        if late_status(row.get("check_in")) == "On Time":
            employee = row.get("employee_name")
            if employee:
                on_time_people.append(employee)

    completed = today_completed_task_counts()
    activity = today_activity_counts()

    if on_time_people:
        if len(on_time_people) == 1:
            return (
                "👏",
                f"Shout-out to {on_time_people[0]} for being on time today!",
                "On-time arrival keeps the day moving smoothly."
            )
        names = ", ".join(on_time_people[:3])
        suffix = "" if len(on_time_people) <= 3 else f" +{len(on_time_people)-3} more"
        return (
            "🌟",
            f"Great start today: {names}{suffix}",
            "These team members checked in within the official on-time window."
        )

    if completed:
        top_person = max(completed, key=completed.get)
        top_count = completed[top_person]
        if top_count > 0:
            return (
                "🏆",
                f"Activity shout-out: {top_person}",
                f"{top_count} task{'s' if top_count != 1 else ''} completed/approved today."
            )

    if activity:
        top_person = max(activity, key=activity.get)
        top_count = activity[top_person]
        if top_count >= 3:
            return (
                "⚡",
                f"{top_person} is active today",
                f"{top_count} task updates recorded so far."
            )

    return (
        "🕙",
        "Office hours: 10:00 AM – 6:00 PM",
        "Arrival up to 10:15 AM is considered on time."
    )


def render_team_shoutout_bar():
    icon, title, body = build_team_shoutout()
    st.markdown(
        f"""
        <div style="
            padding:14px 18px;
            border-radius:14px;
            border:1px solid #dfe7e5;
            background:linear-gradient(90deg,#f7fffd 0%,#ffffff 100%);
            margin:4px 0 18px 0;
            box-shadow:0 2px 8px rgba(20,90,80,.05);
        ">
            <div style="font-size:14px;font-weight:800;color:#173c37;">
                {icon} {title}
            </div>
            <div style="font-size:12px;color:#65736f;margin-top:3px;">
                {body}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_value(value, fallback="—"):
    """Return a clean display value instead of None / empty strings."""
    if value is None:
        return fallback
    value = str(value).strip()
    return value if value else fallback


def portal_header(page_name="Techloom HQ"):
    unread = 0
    try:
        unread = len(get_unread_notifications())
    except Exception:
        pass
    initial = (name or "U")[:1].upper()
    st.markdown(
        f"""
        <div class="portal-topbar">
          <div class="crumb"><span class="crumb-mark">◢</span><span>{page_name}</span></div>
          <div class="top-user">
            <span class="notify-dot">▤</span>
            <span class="top-avatar">{initial}</span>
            <span>{name}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def sprint_tasks():
    tasks = load_all_tasks() if is_manager() else load_my_tasks()
    cutoff = datetime.now(PK_TZ).date() + timedelta(days=7)
    result = []
    for task in tasks:
        if task.get("status") in ["Completed", "Approved"]:
            continue
        due = parse_timestamp(task.get("due_date")) if task.get("due_date") else None
        if not due or due.astimezone(PK_TZ).date() <= cutoff:
            result.append(task)
    return result


def load_personal_note():
    try:
        rows = (
            supabase.table("personal_notes")
            .select("*")
            .eq("user_id", current_user_id)
            .limit(1)
            .execute()
        ).data or []
        return rows[0].get("content", "") if rows else ""
    except Exception:
        return ""


def save_personal_note(content):
    try:
        supabase.table("personal_notes").upsert({
            "user_id": current_user_id,
            "content": content,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }, on_conflict="user_id").execute()
        return True
    except Exception as error:
        st.error(error)
        return False


def upload_hub_file(uploaded_file):
    meta = upload_private_file("data-hub", uploaded_file, "shared")
    if not meta:
        return False
    try:
        supabase.table("shared_files").insert({
            "uploader_id": current_user_id,
            "uploader_name": name,
            "file_path": meta["path"],
            "file_name": meta["name"],
            "file_type": meta["type"],
            "file_size": meta["size"]
        }).execute()
        return True
    except Exception as error:
        st.error(error)
        return False


def load_hub_files():
    try:
        return (
            supabase.table("shared_files")
            .select("*")
            .order("created_at", desc=True)
            .limit(100)
            .execute()
        ).data or []
    except Exception:
        return []


def upload_secure_portal_file(uploaded_file, allowed_user_ids):
    meta = upload_private_file("secure-files", uploaded_file, "secure")
    if not meta:
        return False
    try:
        created = supabase.table("secure_files").insert({
            "owner_id": current_user_id,
            "owner_name": name,
            "file_path": meta["path"],
            "file_name": meta["name"],
            "file_type": meta["type"],
            "file_size": meta["size"]
        }).execute()
        file_id = created.data[0]["id"] if created.data else None
        if file_id:
            for uid in allowed_user_ids:
                supabase.table("secure_file_access").insert({
                    "file_id": file_id,
                    "user_id": uid
                }).execute()
        return True
    except Exception as error:
        st.error(error)
        return False


def load_secure_portal_files():
    try:
        result = supabase.rpc("get_accessible_secure_files").execute()
        return result.data or []
    except Exception:
        return []

def go_to_chat():
    """Open Team Chat from the dashboard shortcut."""
    st.session_state["main_portal_nav"] = "Chat"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="side-brand">
          <span class="brand-mark">T</span>
          <strong>Techloom</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="side-user">
          <b>{name}</b>
          <small>{role} • {department}</small>
        </div>
        """,
        unsafe_allow_html=True
    )

    chat_unread_count = get_unread_chat_count()
    chat_label = "Chat"

    if is_manager():
        menu_options = [
            "Company HQ",
            "My Tasks",
            "Current Sprint",
            "Timeline",
            "Attendance",
            "Team",
            chat_label,
            "Direct Messages",
            "Data Hub",
            "Knowledge Base",
            "My Notes",
            "Secure Folder",
            "Settings",
        ]
    else:
        menu_options = [
            "Company HQ",
            "My Tasks",
            "Current Sprint",
            "Timeline",
            "Attendance",
            "Team",
            chat_label,
            "Direct Messages",
            "Data Hub",
            "Knowledge Base",
            "My Notes",
            "Secure Folder",
            "Settings",
        ]

    page = st.radio(
        "Navigation",
        menu_options,
        label_visibility="collapsed",
        key="main_portal_nav"
    )

    st.write("")
    if is_manager():
        if st.button("＋ New task", type="primary", use_container_width=True, key="sidebar_new_task"):
            st.session_state["force_create_task"] = True

    if st.button("Sign out", use_container_width=True, key="portal_logout"):
        logout()

# sidebar quick-create override
if st.session_state.pop("force_create_task", False):
    page = "Create Task"

# ============================================================
# DASHBOARD
# ============================================================

if page == "Company HQ":

    portal_header("Techloom HQ")

    current_day = datetime.now(PK_TZ)
    tasks = load_all_tasks() if is_manager() else load_my_tasks()

    active_statuses = {
        "New",
        "In Progress",
        "Waiting on Information",
        "Waiting on Platform",
        "Submitted for Review",
        "Changes Requested"
    }

    active_tasks = [
        t for t in tasks
        if t.get("status", "New") in active_statuses
        and not t.get("archived", False)
    ]

    def _due_local(task):
        if not task.get("due_date"):
            return None
        parsed = parse_timestamp(task.get("due_date"))
        return parsed.astimezone(PK_TZ) if parsed else None

    today = current_day.date()
    due_today = [t for t in active_tasks if _due_local(t) and _due_local(t).date() == today]
    overdue = [t for t in active_tasks if _due_local(t) and _due_local(t).date() < today]
    urgent = [t for t in active_tasks if t.get("priority") == "Urgent"]
    review = [t for t in active_tasks if t.get("status") == "Submitted for Review"]

    st.markdown(
        f"""
        <div class="dashboard-hero">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:20px">
            <div>
              <div class="dashboard-hero-title">Dashboard</div>
              <div class="dashboard-hero-copy">Your live workspace for today.</div>
            </div>
            <div class="hero-date">{current_day.strftime("%A")}<br>{current_day.strftime("%d %B %Y")}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="today-strip">
          <b>Today at Techloom</b> &nbsp; · &nbsp;
          {len(due_today)} due today &nbsp; · &nbsp;
          {len(overdue)} overdue &nbsp; · &nbsp;
          {len(review)} awaiting review
        </div>
        """,
        unsafe_allow_html=True
    )

    # Front-page chat shortcut with live unread badge.
    unread_chat = get_unread_chat_count()

    chat_space, chat_widget = st.columns([4.8, 1.2])

    with chat_widget:
        badge_html = (
            f'<span class="chat-unread-badge">{unread_chat if unread_chat < 100 else "99+"}</span>'
            if unread_chat > 0 else ""
        )
        chat_copy = (
            f"{unread_chat} unread message{'s' if unread_chat != 1 else ''}"
            if unread_chat > 0 else "No unread messages"
        )

        st.markdown(
            f"""
            <div class="chat-shortcut-card">
                <div class="chat-shortcut-icon">
                    💬
                    {badge_html}
                </div>
                <div>
                    <div class="chat-shortcut-title">Team Chat</div>
                    <div class="chat-shortcut-copy">{chat_copy}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.button(
            "Open Chat",
            key="dashboard_open_chat",
            use_container_width=True,
            on_click=go_to_chat
        )

    # Compact announcement: show only latest active one
    try:
        ann = (
            supabase.table("announcements")
            .select("*")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        ).data or []
    except Exception:
        ann = []

    if ann:
        latest = ann[0]
        st.markdown(
            f"""
            <div class="announcement-mini">
              📣 <b>{display_value(latest.get("title"))}</b> — {display_value(latest.get("body"))}
            </div>
            """,
            unsafe_allow_html=True
        )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active", len(active_tasks))
    m2.metric("Due Today", len(due_today))
    m3.metric("Urgent", len(urgent))
    m4.metric("For Review", len(review))

    st.write("")

    left, right = st.columns([1.55, 1])

    with left:
        st.markdown('<div class="section-title">Priority work</div>', unsafe_allow_html=True)

        priority = []
        seen = set()
        for group in [overdue, urgent, due_today, review, active_tasks]:
            for task in group:
                tid = task.get("id")
                if tid not in seen:
                    priority.append(task)
                    seen.add(tid)

        if priority:
            for idx, task in enumerate(priority[:6]):
                due = _due_local(task)
                due_label = due.strftime("%d %b") if due else "No due date"
                priority_value = display_value(task.get("priority"), "Normal")
                priority_class = str(priority_value).lower()

                st.markdown(
                    f"""
                    <div class="attention-card">
                      <div class="attention-card-title">{display_value(task.get("title"))}</div>
                      <div class="attention-card-meta">
                        <span class="tl-chip tl-chip-platform">{display_value(task.get("platform"))}</span>
                        <span class="tl-chip tl-chip-status">{display_value(task.get("status"))}</span>
                        <span class="tl-chip tl-chip-{priority_class}">{priority_value}</span>
                        <span>Due {due_label}</span>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.caption("Nothing urgent right now.")

    with right:
        st.markdown('<div class="section-title">Team today</div>', unsafe_allow_html=True)

        try:
            today_att = today_team_attendance()
        except Exception:
            today_att = []

        att_map = {r.get("employee_name"): r for r in today_att}

        unique_people = []
        seen_people = set()

        for person in load_team_profiles():
            person_name = str(person.get("name") or "").strip()
            person_email = str(person.get("email") or "").strip().lower()
            person_id = str(person.get("id") or "").strip()
            dedupe_key = person_id or person_email or person_name.lower()

            if not dedupe_key or dedupe_key in seen_people:
                continue

            seen_people.add(dedupe_key)
            unique_people.append(person)

        for person in unique_people[:8]:
            person_name = person.get("name")
            rec = att_map.get(person_name)

            if rec:
                arrival = late_status(rec.get("check_in"))
                dot_class = (
                    "tl-dot-good" if arrival == "On Time"
                    else "tl-dot-warn" if arrival in ["Late", "Very Late"]
                    else "tl-dot-bad"
                )
                status = f"{arrival} · {format_pk_time(rec.get('check_in'))}"
            else:
                dot_class = "tl-dot-neutral"
                status = "Not marked"

            st.markdown(
                f"""
                <div class="attention-card">
                  <div class="attention-card-title">
                    <span class="tl-dot {dot_class}"></span>{display_value(person_name)}
                  </div>
                  <div class="attention-card-meta">{status}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")
    st.markdown('<div class="section-title">Recent activity</div>', unsafe_allow_html=True)

    try:
        activity = (
            supabase.table("task_activity")
            .select("*")
            .order("created_at", desc=True)
            .limit(6)
            .execute()
        ).data or []
    except Exception:
        activity = []

    if activity:
        for item in activity:
            st.markdown(
                f"""
                <div class="attention-card">
                  <div class="attention-card-title">
                    {display_value(item.get("user_name"), "User")} · {display_value(item.get("action"))}
                  </div>
                  <div class="attention-card-meta">
                    {display_value(item.get("details"))} · {display_value(item.get("created_at"))}
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ============================================================
# MY TASKS / TEAM TASKS — WORK INBOX + KANBAN
# ============================================================

elif page == "My Tasks":

    portal_header("Tasks")
    is_team_view = is_manager() and st.toggle("Team view", value=False, key="task_team_view_toggle")
    tasks = load_all_tasks() if is_team_view else load_my_tasks()

    st.markdown(
        '<div class="task-board-header">'
        '<div>'
        f'<div class="task-board-title">{"Team Control Board" if is_team_view else "My Work Inbox"}</div>'
        f'<div class="task-board-copy">{"See team workload by status and owner." if is_team_view else "Focus on what needs attention first, then move work through the workflow."}</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    if not tasks:
        st.info("No active tasks.")
        st.stop()

    # Work Inbox
    today = datetime.now(PK_TZ).date()

    def due_date_local(task):
        due = parse_timestamp(task.get("due_date")) if task.get("due_date") else None
        return due.astimezone(PK_TZ).date() if due else None

    new_today = [
        t for t in tasks
        if parse_timestamp(t.get("created_at")) and
        parse_timestamp(t.get("created_at")).astimezone(PK_TZ).date() == today
    ]
    due_today = [t for t in tasks if due_date_local(t) == today and t.get("status") not in ["Completed","Approved"]]
    urgent = [t for t in tasks if t.get("priority") == "Urgent" and t.get("status") not in ["Completed","Approved"]]
    review = [t for t in tasks if t.get("status") == "Submitted for Review"]
    changes = [t for t in tasks if t.get("status") == "Changes Requested"]

    a,b,c,d,e = st.columns(5)
    a.metric("New Today", len(new_today))
    b.metric("Due Today", len(due_today))
    c.metric("Urgent", len(urgent))
    d.metric("For Review", len(review))
    e.metric("Changes", len(changes))

    st.write("")

    search_col, status_col, priority_col, platform_col = st.columns(4)
    with search_col:
        search = st.text_input("Search", placeholder="Title, Goods ID, ASIN...")
    with status_col:
        status_filter = st.selectbox("Status", ["All","New","In Progress","Waiting on Information","Waiting on Platform","Submitted for Review","Changes Requested","Approved","Completed"])
    with priority_col:
        priority_filter = st.selectbox("Priority", ["All","Urgent","High","Normal","Low"])
    with platform_col:
        platform_filter = st.selectbox("Platform", ["All","Temu","Amazon","eBay","TikTok","Multiple"])

    filtered = []
    for task in tasks:
        haystack = " ".join(str(task.get(k,"")) for k in ["title","goods_id","platform","task_type","assigned_to"]).lower()
        if search and search.lower() not in haystack:
            continue
        if status_filter != "All" and task.get("status") != status_filter:
            continue
        if priority_filter != "All" and task.get("priority") != priority_filter:
            continue
        if platform_filter != "All" and task.get("platform") != platform_filter:
            continue
        filtered.append(task)

    tabs = st.tabs(["📥 Work Inbox","🧱 Kanban","👤 By Owner"] if is_team_view else ["📥 Work Inbox","🧱 Kanban"])

    with tabs[0]:
        inbox_groups = [
            ("🔴 Urgent", urgent),
            ("📅 Due Today", due_today),
            ("🔄 Changes Requested", changes),
            ("🆕 New", [t for t in filtered if t.get("status")=="New"]),
            ("🟡 In Progress", [t for t in filtered if t.get("status")=="In Progress"]),
        ]

        for heading, group in inbox_groups:
            matching = [t for t in group if t in filtered]
            if not matching:
                continue
            st.markdown(f"### {heading}")
            cols = st.columns(2)
            for i, task in enumerate(matching):
                with cols[i % 2]:
                    render_task_card(task, f"inbox_{heading}_{i}")

    with tabs[1]:
        columns = [
            ("New","New"),
            ("In Progress","In Progress"),
            ("Waiting","Waiting on Information"),
            ("For Review","Submitted for Review"),
            ("Changes","Changes Requested"),
            ("Done","Completed"),
        ]

        kanban_cols = st.columns(len(columns))
        for col_index, (label, status_value) in enumerate(columns):
            with kanban_cols[col_index]:
                group = [
                    t for t in filtered
                    if (
                        t.get("status") == status_value
                        or (
                            label == "Waiting"
                            and t.get("status") in ["Waiting on Information","Waiting on Platform"]
                        )
                        or (
                            label == "Done"
                            and t.get("status") in ["Completed","Approved"]
                        )
                    )
                ]
                st.markdown(
                    f'<div class="kanban-column-title">{label}<span class="kanban-count">{len(group)}</span></div>',
                    unsafe_allow_html=True
                )
                for i, task in enumerate(group):
                    render_task_card(task, f"kanban_{col_index}_{i}")

    if is_team_view:
        with tabs[2]:
            owners = sorted(set(t.get("assigned_to","Unassigned") for t in filtered))
            for owner in owners:
                owner_tasks = [t for t in filtered if t.get("assigned_to","Unassigned")==owner]
                with st.expander(f"{owner} • {len(owner_tasks)} tasks"):
                    for i, task in enumerate(owner_tasks):
                        render_task_card(task, f"owner_{owner}_{i}")

    selected_id = st.session_state.get("selected_task_id")
    if selected_id:
        selected_task = find_task_by_id(selected_id, tasks)
        if selected_task:
            render_task_detail_panel(selected_task)

# ============================================================
# CREATE TASK
# ============================================================

elif page == "Create Task":

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

elif page == "✓ Approvals":

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

elif page == "Attendance":

    portal_header("Attendance")

    now_local = datetime.now(PK_TZ)
    attendance_date = now_local.date()
    attendance_day_name = now_local.strftime("%A")
    attendance_date_label = now_local.strftime("%d %B %Y")

    st.markdown(
        f"""
        <div class="attendance-hero">
            <div class="attendance-eyebrow">Today's Attendance</div>
            <div class="attendance-date">{attendance_date_label}</div>
            <div class="attendance-day">{attendance_day_name} • Office Hours 10:00 AM – 6:00 PM</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="attendance-rules">
            <b>Arrival grading:</b>
            On Time up to 10:15 AM •
            Late 10:16–10:30 AM •
            Very Late 10:31–10:45 AM •
            Extremely Late after 10:45 AM
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    attendance = get_today_attendance()

    if attendance is None:

        st.warning(
            f"Attendance has not been marked for {attendance_day_name}, {attendance_date_label}."
        )

        st.markdown(
            f"""
            <div class="attendance-status-card">
                <div class="attendance-label">Current Status</div>
                <div class="attendance-value">Not Marked</div>
                <div class="attendance-note">
                    Attendance date: {attendance_date_label} • {attendance_day_name}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        if st.button(
            f"✅ Mark Attendance for {attendance_day_name}",
            type="primary",
            use_container_width=True,
            key="attendance_page_checkin"
        ):
            if check_in_employee():
                st.success("Check-in recorded successfully.")
                st.rerun()

    else:

        check_in_value = attendance.get("check_in")
        check_out_value = attendance.get("check_out")
        arrival_grade = late_status(check_in_value)
        work_duration = working_time(check_in_value, check_out_value)

        a1, a2, a3, a4 = st.columns(4)

        with a1:
            st.markdown(
                f"""
                <div class="attendance-status-card">
                    <div class="attendance-label">Check In</div>
                    <div class="attendance-value">{format_pk_time(check_in_value)}</div>
                    <div class="attendance-note">{arrival_grade}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with a2:
            st.markdown(
                f"""
                <div class="attendance-status-card">
                    <div class="attendance-label">Check Out</div>
                    <div class="attendance-value">{format_pk_time(check_out_value) if check_out_value else "Not Yet"}</div>
                    <div class="attendance-note">{early_departure_status(check_out_value) if check_out_value else "Working day in progress"}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with a3:
            st.markdown(
                f"""
                <div class="attendance-status-card">
                    <div class="attendance-label">Working Time</div>
                    <div class="attendance-value">{work_duration}</div>
                    <div class="attendance-note">Recorded for {attendance_day_name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with a4:
            st.markdown(
                f"""
                <div class="attendance-status-card">
                    <div class="attendance-label">Attendance Date</div>
                    <div class="attendance-value">{attendance_date.strftime("%d %b")}</div>
                    <div class="attendance-note">{attendance_day_name}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")
        st.subheader("Today's Actions")

        if not check_out_value:
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
            st.success("Today's attendance is complete.")

    st.write("")
    st.subheader("Break Management")

    open_break = current_break()
    b1, b2 = st.columns(2)

    with b1:
        if open_break:
            st.warning("You are currently on break.")
        else:
            if st.button(
                "☕ Start Break",
                use_container_width=True,
                key="start_break"
            ):
                if mark_break_start():
                    st.rerun()

    with b2:
        if open_break:
            if st.button(
                "▶️ End Break",
                type="primary",
                use_container_width=True,
                key="end_break"
            ):
                if mark_break_end():
                    st.rerun()
        else:
            st.caption("No active break.")

    st.write("")
    st.subheader("Attendance History")

    try:
        history_result = (
            supabase
            .table("attendance")
            .select("*")
            .eq("user_id", current_user_id)
            .order("attendance_date", desc=True)
            .limit(60)
            .execute()
        )

        history = history_result.data or []
        history_rows = []

        for record in history:
            record_date = record.get("attendance_date")
            try:
                date_obj = datetime.fromisoformat(str(record_date)).date()
                day_name = date_obj.strftime("%A")
            except Exception:
                day_name = "—"

            history_rows.append({
                "Date": record_date,
                "Day": day_name,
                "Check In": format_pk_time(record.get("check_in")),
                "Arrival": late_status(record.get("check_in")),
                "Check Out": format_pk_time(record.get("check_out")),
                "Departure": early_departure_status(record.get("check_out")),
                "Working Time": working_time(
                    record.get("check_in"),
                    record.get("check_out")
                ),
                "Status": record.get("status", "Present")
            })

        if history_rows:
            st.dataframe(
                pd.DataFrame(history_rows),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No attendance history yet.")

    except Exception as error:
        st.error("Could not load attendance history.")
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

elif page == "Team":

    portal_header("Team")

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

            card_html = (
                '<div class="task-card">'
                f'<div class="task-card-title">{display_value(task.get("title"))}</div>'
                f'<div class="task-meta">{display_value(task.get("task_type"))}'
                f' &nbsp; • &nbsp; {display_value(task.get("priority"))}</div>'
                f'<div class="task-meta">Status: '
                f'<b>{display_value(task.get("status"))}</b></div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)


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

            card_html = (
                '<div class="task-card">'
                f'<div class="task-card-title">{display_value(task.get("title"))}</div>'
                f'<div class="task-meta">{display_value(task.get("platform"))}'
                f' &nbsp; • &nbsp; {display_value(task.get("status"))}</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)


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

            card_html = (
                '<div class="task-card">'
                f'<div class="task-card-title">{display_value(task.get("title"))}</div>'
                f'<div class="task-meta">Goods ID: {display_value(task.get("goods_id"))}</div>'
                f'<div class="task-meta">Status: {display_value(task.get("status"))}</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)


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

            card_html = (
                '<div class="task-card">'
                f'<div class="task-card-title">{display_value(task.get("title"))}</div>'
                f'<div class="task-meta">Case ID: {display_value(task.get("case_id"))}</div>'
                f'<div class="task-meta">Status: {display_value(task.get("status"))}</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)


# ============================================================
# GROUP CHAT
# ============================================================

elif page.startswith("Chat"):

    portal_header("Team Chat")

    # Opening the chat clears the red unread-chat badge.
    mark_chat_notifications_read()

    st.markdown('<div class="tech-title">Techloom Group Chat</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="tech-subtitle">'
        'Shared team conversation for quick updates, files, images and coordination.'
        '</div>',
        unsafe_allow_html=True
    )

    top_a, top_b, top_c = st.columns([2, 1, 1])

    with top_a:
        st.markdown(
            '<div class="workspace-hero">'
            '<div class="workspace-hero-title">💬 Team channel</div>'
            '<div class="workspace-hero-copy">'
            'Chat refreshes automatically every 2 seconds. '
            'New messages create an unread badge and notification for teammates.'
            '</div></div>',
            unsafe_allow_html=True
        )

    with top_b:
        st.metric("Unread Chat", get_unread_chat_count())

    with top_c:
        st.metric("Refresh", "2 sec")

    upload_col, caption_col = st.columns([1, 2])

    with upload_col:
        chat_file = st.file_uploader(
            "📎 Attach image or file",
            type=[
                "png", "jpg", "jpeg", "webp", "gif",
                "pdf", "doc", "docx", "xls", "xlsx",
                "csv", "txt", "zip"
            ],
            key="chat_attachment"
        )

    with caption_col:
        chat_caption = st.text_input(
            "Caption (optional)",
            placeholder="Add a short note about the attachment...",
            key="chat_attachment_caption"
        )

        if chat_file is not None:
            st.caption(
                f"Selected: {chat_file.name} • "
                f"{human_file_size(chat_file.size)}"
            )

            if st.button(
                "📤 Send Attachment",
                type="primary",
                use_container_width=True,
                key="send_chat_attachment"
            ):
                if send_chat_attachment(chat_file, chat_caption):
                    st.success("Attachment sent.")
                    st.rerun()

    st.divider()

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
# CURRENT SPRINT
# ============================================================

elif page == "Current Sprint":
    portal_header("Current Sprint")
    st.markdown(
        '<div class="page-head-new"><div><span class="eyebrow">WEEKLY FOCUS</span>'
        '<h1>Current sprint</h1><p>Incomplete work due within the next seven days, plus tasks without a deadline.</p>'
        '</div></div>',
        unsafe_allow_html=True
    )

    tasks = sprint_tasks()
    if not tasks:
        st.success("No sprint work is currently pending.")
    else:
        columns = [
            ("To-do", ["New"]),
            ("In progress", ["In Progress"]),
            ("Waiting / review", ["Waiting on Information","Waiting on Platform","Submitted for Review","Changes Requested"]),
            ("Complete", ["Completed","Approved"]),
        ]
        board = st.columns(4)
        for idx, (label, statuses) in enumerate(columns):
            with board[idx]:
                group = [t for t in tasks if t.get("status") in statuses]
                st.markdown(
                    f'<div class="kanban-column-title">{label}<span class="kanban-count">{len(group)}</span></div>',
                    unsafe_allow_html=True
                )
                for j, task in enumerate(group):
                    render_task_card(task, f"sprint_{idx}_{j}")


# ============================================================
# TIMELINE
# ============================================================

elif page == "Timeline":
    portal_header("Timeline")
    st.markdown(
        '<div class="page-head-new"><div><span class="eyebrow">WORK HISTORY</span>'
        '<h1>Timeline</h1><p>A chronological view of task changes, submissions and team activity.</p>'
        '</div></div>',
        unsafe_allow_html=True
    )

    try:
        q = (
            supabase.table("task_activity")
            .select("*")
            .order("created_at", desc=True)
            .limit(120)
        )
        if not is_manager():
            q = q.eq("user_id", current_user_id)
        rows = q.execute().data or []
    except Exception:
        rows = []

    if not rows:
        st.info("No timeline activity yet.")
    else:
        for item in rows:
            st.markdown(
                f"""
                <div class="attention-card">
                  <div class="attention-card-title">
                    {display_value(item.get("user_name"), "User")} — {display_value(item.get("action"))}
                  </div>
                  <div class="attention-card-meta">
                    {display_value(item.get("details"))} • {display_value(item.get("created_at"))}
                  </div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# DATA HUB
# ============================================================

elif page == "Data Hub":
    portal_header("Data Hub")
    st.markdown(
        '<div class="page-head-new"><div><span class="eyebrow">SHARED FILES</span>'
        '<h1>Data Hub</h1><p>Company files available to every authenticated team member.</p>'
        '</div></div>',
        unsafe_allow_html=True
    )

    upload = st.file_uploader(
        "Share a file with the team",
        type=["pdf","doc","docx","xls","xlsx","csv","txt","png","jpg","jpeg","webp","zip"],
        key="hub_file"
    )
    if upload and st.button("Upload to Data Hub", type="primary", key="hub_upload"):
        if upload_hub_file(upload):
            st.success("File shared.")
            st.rerun()

    st.write("")
    files = load_hub_files()
    if not files:
        st.info("No shared files yet.")
    else:
        for f in files:
            url = signed_file_url("data-hub", f.get("file_path"))
            with st.container(border=True):
                c1, c2 = st.columns([4,1])
                with c1:
                    st.markdown(f"**{display_value(f.get('file_name'))}**")
                    st.caption(
                        f"{display_value(f.get('uploader_name'))} • "
                        f"{human_file_size(f.get('file_size'))} • "
                        f"{display_value(f.get('created_at'))}"
                    )
                with c2:
                    if url:
                        st.link_button("Open", url, use_container_width=True)


# ============================================================
# MY NOTES
# ============================================================

elif page == "My Notes":
    portal_header("My Notes")
    st.markdown(
        '<div class="page-head-new"><div><span class="eyebrow">PRIVATE</span>'
        '<h1>My notes</h1><p>A personal scratchpad visible only to your account.</p>'
        '</div></div>',
        unsafe_allow_html=True
    )
    note = load_personal_note()
    content = st.text_area(
        "Notes",
        value=note,
        height=440,
        label_visibility="collapsed",
        placeholder="Start writing…"
    )
    if st.button("Save note", type="primary"):
        if save_personal_note(content):
            st.success("Note saved.")


# ============================================================
# SECURE FOLDER
# ============================================================

elif page == "Secure Folder":
    portal_header("Secure Folder")
    st.markdown(
        '<div class="page-head-new"><div><span class="eyebrow">RESTRICTED FILES</span>'
        '<h1>Secure Folder</h1><p>Upload sensitive work files and choose who may access them.</p>'
        '</div></div>',
        unsafe_allow_html=True
    )

    team = [p for p in load_team_profiles() if str(p.get("id")) != str(current_user_id)]
    label_to_id = {f"{p.get('name')} • {p.get('department','')}": p.get("id") for p in team}

    secure_upload = st.file_uploader(
        "Secure file",
        type=["pdf","doc","docx","xls","xlsx","csv","txt","png","jpg","jpeg","webp","zip"],
        key="secure_portal_upload"
    )
    allowed_labels = st.multiselect(
        "Give access to",
        list(label_to_id.keys()),
        key="secure_portal_allowed"
    )
    if secure_upload and st.button("Upload securely", type="primary", key="secure_upload_btn"):
        ids = [label_to_id[x] for x in allowed_labels]
        if upload_secure_portal_file(secure_upload, ids):
            st.success("Secure file uploaded.")
            st.rerun()

    st.write("")
    secure_rows = load_secure_portal_files()
    if not secure_rows:
        st.info("No accessible secure files.")
    else:
        for f in secure_rows:
            url = signed_file_url("secure-files", f.get("file_path"))
            with st.container(border=True):
                c1, c2 = st.columns([4,1])
                with c1:
                    st.markdown(f"**{display_value(f.get('file_name'))}**")
                    st.caption(
                        f"Owner: {display_value(f.get('owner_name'))} • "
                        f"{human_file_size(f.get('file_size'))}"
                    )
                with c2:
                    if url:
                        st.link_button("Download", url, use_container_width=True)


# ============================================================
# GLOBAL SEARCH
# ============================================================

elif page == "🔎 Global Search":
    st.markdown('<div class="tech-title">Global Search</div>', unsafe_allow_html=True)
    st.caption("Search tasks, IDs, case references, chat, comments and knowledge items.")

    query = st.text_input("Search everything", placeholder="Goods ID, ASIN, title, case ID, keyword...")
    if query.strip():
        q = query.strip().lower()

        task_rows = load_all_tasks() if is_manager() else load_my_tasks()
        task_hits = [
            t for t in task_rows
            if q in " ".join(str(t.get(k, "")) for k in [
                "title", "description", "goods_id", "platform", "task_type",
                "supplier_link", "submission_link", "case_id"
            ]).lower()
        ]

        try:
            chat_rows = (
                supabase.table("chat_messages")
                .select("*")
                .ilike("message", f"%{query}%")
                .limit(30)
                .execute()
            ).data or []
        except Exception:
            chat_rows = []

        try:
            comment_rows = (
                supabase.table("task_comments")
                .select("*")
                .ilike("comment", f"%{query}%")
                .limit(30)
                .execute()
            ).data or []
        except Exception:
            comment_rows = []

        knowledge_hits = [
            item for item in load_knowledge_items()
            if q in f"{item.get('title','')} {item.get('category','')} {item.get('content','')}".lower()
        ]

        st.subheader(f"Tasks ({len(task_hits)})")
        for task in task_hits[:30]:
            with st.container(border=True):
                st.markdown(f"**{task.get('title','Untitled')}**")
                st.caption(f"{task.get('platform','')} • {task.get('status','')} • {task.get('assigned_to','')}")

        st.subheader(f"Chat messages ({len(chat_rows)})")
        for row in chat_rows:
            st.write(f"**{row.get('user_name','')}**: {row.get('message','')}")

        st.subheader(f"Task comments ({len(comment_rows)})")
        for row in comment_rows:
            st.write(f"**{row.get('user_name','')}**: {row.get('comment','')}")

        st.subheader(f"Knowledge ({len(knowledge_hits)})")
        for item in knowledge_hits:
            st.write(f"**{item.get('title','')}** — {item.get('category','')}")


# ============================================================
# TASK WORKSPACE
# ============================================================

elif page == "🧰 Task Workspace":
    st.markdown('<div class="tech-title">Task Workspace</div>', unsafe_allow_html=True)
    st.caption("Comments, checklists, attachments, timeline, handover and archiving in one place.")

    workspace_tasks = load_all_tasks() if is_manager() else load_my_tasks()
    if not workspace_tasks:
        st.info("No active tasks.")
    else:
        task_options = {
            f"#{t['id']} • {t.get('title','Untitled')} • {t.get('assigned_to','')}": t
            for t in workspace_tasks
        }
        chosen_label = st.selectbox("Choose task", list(task_options.keys()))
        chosen = task_options[chosen_label]
        task_id = chosen["id"]
        register_task_view(task_id)

        h1, h2, h3 = st.columns(3)
        h1.metric("Status", chosen.get("status", "New"))
        h2.metric("Priority", chosen.get("priority", "Normal"))
        h3.metric("Owner", chosen.get("assigned_to", ""))

        if chosen.get("submission_link"):
            st.link_button("🔗 Open submitted work", chosen["submission_link"])
        if chosen.get("review_reference_link"):
            st.link_button("🧭 Open reviewer reference", chosen["review_reference_link"])

        tabs = st.tabs(["💬 Comments", "☑️ Checklist", "📎 Attachments", "🕓 Timeline", "🔁 Handover", "🗄 Archive"])

        with tabs[0]:
            comments = task_comments(task_id)
            for row in comments:
                with st.container(border=True):
                    st.markdown(f"**{row.get('user_name','User')}**")
                    st.write(row.get("comment", ""))
                    st.caption(row.get("created_at", ""))
            new_comment = st.text_area("Add comment", key=f"task_comment_{task_id}")
            if st.button("Post comment", key=f"post_comment_{task_id}"):
                if add_task_comment(task_id, new_comment):
                    st.rerun()

        with tabs[1]:
            subtasks = task_subtasks(task_id)
            for sub in subtasks:
                checked = st.checkbox(
                    sub.get("title", "Subtask"),
                    value=bool(sub.get("completed")),
                    key=f"subtask_{sub['id']}"
                )
                if checked != bool(sub.get("completed")):
                    if toggle_subtask(sub["id"], checked):
                        st.rerun()
            add_sub = st.text_input("New checklist item", key=f"new_sub_{task_id}")
            if st.button("Add checklist item", key=f"add_sub_{task_id}"):
                if add_subtask(task_id, add_sub):
                    st.rerun()

        with tabs[2]:
            task_file = st.file_uploader(
                "Upload task file",
                type=["png","jpg","jpeg","webp","pdf","doc","docx","xls","xlsx","csv","txt","zip"],
                key=f"task_file_{task_id}"
            )
            if task_file and st.button("Upload to task", key=f"upload_task_file_{task_id}"):
                if attach_file_to_task(task_id, task_file):
                    st.rerun()

            for att in load_task_attachments(task_id):
                url = signed_file_url("task-files", att.get("file_path"))
                if url:
                    st.link_button(
                        f"📎 {att.get('file_name','Attachment')} ({human_file_size(att.get('file_size'))})",
                        url
                    )

        with tabs[3]:
            try:
                timeline = (
                    supabase.table("task_activity")
                    .select("*")
                    .eq("task_id", task_id)
                    .order("created_at", desc=True)
                    .execute()
                ).data or []
            except Exception:
                timeline = []
            for event in timeline:
                with st.container(border=True):
                    st.markdown(f"**{event.get('action','Activity')}**")
                    st.write(event.get("details",""))
                    st.caption(f"{event.get('user_name','')} • {event.get('created_at','')}")

        with tabs[4]:
            profiles = [p for p in load_team_profiles() if p.get("name")]
            names = [p["name"] for p in profiles if p["name"] != chosen.get("assigned_to")]
            if names:
                new_owner = st.selectbox("New owner", names, key=f"handover_owner_{task_id}")
                handover_reason = st.text_area("Handover reason", key=f"handover_reason_{task_id}")
                if st.button("Hand over task", type="primary", key=f"handover_{task_id}"):
                    if handover_task(task_id, new_owner, handover_reason):
                        st.success("Task handed over.")
                        st.rerun()

        with tabs[5]:
            if is_manager():
                st.warning("Archiving removes this task from normal task lists but keeps its history.")
                if st.button("Archive task", key=f"archive_{task_id}"):
                    if archive_task(task_id):
                        st.rerun()
            else:
                st.info("Only management can archive tasks.")


# ============================================================
# DIRECT MESSAGES
# ============================================================

elif page == "Direct Messages":

    portal_header("Direct Messages")
    st.markdown('<div class="tech-title">Direct Messages</div>', unsafe_allow_html=True)
    st.caption("Private one-to-one team chat.")

    people = [p for p in load_team_profiles() if str(p.get("id")) != str(current_user_id)]
    if not people:
        st.info("No other users found.")
    else:
        labels = {f"{p.get('name')} • {p.get('department','')}": p for p in people}
        selected_label = st.selectbox("Chat with", list(labels.keys()))
        person = labels[selected_label]

        messages = load_direct_messages(person.get("id"))
        for msg in messages:
            with st.chat_message("user" if str(msg.get("sender_id")) == str(current_user_id) else "assistant"):
                st.markdown(f"**{msg.get('sender_name','')}**")
                st.write(msg.get("message",""))
                st.caption(msg.get("created_at",""))

        dm = st.chat_input(f"Message {person.get('name')}…")
        if dm:
            if send_direct_message(person.get("id"), person.get("name"), dm):
                st.rerun()


# ============================================================
# CALENDAR
# ============================================================

elif page == "📆 Calendar":
    st.markdown('<div class="tech-title">Work Calendar</div>', unsafe_allow_html=True)
    st.caption("Deadlines and attendance on one date.")

    selected = st.date_input("Select date", value=datetime.now(PK_TZ).date())
    tasks = load_all_tasks() if is_manager() else load_my_tasks()

    due = []
    for task in tasks:
        value = task.get("due_date")
        if value:
            try:
                due_dt = parse_timestamp(value)
                if due_dt and due_dt.astimezone(PK_TZ).date() == selected:
                    due.append(task)
            except Exception:
                pass

    st.subheader(f"Tasks due ({len(due)})")
    for task in due:
        st.write(f"{priority_badge(task.get('priority','Normal'))} **{task.get('title','')}** — {task.get('assigned_to','')}")

    st.subheader("Attendance")
    try:
        q = supabase.table("attendance").select("*").eq("attendance_date", selected.isoformat())
        if not is_manager():
            q = q.eq("user_id", current_user_id)
        rows = q.execute().data or []
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No attendance recorded for this date.")
    except Exception as error:
        st.error(error)


# ============================================================
# ANNOUNCEMENTS
# ============================================================

elif page == "Announcements":

    portal_header("Announcements")
    st.markdown('<div class="tech-title">Announcements</div>', unsafe_allow_html=True)
    st.caption("Pinned management messages for the whole team.")

    if is_manager():
        with st.expander("➕ New announcement"):
            a_title = st.text_input("Title", key="announcement_title")
            a_body = st.text_area("Message", key="announcement_body")
            a_pinned = st.checkbox("Pin to dashboards", value=True, key="announcement_pin")
            a_urgent = st.checkbox("Urgent tone", key="announcement_urgent")
            if st.button("Publish announcement", type="primary"):
                if a_title.strip() and a_body.strip():
                    try:
                        supabase.table("announcements").insert({
                            "title": a_title.strip(),
                            "body": a_body.strip(),
                            "created_by": current_user_id,
                            "created_by_name": name,
                            "pinned": a_pinned,
                            "urgent": a_urgent,
                            "active": True
                        }).execute()
                        for person in load_team_profiles():
                            if str(person.get("id")) != str(current_user_id):
                                create_notification(
                                    person.get("id"),
                                    a_title.strip(),
                                    a_body.strip()[:180],
                                    "announcement"
                                )
                        audit("Announcement published", "announcement", None, a_title)
                        st.rerun()
                    except Exception as error:
                        st.error(error)

    announcements = load_announcements()
    for item in announcements:
        with st.container(border=True):
            prefix = "📌 " if item.get("pinned") else ""
            urgent = "🚨 " if item.get("urgent") else ""
            st.markdown(f"### {urgent}{prefix}{item.get('title','')}")
            st.write(item.get("body",""))
            st.caption(f"{item.get('created_by_name','')} • {item.get('created_at','')}")


# ============================================================
# KNOWLEDGE BASE
# ============================================================

elif page == "Knowledge Base":

    portal_header("Knowledge Base")
    st.markdown('<div class="tech-title">Knowledge & SOPs</div>', unsafe_allow_html=True)
    st.caption("Marketplace procedures, compliance notes, SOPs and internal references.")

    if is_manager():
        with st.expander("➕ Add knowledge item"):
            kb_title = st.text_input("Title", key="kb_title")
            kb_category = st.selectbox("Category", ["General","Temu","Amazon","eBay","TikTok","Compliance","Operations"], key="kb_category")
            kb_content = st.text_area("Content / SOP", height=180, key="kb_content")
            kb_link = st.text_input("Reference link (optional)", key="kb_link")
            kb_file = st.file_uploader("Optional document", type=["pdf","doc","docx","xls","xlsx","txt"], key="kb_file")
            if st.button("Save knowledge item", type="primary"):
                file_meta = upload_private_file("knowledge-files", kb_file, "knowledge") if kb_file else None
                try:
                    supabase.table("knowledge_items").insert({
                        "title": kb_title.strip(),
                        "category": kb_category,
                        "content": kb_content.strip(),
                        "reference_link": kb_link.strip(),
                        "file_path": file_meta["path"] if file_meta else None,
                        "file_name": file_meta["name"] if file_meta else None,
                        "created_by": current_user_id,
                        "created_by_name": name,
                        "active": True
                    }).execute()
                    audit("Knowledge item created", "knowledge", None, kb_title)
                    st.rerun()
                except Exception as error:
                    st.error(error)

    items = load_knowledge_items()
    category_filter = st.selectbox("Filter category", ["All"] + sorted(set(i.get("category","General") for i in items)))
    for item in items:
        if category_filter != "All" and item.get("category") != category_filter:
            continue
        with st.expander(f"{item.get('category','General')} • {item.get('title','')}"):
            st.write(item.get("content",""))
            if item.get("reference_link"):
                st.link_button("Open reference", item.get("reference_link"))
            if item.get("file_path"):
                url = signed_file_url("knowledge-files", item.get("file_path"))
                if url:
                    st.link_button(f"📎 {item.get('file_name','Document')}", url)



# ============================================================
# TEAM ATTENDANCE — EVERYONE CAN VIEW + EXPORT
# ============================================================

elif page == "Team Attendance":

    portal_header("Team Attendance")
    st.markdown('<div class="tech-title">Team Attendance</div>', unsafe_allow_html=True)
    st.info("Official attendance tracking starts on 25 Aug 2026. Earlier dates are not counted as absent.")
    st.caption(
        "Everyone can view team attendance. If a member has not marked attendance "
        "for a date, that date is shown as Absent."
    )

    period_col, date_col, scope_col = st.columns(3)

    with period_col:
        period_type = st.selectbox(
            "Period",
            ["Weekly", "Monthly"],
            key="team_att_period"
        )

    with date_col:
        anchor_date = st.date_input(
            "Choose date",
            value=datetime.now(PK_TZ).date(),
            key="team_att_anchor"
        )

    with scope_col:
        team_names = [p.get("name") for p in load_team_profiles() if p.get("name")]
        scope = st.selectbox(
            "View",
            ["All Members", "My Attendance"] + team_names,
            key="team_att_scope"
        )

    start_date, end_date = attendance_period_dates(period_type, anchor_date)
    all_rows = get_attendance_scope_rows(start_date, end_date)

    if scope == "My Attendance":
        visible_rows = [r for r in all_rows if r["Employee"] == name]
    elif scope == "All Members":
        visible_rows = all_rows
    else:
        visible_rows = [r for r in all_rows if r["Employee"] == scope]

    detail_df = pd.DataFrame(visible_rows)
    summary_df = attendance_summary_dataframe(visible_rows)

    st.markdown(
        f"**Period:** {start_date.strftime('%d %b %Y')} — "
        f"{end_date.strftime('%d %b %Y')}"
    )

    if not summary_df.empty:
        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric("Present", int(summary_df["Present Days"].sum()))
        s2.metric("Absent", int(summary_df["Absent Days"].sum()))
        s3.metric("On Time", int(summary_df["On Time Days"].sum()))
        s4.metric(
            "Late / Very Late",
            int(summary_df["Late Days"].sum() + summary_df["Very Late Days"].sum())
        )
        s5.metric("Extremely Late", int(summary_df["Extremely Late Days"].sum()))

        st.subheader("Summary")
        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

    st.subheader("Attendance Sheet")
    if not detail_df.empty:
        st.dataframe(
            detail_df,
            use_container_width=True,
            hide_index=True
        )

        excel_bytes = attendance_excel_bytes(
            detail_df,
            summary_df,
            f"{period_type} Attendance"
        )

        file_label = (
            "all_members"
            if scope == "All Members"
            else scope.lower().replace(" ", "_")
        )

        st.download_button(
            f"⬇️ Download {period_type} Attendance Excel",
            data=excel_bytes,
            file_name=(
                f"techloom_{period_type.lower()}_attendance_"
                f"{file_label}_{start_date.isoformat()}_to_{end_date.isoformat()}.xlsx"
            ),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

        st.download_button(
            f"⬇️ Download {period_type} Attendance CSV",
            data=detail_df.to_csv(index=False).encode("utf-8"),
            file_name=(
                f"techloom_{period_type.lower()}_attendance_"
                f"{file_label}_{start_date.isoformat()}_to_{end_date.isoformat()}.csv"
            ),
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No attendance records for this period.")

# ============================================================
# TEAM STATUS
# ============================================================

elif page == "🟢 Team Status":
    if not is_manager():
        st.error("Management access only.")
        st.stop()

    st.markdown('<div class="tech-title">Team Status</div>', unsafe_allow_html=True)
    st.caption("Live working, break and offline indicators.")

    rows = load_presence()
    now_utc = datetime.now(timezone.utc)
    display = []
    for row in rows:
        seen = parse_timestamp(row.get("last_seen"))
        minutes = int((now_utc - seen).total_seconds() / 60) if seen else 9999
        status = row.get("status","Offline") if minutes <= 10 else "Offline"
        display.append({
            "Employee": row.get("user_name"),
            "Status": status,
            "Last Seen": format_pk_time(row.get("last_seen")),
            "Minutes Ago": minutes if minutes < 9999 else None
        })
    if display:
        st.dataframe(pd.DataFrame(display), use_container_width=True, hide_index=True)


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    portal_header("Reports")
    if not is_manager():
        st.error("Management access only.")
        st.stop()

    st.markdown('<div class="tech-title">Management Reports</div>', unsafe_allow_html=True)
    st.caption("Performance, attendance and workload reporting.")

    report_month = st.date_input("Month", value=datetime.now(PK_TZ).date().replace(day=1))
    month_start = report_month.replace(day=1)
    month_end = month_start.replace(day=calendar.monthrange(month_start.year, month_start.month)[1])

    try:
        all_tasks = (
            supabase.table("tasks")
            .select("*")
            .gte("created_at", month_start.isoformat())
            .lte("created_at", (month_end + timedelta(days=1)).isoformat())
            .execute()
        ).data or []
    except Exception:
        all_tasks = []

    try:
        attendance = (
            supabase.table("attendance")
            .select("*")
            .gte("attendance_date", month_start.isoformat())
            .lte("attendance_date", month_end.isoformat())
            .execute()
        ).data or []
    except Exception:
        attendance = []

    profiles = [p for p in load_team_profiles() if p.get("name")]
    report_rows = []

    for person in profiles:
        person_name = person.get("name")
        person_tasks = [t for t in all_tasks if t.get("assigned_to") == person_name]
        completed = [t for t in person_tasks if t.get("status") in ["Completed","Approved"]]
        overdue = []
        for t in person_tasks:
            due = parse_timestamp(t.get("due_date")) if t.get("due_date") else None
            if due and due.date() < datetime.now(PK_TZ).date() and t.get("status") not in ["Completed","Approved"]:
                overdue.append(t)
        person_att = [a for a in attendance if a.get("employee_name") == person_name]
        late_days = sum(1 for a in person_att if late_status(a.get("check_in")) == "Late")

        report_rows.append({
            "Employee": person_name,
            "Tasks": len(person_tasks),
            "Completed": len(completed),
            "Overdue": len(overdue),
            "Days Present": len(person_att),
            "Late Days": late_days,
            "Completion %": round((len(completed)/len(person_tasks)*100), 1) if person_tasks else 0
        })

    report_df = pd.DataFrame(report_rows)
    st.dataframe(report_df, use_container_width=True, hide_index=True)

    if not report_df.empty:
        leader = report_df.sort_values(["Completion %","Completed"], ascending=False).iloc[0]
        st.success(f"🏆 Current completion leader: {leader['Employee']} — {leader['Completion %']}%")

    task_df = pd.DataFrame(all_tasks)
    att_df = pd.DataFrame(attendance)
    excel_bytes = to_excel_bytes({
        "Summary": report_df,
        "Tasks": task_df,
        "Attendance": att_df
    })
    st.download_button(
        "⬇️ Export Excel Report",
        data=excel_bytes,
        file_name=f"techloom_report_{month_start.strftime('%Y_%m')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ============================================================
# TASK TEMPLATES
# ============================================================

elif page == "🧩 Task Templates":
    if not is_manager():
        st.error("Management access only.")
        st.stop()

    st.markdown('<div class="tech-title">Task Templates</div>', unsafe_allow_html=True)

    with st.expander("➕ Create template"):
        t_name = st.text_input("Template name", key="tpl_name")
        t_title = st.text_input("Default task title", key="tpl_title")
        t_type = st.selectbox("Task type", ["New Listing","Listing Upload","Listing Update","Image Generation","Compliance","Appeal","Seller Support Case","Product Research","Other"], key="tpl_type")
        t_platform = st.selectbox("Platform", ["Temu","Amazon","eBay","TikTok","Multiple"], key="tpl_platform")
        t_priority = st.selectbox("Priority", ["Normal","High","Urgent","Low"], key="tpl_priority")
        t_desc = st.text_area("Default instructions", key="tpl_desc")
        if st.button("Save template", type="primary"):
            try:
                supabase.table("task_templates").insert({
                    "name": t_name.strip(),
                    "title_template": t_title.strip(),
                    "description_template": t_desc.strip(),
                    "task_type": t_type,
                    "platform": t_platform,
                    "priority": t_priority,
                    "created_by": current_user_id,
                    "active": True
                }).execute()
                st.rerun()
            except Exception as error:
                st.error(error)

    templates = load_task_templates()
    if templates:
        labels = {t.get("name","Template"): t for t in templates}
        chosen_name = st.selectbox("Use template", list(labels.keys()))
        assignee = st.selectbox("Assign to", [p.get("name") for p in load_team_profiles() if p.get("name")], key="tpl_assignee")
        due = st.date_input("Due date", value=datetime.now(PK_TZ).date()+timedelta(days=1), key="tpl_due")
        if st.button("Create task from template"):
            if create_task_from_template(labels[chosen_name], assignee, due):
                st.success("Task created.")
                st.rerun()


# ============================================================
# RECURRING TASKS
# ============================================================

elif page == "🔁 Recurring Tasks":
    if not is_manager():
        st.error("Management access only.")
        st.stop()

    st.markdown('<div class="tech-title">Recurring Tasks</div>', unsafe_allow_html=True)
    st.caption("Daily, weekly or monthly work that creates itself.")

    with st.expander("➕ New recurring task"):
        r_title = st.text_input("Title", key="rec_title")
        r_assignee = st.selectbox("Assign to", [p.get("name") for p in load_team_profiles() if p.get("name")], key="rec_assignee")
        r_cadence = st.selectbox("Cadence", ["Daily","Weekly","Monthly"], key="rec_cadence")
        r_type = st.selectbox("Task type", ["Other","Compliance","Listing Upload","Image Generation","Appeal"], key="rec_type")
        r_platform = st.selectbox("Platform", ["Multiple","Temu","Amazon","eBay","TikTok"], key="rec_platform")
        r_priority = st.selectbox("Priority", ["Normal","High","Urgent","Low"], key="rec_priority")
        r_desc = st.text_area("Instructions", key="rec_desc")
        r_due_hours = st.number_input("Due after hours", min_value=1, max_value=720, value=24, key="rec_due_hours")
        if st.button("Create recurring task"):
            try:
                supabase.table("recurring_tasks").insert({
                    "title": r_title.strip(),
                    "description": r_desc.strip(),
                    "assigned_to": r_assignee,
                    "cadence": r_cadence,
                    "task_type": r_type,
                    "platform": r_platform,
                    "priority": r_priority,
                    "due_after_hours": int(r_due_hours),
                    "next_run": datetime.now(timezone.utc).isoformat(),
                    "created_by": current_user_id,
                    "active": True
                }).execute()
                st.rerun()
            except Exception as error:
                st.error(error)

    try:
        recurring = supabase.table("recurring_tasks").select("*").order("created_at", desc=True).execute().data or []
        if recurring:
            st.dataframe(pd.DataFrame(recurring), use_container_width=True, hide_index=True)
    except Exception as error:
        st.error(error)


# ============================================================
# PERMISSIONS
# ============================================================

elif page == "🛡 Permissions":
    if not is_manager():
        st.error("Management access only.")
        st.stop()

    st.markdown('<div class="tech-title">Role Permissions</div>', unsafe_allow_html=True)
    st.caption("Configure feature permissions by role. Current app still enforces core manager-only areas.")

    roles = ["Team Member","Team Lead","Admin"]
    features = ["create_task","approve_task","view_team_attendance","manage_templates","manage_announcements","manage_knowledge","archive_task","view_audit"]
    selected_role = st.selectbox("Role", roles)

    try:
        rows = (
            supabase.table("role_permissions")
            .select("*")
            .eq("role", selected_role)
            .execute()
        ).data or []
        current = {r.get("feature"): bool(r.get("allowed")) for r in rows}
    except Exception:
        current = {}

    changed = {}
    for feature in features:
        changed[feature] = st.checkbox(
            feature.replace("_"," ").title(),
            value=current.get(feature, selected_role in ["Team Lead","Admin"]),
            key=f"perm_{selected_role}_{feature}"
        )

    if st.button("Save permissions"):
        try:
            for feature, allowed in changed.items():
                supabase.table("role_permissions").upsert({
                    "role": selected_role,
                    "feature": feature,
                    "allowed": allowed
                }, on_conflict="role,feature").execute()
            st.success("Permissions saved.")
        except Exception as error:
            st.error(error)


# ============================================================
# AUDIT LOG
# ============================================================

elif page == "🧾 Audit Log":
    if not is_manager():
        st.error("Management access only.")
        st.stop()

    st.markdown('<div class="tech-title">Audit Log</div>', unsafe_allow_html=True)
    try:
        logs = (
            supabase.table("audit_logs")
            .select("*")
            .order("created_at", desc=True)
            .limit(500)
            .execute()
        ).data or []
        if logs:
            df = pd.DataFrame(logs)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button(
                "Download CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="techloom_audit_log.csv",
                mime="text/csv"
            )
        else:
            st.info("No audit events yet.")
    except Exception as error:
        st.error(error)


# ============================================================
# SETTINGS
# ============================================================

elif page == "Settings":

    portal_header("Settings")
    st.markdown('<div class="tech-title">Settings</div>', unsafe_allow_html=True)
    prefs = get_user_preferences()

    st.subheader("Profile")
    st.write(f"**Name:** {name}")
    st.write(f"**Role:** {role}")
    st.write(f"**Department:** {department}")

    st.subheader("Presence")
    presence_choice = st.selectbox(
        "Current status",
        ["Working","On Break","Busy","Away"],
        index=["Working","On Break","Busy","Away"].index(st.session_state.get("presence_status","Working"))
        if st.session_state.get("presence_status","Working") in ["Working","On Break","Busy","Away"] else 0
    )
    if presence_choice != st.session_state.get("presence_status"):
        st.session_state.presence_status = presence_choice
        update_presence()

    st.subheader("Preferences")
    notify_sound = st.checkbox("Notification sound", value=bool(prefs.get("notification_sound", True)))
    desktop_alerts = st.checkbox("Desktop notification preference", value=bool(prefs.get("desktop_notifications", False)))
    compact_mode = st.checkbox("Compact dashboard mode", value=bool(prefs.get("compact_mode", False)))
    timezone_pref = st.selectbox("Timezone", ["Asia/Karachi","UTC"], index=0)

    if st.button("Save preferences", type="primary"):
        if save_user_preferences({
            "notification_sound": notify_sound,
            "desktop_notifications": desktop_alerts,
            "compact_mode": compact_mode,
            "timezone": timezone_pref
        }):
            st.session_state.notification_sound_enabled = notify_sound
            st.success("Settings saved.")

    st.subheader("Browser desktop notifications")
    request_browser_notification_permission()

    st.subheader("Password")
    user_email = getattr(st.session_state.user, "email", None)
    if user_email and st.button("Send password reset email"):
        try:
            supabase.auth.reset_password_for_email(user_email)
            st.success("Password reset email sent.")
        except Exception as error:
            st.error(error)


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

            card_html = (
                '<div class="task-card">'
                f'<div class="task-card-title">{display_value(activity.get("user_name"), "User")}'
                f' — {display_value(activity.get("action"))}</div>'
                f'<div class="task-meta">{display_value(activity.get("details"))}</div>'
                f'<div class="task-meta">{display_value(activity.get("created_at"))}</div>'
                '</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)
