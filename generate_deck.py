import json

def build_presentation_batch():
    ops = []

    # Slide 1 (ID: p) - Clean up previous test elements if any, or clear
    # Wait, in the first test we added TEST TITLE to p, let's see what elements are on p right now
    # Let's delete existing elements on p or replace them
    # Actually, we can get list of elements on p or delete the ones we know
    
    # Fonts
    SERIF = "Spectral"
    SANS = "Work Sans"
    
    # Palette
    C_TEXT = "#0F172A"       # Deep Slate / Charcoal
    C_BODY = "#475569"       # Refined Charcoal Body
    C_MUTED = "#64748B"      # Muted Label Slate
    C_LIGHT = "#94A3B8"      # Light Meta Slate
    C_BORDER = "#E2E8F0"     # Crisp Light Rule
    C_BORDER_DARK = "#CBD5E1"# Slightly deeper border
    C_BG_CARD = "#F8FAFC"    # Soft Editorial Card Surface
    C_WHITE = "#FFFFFF"      # Crisp Pure White
    
    # Accents
    C_GREEN = "#00684A"      # MongoDB Deep Forest Green
    C_GREEN_BG = "#F0FDF4"   # MongoDB Pale Mint Tint
    C_GREEN_BORDER = "#BBF7D0"
    C_ALERT = "#DC2626"      # Restrained Crimson Alert
    C_ALERT_BG = "#FEF2F2"   # Pale Crimson Tint
    C_ALERT_BORDER = "#FECACA"

    # Slide 1 Background
    ops.append({"op": "set-background", "slide": "p", "color": C_WHITE})

    # =========================================================================
    # SLIDE 1: TITLE
    # =========================================================================
    # Left Column
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "OPERATIONAL CRISIS COORDINATION ENGINE",
        "x": 45, "y": 42, "width": 290, "height": 16,
        "font_size": 9.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "RELIEFMESH",
        "x": 42, "y": 62, "width": 295, "height": 78,
        "font_size": 66, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "A Reactive Operational Core for Disaster Response",
        "x": 45, "y": 148, "width": 285, "height": 24,
        "font_size": 15, "italic": True, "color": C_MUTED, "font_family": SERIF
    })
    ops.append({
        "op": "add-shape", "slide": "p",
        "shape_type": "RECTANGLE",
        "x": 45, "y": 180, "width": 275, "height": 1,
        "background_color": C_BORDER
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "Keeping disaster-response resource allocations synchronized with fast-changing physical ground reality.",
        "x": 45, "y": 192, "width": 275, "height": 50,
        "font_size": 13, "color": C_BODY, "font_family": SANS, "line_spacing": 130
    })

    # Freshness Invariant Card
    ops.append({
        "op": "add-shape", "slide": "p",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 252, "width": 275, "height": 84,
        "background_color": C_GREEN_BG, "outline_color": C_GREEN_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "THE FRESHNESS INVARIANT",
        "x": 56, "y": 258, "width": 253, "height": 16,
        "font_size": 9, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "“No operational allocation may outlive its physical ground truth.”",
        "x": 56, "y": 276, "width": 253, "height": 38,
        "font_size": 11.5, "italic": True, "color": C_TEXT, "font_family": SERIF, "line_spacing": 125
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "Search proposes. CAS disposes. Invalidation rematches.",
        "x": 56, "y": 314, "width": 253, "height": 16,
        "font_size": 8.5, "bold": True, "color": C_MUTED, "font_family": SANS
    })

    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "ReliefMesh Systems Architecture Team · MongoDB Hackathon 2026",
        "x": 45, "y": 362, "width": 285, "height": 16,
        "font_size": 9.5, "color": C_LIGHT, "font_family": SANS
    })

    # Right Column - System Convergence Diagram
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "ARCHITECTURE CONCEPT · CONVERGENT CONTROL PLANE",
        "x": 348, "y": 42, "width": 327, "height": 16,
        "font_size": 9, "bold": True, "color": C_MUTED, "font_family": SANS, "alignment": "center"
    })

    # 4 Field Input Nodes
    sources = [
        ("Distress Audio / SMS", "Whisper + Dialects", 348),
        ("Sensor Telemetry", "River Gauges / ASP", 432),
        ("Agency Inventory", "Depot Stocks / ERPs", 516),
        ("Spatial Inundation", "Hydraulic Sidecar", 600)
    ]
    for title, sub, x_pos in sources:
        ops.append({
            "op": "add-shape", "slide": "p",
            "shape_type": "ROUND_RECTANGLE",
            "x": x_pos, "y": 66, "width": 76, "height": 48,
            "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
        })
        ops.append({
            "op": "add-textbox", "slide": "p",
            "text": title,
            "x": x_pos + 2, "y": 70, "width": 72, "height": 24,
            "font_size": 7.5, "bold": True, "color": C_TEXT, "font_family": SANS, "alignment": "center"
        })
        ops.append({
            "op": "add-textbox", "slide": "p",
            "text": sub,
            "x": x_pos + 2, "y": 94, "width": 72, "height": 16,
            "font_size": 6.5, "color": C_MUTED, "font_family": SANS, "alignment": "center"
        })
        # Arrow down toward core
        ops.append({
            "op": "add-line", "slide": "p",
            "x": x_pos + 38, "y": 116, "width": 0, "height": 18,
            "line_weight": 1.2, "color": C_BORDER_DARK, "end_arrow": "FILL_ARROW"
        })

    # Central Hero Hub: MONGODB ATLAS
    ops.append({
        "op": "add-shape", "slide": "p",
        "shape_type": "ROUND_RECTANGLE",
        "x": 365, "y": 138, "width": 292, "height": 108,
        "background_color": C_GREEN_BG, "outline_color": C_GREEN, "outline_weight": 1.5
    })
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
    ops.append({
        "op": "add-shape", "slide": "p",
        "shape_type": "RECTANGLE",
        "x": 385, "y": 184, "width": 252, "height": 1,
        "background_color": C_GREEN_BORDER
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "Living Incident Twins · Vernacular Lexical Search · Vector kNN\n2dsphere Spatial Geometries · Single-Document OCC · Change Streams",
        "x": 372, "y": 188, "width": 278, "height": 30,
        "font_size": 7.5, "color": "#166534", "font_family": SANS, "alignment": "center", "line_spacing": 130
    })
    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "The authoritative transactional state coordinator bridging awareness and logistics.",
        "x": 372, "y": 222, "width": 278, "height": 18,
        "font_size": 7, "italic": True, "color": C_MUTED, "font_family": SANS, "alignment": "center"
    })

    # Diverging Arrows from MongoDB Core down to Coordinated Output State
    out_targets = [
        ("ATOMIC ALLOCATION", "Zero phantom claims\nPredicate guard __v", 348),
        ("DYNAMIC REROUTING", "Delta invalidation\n$geoIntersects check", 454),
        ("INCIDENT TWINS", "Coherent ground truth\nCross-agency audit", 560)
    ]
    for title, desc, x_pos in out_targets:
        # Arrow down
        ops.append({
            "op": "add-line", "slide": "p",
            "x": x_pos + 52, "y": 248, "width": 0, "height": 18,
            "line_weight": 1.2, "color": C_GREEN, "end_arrow": "FILL_ARROW"
        })
        ops.append({
            "op": "add-shape", "slide": "p",
            "shape_type": "ROUND_RECTANGLE",
            "x": x_pos, "y": 270, "width": 104, "height": 68,
            "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
        })
        ops.append({
            "op": "add-textbox", "slide": "p",
            "text": title,
            "x": x_pos + 4, "y": 275, "width": 96, "height": 16,
            "font_size": 8, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
        })
        ops.append({
            "op": "add-textbox", "slide": "p",
            "text": desc,
            "x": x_pos + 4, "y": 293, "width": 96, "height": 40,
            "font_size": 7.5, "color": C_BODY, "font_family": SANS, "alignment": "center", "line_spacing": 125
        })

    ops.append({
        "op": "add-textbox", "slide": "p",
        "text": "Closed Operating Loop: Ingest → Twin → 4-R Retrieval → OCC Commit → Invalidate → Rematch",
        "x": 348, "y": 352, "width": 327, "height": 16,
        "font_size": 8, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
    })

    ops.append({"op": "set-notes", "slide": "p", "text": "ReliefMesh: Operational Crisis Coordination Engine. Submission for MongoDB Hackathon 2026. Central thesis: Keeping disaster-response allocations synchronized with changing physical reality via MongoDB Atlas as the unified operational core."})

    # =========================================================================
    # SLIDE 2: THE PROBLEM
    # =========================================================================
    ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_2"})
    ops.append({"op": "set-background", "slide": "SLIDE_2", "color": C_WHITE})

    # Section Label & Heading
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "THE PROBLEM",
        "x": 45, "y": 22, "width": 300, "height": 16,
        "font_size": 10.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "Disaster response breaks when operational state drifts from reality.",
        "x": 45, "y": 38, "width": 630, "height": 34,
        "font_size": 22, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "The failure is not lack of inbound data. It is stale, fragmented, and inconsistent operational state.",
        "x": 45, "y": 74, "width": 630, "height": 20,
        "font_size": 12, "color": C_BODY, "font_family": SANS
    })
    ops.append({
        "op": "add-shape", "slide": "SLIDE_2",
        "shape_type": "RECTANGLE",
        "x": 45, "y": 96, "width": 630, "height": 1,
        "background_color": C_BORDER
    })

    # Comparison 1: Scenario A - Phantom Allocation
    ops.append({
        "op": "add-shape", "slide": "SLIDE_2",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 106, "width": 305, "height": 150,
        "background_color": C_BG_CARD, "outline_color": C_BORDER_DARK, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "SCENARIO A · RESOURCE CONTENTION (PHANTOM ALLOCATION)",
        "x": 56, "y": 112, "width": 283, "height": 16,
        "font_size": 8.5, "bold": True, "color": C_ALERT, "font_family": SANS
    })
    # Sub-card Left: Field Reality
    ops.append({
        "op": "add-shape", "slide": "SLIDE_2",
        "shape_type": "ROUND_RECTANGLE",
        "x": 56, "y": 132, "width": 135, "height": 76,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "FIELD REALITY\nBlood Bank: 5 units available\n• Ambulance A needs: 4 units\n• Ambulance B needs: 4 units\nTotal Required: 8 units",
        "x": 62, "y": 136, "width": 123, "height": 68,
        "font_size": 8, "color": C_TEXT, "font_family": SANS, "line_spacing": 125
    })
    # Sub-card Right: Operations View
    ops.append({
        "op": "add-shape", "slide": "SLIDE_2",
        "shape_type": "ROUND_RECTANGLE",
        "x": 201, "y": 132, "width": 138, "height": 76,
        "background_color": C_ALERT_BG, "outline_color": C_ALERT_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "OPERATIONS VIEW\nBoth dispatchers see: AVAILABLE\n2 dispatch decisions\n1 scarce resource\nCONFLICT: 1 arrives empty!",
        "x": 207, "y": 136, "width": 126, "height": 68,
        "font_size": 8, "bold": True, "color": C_ALERT, "font_family": SANS, "line_spacing": 125
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "TRAGEDY: Ambulance drives 45 mins through debris for empty depot. Patient dies in transit.",
        "x": 56, "y": 216, "width": 283, "height": 32,
        "font_size": 8, "italic": True, "color": C_ALERT, "font_family": SANS
    })

    # Comparison 2: Scenario B - Blind Routing
    ops.append({
        "op": "add-shape", "slide": "SLIDE_2",
        "shape_type": "ROUND_RECTANGLE",
        "x": 370, "y": 106, "width": 305, "height": 150,
        "background_color": C_BG_CARD, "outline_color": C_BORDER_DARK, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "SCENARIO B · ENVIRONMENTAL DRIFT (BLIND ROUTING)",
        "x": 381, "y": 112, "width": 283, "height": 16,
        "font_size": 8.5, "bold": True, "color": C_ALERT, "font_family": SANS
    })
    # Sub-card Left: Road Safe
    ops.append({
        "op": "add-shape", "slide": "SLIDE_2",
        "shape_type": "ROUND_RECTANGLE",
        "x": 381, "y": 132, "width": 135, "height": 76,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "DISPATCH TIME (02:00)\nHighway 4: Marked Safe ✓\nSupply convoy launched\nStatic route cached\nZero stream reactivity",
        "x": 387, "y": 136, "width": 123, "height": 68,
        "font_size": 8, "color": C_TEXT, "font_family": SANS, "line_spacing": 125
    })
    # Sub-card Right: Flood Expands
    ops.append({
        "op": "add-shape", "slide": "SLIDE_2",
        "shape_type": "ROUND_RECTANGLE",
        "x": 526, "y": 132, "width": 138, "height": 76,
        "background_color": C_ALERT_BG, "outline_color": C_ALERT_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "MUTATION (02:15)\nLevee breaches 2.4km north\nFlood perimeter expands\nHighway submerged\nDISPATCHED ROUTE INVALID!",
        "x": 532, "y": 136, "width": 126, "height": 68,
        "font_size": 8, "bold": True, "color": C_ALERT, "font_family": SANS, "line_spacing": 125
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "TRAGEDY: Supply convoy enters flooded corridor unaware. Rescuers become casualties.",
        "x": 381, "y": 216, "width": 283, "height": 32,
        "font_size": 8, "italic": True, "color": C_ALERT, "font_family": SANS
    })

    # Exactly 3 Pain Points
    pain_points = [
        ("01", "STATE DRIFT", "Physical reality changes faster than coordination state. Point-in-time reads become deadly falsehoods without transactional controls."),
        ("02", "FRAGMENTED AWARENESS", "Different systems know different parts of the incident. Ushahidi crowdsources distress; Sahana logs warehouses — neither coordinates."),
        ("03", "STALE ALLOCATIONS", "Teams act on inventory or route information that is no longer valid. Relational lock contention deadlocks during peak emergencies.")
    ]
    col_w = 198
    for i, (num, title, desc) in enumerate(pain_points):
        x_col = 45 + i * 216
        ops.append({
            "op": "add-shape", "slide": "SLIDE_2",
            "shape_type": "ROUND_RECTANGLE",
            "x": x_col, "y": 266, "width": col_w, "height": 74,
            "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
        })
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

    # Bottom Message
    ops.append({
        "op": "add-shape", "slide": "SLIDE_2",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 348, "width": 630, "height": 24,
        "background_color": C_GREEN_BG, "outline_color": C_GREEN_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "THE CORE PROBLEM: KEEPING OPERATIONAL DECISIONS FRESH.",
        "x": 45, "y": 352, "width": 630, "height": 16,
        "font_size": 9.5, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
    })

    # Footer & Page Number
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "RELIEFMESH · THE OPERATIONAL FAILURE MODE",
        "x": 45, "y": 382, "width": 450, "height": 14,
        "font_size": 8.5, "color": C_LIGHT, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_2",
        "text": "02",
        "x": 630, "y": 382, "width": 45, "height": 14,
        "font_size": 9, "bold": True, "color": C_MUTED, "font_family": SANS, "alignment": "right"
    })
    ops.append({"op": "set-notes", "slide": "SLIDE_2", "text": "Disaster response breaks when operational state drifts from reality. The core problem is not inbound data collection; it is keeping allocation decisions fresh. Traditional disconnected architectures produce phantom allocations and blind routings."})

    # =========================================================================
    # SLIDE 3: YOUR SOLUTION
    # =========================================================================
    ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_3"})
    ops.append({"op": "set-background", "slide": "SLIDE_3", "color": C_WHITE})

    # Header
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_3",
        "text": "YOUR SOLUTION",
        "x": 45, "y": 22, "width": 300, "height": 16,
        "font_size": 10.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_3",
        "text": "ReliefMesh closes the loop between awareness, allocation and changing reality.",
        "x": 45, "y": 38, "width": 630, "height": 34,
        "font_size": 20, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    ops.append({
        "op": "add-shape", "slide": "SLIDE_3",
        "shape_type": "RECTANGLE",
        "x": 45, "y": 76, "width": 630, "height": 1,
        "background_color": C_BORDER
    })

    # Three Columns (45, 261, 477 - width 198)
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
    ops.append({
        "op": "add-shape", "slide": "SLIDE_3",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 128, "width": 198, "height": 108,
        "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_3",
        "text": "FIELD DISTRESS MESSAGE:\n“Need pediatric O-negative blood urgently”\n(Vernacular: “bachhe ke liye khoon chahiye”)",
        "x": 52, "y": 133, "width": 184, "height": 34,
        "font_size": 7.5, "italic": True, "color": C_TEXT, "font_family": SANS, "line_spacing": 120
    })
    ops.append({
        "op": "add-shape", "slide": "SLIDE_3",
        "shape_type": "ROUND_RECTANGLE",
        "x": 52, "y": 170, "width": 184, "height": 28,
        "background_color": C_WHITE, "outline_color": C_GREEN_BORDER, "outline_weight": 1
    })
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
        "text": "Understand what the request means even when field terminology differs from inventory terminology. Degrades to keyword + proximity if embeddings fail.",
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
    ops.append({
        "op": "add-shape", "slide": "SLIDE_3",
        "shape_type": "ROUND_RECTANGLE",
        "x": 261, "y": 128, "width": 198, "height": 108,
        "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_3",
        "text": "REQUEST LOCATION  ───►  NEARBY DEPOTS\nRadius Filter (50km) → OSRM Road LineString",
        "x": 268, "y": 133, "width": 184, "height": 24,
        "font_size": 7.5, "bold": True, "color": C_TEXT, "font_family": SANS
    })
    # Hazard check visual box
    ops.append({
        "op": "add-shape", "slide": "SLIDE_3",
        "shape_type": "ROUND_RECTANGLE",
        "x": 268, "y": 160, "width": 184, "height": 42,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
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
    ops.append({
        "op": "add-shape", "slide": "SLIDE_3",
        "shape_type": "ROUND_RECTANGLE",
        "x": 477, "y": 128, "width": 198, "height": 108,
        "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_3",
        "text": "DEPOT STATE: 5 UNITS AVAILABLE\nDispatcher A: 4 units → COMMIT ✓ (OCC __v: 1)\nDispatcher B: 4 units → PREDICATE FAIL ✕",
        "x": 484, "y": 133, "width": 184, "height": 34,
        "font_size": 7.5, "bold": True, "color": C_TEXT, "font_family": SANS, "line_spacing": 120
    })
    ops.append({
        "op": "add-shape", "slide": "SLIDE_3",
        "shape_type": "ROUND_RECTANGLE",
        "x": 484, "y": 170, "width": 184, "height": 28,
        "background_color": C_WHITE, "outline_color": C_GREEN_BORDER, "outline_weight": 1
    })
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

    # Bottom Quote & Moonshot Callout
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

    ops.append({
        "op": "add-shape", "slide": "SLIDE_3",
        "shape_type": "ROUND_RECTANGLE",
        "x": 370, "y": 314, "width": 305, "height": 52,
        "background_color": C_GREEN_BG, "outline_color": C_GREEN_BORDER, "outline_weight": 1
    })
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

    # Footer & Page Number
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_3",
        "text": "RELIEFMESH · DOMAIN ARCHITECTURE · THE 4-R OPERATIONAL SPINE",
        "x": 45, "y": 382, "width": 450, "height": 14,
        "font_size": 8.5, "color": C_LIGHT, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_3",
        "text": "03",
        "x": 630, "y": 382, "width": 45, "height": 14,
        "font_size": 9, "bold": True, "color": C_MUTED, "font_family": SANS, "alignment": "right"
    })
    ops.append({"op": "set-notes", "slide": "SLIDE_3", "text": "ReliefMesh closes the loop between awareness, allocation, and changing reality via 4 operational gates: Relevant (Search/Vector/Synonyms), Reachable (2dsphere route checks), Reserved (Single-document OCC), and Resilient (Delta-scoped invalidation)."})

    # =========================================================================
    # SLIDE 4: TECHNOLOGY & AI FEATURES
    # =========================================================================
    ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_4"})
    ops.append({"op": "set-background", "slide": "SLIDE_4", "color": C_WHITE})

    # Header
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "TECHNOLOGY & AI FEATURES",
        "x": 45, "y": 22, "width": 300, "height": 16,
        "font_size": 10.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "Technology Stack",
        "x": 45, "y": 38, "width": 220, "height": 34,
        "font_size": 22, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "Key Features & Unified Operational Core",
        "x": 285, "y": 38, "width": 390, "height": 34,
        "font_size": 22, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "RECTANGLE",
        "x": 45, "y": 76, "width": 630, "height": 1,
        "background_color": C_BORDER
    })

    # Left Column: Tech Stack & Architecture Trade-off
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 86, "width": 220, "height": 136,
        "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
    })
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
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 230, "width": 220, "height": 136,
        "background_color": C_WHITE, "outline_color": C_BORDER_DARK, "outline_weight": 1
    })
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

    # Right Column: HERO VISUAL - Central Core & 6 Surrounding Modules
    # Central Hub
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 412, "y": 178, "width": 140, "height": 60,
        "background_color": C_GREEN_BG, "outline_color": C_GREEN, "outline_weight": 2
    })
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

    # 6 Modules around it:
    # 01 Document State (Top Left)
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 285, "y": 86, "width": 120, "height": 56,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "01 · DOCUMENT STATE",
        "x": 290, "y": 90, "width": 110, "height": 14,
        "font_size": 7.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "Living Incidents, inventory, active missions & dynamic hazard bounds.",
        "x": 290, "y": 104, "width": 110, "height": 34,
        "font_size": 6.8, "color": C_BODY, "font_family": SANS, "line_spacing": 120
    })

    # 02 Search (Top Center)
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 422, "y": 86, "width": 120, "height": 56,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "02 · ATLAS SEARCH",
        "x": 427, "y": 90, "width": 110, "height": 14,
        "font_size": 7.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "Lucene tokenization + dynamic synonym mappings (disaster dialects).",
        "x": 427, "y": 104, "width": 110, "height": 34,
        "font_size": 6.8, "color": C_BODY, "font_family": SANS, "line_spacing": 120
    })

    # 03 Vector Search (Top Right)
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 555, "y": 86, "width": 120, "height": 56,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "03 · VECTOR SEARCH",
        "x": 560, "y": 90, "width": 110, "height": 14,
        "font_size": 7.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "1536-dim cosine similarity for unstructured distress semantic intent.",
        "x": 560, "y": 104, "width": 110, "height": 34,
        "font_size": 6.8, "color": C_BODY, "font_family": SANS, "line_spacing": 120
    })

    # ASP Telemetry Sub-node (Mid Left)
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 285, "y": 178, "width": 110, "height": 60,
        "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
    })
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

    # 04 Geospatial (Bottom Left)
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 285, "y": 268, "width": 120, "height": 56,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "04 · 2DSPHERE GEO",
        "x": 290, "y": 272, "width": 110, "height": 14,
        "font_size": 7.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "Spherical indexing & $geoIntersects route collision detection.",
        "x": 290, "y": 286, "width": 110, "height": 34,
        "font_size": 6.8, "color": C_BODY, "font_family": SANS, "line_spacing": 120
    })

    # 05 Allocation (Bottom Center)
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 422, "y": 268, "width": 120, "height": 56,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "05 · OCC ALLOCATION",
        "x": 427, "y": 272, "width": 110, "height": 14,
        "font_size": 7.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "Single-document OCC (__v) + Multi-doc ACID only where required.",
        "x": 427, "y": 286, "width": 110, "height": 34,
        "font_size": 6.8, "color": C_BODY, "font_family": SANS, "line_spacing": 120
    })

    # 06 Reactivity (Bottom Right)
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 555, "y": 268, "width": 120, "height": 56,
        "background_color": C_WHITE, "outline_color": C_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "06 · CHANGE STREAMS",
        "x": 560, "y": 272, "width": 110, "height": 14,
        "font_size": 7.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "Pre/Post-images for delta-scoped dynamic invalidation & rerouting.",
        "x": 560, "y": 286, "width": 110, "height": 34,
        "font_size": 6.8, "color": C_BODY, "font_family": SANS, "line_spacing": 120
    })

    # Connecting Lines from Center Hub
    conn_coords = [
        (345, 142), # To 01
        (472, 142), # To 02
        (595, 142), # To 03
        (345, 268), # To 04
        (472, 268), # To 05
        (595, 268)  # To 06
    ]
    for cx, cy in conn_coords:
        ops.append({
            "op": "add-line", "slide": "SLIDE_4",
            "x": cx, "y": cy, "width": 0, "height": (178 - cy) if cy < 178 else (cy - 238),
            "line_weight": 1, "color": C_BORDER_DARK
        })

    # Summary Line
    ops.append({
        "op": "add-shape", "slide": "SLIDE_4",
        "shape_type": "ROUND_RECTANGLE",
        "x": 285, "y": 342, "width": 390, "height": 24,
        "background_color": C_GREEN_BG, "outline_color": C_GREEN_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "MongoDB connects retrieval, spatial safety, allocation and reactivity in one operational plane.",
        "x": 285, "y": 346, "width": 390, "height": 16,
        "font_size": 8, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
    })

    # Footer & Page Number
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "RELIEFMESH · TECHNOLOGY STACK & MONGODB ATLAS CORE",
        "x": 45, "y": 382, "width": 450, "height": 14,
        "font_size": 8.5, "color": C_LIGHT, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_4",
        "text": "04",
        "x": 630, "y": 382, "width": 45, "height": 14,
        "font_size": 9, "bold": True, "color": C_MUTED, "font_family": SANS, "alignment": "right"
    })
    ops.append({"op": "set-notes", "slide": "SLIDE_4", "text": "MongoDB Atlas serves as the unified operational control plane, integrating Document State, Atlas Search, Vector Search, Geospatial Indexing, OCC Allocation, and Change Streams. Replaces 5 independent distributed components with one unified engine."})

    # =========================================================================
    # SLIDE 5: HOW IT WORKS
    # =========================================================================
    ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_5"})
    ops.append({"op": "set-background", "slide": "SLIDE_5", "color": C_WHITE})

    # Header
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_5",
        "text": "HOW IT WORKS",
        "x": 45, "y": 22, "width": 300, "height": 16,
        "font_size": 10.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_5",
        "text": "One request travels through four operational gates.",
        "x": 45, "y": 38, "width": 630, "height": 34,
        "font_size": 22, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    ops.append({
        "op": "add-shape", "slide": "SLIDE_5",
        "shape_type": "RECTANGLE",
        "x": 45, "y": 76, "width": 630, "height": 1,
        "background_color": C_BORDER
    })

    # 4-Part Grid (2x2)
    # Part 1: RELEVANT (Top Left)
    ops.append({
        "op": "add-shape", "slide": "SLIDE_5",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 86, "width": 305, "height": 128,
        "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
    })
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
    ops.append({
        "op": "add-shape", "slide": "SLIDE_5",
        "shape_type": "ROUND_RECTANGLE",
        "x": 370, "y": 86, "width": 305, "height": 128,
        "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
    })
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
    ops.append({
        "op": "add-shape", "slide": "SLIDE_5",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 222, "width": 305, "height": 128,
        "background_color": C_BG_CARD, "outline_color": C_BORDER, "outline_weight": 1
    })
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
    ops.append({
        "op": "add-shape", "slide": "SLIDE_5",
        "shape_type": "ROUND_RECTANGLE",
        "x": 370, "y": 222, "width": 305, "height": 128,
        "background_color": C_ALERT_BG, "outline_color": C_ALERT_BORDER, "outline_weight": 1.5
    })
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
    ops.append({
        "op": "add-shape", "slide": "SLIDE_5",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 356, "width": 630, "height": 22,
        "background_color": C_GREEN_BG, "outline_color": C_GREEN_BORDER, "outline_weight": 1
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_5",
        "text": "RELEVANT  →  REACHABLE  →  RESERVED  →  RESILIENT",
        "x": 45, "y": 359, "width": 630, "height": 16,
        "font_size": 9, "bold": True, "color": C_GREEN, "font_family": SANS, "alignment": "center"
    })

    # Footer & Page Number
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_5",
        "text": "RELIEFMESH · THE 4-GATE OPERATIONAL WORKFLOW",
        "x": 45, "y": 382, "width": 450, "height": 14,
        "font_size": 8.5, "color": C_LIGHT, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_5",
        "text": "05",
        "x": 630, "y": 382, "width": 45, "height": 14,
        "font_size": 9, "bold": True, "color": C_MUTED, "font_family": SANS, "alignment": "right"
    })
    ops.append({"op": "set-notes", "slide": "SLIDE_5", "text": "Every relief request passes through 4 operational gates: Relevant (vernacular synonyms and rankFusion), Reachable (OSRM route checked against 2dsphere hazard polygons), Reserved (single-document OCC with version guard), and Resilient (pre/post-image delta-scoped invalidation and dynamic reroute)."})

    # =========================================================================
    # SLIDE 6: DATA FLOW
    # =========================================================================
    ops.append({"op": "add-slide", "layout": "BLANK", "id": "SLIDE_6"})
    ops.append({"op": "set-background", "slide": "SLIDE_6", "color": C_WHITE})

    # Header
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_6",
        "text": "DATA FLOW",
        "x": 45, "y": 22, "width": 300, "height": 16,
        "font_size": 10.5, "bold": True, "color": C_GREEN, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_6",
        "text": "From field signal to a continuously updated operational state.",
        "x": 45, "y": 38, "width": 630, "height": 34,
        "font_size": 22, "bold": True, "color": C_TEXT, "font_family": SERIF
    })
    ops.append({
        "op": "add-shape", "slide": "SLIDE_6",
        "shape_type": "RECTANGLE",
        "x": 45, "y": 76, "width": 630, "height": 1,
        "background_color": C_BORDER
    })

    # 5 Sequential Stages (Horizontal)
    # Positions: 45, 175, 305, 435, 565 | Width: 114 each | Gap: 16
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
        ops.append({
            "op": "add-shape", "slide": "SLIDE_6",
            "shape_type": "ROUND_RECTANGLE",
            "x": x_st, "y": 86, "width": 118, "height": 218,
            "background_color": bg_col, "outline_color": border_col, "outline_weight": 1.5 if i == 2 else 1
        })
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
        ops.append({
            "op": "add-shape", "slide": "SLIDE_6",
            "shape_type": "RECTANGLE",
            "x": x_st + 6, "y": 126, "width": 106, "height": 1,
            "background_color": border_col
        })
        
        text_content = "\n\n".join([f"• {item}" for item in items])
        ops.append({
            "op": "add-textbox", "slide": "SLIDE_6",
            "text": text_content,
            "x": x_st + 6, "y": 132, "width": 106, "height": 164,
            "font_size": 7, "color": C_BODY if i != 2 else "#166534", "font_family": SANS, "line_spacing": 120
        })

        # Connecting Arrows between stages
        if i < 4:
            ops.append({
                "op": "add-line", "slide": "SLIDE_6",
                "x": x_st + 119, "y": 190, "width": 8, "height": 0,
                "line_weight": 1.5, "color": C_BORDER_DARK, "end_arrow": "FILL_ARROW"
            })

    # Closed Reactive Loop Banner
    ops.append({
        "op": "add-shape", "slide": "SLIDE_6",
        "shape_type": "ROUND_RECTANGLE",
        "x": 45, "y": 314, "width": 630, "height": 34,
        "background_color": C_GREEN_BG, "outline_color": C_GREEN_BORDER, "outline_weight": 1
    })
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

    # Footer & Page Number
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_6",
        "text": "RELIEFMESH · CONTINUOUS OPERATIONAL DATA FLOW PIPELINE",
        "x": 45, "y": 382, "width": 450, "height": 14,
        "font_size": 8.5, "color": C_LIGHT, "font_family": SANS
    })
    ops.append({
        "op": "add-textbox", "slide": "SLIDE_6",
        "text": "06",
        "x": 630, "y": 382, "width": 45, "height": 14,
        "font_size": 9, "bold": True, "color": C_MUTED, "font_family": SANS, "alignment": "right"
    })
    ops.append({"op": "set-notes", "slide": "SLIDE_6", "text": "Continuous end-to-end data flow: 5 sequential stages from Input through Processing, MongoDB Core Storage, Retrieval & CAS, and Execution, closed by a continuous reactive invalidation and rematch loop."})

    return ops

if __name__ == "__main__":
    batch = build_presentation_batch()
    with open("reliefmesh_master_batch.json", "w", encoding="utf-8") as f:
        json.dump(batch, f, indent=2)
    print(f"Generated {len(batch)} operations.")
