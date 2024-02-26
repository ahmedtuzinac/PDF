import os

import uuid
from typing import List, Tuple

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np
from datetime import datetime
import json


def create_bar_chart(json_content: dict):
    categories = [i for i in range(5)]
    colors: list[tuple[float, float, float]] = [
        (209 / 255, 228 / 255, 209 / 255),
        (172 / 255, 198 / 255, 172 / 255),
        (152 / 255, 205 / 255, 149 / 255),
        (149 / 255, 189 / 255, 147 / 255),
        (146 / 255, 174 / 255, 145 / 255)
    ]
    values = get_values_for_bar_chart(json_content)

    fig, ax = plt.subplots()
    bars = ax.bar(categories, values, color=colors, width=0.7)

    for i, value in enumerate(values):
        plt.text(i, value + 2, str(value) + '€', ha='center', va='bottom', fontsize=12, color=(116 / 255, 120 / 255, 122 / 255))

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.axis('off')

    # Add a line at the midpoint of the y-axis
    midpoint = sum(ax.get_ylim()) / 2
    line_length = max(values) + 5  # Adjust the length as needed
    ax.axhline(0.3, linestyle='-', color=(207 / 255, 209 / 255, 208 / 255), linewidth=2, xmin=-0.1, xmax=len(categories))
    ax.axhline(midpoint * 2, linestyle='-', color=(207 / 255, 209 / 255, 208 / 255), linewidth=1, xmin=-0.1, xmax=len(categories))
    ax.axhline(midpoint, linestyle='-', color=(207 / 255, 209 / 255, 208 / 255), linewidth=1, xmin=-0.1, xmax=len(categories))

    bar_chart_filepath = f"/tmp/{uuid.uuid4()}.png"
    plt.savefig(bar_chart_filepath)
    plt.close()

    return bar_chart_filepath


def get_values_for_bar_chart(json_content: dict):
    data = json_content
    summary = data['invoice_json']['summary']
    components = summary['components']

    n = 0

    for item in summary['additional_cost']:
        n += item['amount']

    values = [
        float(components['energy']),
        float(components['transport']),
        float(components['system']),
        float(summary['tax']['vat']),
        float(n)
    ]

    return values


def get_values_for_donut_chart(json_content: dict):
    metering = json_content['invoice_json']['summary']['metering']
    active = []
    for item in metering:
        if item['type'] == 'active':
            active.append(item)

    f1 = 0
    f2 = 0
    f3 = 0

    f1 = active[1]['f1'] - active[0]['f1']
    f2 = active[1]['f2'] - active[0]['f2']
    f3 = active[1]['f3'] - active[0]['f3']

    return ['F2 + F3', 'F1'], [f2 + f3, f1]


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import numpy as np


def create_donut_chart(json_content: dict):
    labels, sizes = get_values_for_donut_chart(json_content)
    colors = [
        (156 / 255, 182 / 255, 154 / 255),
        (209 / 255, 228 / 255, 207 / 255)
    ]

    # Create a pie chart
    fig, ax = plt.subplots()

    # Draw the outer circle (donut shape)
    wedges, texts = ax.pie(sizes, startangle=90, wedgeprops=dict(width=0.35, edgecolor='w'), colors=colors)

    # Draw a white circle in the center to create the donut hole
    center_circle = plt.Circle((0, 0), 0.6, color='white', fc='white', linewidth=1.25)
    ax.add_patch(center_circle)

    angles = [0] + [w.theta2 for w in wedges]
    mid_angles = [(a + b) / 2.0 for a, b in zip(angles[:-1], angles[1:])]

    angle1 = (wedges[0].theta2 + wedges[1].theta1) / 2.0
    angle2 = (wedges[1].theta2 + wedges[0].theta1) / 2.0
    angle1_rad = np.deg2rad(angle1)
    angle2_rad = np.deg2rad(angle2 + 180)
    line_length_factor = 1.7

    ax.plot([0, line_length_factor * 0.70 * np.cos(angle1_rad)], [0, line_length_factor * 0.70 * np.sin(angle1_rad)], linestyle='-', color=(61 / 255, 81 / 255, 45 / 255),
            linewidth=1)
    ax.plot([0, line_length_factor * 0.70 * np.cos(angle2_rad)], [0, line_length_factor * 0.70 * np.sin(angle2_rad)], linestyle='-', color=(61 / 255, 81 / 255, 45 / 255),
            linewidth=1)

    ax.axis('equal')

    # plt.show()
    donut_chart_filepath = f"/tmp/{uuid.uuid4()}.png"
    plt.savefig(donut_chart_filepath)
    plt.close()
    return donut_chart_filepath


def create_hist_char(json_content):

    hist_data = json_content['invoice_json']['hist_data']

    months = {}
    current_year = datetime.utcnow().year
    for item in hist_data:
        if item.split('-')[0] == str(current_year):
            months[item.split('-')[1]] = [
                hist_data[item]['active']['F1'],
                hist_data[item]['active']['F2'],
                hist_data[item]['active']['F3'],
            ]
    try:
        return dict(list(months.items())[-12:])
    except IndexError as e:
        return months


hist = {"hist_data": {
    "2024-01": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-02": {
        "active": {
            "F1": 1200,
            "F2": 500,
            "F3": 900
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-03": {
        "active": {
            "F1": 500,
            "F2": 501,
            "F3": 900
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-04": {
        "active": {
            "F1": 900,
            "F2": 903,
            "F3": 501
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-05": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-06": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-07": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-08": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-09": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-10": {
        "active": {
            "F1": 231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-11": {
        "active": {
            "F1": 1231,
            "F2": 231,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
    "2024-12": {
        "active": {
            "F1": 931,
            "F2": 931,
            "F3": 931
        },
        "peak": 1234,
        "total_cost": 342342
    },
}}


def create_history_chart(json_content):
    months_real = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    months = create_hist_char(json_content)
    colors = [
        (105 / 255, 197 / 255, 47 / 255),
        (30 / 255, 103 / 255, 67 / 255),
        (44 / 255, 75 / 255, 33 / 255)
    ]
    fig, ax = plt.subplots(figsize=(15, 3))

    for i in range(len(months_real)):
        bottom = 0
        if months_real[i] in months:
            for j in range(len(months[months_real[i]])):
                ax.bar(i, months[months_real[i]][j], bottom=bottom, label=f'Section {j + 1}', width=0.8, color=colors[j])
                bottom += months[months_real[i]][j]
                bottom += 100
        else:
            for j in range(3):
                ax.bar(i, 0, bottom=bottom, label=f'Section {j + 1}', color=colors[j])
                bottom += 0

    # Show the plot
    from PIL import Image

    ax.axis('off')
    plt_filepath = f"/tmp/{uuid.uuid4()}.png"
    plt.savefig(plt_filepath, dpi=300, bbox_inches='tight', pad_inches=0.1)
    img = Image.open(plt_filepath)
    hist_chart_filepath = f"/tmp/{uuid.uuid4()}.png"
    cropped_img = img.crop((0, 0, img.width, img.height - 25))
    if os.path.exists(plt_filepath):
        os.remove(plt_filepath)
    cropped_img.save(hist_chart_filepath, dpi=(300, 300))
    plt.close()
    return hist_chart_filepath