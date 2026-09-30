import json
import subprocess
import os

PRES_ID = "1B4Mgq41Ye5M1kj1W5zbzCRPVkUG80WfLJahQeSWJZCo"

# Typography
SERIF = "Spectral"
SANS = "Work Sans"

# Color Palette (Refined Minimalist Editorial + MongoDB Green Accent)
C_TEXT = "#0F172A"       # Charcoal / Black display & primary text
C_BODY = "#334155"       # Slate body copy (crisp, readable)
C_MUTED = "#64748B"      # Secondary labels & subtitles
C_LIGHT = "#94A3B8"      # Light metadata, footers, rules
C_BORDER = "#E2E8F0"     # Ultra-subtle divider lines
C_BORDER_DARK = "#CBD5E1"# Card outlines
C_WHITE = "#FFFFFF"      # Pure canvas white
C_BG_CARD = "#F8FAFC"    # Soft editorial surface fill

# Accents
C_GREEN = "#00684A"      # MongoDB Deep Forest Green
C_GREEN_BG = "#F0FDF4"   # Subtle Mint Green Tint
C_GREEN_BORDER = "#86EFAC"# Mint border
C_ALERT = "#DC2626"      # Restrained Crimson Alert
C_ALERT_BG = "#FEF2F2"   # Subtle Crimson Tint
C_ALERT_BORDER = "#FCA5A5"# Light Crimson Border

ops = []
shape_counter = 0

def add_card(slide, x, y, width, height, bg_color=C_WHITE, border_color=C_BORDER, border_weight=1.0):
    global shape_counter
    shape_counter += 1
    s_id = f"card_{slide}_{shape_counter}"
    ops.append({
        "op": "add-shape",
        "slide": slide,
        "shape_type": "ROUND_RECTANGLE",
        "x": x, "y": y, "width": width, "height": height,
        "background_color": bg_color,
        "id": s_id
    })
    if border_color:
        ops.append({
            "op": "style-shape",
            "element": s_id,
            "background_color": bg_color,
            "outline_color": border_color,
            "outline_weight": border_weight
        })
    return s_id

def add_rule(slide, x, y, width, height=1, color=C_BORDER):
    ops.append({
        "op": "add-shape",
        "slide": slide,
        "shape_type": "RECTANGLE",
        "x": x, "y": y, "width": width, "height": height,
        "background_color": color
    })

def add_header(slide, section_label, main_heading, supporting_copy=None):
    # Section Label
    ops.append({
        "op": "add-textbox", "slide": slide,
        "text": section_label.upper(),
        "x": 45, "y": 20, "width": 350, "height": 16,
        "font_size": 10.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    # Main Heading
    ops.append({
        "op": "add-textbox", "slide": slide,
        "text": main_heading,
        "x": 45, "y": 36, "width": 630, "height": 34,
        "font_size": 22, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    # Supporting Copy
    if supporting_copy:
        ops.append({
            "op": "add-textbox", "slide": slide,
            "text": supporting_copy,
            "x": 45, "y": 72, "width": 630, "height": 18,
            "font_size": 12, "color": C_BODY, "font_family": SANS
        })
        add_rule(slide, 45, 93, 630, 1, C_BORDER)
    else:
        add_rule(slide, 45, 74, 630, 1, C_BORDER)

def add_footer(slide, current_slide_str, section_context):
    ops.append({
        "op": "add-textbox", "slide": slide,
        "text": f"RELIEFMESH · {section_context.upper()}",
        "x": 45, "y": 382, "width": 450, "height": 14,
        "font_size": 8.5, "color": C_LIGHT, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": slide,
        "text": current_slide_str,
        "x": 630, "y": 382, "width": 45, "height": 14,
        "font_size": 9, "bold": True, "color": C_MUTED, "font_family": SANS, "alignment": "right"
    })

# =============================================================================
# SLIDE 1: TITLE
# =============================================================================
ops.append({"op": "set-background", "slide": "p", "color": C_WHITE})

# Left Column (x: 45 to 330)
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "RELIEFMESH SYSTEMS ARCHITECTURE",
    "x": 45, "y": 38, "width": 290, "height": 16,
    "font_size": 10.5, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "RELIEFMESH",
    "x": 42, "y": 58, "width": 295, "height": 78,
    "font_size": 68, "bold": True, "color": C_TEXT, "font_family": SERIF
})
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "Operational Crisis Coordination Engine",
    "x": 45, "y": 144, "width": 290, "height": 26,
    "font_size": 17, "bold": True, "italic": True, "color": C_MUTED, "font_family": SERIF
})
add_rule("p", 45, 178, 275, 1, C_BORDER)
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "Keeping disaster-response resource allocations synchronized with fast-changing physical ground reality.",
    "x": 45, "y": 190, "width": 275, "height": 48,
    "font_size": 13.5, "color": C_BODY, "font_family": SANS, "line_spacing": 130
})

