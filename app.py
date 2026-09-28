"""
My Invoice App
==============
Streamlit application to enter customer & product details,
calculate totals, and generate a simple printable invoice.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List

import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="My Invoice App",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
def init_state() -> None:
    defaults: Dict[str, Any] = {
        "items": [],  # list of dicts: name, qty, unit_price
        "invoice_number": f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "invoice_date": date.today(),
        "company_name": "My Company",
        "company_address": "123 Business Street\nCity, State 00000",
        "company_email": "billing@mycompany.com",
        "company_phone": "+1 (555) 000-0000",
        "customer_name": "",
        "customer_address": "",
        "customer_email": "",
        "customer_phone": "",
        "tax_rate": 0.0,  # percent
        "notes": "Thank you for your business!",
        "currency": "₹",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def add_item(name: str, qty: float, unit_price: float) -> None:
    if not name.strip():
        st.warning("Product name is required.")
        return
    if qty <= 0:
        st.warning("Quantity must be greater than 0.")
        return
    if unit_price < 0:
        st.warning("Unit price cannot be negative.")
        return
    st.session_state.items.append(
        {
            "name": name.strip(),
            "qty": float(qty),
            "unit_price": float(unit_price),
            "amount": round(float(qty) * float(unit_price), 2),
        }
    )


def remove_item(index: int) -> None:
    if 0 <= index < len(st.session_state.items):
        st.session_state.items.pop(index)


def calc_totals() -> Dict[str, float]:
    subtotal = sum(i["amount"] for i in st.session_state.items)
    tax = round(subtotal * (st.session_state.tax_rate / 100.0), 2)
    total = round(subtotal + tax, 2)
    return {"subtotal": subtotal, "tax": tax, "total": total}


def money(amount: float) -> str:
    cur = st.session_state.currency
    return f"{cur}{amount:,.2f}"


# ---------------------------------------------------------------------------
# Invoice HTML (for display + download)
# ---------------------------------------------------------------------------
def build_invoice_html() -> str:
    items = st.session_state.items
    totals = calc_totals()
    inv_no = st.session_state.invoice_number
    inv_date = st.session_state.invoice_date
    if hasattr(inv_date, "strftime"):
        inv_date_str = inv_date.strftime("%d %b %Y")
    else:
        inv_date_str = str(inv_date)

    rows = ""
    for i, it in enumerate(items, 1):
        rows += f"""
        <tr>
            <td style="padding:8px;border-bottom:1px solid #eee;">{i}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;">{it['name']}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;text-align:right;">{it['qty']:g}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;text-align:right;">{money(it['unit_price'])}</td>
            <td style="padding:8px;border-bottom:1px solid #eee;text-align:right;">{money(it['amount'])}</td>
        </tr>
        """

    if not rows:
        rows = '<tr><td colspan="5" style="padding:16px;text-align:center;color:#888;">No items</td></tr>'

    notes = st.session_state.notes or ""
    notes_html = f'<p style="margin-top:24px;color:#555;font-size:13px;"><strong>Notes:</strong> {notes}</p>' if notes else ""

    html = f"""
    <div style="font-family:Segoe UI,Arial,sans-serif;max-width:800px;margin:0 auto;color:#222;background:#fff;padding:24px;border:1px solid #e0e0e0;border-radius:8px;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
            <div>
                <h1 style="margin:0;font-size:28px;color:#1a73e8;">INVOICE</h1>
                <p style="margin:4px 0 0;color:#666;">#{inv_no}</p>
                <p style="margin:0;color:#666;">Date: {inv_date_str}</p>
            </div>
            <div style="text-align:right;">
                <strong style="font-size:16px;">{st.session_state.company_name}</strong><br/>
                <span style="color:#555;white-space:pre-line;font-size:13px;">{st.session_state.company_address}</span><br/>
                <span style="color:#555;font-size:13px;">{st.session_state.company_email}</span><br/>
                <span style="color:#555;font-size:13px;">{st.session_state.company_phone}</span>
            </div>
        </div>

        <hr style="border:none;border-top:2px solid #1a73e8;margin:20px 0;"/>

        <div style="margin-bottom:20px;">
            <strong style="color:#1a73e8;">Bill To</strong><br/>
            <strong>{st.session_state.customer_name or "—"}</strong><br/>
            <span style="color:#555;white-space:pre-line;font-size:13px;">{st.session_state.customer_address or ""}</span><br/>
            <span style="color:#555;font-size:13px;">{st.session_state.customer_email or ""}</span><br/>
            <span style="color:#555;font-size:13px;">{st.session_state.customer_phone or ""}</span>
        </div>

        <table style="width:100%;border-collapse:collapse;font-size:14px;">
            <thead>
                <tr style="background:#f5f8ff;">
                    <th style="padding:10px 8px;text-align:left;border-bottom:2px solid #1a73e8;">#</th>
                    <th style="padding:10px 8px;text-align:left;border-bottom:2px solid #1a73e8;">Product / Service</th>
                    <th style="padding:10px 8px;text-align:right;border-bottom:2px solid #1a73e8;">Qty</th>
                    <th style="padding:10px 8px;text-align:right;border-bottom:2px solid #1a73e8;">Unit Price</th>
                    <th style="padding:10px 8px;text-align:right;border-bottom:2px solid #1a73e8;">Amount</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>

        <div style="margin-top:20px;text-align:right;font-size:14px;">
            <div style="margin:4px 0;">Subtotal: <strong>{money(totals['subtotal'])}</strong></div>
            <div style="margin:4px 0;">Tax ({st.session_state.tax_rate:g}%): <strong>{money(totals['tax'])}</strong></div>
            <div style="margin:12px 0 0;font-size:18px;color:#1a73e8;">
                Total: <strong>{money(totals['total'])}</strong>
            </div>
        </div>

        {notes_html}

        <p style="margin-top:32px;text-align:center;color:#999;font-size:12px;">
            Generated with My Invoice App · {datetime.now().strftime("%Y-%m-%d %H:%M")}
        </p>
    </div>
    """
    return html


def build_invoice_text() -> str:
    totals = calc_totals()
    inv_date = st.session_state.invoice_date
    inv_date_str = inv_date.strftime("%d %b %Y") if hasattr(inv_date, "strftime") else str(inv_date)
    lines = [
        "=" * 48,
        "INVOICE",
        f"No: {st.session_state.invoice_number}",
        f"Date: {inv_date_str}",
        "=" * 48,
        "",
        f"From: {st.session_state.company_name}",
        st.session_state.company_address,
        st.session_state.company_email,
        st.session_state.company_phone,
        "",
        f"Bill To: {st.session_state.customer_name}",
        st.session_state.customer_address,
        st.session_state.customer_email,
        st.session_state.customer_phone,
        "",
        "-" * 48,
        f"{'#':<4}{'Product':<22}{'Qty':>6}{'Price':>8}{'Amount':>8}",
        "-" * 48,
    ]
    for i, it in enumerate(st.session_state.items, 1):
        name = (it["name"][:20] + "..") if len(it["name"]) > 22 else it["name"]
        lines.append(
            f"{i:<4}{name:<22}{it['qty']:>6g}{it['unit_price']:>8.2f}{it['amount']:>8.2f}"
        )
    lines += [
        "-" * 48,
        f"{'Subtotal:':>40} {money(totals['subtotal'])}",
        f"{'Tax:':>40} {money(totals['tax'])}",
        f"{'TOTAL:':>40} {money(totals['total'])}",
        "",
        f"Notes: {st.session_state.notes}",
        "=" * 48,
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main UI
# ---------------------------------------------------------------------------
def main() -> None:
    init_state()

    st.title("🧾 My Invoice App")
    st.caption("Enter customer & product details → calculate total → generate invoice")

    # ----- Sidebar: company settings -----
    with st.sidebar:
        st.header("Company / Seller")
        st.session_state.company_name = st.text_input("Company name", st.session_state.company_name)
        st.session_state.company_address = st.text_area(
            "Address", st.session_state.company_address, height=80
        )
        st.session_state.company_email = st.text_input("Email", st.session_state.company_email)
        st.session_state.company_phone = st.text_input("Phone", st.session_state.company_phone)
        st.session_state.currency = st.selectbox(
            "Currency symbol",
            options=["₹", "$", "€", "£", "¥"],
            index=["₹", "$", "€", "£", "¥"].index(st.session_state.currency)
            if st.session_state.currency in ["₹", "$", "€", "£", "¥"]
            else 0,
        )
        st.session_state.tax_rate = st.number_input(
            "Tax rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.tax_rate),
            step=0.5,
        )
        st.markdown("---")
        if st.button("🔄 New invoice (clear items)", use_container_width=True):
            st.session_state.items = []
            st.session_state.invoice_number = f"INV-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            st.session_state.invoice_date = date.today()
            st.rerun()

    # ----- Customer + invoice meta -----
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Customer details")
        st.session_state.customer_name = st.text_input(
            "Customer name *", st.session_state.customer_name
        )
        st.session_state.customer_address = st.text_area(
            "Customer address", st.session_state.customer_address, height=80
        )
        st.session_state.customer_email = st.text_input(
            "Customer email", st.session_state.customer_email
        )
        st.session_state.customer_phone = st.text_input(
            "Customer phone", st.session_state.customer_phone
        )
    with col2:
        st.subheader("Invoice details")
        st.session_state.invoice_number = st.text_input(
            "Invoice number", st.session_state.invoice_number
        )
        st.session_state.invoice_date = st.date_input(
            "Invoice date", st.session_state.invoice_date
        )
        st.session_state.notes = st.text_area(
            "Notes / payment terms", st.session_state.notes, height=80
        )

    st.markdown("---")
    st.subheader("Products / Services")

    # Add item form
    with st.form("add_item_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        with c1:
            pname = st.text_input("Product / service name")
        with c2:
            pqty = st.number_input("Qty", min_value=0.01, value=1.0, step=1.0)
        with c3:
            pprice = st.number_input("Unit price", min_value=0.0, value=0.0, step=1.0)
        with c4:
            st.write("")  # spacer
            st.write("")
            submitted = st.form_submit_button("➕ Add item", use_container_width=True)
        if submitted:
            add_item(pname, pqty, pprice)
            st.rerun()

    # Items table
    if st.session_state.items:
        df = pd.DataFrame(st.session_state.items)
        df_display = df.copy()
        df_display.index = range(1, len(df_display) + 1)
        df_display = df_display.rename(
            columns={
                "name": "Product / Service",
                "qty": "Qty",
                "unit_price": "Unit Price",
                "amount": "Amount",
            }
        )
        st.dataframe(df_display, use_container_width=True)

        # Remove controls
        st.caption("Remove an item:")
        rm_cols = st.columns(min(len(st.session_state.items), 6))
        for idx, it in enumerate(st.session_state.items):
            col = rm_cols[idx % len(rm_cols)]
            with col:
                if st.button(f"🗑 {idx+1}. {it['name'][:18]}", key=f"rm_{idx}"):
                    remove_item(idx)
                    st.rerun()

        totals = calc_totals()
        m1, m2, m3 = st.columns(3)
        m1.metric("Subtotal", money(totals["subtotal"]))
        m2.metric(f"Tax ({st.session_state.tax_rate:g}%)", money(totals["tax"]))
        m3.metric("Grand Total", money(totals["total"]))
    else:
        st.info("No products added yet. Use the form above to add line items.")

    st.markdown("---")
    st.subheader("Invoice preview")

    if not st.session_state.customer_name.strip():
        st.warning("Enter a customer name to generate the invoice.")
    elif not st.session_state.items:
        st.warning("Add at least one product to generate the invoice.")
    else:
        html = build_invoice_html()
        # Render invoice preview
        st.markdown(html, unsafe_allow_html=True)

        text_inv = build_invoice_text()
        d1, d2 = st.columns(2)
        with d1:
            st.download_button(
                "⬇️ Download invoice (.txt)",
                data=text_inv,
                file_name=f"{st.session_state.invoice_number}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with d2:
            st.download_button(
                "⬇️ Download invoice (.html)",
                data=html,
                file_name=f"{st.session_state.invoice_number}.html",
                mime="text/html",
                use_container_width=True,
            )
        st.caption("Open the HTML file in a browser and use Print → Save as PDF if you need a PDF.")


if __name__ == "__main__":
    main()
