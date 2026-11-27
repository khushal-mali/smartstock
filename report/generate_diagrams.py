import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'diagrams')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global styles
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# 1. Gantt Chart
def draw_gantt():
    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
    tasks = [
        ("A. Requirement gathering", 0, 2, "2d"),
        ("B. Analysis and design", 2, 3, "3d"),
        ("C. Database setup (Prisma)", 5, 1, "1d"),
        ("D. Backend API development", 6, 5, "5d"),
        ("E. Frontend development", 11, 5, "5d"),
        ("F. Integration and testing", 16, 4, "4d"),
        ("G. Deployment and documentation", 20, 3, "3d"),
    ]
    y_pos = range(len(tasks)-1, -1, -1)
    
    for i, (name, start, dur, label) in enumerate(tasks):
        y = len(tasks) - 1 - i
        ax.barh(y, dur, left=start, height=0.55, align='center', color='#b91c1c', edgecolor='#7f1d1d', linewidth=1.5)
        ax.text(start + dur/2, y, label, ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([t[0] for t in reversed(tasks)], fontsize=10, fontweight='bold', color='#1e293b')
    ax.set_xlabel('Project Timeline (Days 1 to 23: Nov 5 to Nov 27, 2026)', fontsize=10, fontweight='bold', labelpad=10)
    ax.set_xlim(-0.5, 24)
    ax.set_xticks(range(0, 25, 2))
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    ax.set_title('Figure 3.1: SmartStock Gantt Chart (Sequential Critical Path)', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '01_gantt_chart.png'))
    plt.close()

# 2. PERT Chart
def draw_pert():
    fig, ax = plt.subplots(figsize=(12, 3.5), dpi=300)
    ax.set_xlim(0, 24)
    ax.set_ylim(0, 6)
    ax.axis('off')

    nodes = [
        (1, 1.5, 3, "1\n0 | 0"),
        (2, 4.5, 3, "2\n2 | 2"),
        (3, 7.5, 3, "3\n5 | 5"),
        (4, 10.5, 3, "4\n6 | 6"),
        (5, 13.5, 3, "5\n11 | 11"),
        (6, 16.5, 3, "6\n16 | 16"),
        (7, 19.5, 3, "7\n20 | 20"),
        (8, 22.5, 3, "8\n23 | 23"),
    ]
    edges = [
        (1, 2, "A (2d)"),
        (2, 3, "B (3d)"),
        (3, 4, "C (1d)"),
        (4, 5, "D (5d)"),
        (5, 6, "E (5d)"),
        (6, 7, "F (4d)"),
        (7, 8, "G (3d)"),
    ]

    for start_id, end_id, label in edges:
        x1 = nodes[start_id-1][1]
        y1 = nodes[start_id-1][2]
        x2 = nodes[end_id-1][1]
        y2 = nodes[end_id-1][2]
        ax.annotate('', xy=(x2-0.8, y2), xytext=(x1+0.8, y1),
                    arrowprops=dict(arrowstyle="-|>", color='#b91c1c', lw=2.5, mutation_scale=15))
        ax.text((x1+x2)/2, y1 + 0.45, label, ha='center', va='center', color='#b91c1c', fontweight='bold', fontsize=9)

    for nid, x, y, txt in nodes:
        circle = plt.Circle((x, y), 0.8, color='#fef3c7', ec='#1e293b', lw=2, zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, txt, ha='center', va='center', fontsize=9, fontweight='bold', color='#0f172a', zorder=4)

    ax.set_title('Figure 3.2: SmartStock PERT Network Chart (Earliest | Latest Event Times)', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '02_pert_chart.png'))
    plt.close()