# Freshness Invariant Box
add_card("p", 45, 252, 275, 86, C_GREEN_BG, C_GREEN_BORDER, 1.2)
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "THE FRESHNESS INVARIANT",
    "x": 56, "y": 258, "width": 253, "height": 15,
    "font_size": 9, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "“No operational allocation may outlive its physical ground truth.”",
    "x": 56, "y": 275, "width": 253, "height": 38,
    "font_size": 11.5, "italic": True, "color": C_TEXT, "font_family": SERIF, "line_spacing": 125
})
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "Search proposes. CAS disposes. Invalidation rematches.",
    "x": 56, "y": 315, "width": 253, "height": 15,
    "font_size": 8.5, "bold": True, "color": C_MUTED, "font_family": SANS
})

ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "ReliefMesh Engineering Team · MongoDB Hackathon 2026",
    "x": 45, "y": 362, "width": 290, "height": 16,
    "font_size": 10.5, "color": C_LIGHT, "font_family": SANS
})

# Right Column - System Convergence Diagram (x: 345 to 675)
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "OPERATIONAL CONTROL PLANE CONVERGENCE",
    "x": 348, "y": 38, "width": 327, "height": 16,
    "font_size": 9.5, "bold": True, "color": C_MUTED, "font_family": SANS, "alignment": "center"
})

# 4 Inbound Signal Source Nodes
sources = [
    ("Distress Audio", "Whisper + Dialects", 348),
    ("Sensor Telemetry", "River Gauges / ASP", 432),
    ("Agency Stocks", "Depot ERPs / Leases", 516),
    ("Hazard Inundation", "Hydraulic Sidecar", 600)
]
for title, sub, x_pos in sources:
    add_card("p", x_pos, 62, 76, 50, C_BG_CARD, C_BORDER_DARK, 1)
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": title,
        "x": x_pos + 2, "y": 66, "width": 72, "height": 22,
        "font_size": 7.5, "bold": True, "color": C_TEXT, "font_family": SANS, "alignment": "center"
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": sub,
        "x": x_pos + 2, "y": 90, "width": 72, "height": 18,
        "font_size": 6.8, "color": C_MUTED, "font_family": SANS, "alignment": "center"
    })
    ops.append({
        "op": "add-line", "slide": "p",
        "x": x_pos + 38, "y": 114, "width": 0, "height": 20,
        "line_weight": 1.2, "color": C_BORDER_DARK, "end_arrow": "FILL_ARROW"
    })

# Center Hero Node: MongoDB Atlas Unified Core
add_card("p", 365, 138, 292, 108, C_GREEN_BG, C_GREEN, 1.8)
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "MONGODB ATLAS",
    "x": 375, "y": 144, "width": 272, "height": 18,
    "font_size": 13, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "Unified Operational Control Plane",
    "x": 375, "y": 163, "width": 272, "height": 18,
    "font_size": 11, "bold": True, "color": C_TEXT, "font_family": SERIF, "alignment": "center"
})
add_rule("p", 385, 184, 252, 1, C_GREEN_BORDER)
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "Living Incident Twins · Vernacular Lexical Search · Vector kNN\n2dsphere Spatial Geometries · Single-Document OCC · Change Streams",
    "x": 372, "y": 188, "width": 278, "height": 30,
    "font_size": 7.5, "color": "#166534", "font_family": SANS, "alignment": "center", "line_spacing": 130
})
ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "Authoritative transactional state coordinator bridging awareness and logistics.",
    "x": 372, "y": 222, "width": 278, "height": 18,
    "font_size": 7, "italic": True, "color": C_MUTED, "font_family": SANS, "alignment": "center"
})

# 3 Coordinated Operational Output States
out_states = [
    ("ATOMIC ALLOCATION", "Zero phantom claims\nPredicate guard __v", 348),
    ("DYNAMIC REROUTING", "Delta invalidation\n$geoIntersects check", 454),
    ("INCIDENT TWINS", "Coherent ground truth\nCross-agency audit", 560)
]
for title, desc, x_pos in out_states:
    ops.append({
        "op": "add-line", "slide": "p",
        "x": x_pos + 52, "y": 248, "width": 0, "height": 18,
        "line_weight": 1.2, "color": C_GREEN, "end_arrow": "FILL_ARROW"
    })
    add_card("p", x_pos, 268, 104, 70, C_WHITE, C_BORDER_DARK, 1)
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": title,
        "x": x_pos + 4, "y": 273, "width": 96, "height": 16,
        "font_size": 8, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": desc,
        "x": x_pos + 4, "y": 292, "width": 96, "height": 40,
        "font_size": 7.5, "color": C_BODY, "font_family": SANS, "alignment": "center", "line_spacing": 125
    })

ops.append({
    "op": "add-textbox", "slide": "p",
    "text": "Closed Operating Loop: Ingest → Twin → 4-R Retrieval → OCC Commit → Invalidate → Rematch",
    "x": 348, "y": 352, "width": 327, "height": 16,
    "font_size": 8, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})

