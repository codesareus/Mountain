import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Create a figure
fig, ax = plt.subplots()

x = [1, 2, 3, 4, 5, 6, 8, 10, 20]
y = [1, 2, 3, 4, 5, 6, 8, 10, 20]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.plot(x, y)

# Use Streamlit sliders to adjust line positions
h_line_pos = st.sidebar.slider('Horizontal Line Position', 0.0, 10.0, 5.0)
v_line_pos = st.sidebar.slider('Vertical Line Position', 0.0, 10.0, 5.0)

# Add lines based on slider values
ax.axhline(y=h_line_pos, color='r', lw=2, linestyle='-')
ax.axvline(x=v_line_pos, color='b', lw=2, linestyle='--')

st.pyplot(fig)