# 3. Use Case Diagram
def draw_use_case():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Boundary Box
    rect = patches.FancyBboxPatch((3.2, 0.5), 5.5, 8.8, boxstyle="round,pad=0.2", fc="#f8fafc", ec="#334155", lw=2)
    ax.add_patch(rect)
    ax.text(5.95, 9.0, 'SmartStock System Boundary', ha='center', fontweight='bold', fontsize=12, color='#0f172a')

    # Use Cases
    cases = [
        (5.95, 8.2, "UC1: User Authentication & JWT Login"),
        (5.95, 7.1, "UC2: Manage Users & Roles (Admin Only)"),
        (5.95, 6.0, "UC3: Manage Products, SKU & Categories"),
        (5.95, 4.9, "UC4: Manage Suppliers & Directory"),
        (5.95, 3.8, "UC5: Record Purchases & Auto-Restock"),
        (5.95, 2.7, "UC6: Sales Billing & Stock Check (POS)"),
        (5.95, 1.6, "UC7: Generate Invoices & Low-Stock Reports"),
    ]

    for x, y, label in cases:
        ellipse = patches.Ellipse((x, y), 4.6, 0.75, fc='#dbeafe', ec='#1d4ed8', lw=1.5, zorder=3)
        ax.add_patch(ellipse)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold', color='#1e3a8a', zorder=4)

    # Actors
    def draw_actor(x, y, name):
        ax.plot(x, y+0.4, 'o', ms=12, color='#0f172a') # head
        ax.plot([x, x], [y+0.25, y-0.3], '-', color='#0f172a', lw=2) # body
        ax.plot([x-0.35, x+0.35], [y+0.05, y+0.05], '-', color='#0f172a', lw=2) # arms
        ax.plot([x, x-0.3], [y-0.3, y-0.75], '-', color='#0f172a', lw=2) # leg L
        ax.plot([x, x+0.3], [y-0.3, y-0.75], '-', color='#0f172a', lw=2) # leg R
        ax.text(x, y-1.0, name, ha='center', fontweight='bold', fontsize=10, color='#0f172a')

    draw_actor(1.2, 7.2, "Admin")
    draw_actor(1.2, 2.8, "Staff")

    # Lines from Admin
    for idx in [0, 1, 2, 3, 4, 5, 6]:
        ax.plot([1.5, 3.65], [7.2, cases[idx][1]], color='#2563eb', lw=1.3, linestyle='-')

    # Lines from Staff (No UC2)
    for idx in [0, 2, 3, 4, 5, 6]:
        ax.plot([1.5, 3.65], [2.8, cases[idx][1]], color='#059669', lw=1.3, linestyle='-')

    ax.set_title('Figure 3.3: Use Case Diagram for SmartStock', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '03_use_case_diagram.png'))
    plt.close()

