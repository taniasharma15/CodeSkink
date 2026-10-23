"""
LifeLine Navigator — Family Tracker Page
Create/join groups, share locations, calculate meetup points.
"""
import streamlit as st
import textwrap
from src.ui import (
    init_page, init_sidebar, render_emergency_title, render_page_title,
    render_section_title, render_offline_badge
)
from src.api import get_family_service
from src.api.schemas import FamilyGroupCreate, FamilyGroupJoin, LocationUpdate
from src.config import LOCATION_SHARE_INTERVAL_SEC


def render_family_page():
    """Render professional family tracker page."""
    init_page("LifeLine Navigator — Family Tracker")
    init_sidebar()

    # Header with description
    header_html = textwrap.dedent("""
        <div style="margin-bottom: var(--spacing-2xl);">
            <h2 style="font-size: 32px; font-weight: 800; margin-bottom: var(--spacing-md);">
                👨‍👩‍👧‍👦 Family Tracker
            </h2>
            <p style="color: var(--text-secondary); font-size: 18px; margin-bottom: var(--spacing-xl);">
                Stay connected with your family during emergencies. Create safety groups and find safe meetup points.
            </p>
        </div>
    """)
    st.markdown(header_html, unsafe_allow_html=True)

    # Emergency contacts
    st.markdown("""
    <div style="margin-bottom: var(--spacing-xl); display: flex; gap: var(--spacing-sm); flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: var(--spacing-xs); padding: 6px 16px;
                     background: rgba(34, 197, 94, 0.2); border: 1px solid var(--success);
                     border-radius: 20px; font-size: 14px; font-weight: 600;">
            <span>📞 Emergency: 112</span>
            <span>🆘 SOS: 108</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    family_service = get_family_service()

    # Check if user is in a group
    active_group_code = st.session_state.get("active_group_code")
    active_member_id = st.session_state.get("active_member_id")

    if not active_group_code:
        # Create/Join Group Section
        st.markdown("""
        <div class="glass-card" style="margin-bottom: var(--spacing-2xl);">
            <div style="text-align: center; padding: var(--spacing-2xl); margin-bottom: var(--spacing-xl);">
                <span style="font-size: 64px;">👨‍👩‍👧‍👦</span>
                <h3 style="font-size: 24px; font-weight: 700; margin: var(--spacing-md) 0;">
                    Create or Join Family Group
                </h3>
                <p style="color: var(--text-secondary); margin: 0;">
                    Coordinate with your family during emergencies with real-time location sharing
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_create, col_join = st.columns([1, 1])

        with col_create:
            # Create Group Card
            create_card = textwrap.dedent("""
                <div style="background: var(--bg-card); backdrop-filter: blur(10px);
                            border: 1px solid var(--border); border-radius: var(--radius-lg);
                            padding: var(--spacing-xl); height: 100%; display: flex; flex-direction: column;">
                    <div style="text-align: center; margin-bottom: var(--spacing-xl);">
                        <span style="font-size: 48px;">➕</span>
                        <h3 style="font-size: 20px; font-weight: 700; margin: var(--spacing-md) 0;">
                            Create New Group
                        </h3>
                    </div>

                    <div style="flex: 1;">
                        <div style="margin-bottom: var(--spacing-md);">
                            <label style="display: block; color: var(--text-secondary); font-size: 14px; margin-bottom: var(--spacing-xs);">
                                Your Name
                            </label>
                            <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                                        border-radius: var(--radius-md); padding: 12px;">
                                <input type="text" placeholder="e.g., Rajesh Kumar"
                                       style="background: transparent; border: none; color: var(--text-primary);
                                              width: 100%; font-size: 15px;">
                            </div>
                        </div>

                        <div style="margin-bottom: var(--spacing-md);">
                            <label style="display: block; color: var(--text-secondary); font-size: 14px; margin-bottom: var(--spacing-xs);">
                                Phone (optional)
                            </label>
                            <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                                        border-radius: var(--radius-md); padding: 12px;">
                                <input type="text" placeholder="+91 98765 43210"
                                       style="background: transparent; border: none; color: var(--text-primary);
                                              width: 100%; font-size: 15px;">
                            </div>
                        </div>
                    </div>

                    if st.button("🚀 Create Group", type="primary", use_container_width=True, key="create_group_html"):
                pass  # Handled by form below
                </div>
            """)
            st.markdown(create_card, unsafe_allow_html=True)

        with col_join:
            # Join Group Card
            join_card = textwrap.dedent("""
                <div style="background: var(--bg-card); backdrop-filter: blur(10px);
                            border: 1px solid var(--border); border-radius: var(--radius-lg);
                            padding: var(--spacing-xl); height: 100%; display: flex; flex-direction: column;">
                    <div style="text-align: center; margin-bottom: var(--spacing-xl);">
                        <span style="font-size: 48px;">🔗</span>
                        <h3 style="font-size: 20px; font-weight: 700; margin: var(--spacing-md) 0;">
                            Join Existing Group
                        </h3>
                    </div>

                    <div style="flex: 1;">
                        <div style="margin-bottom: var(--spacing-md);">
                            <label style="display: block; color: var(--text-secondary); font-size: 14px; margin-bottom: var(--spacing-xs);">
                                6-Character Group Code
                            </label>
                            <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                                        border-radius: var(--radius-md); padding: 12px; font-family: monospace;
                                        font-size: 24px; text-align: center; letter-spacing: 8px;">
                                <input type="text" maxlength="6" placeholder="ABCDEF"
                                       style="background: transparent; border: none; color: var(--text-primary);
                                              width: 100%; text-align: center;">
                            </div>
                        </div>

                        <div style="margin-bottom: var(--spacing-md);">
                            <label style="display: block; color: var(--text-secondary); font-size: 14px; margin-bottom: var(--spacing-xs);">
                                Your Name
                            </label>
                            <div style="background: var(--bg-tertiary); border: 1px solid var(--border);
                                        border-radius: var(--radius-md); padding: 12px;">
                                <input type="text" placeholder="e.g., Priya Sharma"
                                       style="background: transparent; border: none; color: var(--text-primary);
                                              width: 100%; font-size: 15px;">
                            </div>
                        </div>
                    </div>

                    if st.button("🚀 Join Group", type="primary", use_container_width=True, key="join_group_html"):
                pass  # Handled by form below
                </div>
            """)
            st.markdown(join_card, unsafe_allow_html=True)

        with st.form("create_group_form"):
            creator_name = st.text_input("Your Name")
            creator_phone = st.text_input("Phone (optional)")
            submitted = st.form_submit_button("Create Group", type="primary")

            if submitted and creator_name:
                try:
                    group = family_service.create_group(FamilyGroupCreate(
                        creator_name=creator_name,
                        creator_phone=creator_phone
                    ))
                    st.session_state.active_group_code = group.code
                    st.session_state.active_member_id = group.members[next(iter(group.members))].id
                    st.success("✅ Group created successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to create group: {e}")

        with st.form("join_group_form"):
            group_code = st.text_input("Group Code", max_chars=6).upper()
            member_name = st.text_input("Your Name")
            submitted = st.form_submit_button("Join Group", type="primary")

            if submitted and group_code and member_name:
                try:
                    group = family_service.join_group(FamilyGroupJoin(
                        group_code=group_code,
                        member_name=member_name,
                        member_phone=st.text_input("Phone (optional)")
                    ))
                    st.session_state.active_group_code = group_code
                    st.session_state.active_member_id = group.members[next(iter(group.members))].id
                    st.success("✅ Successfully joined group!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to join group: {e}")

    else:
        # Group Dashboard - Show current group
        st.markdown("""
        <div style="margin-bottom: var(--spacing-2xl);">
            <h3 style="font-size: 24px; font-weight: 700; margin-bottom: var(--spacing-md);">
                Your Family Group
            </h3>
        </div>
        """, unsafe_allow_html=True)

        # Display group code prominently
        group_code_html = textwrap.dedent(f"""
            <div class="glass-card" style="text-align: center; padding: var(--spacing-2xl); margin-bottom: var(--spacing-xl);">
                <div style="color: var(--text-secondary); font-size: 14px; margin-bottom: var(--spacing-md);">
                    SHARE THIS CODE WITH FAMILY MEMBERS
                </div>
                <div style="font-family: monospace; font-size: 48px; font-weight: 800; letter-spacing: 8px;
                           background: var(--bg-tertiary); padding: 20px; border-radius: var(--radius-lg);
                           border: 2px solid var(--accent-gradient);">
                    {active_group_code}
                </div>
                <div style="margin-top: var(--spacing-md);">
                    if st.button("📋 Copy Code", type="secondary", key="copy_code"):
                    st.session_state.copied_code = True
                    st.toast("Code copied to clipboard!")
                </div>
            </div>
        """)
        st.markdown(group_code_html, unsafe_allow_html=True)

        # Get current group data
        try:
            group = family_service.get_group(active_group_code)

            if group:
                # Members Section
                render_section_title("👥 Family Members")

                member_col1, member_col2 = st.columns(2)
                for i, (member_id, member) in enumerate(group.members.items()):
                    with member_col1 if i % 2 == 0 else member_col2:
                        # Member card
                        member_card = textwrap.dedent(f"""
                            <div class="glass-card" style="display: flex; align-items: center; gap: var(--spacing-md); padding: var(--spacing-md);">
                                <div style="width: 56px; height: 56px; border-radius: 50%; background: var(--bg-tertiary);
                                             display: flex; align-items: center; justify-content: center; font-weight: 700;
                                             font-size: 24px; color: var(--text-primary);">
                                    {member.name[0].upper()}
                                </div>
                                <div style="flex: 1;">
                                    <h4 style="margin: 0 0 var(--spacing-xs) 0; font-weight: 600;">{member.name}</h4>
                                    <p style="margin: 0; color: var(--text-secondary); font-size: 14px;">
                                        Last seen: {member.last_seen.strftime('%H:%M:%S')}
                                    </p>
                                </div>
                                <div style="display: flex; flex-direction: column; align-items: center; gap: 4px;">
                                    <div style="width: 12px; height: 12px; border-radius: 50%;
                                                 {'background: var(--success)' if member.status == 'safe' else 'background: var(--warning)'};"></div>
                                    <span style="font-size: 12px; color: var(--text-secondary);">
                                        {member.status.replace('_', ' ').title()}
                                    </span>
                                </div>
                            </div>
                        """)
                        st.markdown(member_card, unsafe_allow_html=True)

                # Meetup Point Section
                render_section_title("🎯 Meetup Point")

                if group.meetup_point:
                    meetup_card = textwrap.dedent(f"""
                        <div class="glass-card" style="text-align: center;">
                            <div style="display: flex; align-items: center; justify-content: center; gap: var(--spacing-sm); margin-bottom: var(--spacing-md);">
                                <span style="font-size: 32px;">📍</span>
                                <h4 style="margin: 0; font-weight: 600;">Designated Safe Meetup Point</h4>
                            </div>
                            <p style="color: var(--text-secondary); margin-bottom: var(--spacing-md);">
                                Coordinates: {group.meetup_point.latitude:.4f}, {group.meetup_point.longitude:.4f}
                            </p>
                            <div style="display: flex; gap: var(--spacing-md); justify-content: center;">
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("🧭 Navigate to Meetup", type="primary", key="navigate_meetup"):
                                        st.toast("🧭 Starting navigation to meetup point...")
                                with col2:
                                    if st.button("🔄 Find New Point", type="secondary", key="find_new_point"):
                                        st.toast("🔄 Finding new meetup point...")
                            </div>
                        </div>
                    """)
                    st.markdown(meetup_card, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="glass-card" style="text-align: center; padding: var(--spacing-xl);">
                        <span style="font-size: 48px;">🗺️</span>
                        <h4 style="margin: var(--spacing-md) 0; font-weight: 600;">No Meetup Point Set</h4>
                        <p style="color: var(--text-secondary); margin-bottom: var(--spacing-md);">
                            Set a safe meetup point for your family during emergencies
                        </p>
                        if st.button("🎯 Set Meetup Point", type="primary", use_container_width=False, key="set_meetup_point"):
                st.toast("🎯 Tap on map to set meetup point")
                    </div>
                    """, unsafe_allow_html=True)

                # Group Actions
                render_section_title("⚙️ Group Settings")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔄 Refresh Locations", use_container_width=True):
                        st.toast("Location refresh initiated")
                with col2:
                    if st.button("📤 Share Location", use_container_width=True):
                        st.toast("Location shared with group")
                with col3:
                    if st.button("🚪 Leave Group", use_container_width=True):
                        if st.confirm("Are you sure you want to leave the group?"):
                            family_service.leave_group(active_group_code, active_member_id)
                            del st.session_state.active_group_code
                            del st.session_state.active_member_id
                            st.success("✅ Left group successfully")
                            st.rerun()

        except Exception as e:
            st.error(f"❌ Error loading group data: {e}")
            if st.button("🔄 Try Again", use_container_width=True):
                st.rerun()

    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: var(--spacing-2xl); padding: var(--spacing-xl);
                 border-top: 1px solid var(--border); color: var(--text-secondary);">
        <p style="margin: 0; font-size: var(--font-size-sm);">
            Real-time location sharing • Offline capable • Family safety first
        </p>
    </div>
    """, unsafe_allow_html=True)


# Form handling for Streamlit
if __name__ == "__main__":
    render_family_page()