ops.append({
    "op": "set-notes", "slide": "p",
    "text": "ReliefMesh: Operational Crisis Coordination Engine. Master submission for MongoDB Hackathon 2026. Central thesis: Keeping disaster-response allocations synchronized with changing physical reality via MongoDB Atlas as the unified operational core."
})

# =============================================================================
# SLIDE 2: THE PROBLEM
# =============================================================================
ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_2"})
ops.append({"op": "set-background", "slide": "SLIDE_2", "color": C_WHITE})
add_header("SLIDE_2", "THE PROBLEM", "Disaster response breaks when operational state drifts from reality.", "The failure is not lack of inbound data. It is stale, fragmented, and inconsistent operational state.")

# Comparison 1: Scenario A - Phantom Allocation
add_card("SLIDE_2", 45, 106, 305, 150, C_BG_CARD, C_BORDER_DARK, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "SCENARIO A · RESOURCE CONTENTION (PHANTOM ALLOCATION)",
    "x": 56, "y": 112, "width": 283, "height": 16,
    "font_size": 8.5, "bold": True, "color": C_ALERT, "font_family": SANS
})
# Left Sub-card: Field Reality
add_card("SLIDE_2", 56, 132, 135, 76, C_WHITE, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "FIELD REALITY\nBlood Bank: 5 units available\n• Ambulance A needs: 4 units\n• Ambulance B needs: 4 units\nTotal Required: 8 units",
    "x": 62, "y": 136, "width": 123, "height": 68,
    "font_size": 8, "color": C_TEXT, "font_family": SANS, "line_spacing": 125
})
# Right Sub-card: Operations View
add_card("SLIDE_2", 201, 132, 138, 76, C_ALERT_BG, C_ALERT_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "OPERATIONS VIEW\nBoth dispatchers see: AVAILABLE\n2 dispatch decisions\n1 scarce resource\nCONFLICT: 1 arrives empty!",
    "x": 207, "y": 136, "width": 126, "height": 68,
    "font_size": 8, "bold": True, "color": C_ALERT, "font_family": SANS, "line_spacing": 125
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "FAILURE: PHANTOM ALLOCATION — 45 mins wasted through debris, patient dies in transit.",
    "x": 56, "y": 216, "width": 283, "height": 32,
    "font_size": 8, "italic": True, "color": C_ALERT, "font_family": SANS
})

# Comparison 2: Scenario B - Blind Routing
add_card("SLIDE_2", 370, 106, 305, 150, C_BG_CARD, C_BORDER_DARK, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "SCENARIO B · ENVIRONMENTAL MUTATION (BLIND ROUTING)",
    "x": 381, "y": 112, "width": 283, "height": 16,
    "font_size": 8.5, "bold": True, "color": C_ALERT, "font_family": SANS
})
# Left Sub-card: Dispatch Time
add_card("SLIDE_2", 381, 132, 135, 76, C_WHITE, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "DISPATCH TIME (02:00)\nHighway 4: Marked Safe ✓\nSupply convoy launched\nStatic route cached\nZero stream reactivity",
    "x": 387, "y": 136, "width": 123, "height": 68,
    "font_size": 8, "color": C_TEXT, "font_family": SANS, "line_spacing": 125
})
# Right Sub-card: Flood Mutation
add_card("SLIDE_2", 526, 132, 138, 76, C_ALERT_BG, C_ALERT_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "MUTATION (02:15)\nLevee breaches 2.4km north\nFlood perimeter expands\nHighway submerged\nDISPATCHED ROUTE INVALID!",
    "x": 532, "y": 136, "width": 126, "height": 68,
    "font_size": 8, "bold": True, "color": C_ALERT, "font_family": SANS, "line_spacing": 125
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "FAILURE: BLIND ROUTING — Rescue crew enters submerged corridor unaware. Rescuers become victims.",
    "x": 381, "y": 216, "width": 283, "height": 32,
    "font_size": 8, "italic": True, "color": C_ALERT, "font_family": SANS
})

# Exactly 3 Pain Points (Matching template 16 pt heading equivalent, clean columns)
pain_points = [
    ("01", "STATE DRIFT", "Physical reality changes faster than coordination state. Point-in-time reads become deadly falsehoods without transactional controls."),
    ("02", "FRAGMENTED AWARENESS", "Different systems know different parts of the incident. Ushahidi crowdsources distress; Sahana logs warehouses — neither coordinates."),
    ("03", "STALE ALLOCATIONS", "Teams act on inventory or route information that is no longer valid. Relational lock contention deadlocks during peak emergencies.")
]
col_w = 198
for i, (num, title, desc) in enumerate(pain_points):
    x_col = 45 + i * 216
    add_card("SLIDE_2", x_col, 266, col_w, 74, C_WHITE, C_BORDER, 1)
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": f"{num} · {title}",
        "x": x_col + 8, "y": 271, "width": col_w - 16, "height": 16,
        "font_size": 9, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": desc,
        "x": x_col + 8, "y": 289, "width": col_w - 16, "height": 46,
        "font_size": 7.5, "color": C_BODY, "font_family": SANS, "line_spacing": 125
    })

