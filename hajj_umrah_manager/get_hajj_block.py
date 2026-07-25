import frappe

def run():
    blocks = frappe.get_all("Custom HTML Block", fields=["name"])
    print(f"TOTAL BLOCKS: {len(blocks)}")
    for b in blocks:
        doc = frappe.get_doc("Custom HTML Block", b.name)
        print(f"=== BLOCK NAME: '{doc.name}' ===")
        print("HTML LENGTH:", len(doc.html or ""))
        print("STYLE LENGTH:", len(doc.style or ""))
        print("SCRIPT LENGTH:", len(doc.script or ""))
        print("HTML PREVIEW:")
        print((doc.html or "")[:300])
        print("-----------------------------------")