# 4. Activity Diagram (Sales & Billing Flow)
def draw_activity():
    fig, ax = plt.subplots(figsize=(8, 10), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Start node
    start = plt.Circle((5, 11.2), 0.25, color='#0f172a', zorder=3)
    ax.add_patch(start)

    steps = [
        (5, 10.0, "Select Products & Input Quantities in POS"),
        (5, 8.7, "Validate Input & Request Stock Availability"),
    ]
    for x, y, text in steps:
        box = patches.FancyBboxPatch((x-2.8, y-0.45), 5.6, 0.9, boxstyle="round,pad=0.2", fc='#f1f5f9', ec='#334155', lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color='#0f172a')

    # Decision Diamond (Stock Check)
    diamond = patches.Polygon([[5, 7.6], [6.2, 6.9], [5, 6.2], [3.8, 6.9]], closed=True, fc='#fef3c7', ec='#d97706', lw=1.8)
    ax.add_patch(diamond)
    ax.text(5, 6.9, "Sufficient\nStock?", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#92400e')

    # Rejection Box
    rej_box = patches.FancyBboxPatch((0.5, 6.45), 2.4, 0.9, boxstyle="round,pad=0.2", fc='#fee2e2', ec='#ef4444', lw=1.5)
    ax.add_patch(rej_box)
    ax.text(1.7, 6.9, "Reject Sale\n(400 Bad Request)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#991b1b')

    # Success Flow steps
    steps2 = [
        (5, 5.0, "Initiate Atomic Database Transaction (ACID)"),
        (5, 3.8, "Create Sale & SaleItems Records"),
        (5, 2.6, "Decrement Inventory Product Stock Automatically"),
        (5, 1.4, "Commit Transaction & Generate Tax Invoice"),
    ]
    for x, y, text in steps2:
        box = patches.FancyBboxPatch((x-2.8, y-0.45), 5.6, 0.9, boxstyle="round,pad=0.2", fc='#ecfdf5', ec='#059669', lw=1.5)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, fontweight='bold', color='#065f46')

    # End Node
    end_outer = plt.Circle((5, 0.35), 0.3, color='#0f172a', fill=False, lw=2)
    end_inner = plt.Circle((5, 0.35), 0.2, color='#0f172a')
    ax.add_patch(end_outer)
    ax.add_patch(end_inner)

    # Connectors
    arrows = [
        ((5, 10.95), (5, 10.45)),
        ((5, 9.55), (5, 9.15)),
        ((5, 8.25), (5, 7.6)),
        ((5, 6.2), (5, 5.45)),
        ((5, 4.55), (5, 4.25)),
        ((5, 3.35), (5, 3.05)),
        ((5, 2.15), (5, 1.85)),
        ((5, 0.95), (5, 0.65)),
    ]
    for p1, p2 in arrows:
        ax.annotate('', xy=p2, xytext=p1, arrowprops=dict(arrowstyle="-|>", color='#1e293b', lw=1.5, mutation_scale=12))

    # Decision branches
    ax.annotate('', xy=(2.9, 6.9), xytext=(3.8, 6.9), arrowprops=dict(arrowstyle="-|>", color='#dc2626', lw=1.5, mutation_scale=12))
    ax.text(3.35, 7.15, "No", ha='center', color='#dc2626', fontweight='bold', fontsize=8.5)
    ax.text(5.3, 5.85, "Yes", ha='left', color='#059669', fontweight='bold', fontsize=8.5)

    ax.set_title('Figure 3.4: Activity Diagram – Sales & Stock Deduction Process', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '04_activity_diagram.png'))
    plt.close()

# 5. Sequence Diagram (Point of Sale Transaction)
def draw_sequence():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    lifelines = [
        (1.5, "Staff User\n(Client/Browser)"),
        (4.2, "Next.js UI\n(Frontend)"),
        (6.8, "NestJS API\n(SalesService)"),
        (9.2, "PostgreSQL DB\n(Prisma ORM)"),
    ]

    for x, label in lifelines:
        box = patches.FancyBboxPatch((x-1.0, 9.0), 2.0, 0.75, boxstyle="round,pad=0.1", fc='#e2e8f0', ec='#334155', lw=1.5)
        ax.add_patch(box)
        ax.text(x, 9.35, label, ha='center', va='center', fontsize=9, fontweight='bold', color='#0f172a')
        ax.plot([x, x], [9.0, 0.8], 'k--', lw=1, alpha=0.6)

    calls = [
        (1.5, 4.2, 8.4, "1: Click 'Generate Bill'", False),
        (4.2, 6.8, 7.6, "2: POST /api/sales (itemIds, quantities)", False),
        (6.8, 9.2, 6.8, "3: Query stock levels (SELECT Product)", False),
        (9.2, 6.8, 6.0, "4: Return available stock counts", True),
        (6.8, 6.8, 5.2, "5: Verify: requested <= available", False),
        (6.8, 9.2, 4.4, "6: BEGIN TRANSACTION (Sale, SaleItems, Stock--)", False),
        (9.2, 6.8, 3.6, "7: COMMIT & return invoiceNo", True),
        (6.8, 4.2, 2.8, "8: HTTP 201 Created (Sale Data)", True),
        (4.2, 1.5, 2.0, "9: Display Printable Tax Invoice Modal", False),
    ]

    for x1, x2, y, txt, is_return in calls:
        if x1 == x2: # self call
            ax.annotate('', xy=(x1, y-0.3), xytext=(x1+0.7, y-0.1),
                        arrowprops=dict(arrowstyle="-|>", color='#2563eb', lw=1.3, mutation_scale=10))
            ax.plot([x1, x1+0.7], [y+0.1, y-0.1], color='#2563eb', lw=1.3)
            ax.text(x1+0.8, y, txt, ha='left', va='center', fontsize=8, fontweight='bold', color='#1e3a8a')
        else:
            style = "--" if is_return else "-"
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle="-|>", linestyle=style, color='#0f172a', lw=1.3, mutation_scale=10))
            ax.text((x1+x2)/2, y+0.2, txt, ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1e293b')

    ax.set_title('Figure 3.5: Sequence Diagram – Atomic POS Sales Transaction', fontsize=12, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '05_sequence_diagram.png'))
    plt.close()

draw_gantt()
draw_pert()
draw_use_case()
draw_activity()
draw_sequence()
print("All system diagrams generated successfully in:", OUTPUT_DIR)