# Bottom Message Callout
add_card("SLIDE_2", 45, 348, 630, 24, C_GREEN_BG, C_GREEN_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_2",
    "text": "THE CORE PROBLEM: KEEPING OPERATIONAL DECISIONS FRESH.",
    "x": 45, "y": 352, "width": 630, "height": 16,
    "font_size": 9.5, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})

add_footer("SLIDE_2", "02", "THE OPERATIONAL FAILURE MODE")
ops.append({
    "op": "set-notes", "slide": "SLIDE_2",
    "text": "Disaster response breaks when operational state drifts from reality. The core problem is not inbound data collection; it is keeping allocation decisions fresh. Traditional disconnected architectures produce phantom allocations and blind routings."
})

# =============================================================================
# SLIDE 3: YOUR SOLUTION
# =============================================================================
ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_3"})
ops.append({"op": "set-background", "slide": "SLIDE_3", "color": C_WHITE})
add_header("SLIDE_3", "YOUR SOLUTION", "ReliefMesh closes the loop between awareness, allocation and changing reality.")

# Exactly Three Columns (x: 45, 261, 477 - width 198 each)
# Column 1: RELEVANT
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "01",
    "x": 45, "y": 84, "width": 50, "height": 18,
    "font_size": 15, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "RELEVANT",
    "x": 45, "y": 102, "width": 198, "height": 24,
    "font_size": 18, "bold": True, "color": C_TEXT, "font_family": SERIF
})
add_card("SLIDE_3", 45, 128, 198, 108, C_BG_CARD, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "FIELD DISTRESS MESSAGE:\n“Need pediatric O-negative blood urgently”\n(Vernacular: “bachhe ke liye khoon chahiye”)",
    "x": 52, "y": 133, "width": 184, "height": 34,
    "font_size": 7.5, "italic": True, "color": C_TEXT, "font_family": SANS, "line_spacing": 120
})
add_card("SLIDE_3", 52, 170, 184, 28, C_WHITE, C_GREEN_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "LEXICAL SYNONYM + VECTOR EMBEDDING\nAtlas Search 8.1+ $rankFusion → Relevant Candidates",
    "x": 54, "y": 172, "width": 180, "height": 24,
    "font_size": 7, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "Annotation: Atlas Search + Vector Search + Synonyms",
    "x": 52, "y": 204, "width": 184, "height": 24,
    "font_size": 6.8, "color": C_MUTED, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "Understand what the request means even when field terminology differs from inventory terminology. Degrades gracefully if embedding APIs fail.",
    "x": 45, "y": 242, "width": 198, "height": 62,
    "font_size": 8, "color": C_BODY, "font_family": SANS, "line_spacing": 130
})

# Column 2: REACHABLE
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "02",
    "x": 261, "y": 84, "width": 50, "height": 18,
    "font_size": 15, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "REACHABLE",
    "x": 261, "y": 102, "width": 198, "height": 24,
    "font_size": 18, "bold": True, "color": C_TEXT, "font_family": SERIF
})
add_card("SLIDE_3", 261, 128, 198, 108, C_BG_CARD, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "REQUEST LOCATION  ───►  NEARBY DEPOTS\nRadius Filter (50km) → OSRM Road LineString",
    "x": 268, "y": 133, "width": 184, "height": 24,
    "font_size": 7.5, "bold": True, "color": C_TEXT, "font_family": SANS
})
add_card("SLIDE_3", 268, 160, 184, 42, C_WHITE, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "HAZARD CHECK: 2dsphere $geoIntersects\nCandidate A: Intersects flood polygon ✕ (Pruned!)\nCandidate B: Safe path verified ✓ (Approved)",
    "x": 272, "y": 164, "width": 176, "height": 34,
    "font_size": 7, "color": C_TEXT, "font_family": SANS, "line_spacing": 120
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "Visual: Route LineString vs Flood Barrier Polygon",
    "x": 268, "y": 204, "width": 184, "height": 24,
    "font_size": 6.8, "color": C_MUTED, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "A nearby resource is not necessarily reachable. Euclidean proximity is deceptive; ReliefMesh prunes routes intersecting dynamic hazard barriers before allocation.",
    "x": 261, "y": 242, "width": 198, "height": 62,
    "font_size": 8, "color": C_BODY, "font_family": SANS, "line_spacing": 130
})

