import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'diagrams')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 6. UML Class Diagram
def draw_class_diagram():
    fig, ax = plt.subplots(figsize=(11, 9), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9)
    ax.axis('off')

    classes = [
        # (x, y, w, h, name, attributes, methods)
        (0.6, 6.6, 2.2, 1.8, "Category", ["- id: int", "- name: string"], ["+ getProducts()"]),
        (3.8, 6.4, 2.6, 2.1, "Supplier", ["- id: int", "- name: string", "- phone: string", "- email: string"], ["+ getProducts()", "+ getPurchases()"]),
        (7.4, 6.4, 2.6, 2.1, "User", ["- id: int", "- name: string", "- email: string", "- role: Role"], ["+ login(dto): JWT", "+ getProfile()"]),
        (0.6, 3.2, 2.5, 2.4, "Product", ["- id: int", "- sku: string", "- name: string", "- price: decimal", "- quantity: int", "- reorderLevel: int"], ["+ isLowStock(): bool"]),
        (4.0, 3.2, 2.6, 2.3, "Purchase", ["- id: int", "- date: DateTime", "- total: decimal", "- supplierId: int", "- userId: int"], ["+ addItem()", "+ save(): Transaction"]),
        (7.4, 3.2, 2.6, 2.3, "Sale", ["- id: int", "- invoiceNo: string", "- date: DateTime", "- total: decimal", "- userId: int"], ["+ checkStock(): bool", "+ save(): Transaction", "+ generateInvoice()"]),
        (4.0, 0.4, 2.6, 1.8, "PurchaseItem", ["- id: int", "- purchaseId: int", "- productId: int", "- quantity: int", "- costPrice: decimal"], []),
        (7.4, 0.4, 2.6, 1.8, "SaleItem", ["- id: int", "- saleId: int", "- productId: int", "- quantity: int", "- price: decimal"], []),
    ]

    for x, y, w, h, name, attrs, methods in classes:
        # Outer box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc='#f8fafc', ec='#1e293b', lw=1.5)
        ax.add_patch(rect)
        # Header banner
        header = patches.Rectangle((x, y + h - 0.5), w, 0.5, fc='#e2e8f0', ec='#1e293b', lw=1.5)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.25, name, ha='center', va='center', fontweight='bold', fontsize=9.5, color='#0f172a')
        
        # Attributes
        curr_y = y + h - 0.75
        for a in attrs:
            ax.text(x + 0.1, curr_y, a, ha='left', va='center', fontsize=8, color='#334155')
            curr_y -= 0.22
        
        # Methods
        if methods:
            ax.plot([x, x + w], [curr_y + 0.05, curr_y + 0.05], color='#cbd5e1', lw=1)
            curr_y -= 0.15
            for m in methods:
                ax.text(x + 0.1, curr_y, m, ha='left', va='center', fontsize=8, color='#0369a1')
                curr_y -= 0.22

    # Draw associations
    ax.annotate('', xy=(1.85, 5.6), xytext=(1.85, 6.6), arrowprops=dict(arrowstyle="-", color='#1e293b', lw=1.2))
    ax.text(1.95, 6.1, "1..*", fontsize=7.5, fontweight='bold')
    
    # Composition diamonds for Purchase -> PurchaseItem and Sale -> SaleItem
    ax.annotate('', xy=(5.3, 2.2), xytext=(5.3, 3.2), arrowprops=dict(arrowstyle="-", color='#1e293b', lw=1.2))
    ax.plot(5.3, 3.2, 'D', ms=7, color='#0f172a') # filled diamond
    ax.text(5.4, 2.6, "1..*", fontsize=7.5, fontweight='bold')

    ax.annotate('', xy=(8.7, 2.2), xytext=(8.7, 3.2), arrowprops=dict(arrowstyle="-", color='#1e293b', lw=1.2))
    ax.plot(8.7, 3.2, 'D', ms=7, color='#0f172a') # filled diamond
    ax.text(8.8, 2.6, "1..*", fontsize=7.5, fontweight='bold')

    ax.set_title('Figure 3.6: UML Class Diagram with Attributes, Methods, and Composition Multiplicity', fontsize=11, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '06_class_diagram.png'))
    plt.close()

# 7. ER Diagram
def draw_er_diagram():
    fig, ax = plt.subplots(figsize=(11, 8.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 8.5)
    ax.axis('off')

    entities = [
        (0.6, 6.2, 2.4, 1.8, "CATEGORIES", ["category_id (PK)", "name"]),
        (4.0, 6.0, 2.6, 2.1, "SUPPLIERS", ["supplier_id (PK)", "name", "phone", "email"]),
        (7.6, 6.0, 2.6, 2.1, "USERS", ["user_id (PK)", "name", "email", "password_hash", "role"]),
        (0.6, 2.8, 2.5, 2.4, "PRODUCTS", ["product_id (PK)", "sku", "name", "price", "quantity", "reorder_level", "category_id (FK)", "supplier_id (FK)"]),
        (4.0, 2.8, 2.6, 2.3, "PURCHASES", ["purchase_id (PK)", "date", "total", "supplier_id (FK)", "user_id (FK)"]),
        (7.6, 2.8, 2.6, 2.3, "SALES", ["sale_id (PK)", "invoice_no", "date", "total", "user_id (FK)"]),
        (4.0, 0.4, 2.6, 1.8, "PURCHASE_ITEMS", ["item_id (PK)", "purchase_id (FK)", "product_id (FK)", "quantity", "cost_price"]),
        (7.6, 0.4, 2.6, 1.8, "SALE_ITEMS", ["item_id (PK)", "sale_id (FK)", "product_id (FK)", "quantity", "price"]),
    ]

    for x, y, w, h, name, fields in entities:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc='#f8fafc', ec='#0f172a', lw=1.5)
        ax.add_patch(rect)
        header = patches.Rectangle((x, y + h - 0.45), w, 0.45, fc='#e0f2fe', ec='#0f172a', lw=1.5)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.22, name, ha='center', va='center', fontweight='bold', fontsize=9, color='#0369a1')
        
        curr_y = y + h - 0.65
        for f in fields:
            is_pk = "(PK)" in f
            is_fk = "(FK)" in f
            col = "#047857" if is_pk else ("#b45309" if is_fk else "#334155")
            weight = "bold" if is_pk else "normal"
            ax.text(x + 0.1, curr_y, f, ha='left', va='center', fontsize=7.5, color=col, fontweight=weight)
            curr_y -= 0.2

    # ER Connectors
    ax.annotate('', xy=(1.8, 5.2), xytext=(1.8, 6.2), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.2))
    ax.text(1.9, 5.7, "1 : N (has)", fontsize=7.5, fontweight='bold')

    ax.annotate('', xy=(5.3, 2.2), xytext=(5.3, 2.8), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.2))
    ax.text(5.4, 2.5, "1 : N (contains)", fontsize=7.5, fontweight='bold')

    ax.annotate('', xy=(8.9, 2.2), xytext=(8.9, 2.8), arrowprops=dict(arrowstyle="->", color='#0f172a', lw=1.2))
    ax.text(9.0, 2.5, "1 : N (contains)", fontsize=7.5, fontweight='bold')

    ax.set_title('Figure 3.7: Entity Relationship Diagram (ERD) with Primary & Foreign Keys (3NF Normalized)', fontsize=11, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '07_er_diagram.png'))
    plt.close()

draw_class_diagram()
draw_er_diagram()
print("Class and ER diagrams generated!")

