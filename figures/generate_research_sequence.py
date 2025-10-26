#!/usr/bin/env python3
"""
Generate sequence diagram showing Researcher agent interactions with MCP tools.
Based on actual tool calls from DefaultParser.parse research phase.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# Configuration for single-column figure
fig_width = 3.5  # inches (single column width for ACM format)
fig_height = 6  # adjusted for fewer interactions
dpi = 300

# Actor positions (x-coordinates) - closer together for narrow figure
actors = {
    'javadoc': 0.4,
    'researcher': 1.5,
    'codecontext': 2.6
}

# Colors
color_call = '#2C3E50'
color_return = '#7F8C8D'
color_lifeline = '#BDC3C7'
color_box = '#ECF0F1'

fig, ax = plt.subplots(figsize=(fig_width, fig_height))

# Y-axis setup (top to bottom)
y_start = 9.5
y_step = 0.35  # spacing between messages
y_return_offset = 0.15  # spacing between call and its return (closer)

# Draw actor boxes at top
actor_height = 0.35
actor_width = 0.8

for name, x in actors.items():
    label_map = {
        'javadoc': 'Javadoc\nMCP',
        'researcher': 'Researcher',
        'codecontext': 'CodeContext\nMCP'
    }
    rect = FancyBboxPatch((x - actor_width/2, y_start - actor_height/2),
                           actor_width, actor_height,
                           boxstyle="round,pad=0.05",
                           edgecolor=color_call, facecolor=color_box,
                           linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x, y_start, label_map[name], ha='center', va='center',
            fontsize=8, weight='bold')

# Draw lifelines
y_end = 0.5
for x in actors.values():
    ax.plot([x, x], [y_start - actor_height/2 - 0.1, y_end],
            color=color_lifeline, linewidth=1, linestyle='--', zorder=1)

# Helper function to draw messages with multiline labels
def draw_message(y, from_actor, to_actor, label, label_line2=None, is_return=False):
    x1 = actors[from_actor]
    x2 = actors[to_actor]

    color = color_return if is_return else color_call
    linestyle = '--' if is_return else '-'
    # Filled arrow heads, smaller tips
    arrowstyle = '-|>' if not is_return else '<|-'

    arrow = FancyArrowPatch((x1, y), (x2, y),
                           arrowstyle=arrowstyle,
                           color=color,
                           linewidth=1.0 if not is_return else 0.8,
                           linestyle=linestyle,
                           mutation_scale=8,  # smaller arrow tips
                           zorder=2)
    ax.add_patch(arrow)

    # Label positioning
    mid_x = (x1 + x2) / 2

    if label_line2 and not is_return:
        # Two-line label for tool calls
        ax.text(mid_x, y + 0.12, label, ha='center', va='bottom',
                fontsize=6.5, weight='bold')
        ax.text(mid_x, y + 0.02, label_line2, ha='center', va='bottom',
                fontsize=6)
    else:
        # Single line for returns
        label_y = y + 0.06 if not is_return else y - 0.08
        ax.text(mid_x, label_y, label, ha='center', va='bottom' if not is_return else 'top',
                fontsize=6.5, style='italic' if is_return else 'normal')

    # Return different offsets for calls vs returns
    if is_return:
        return y - y_return_offset
    else:
        return y - y_step

# Initial prompt annotation
y_current = y_start - actor_height/2 - 0.3
ax.text(actors['researcher'], y_current, 'Initial prompt',
        ha='center', va='top', fontsize=8, style='italic',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', linewidth=0.5))
y_current -= y_step * 1.5

# Round 1: Four get_class_documentation calls
y_current = draw_message(y_current, 'researcher', 'javadoc',
                         'get_class_documentation', 'DefaultParser')
y_current = draw_message(y_current, 'javadoc', 'researcher',
                         'class methods & docs', is_return=True)

y_current = draw_message(y_current, 'researcher', 'javadoc',
                         'get_class_documentation', 'Options')
y_current = draw_message(y_current, 'javadoc', 'researcher',
                         'class methods & docs', is_return=True)

y_current = draw_message(y_current, 'researcher', 'javadoc',
                         'get_class_documentation', 'CommandLine')
y_current = draw_message(y_current, 'javadoc', 'researcher',
                         'class methods & docs', is_return=True)

y_current = draw_message(y_current, 'researcher', 'javadoc',
                         'get_class_documentation', 'ParseException')
y_current = draw_message(y_current, 'javadoc', 'researcher',
                         'exception docs', is_return=True)

# Round 2: get_method_code and list_classes
y_current -= y_step * 0.3
y_current = draw_message(y_current, 'researcher', 'codecontext',
                         'get_method_code', 'parse(Options, String[])')
y_current = draw_message(y_current, 'codecontext', 'researcher',
                         '2 implementations', is_return=True)

y_current = draw_message(y_current, 'researcher', 'javadoc',
                         'list_classes', 'org.apache.commons.cli')
y_current = draw_message(y_current, 'javadoc', 'researcher',
                         'package classes', is_return=True)

# Ellipsis to indicate continuation
ax.text(actors['researcher'], y_current - 0.3, '⋮', ha='center', va='center', fontsize=16)

# Styling
ax.set_xlim(-0.1, 3.1)
ax.set_ylim(y_end - 0.5, y_start + 0.5)
ax.axis('off')

plt.tight_layout()
plt.savefig('research-sequence.pdf', dpi=dpi, bbox_inches='tight')
plt.savefig('research-sequence.png', dpi=dpi, bbox_inches='tight')
print("Sequence diagram saved as research-sequence.pdf and research-sequence.png")