# Column 3: RESERVED
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "03",
    "x": 477, "y": 84, "width": 50, "height": 18,
    "font_size": 15, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "RESERVED",
    "x": 477, "y": 102, "width": 198, "height": 24,
    "font_size": 18, "bold": True, "color": C_TEXT, "font_family": SERIF
})
add_card("SLIDE_3", 477, 128, 198, 108, C_BG_CARD, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "DEPOT STATE: 5 UNITS AVAILABLE\nDispatcher A: 4 units → COMMIT ✓ (OCC __v: 1)\nDispatcher B: 4 units → PREDICATE FAIL ✕",
    "x": 484, "y": 133, "width": 184, "height": 34,
    "font_size": 7.5, "bold": True, "color": C_TEXT, "font_family": SANS, "line_spacing": 120
})
add_card("SLIDE_3", 484, 170, 184, 28, C_WHITE, C_GREEN_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "FAILED PREDICATE → IMMEDIATE REMATCH\nAutomated jittered re-query to alternate depot",
    "x": 486, "y": 172, "width": 180, "height": 24,
    "font_size": 7, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "OCC + Conditional Atomic CAS + ACID Transactions",
    "x": 484, "y": 204, "width": 184, "height": 24,
    "font_size": 6.8, "color": C_MUTED, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "Candidate retrieval proposes. Authoritative state is revalidated at commit time. Prevents phantom allocations without heavyweight multi-table locking.",
    "x": 477, "y": 242, "width": 198, "height": 62,
    "font_size": 8, "color": C_BODY, "font_family": SANS, "line_spacing": 130
})

# Large Quote & Moonshot Callout
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "“Search proposes. CAS disposes.”",
    "x": 45, "y": 312, "width": 315, "height": 26,
    "font_size": 18, "bold": True, "italic": True, "color": C_GREEN, "font_family": SERIF
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "Eventual consistency for candidate discovery; authoritative atomic predicates for resource commitment.",
    "x": 45, "y": 340, "width": 315, "height": 26,
    "font_size": 8, "color": C_MUTED, "font_family": SANS
})

add_card("SLIDE_3", 370, 314, 305, 52, C_GREEN_BG, C_GREEN_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "RELIEFMESH IS NOT A DISASTER MAP.",
    "x": 375, "y": 322, "width": 295, "height": 16,
    "font_size": 9.5, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_3",
    "text": "IT IS A REACTIVE OPERATIONAL COORDINATION LOOP.",
    "x": 375, "y": 340, "width": 295, "height": 16,
    "font_size": 8.5, "bold": True, "color": C_TEXT, "font_family": SANS, "alignment": "center"
})

add_footer("SLIDE_3", "03", "DOMAIN ARCHITECTURE · THE 4-R OPERATIONAL SPINE")
ops.append({
    "op": "set-notes", "slide": "SLIDE_3",
    "text": "ReliefMesh closes the loop between awareness, allocation, and changing reality via 4 operational gates: Relevant (Search/Vector/Synonyms), Reachable (2dsphere route checks), Reserved (Single-document OCC), and Resilient (Delta-scoped invalidation)."
})

# =============================================================================
# SLIDE 4: TECHNOLOGY & AI FEATURES
# =============================================================================
ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_4"})
ops.append({"op": "set-background", "slide": "SLIDE_4", "color": C_WHITE})

# Header (Two Columns)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "TECHNOLOGY & AI FEATURES",
    "x": 45, "y": 20, "width": 300, "height": 16,
    "font_size": 10.5, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "Technology Stack",
    "x": 45, "y": 36, "width": 220, "height": 34,
    "font_size": 22, "bold": True, "color": C_TEXT, "font_family": SERIF
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "Key Features & Unified Operational Core",
    "x": 285, "y": 36, "width": 390, "height": 34,
    "font_size": 22, "bold": True, "color": C_TEXT, "font_family": SERIF
})
add_rule("SLIDE_4", 45, 74, 630, 1, C_BORDER)

# Left Column: Tech Stack & Architecture Audit (x: 45 to 265)
add_card("SLIDE_4", 45, 86, 220, 136, C_BG_CARD, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "OPERATIONAL COMPONENT STACK",
    "x": 55, "y": 92, "width": 200, "height": 14,
    "font_size": 8, "bold": True, "color": C_GREEN, "font_family": SANS
})
stack_items = [
    ("Frontend", "React / Operational Console PWA"),
    ("Backend", "Node.js / Allocation Workers"),
    ("Operational Core", "MongoDB Atlas (MongoDB 8.1+)"),
    ("AI Layer", "Whisper Speech + Embeddings API"),
    ("Specialized Sidecars", "OSRM (Roads) + Hydro (Floods)")
]
for idx, (label, val) in enumerate(stack_items):
    y_item = 110 + idx * 21
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": f"• {label}: {val}",
        "x": 55, "y": y_item, "width": 200, "height": 18,
        "font_size": 7.5, "color": C_TEXT, "font_family": SANS
    })

