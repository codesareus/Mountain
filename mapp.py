import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Title and description
st.title("The Boy Who Ran Towards the Mountain")
st.write("Watch as a small boy runs 5 km a day towards a towering mountain 100 km away!")

# Constants
MOUNTAIN_DISTANCE = 100  # Mountain is 100 km away
MOUNTAIN_HEIGHT = 50     # Mountain is 50 units tall
MOUNTAIN_WIDTH = 30      # Mountain is wider (fatter)
DAYS_TO_RUN = 20         # Number of days to animate
KM_PER_DAY = 5           # Boy runs 5 km per day
BOY_SCALE = 3            # Boy is 3 times taller

# Create a function to draw the boy
def draw_boy(x_pos, y_pos, day):
    """
    Draws a simple stick figure boy at the given (x_pos, y_pos) with a day label.
    """
    # Head (circle) - Gray head
    head = go.Scatter(
        x=[x_pos],
        y=[y_pos + 2.5 * BOY_SCALE],  # Head is lower due to shorter upper body
        mode='markers',
        marker=dict(size=5 * BOY_SCALE, color='gray'),  # Gray head
        name='Head'
    )

    # Body (line) - Yellow shirt
    body = go.Scatter(
        x=[x_pos, x_pos],
        y=[y_pos + 2 * BOY_SCALE, y_pos + 0.5 * BOY_SCALE],  # Shorter upper body
        mode='lines',
        line=dict(color='yellow', width=2 * BOY_SCALE),  # Yellow shirt
        name='Body'
    )

    # Arms (lines) - Yellow shirt
    left_arm = go.Scatter(
        x=[x_pos - 0.3 * BOY_SCALE, x_pos],  # Wider arms
        y=[y_pos + 1.5 * BOY_SCALE, y_pos + 1 * BOY_SCALE],  # Adjusted arm height
        mode='lines',
        line=dict(color='yellow', width=2 * BOY_SCALE),  # Yellow shirt
        name='Left Arm'
    )
    right_arm = go.Scatter(
        x=[x_pos + 0.3 * BOY_SCALE, x_pos],  # Wider arms
        y=[y_pos + 1.5 * BOY_SCALE, y_pos + 1 * BOY_SCALE],  # Adjusted arm height
        mode='lines',
        line=dict(color='yellow', width=2 * BOY_SCALE),  # Yellow shirt
        name='Right Arm'
    )

    # Legs (lines) - White pants
    left_leg = go.Scatter(
        x=[x_pos - 0.3 * BOY_SCALE, x_pos],  # Wider legs
        y=[y_pos + 0.5 * BOY_SCALE, y_pos - 1 * BOY_SCALE],  # Longer legs
        mode='lines',
        line=dict(color='white', width=2 * BOY_SCALE),  # White pants
        name='Left Leg'
    )
    right_leg = go.Scatter(
        x=[x_pos + 0.3 * BOY_SCALE, x_pos],  # Wider legs
        y=[y_pos + 0.5 * BOY_SCALE, y_pos - 1 * BOY_SCALE],  # Longer legs
        mode='lines',
        line=dict(color='white', width=2 * BOY_SCALE),  # White pants
        name='Right Leg'
    )

    # Day label
    day_label = go.Scatter(
        x=[x_pos],
        y=[y_pos + 3.5 * BOY_SCALE],  # Label above the head
        mode='text',
        text=[f"Day {day}"],
        textposition="top center",
        textfont=dict(size=12, color='orange'),  # Orange color for the label
        name='Day Label'
    )

    return [head, body, left_arm, right_arm, left_leg, right_leg, day_label]

# Create a function to draw the mountain
def draw_mountain():
    """
    Draws a tall and wide mountain shape at 100 km.
    """
    x = np.linspace(MOUNTAIN_DISTANCE - MOUNTAIN_WIDTH, MOUNTAIN_DISTANCE + MOUNTAIN_WIDTH, 100)
    y = MOUNTAIN_HEIGHT * np.exp(-0.05 * (x - MOUNTAIN_DISTANCE)**2)  # Wider and fatter mountain
    mountain = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        line=dict(color='gray', width=4),
        name='Mountain'
    )
    return mountain

# Create the figure
fig = go.Figure()

# Add the mountain
fig.add_trace(draw_mountain())

# Add the boy's initial position
initial_x = 0  # Boy starts at 0 km
initial_y = 0  # Boy starts at ground level
boy_traces = draw_boy(initial_x, initial_y, 0)
for trace in boy_traces:
    fig.add_trace(trace)

# Set layout
fig.update_layout(
    xaxis=dict(range=[-10, MOUNTAIN_DISTANCE + MOUNTAIN_WIDTH + 10], title='Distance (km)'),
    yaxis=dict(range=[-5, MOUNTAIN_HEIGHT + 10], title='Height', showticklabels=False),
    showlegend=False,
    updatemenus=[{
        'type': 'buttons',
        'showactive': False,
        'buttons': [{
            'label': 'Play',
            'method': 'animate',
            'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]
        }]
    }]
)

# Create frames for animation
frames = []
for day in range(DAYS_TO_RUN + 1):
    # Update boy's position
    x_pos = initial_x + (day * KM_PER_DAY)  # Boy runs 5 km per day

    # Calculate boy's y-position based on mountain slope
    if x_pos < MOUNTAIN_DISTANCE - MOUNTAIN_WIDTH:
        y_pos = 0  # Boy is on flat ground
    else:
        # Boy is on the mountain slope
        y_pos = MOUNTAIN_HEIGHT * np.exp(-0.05 * (x_pos - MOUNTAIN_DISTANCE)**2)

    # Draw the boy at the new position
    boy_traces = draw_boy(x_pos, y_pos, day)

    # If the boy has reached the mountain top, keep the label at the top
    if x_pos >= MOUNTAIN_DISTANCE:
        y_pos = MOUNTAIN_HEIGHT  # Boy is at the top
        boy_traces[-1].y = [y_pos + 3.5 * BOY_SCALE]  # Update label position

    # Create a frame
    frame = go.Frame(
        data=[draw_mountain()] + boy_traces,
        name=str(day)
    )
    frames.append(frame)

# Add frames to the figure
fig.frames = frames

# Display the animation
st.plotly_chart(fig)

# Hide the celebratory message and cones initially
if 'show_message' not in st.session_state:
    st.session_state.show_message = False

# Check if the boy has reached the top
if frames[-1].name == str(DAYS_TO_RUN):  # Last frame
    st.session_state.show_message = True

# Display the celebratory message and cones if the boy has reached the top
if st.session_state.show_message:
    st.markdown("""
    <style>
    .celebrate {
        font-size: 24px;
        color: green;
        font-weight: bold;
        text-align: center;
    }
    </style>
    <div class="celebrate">🎉 The boy reached the top of the mountain! 🎉</div>
    """, unsafe_allow_html=True)


    # Add cones (optional, if you want to show something at the base)
    #st.write("Here are the cones at the base of the mountain! 🎉")
