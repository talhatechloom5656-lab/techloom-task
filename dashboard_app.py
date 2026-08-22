import streamlit as st
import pandas as pd

from datetime import datetime, timedelta, time
from supabase import create_client


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Techloom Task",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# STYLING
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #f6f8fc;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #07152d 0%,
        #0a1d3d 100%
    );
}

[data-testid="stSidebar"] * {
    color: white;
}

/* Titles */
.tech-title {
    font-size: 36px;
    font-weight: 800;
    color: #111827;
    margin-bottom: 2px;
}

.tech-subtitle {
    font-size: 14px;
    color: #6b7280;
    margin-bottom: 24px;
}

.sidebar-logo {
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 0px;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #cbd5e1 !important;
    margin-bottom: 22px;
}

/* Cards */
.task-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.035);
}

.task-card-title {
    font-size: 17px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 7px;
}

.task-meta {
    color: #6b7280;
    font-size: 13px;
    margin-top: 4px;
}

.section-title {
    font-size: 21px;
    font-weight: 700;
    color: #111827;
    margin-top: 10px;
    margin-bottom: 13px;
}

/* Metric cards */
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    padding: 17px;
    border-radius: 14px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.03);
}

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

    st.markdown(
        '<div class="tech-title">📋 TECHLOOM TASK</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="tech-subtitle">'
        'Office Task Management System'
        '</div>',
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1, 1.1, 1])

    with center:

        st.subheader("Sign In")

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Sign In",
            type="primary",
            use_container_width=True
        ):

            if not email or not password:

                st.warning(
                    "Please enter your email and password."
                )

            else:

                if login(email, password):
                    st.rerun()

    st.stop()


# ============================================================
# CURRENT USER
# ============================================================

profile = st.session_state.profile

name = profile["name"]
role = profile["role"]
department = profile["department"]

current_user_id = st.session_state.user.id


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
            "📜 Activity"
        ]

    else:

        menu_options = [
            "🏠 Dashboard",
            "📋 My Tasks"
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

                st.markdown(
                    f"""
                    <div class="task-card">

                        <div class="task-card-title">
                            {title}
                        </div>

                        <div class="task-meta">
                            {platform}
                            &nbsp; • &nbsp;
                            {task_type}
                            &nbsp; • &nbsp;
                            Assigned to:
                            {assigned_to}
                        </div>

                        <div class="task-meta">
                            Priority:
                            <b>{priority}</b>
                            &nbsp; • &nbsp;
                            Status:
                            <b>{status}</b>
                        </div>

                    </div>
                    """,
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