# Honest Architecture Audit (Postgres vs Mongo)
add_card("SLIDE_4", 45, 230, 220, 136, C_WHITE, C_BORDER_DARK, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "HONEST ARCHITECTURE AUDIT",
    "x": 55, "y": 236, "width": 200, "height": 14,
    "font_size": 8, "bold": True, "color": C_TEXT, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "PostgreSQL Stack (5 Distributed Systems):\nPostgreSQL + PostGIS + pgvector + Debezium + Kafka\n\nReliefMesh Stack (1 Managed Control Plane):\nMongoDB Atlas: Search + Vector + Geo + OCC + Streams\n\nTrade-off Reality: pgRouting is superior for road graphs, so we delegate routing to OSRM. MongoDB's win is the integrated reactive loop without Kafka sprawl.",
    "x": 55, "y": 252, "width": 200, "height": 108,
    "font_size": 7, "color": C_BODY, "font_family": SANS, "line_spacing": 125
})

# Right Column: HERO VISUAL - Central Hub & 6 Modules
add_card("SLIDE_4", 412, 178, 140, 60, C_GREEN_BG, C_GREEN, 2)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "MONGODB ATLAS",
    "x": 416, "y": 184, "width": 132, "height": 18,
    "font_size": 11, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "Unified Operational Core",
    "x": 416, "y": 202, "width": 132, "height": 16,
    "font_size": 9.5, "bold": True, "color": C_TEXT, "font_family": SERIF, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "Transactional State Plane",
    "x": 416, "y": 218, "width": 132, "height": 14,
    "font_size": 7, "italic": True, "color": C_MUTED, "font_family": SANS, "alignment": "center"
})

# 6 Surrounding Modules
modules = [
    ("01 · DOCUMENT STATE", "Living Incidents, inventory, active missions & dynamic hazard bounds.", 285, 86, 120, 56),
    ("02 · ATLAS SEARCH", "Lucene tokenization + dynamic synonym mappings (disaster dialects).", 422, 86, 120, 56),
    ("03 · VECTOR SEARCH", "1536-dim cosine similarity for unstructured distress semantic intent.", 555, 86, 120, 56),
    ("04 · 2DSPHERE GEO", "Spherical indexing & $geoIntersects route collision detection.", 285, 268, 120, 56),
    ("05 · OCC ALLOCATION", "Single-document OCC (__v) + Multi-doc ACID only where required.", 422, 268, 120, 56),
    ("06 · CHANGE STREAMS", "Pre/Post-images for delta-scoped dynamic invalidation & rerouting.", 555, 268, 120, 56)
]
for mod_title, mod_desc, mx, my, mw, mh in modules:
    add_card("SLIDE_4", mx, my, mw, mh, C_WHITE, C_BORDER, 1)
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": mod_title,
        "x": mx + 5, "y": my + 4, "width": mw - 10, "height": 14,
        "font_size": 7.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": mod_desc,
        "x": mx + 5, "y": my + 18, "width": mw - 10, "height": 34,
        "font_size": 6.8, "color": C_BODY, "font_family": SANS, "line_spacing": 120
    })

# ASP Telemetry Sub-node
add_card("SLIDE_4", 285, 178, 110, 60, C_BG_CARD, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "ASP TELEMETRY",
    "x": 290, "y": 184, "width": 100, "height": 14,
    "font_size": 7.5, "bold": True, "color": C_TEXT, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "Atlas Stream Processing: windowed rate-of-rise ($derivative) alerts.",
    "x": 290, "y": 200, "width": 100, "height": 34,
    "font_size": 6.8, "color": C_BODY, "font_family": SANS, "line_spacing": 120
})

# Summary Line
add_card("SLIDE_4", 285, 342, 390, 24, C_GREEN_BG, C_GREEN_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_4",
    "text": "MongoDB connects retrieval, spatial safety, allocation and reactivity in one operational plane.",
    "x": 285, "y": 346, "width": 390, "height": 16,
    "font_size": 8, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})

add_footer("SLIDE_4", "04", "TECHNOLOGY STACK & MONGODB ATLAS CORE")
ops.append({
    "op": "set-notes", "slide": "SLIDE_4",
    "text": "MongoDB Atlas serves as the unified operational control plane, integrating Document State, Atlas Search, Vector Search, Geospatial Indexing, OCC Allocation, and Change Streams. Replaces 5 independent distributed components with one unified engine."
})

# =============================================================================
# SLIDE 5: HOW IT WORKS
# =============================================================================
ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_5"})
ops.append({"op": "set-background", "slide": "SLIDE_5", "color": C_WHITE})
add_header("SLIDE_5", "HOW IT WORKS", "One request travels through four operational gates.")

# Part 1: RELEVANT (Top Left)
add_card("SLIDE_5", 45, 86, 305, 128, C_BG_CARD, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "1 · RELEVANT (Vernacular & Adaptive Retrieval)",
    "x": 55, "y": 92, "width": 285, "height": 16,
    "font_size": 9, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "FIELD REPORT: “need khoon o-neg” (Dialect SMS/Audio)\n↓\nSYNONYM MAPPING: “khoon” → “blood”, “dawa” → “medicine”\n↓\nADAPTIVE RETRIEVAL: Named $rankFusion (Uniform RRF)\n• Combines Lucene Keyword + OpenAI 1536-dim Embedding\n• Degrades gracefully to lexical + proximity if embedding API is down",
    "x": 55, "y": 110, "width": 285, "height": 76,
    "font_size": 7.5, "color": C_TEXT, "font_family": SANS, "line_spacing": 125
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "Annotation: Self-healing probe ($searchMeta) widens geo radius if matches < 3.",
    "x": 55, "y": 188, "width": 285, "height": 20,
    "font_size": 7, "italic": True, "color": C_MUTED, "font_family": SANS
})

# Part 2: REACHABLE (Top Right)
add_card("SLIDE_5", 370, 86, 305, 128, C_BG_CARD, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "2 · REACHABLE (Spatial Reachability Gating)",
    "x": 380, "y": 92, "width": 285, "height": 16,
    "font_size": 9, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "CANDIDATE DEPOTS → 2dsphere Geo Filter (50km radius)\n↓\nOSRM ROUTE GENERATION: Produces turn-by-turn LineString\n↓\nHAZARD POLYGON CHECK: 2dsphere $geoIntersects on perimeters\n↓\nSAFE CANDIDATE COMMITTED | FLOODED CANDIDATE PRUNED",
    "x": 380, "y": 110, "width": 285, "height": 76,
    "font_size": 7.5, "color": C_TEXT, "font_family": SANS, "line_spacing": 125
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "ARCHITECTURAL RULE: EUCLIDEAN NEARBY ≠ ROAD REACHABLE.",
    "x": 380, "y": 188, "width": 285, "height": 20,
    "font_size": 7.5, "bold": True, "color": C_ALERT, "font_family": SANS
})

# Part 3: RESERVED (Bottom Left)
add_card("SLIDE_5", 45, 222, 305, 128, C_BG_CARD, C_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "3 · RESERVED (Atomic OCC & Jittered Rematch)",
    "x": 55, "y": 228, "width": 285, "height": 16,
    "font_size": 9, "bold": True, "color": C_GREEN, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "DEPOT INVENTORY: 5 UNITS AVAILABLE\n• Request A (4 units) → CAS match on __v → COMMIT ✓\n• Request B (4 units) → Predicate fail (modifiedCount: 0) ✕\n\nTHUNDERING HERD DEFENSE:\n• Losers execute immediate client rematch across randomized top-3 window\n• Exponential backoff with full jitter prevents depot clumping",
    "x": 55, "y": 246, "width": 285, "height": 80,
    "font_size": 7.5, "color": C_TEXT, "font_family": SANS, "line_spacing": 125
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "Single-Document OCC (__v) + Bounded History ($slice: -10).",
    "x": 55, "y": 328, "width": 285, "height": 16,
    "font_size": 7, "italic": True, "color": C_MUTED, "font_family": SANS
})

# Part 4: RESILIENT (Bottom Right - HERO VISUAL)
add_card("SLIDE_5", 370, 222, 305, 128, C_ALERT_BG, C_ALERT_BORDER, 1.5)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "4 · RESILIENT (Hero: Delta-Scoped Invalidation)",
    "x": 380, "y": 228, "width": 285, "height": 16,
    "font_size": 9, "bold": True, "color": C_ALERT, "font_family": SANS
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "ACTIVE MISSION: Convoy in transit ────────► Hospital\nFLOOD PERIMETER EXPANDS: Old Polygon  ──►  Expanded Polygon\n↓\nCHANGE STREAM WITH PRE/POST-IMAGES:\n• Spatial Delta Diff: Evaluates ONLY the new expansion zone\n• 2dsphere $geoIntersects detects route compromised in real-time\n• Immediate trigger: Flags mission & dispatches instant reroute",
    "x": 380, "y": 246, "width": 285, "height": 80,
    "font_size": 7.5, "color": C_TEXT, "font_family": SANS, "line_spacing": 125
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "Resumable cursor (resumeToken) + Cold-start resync protocol.",
    "x": 380, "y": 328, "width": 285, "height": 16,
    "font_size": 7, "italic": True, "color": C_ALERT, "font_family": SANS
})

# Bottom Flow Line
add_card("SLIDE_5", 45, 356, 630, 22, C_GREEN_BG, C_GREEN_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_5",
    "text": "RELEVANT  →  REACHABLE  →  RESERVED  →  RESILIENT",
    "x": 45, "y": 359, "width": 630, "height": 16,
    "font_size": 9, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})

add_footer("SLIDE_5", "05", "THE 4-GATE OPERATIONAL WORKFLOW")
ops.append({
    "op": "set-notes", "slide": "SLIDE_5",
    "text": "Every relief request passes through 4 operational gates: Relevant (vernacular synonyms and rankFusion), Reachable (OSRM route checked against 2dsphere hazard polygons), Reserved (single-document OCC with version guard), and Resilient (pre/post-image delta-scoped invalidation and dynamic reroute)."
})

# =============================================================================
# SLIDE 6: DATA FLOW
# =============================================================================
ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_6"})
ops.append({"op": "set-background", "slide": "SLIDE_6", "color": C_WHITE})
add_header("SLIDE_6", "DATA FLOW", "From field signal to a continuously updated operational state.")

# 5 Sequential Stages (Horizontal)
stages = [
    ("STAGE 01", "INPUT", [
        "Citizen SMS / Voice (Twilio Gateway)",
        "Field Reports (Audio & text pings)",
        "Agency Consoles (Depot inventories)",
        "IoT River Gauges (Hydrologic sensors)"
    ], C_BG_CARD, C_BORDER, C_TEXT),
    
    ("STAGE 02", "PROCESSING", [
        "Branch A: Whisper + NLP structured incident extraction",
        "Branch B: ASP tumbling window rate-of-rise ($derivative)",
        "Boundary: Hydraulic sidecar computes flood polygon"
    ], C_BG_CARD, C_BORDER, C_TEXT),
    
    ("STAGE 03", "ATLAS CORE", [
        "living_incidents",
        "resource_inventory",
        "hazard_perimeters",
        "active_missions",
        "sensor_telemetry",
        "synonym_mappings"
    ], C_GREEN_BG, C_GREEN, C_GREEN),
    
    ("STAGE 04", "RETRIEVAL & CAS", [
        "Atlas Search ($search)",
        "Vector Search (kNN)",
        "2dsphere $geoNear",
        "Named $rankFusion",
        "Single-Doc OCC (__v)",
        "Change Streams (Pre/Post)"
    ], C_BG_CARD, C_BORDER, C_TEXT),
    
    ("STAGE 05", "EXECUTION", [
        "Mission Dispatched (Route confirmed)",
        "Depot Inventory Committed",
        "Route Breach Alert (Live)",
        "Supervisor Escalation",
        "Auto Closed-Loop Rematch"
    ], C_BG_CARD, C_BORDER, C_TEXT)
]

for i, (tag, title, items, bg_col, border_col, title_col) in enumerate(stages):
    x_st = 45 + i * 128
    add_card("SLIDE_6", x_st, 86, 118, 218, bg_col, border_col, 1.5 if i == 2 else 1)
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_6",
        "text": tag,
        "x": x_st + 6, "y": 92, "width": 106, "height": 14,
        "font_size": 7.5, "bold": True, "color": title_col, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_6",
        "text": title,
        "x": x_st + 6, "y": 106, "width": 106, "height": 18,
        "font_size": 11, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    add_rule("SLIDE_6", x_st + 6, 126, 106, 1, border_col)
    
    text_content = "\n\n".join([f"• {item}" for item in items])
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_6",
        "text": text_content,
        "x": x_st + 6, "y": 132, "width": 106, "height": 164,
        "font_size": 7, "color": C_BODY if i != 2 else "#166534", "font_family": SANS, "line_spacing": 120
    })

    if i < 4:
        ops.append({
            "op": "add-line", "slide": "SLIDE_6",
            "x": x_st + 119, "y": 190, "width": 8, "height": 0,
            "line_weight": 1.5, "color": C_BORDER_DARK, "end_arrow": "FILL_ARROW"
        })

# Closed Reactive Loop Banner
add_card("SLIDE_6", 45, 314, 630, 34, C_GREEN_BG, C_GREEN_BORDER, 1)
ops.append({
    "op": "add-textbox", "slide": "SLIDE_6",
    "text": "CLOSED REACTIVE LOOP",
    "x": 55, "y": 318, "width": 610, "height": 14,
    "font_size": 8, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})
ops.append({
    "op": "add-textbox", "slide": "SLIDE_6",
    "text": "Field Condition Mutates → Change Stream Fires → $geoIntersects Delta Evaluated → Mission Invalidated → Auto-Rematch",
    "x": 55, "y": 330, "width": 610, "height": 16,
    "font_size": 7.5, "bold": True, "color": C_TEXT, "font_family": SANS, "alignment": "center"
})

# Bottom Invariant Flow
ops.append({
    "op": "add-textbox", "slide": "SLIDE_6",
    "text": "INGEST  →  RETRIEVE  →  RESERVE  →  INVALIDATE  →  REMATCH",
    "x": 45, "y": 356, "width": 630, "height": 16,
    "font_size": 9.5, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
})

add_footer("SLIDE_6", "06", "CONTINUOUS OPERATIONAL DATA FLOW PIPELINE")
ops.append({
    "op": "set-notes", "slide": "SLIDE_6",
    "text": "Continuous end-to-end data flow: 5 sequential stages from Input through Processing, MongoDB Core Storage, Retrieval & CAS, and Execution, closed by a continuous reactive invalidation and rematch loop."
})

with open("reliefmesh_master_batch.json", "w", encoding="utf-8") as f:
    json.dump(ops, f, indent=2)

print(f"Total operations in batch: {len(ops)}")
