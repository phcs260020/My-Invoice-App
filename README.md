# My Invoice App

Streamlit application that lets you enter **customer** and **product** details, calculates the **total amount**, and generates a **simple invoice**.

## Features

- Company / seller details (sidebar)
- Customer name, address, email, phone
- Invoice number & date (auto-generated, editable)
- Add multiple products/services with quantity and unit price
- Automatic line amounts and grand total
- Optional tax rate (%)
- Currency symbol (₹ $ € £ ¥)
- Live invoice preview
- Download as **.txt** or **.html** (open HTML → Print → Save as PDF)
- Clear / new invoice button

## Quick Start

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

## Deploy on Streamlit Cloud

1. Push this folder to a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select the repo, set main file to `app.py`, deploy.

No API keys required.

## Project Structure

```
my_invoice_app/
├── app.py
├── requirements.txt
└── README.md
```

## How to use

1. Fill **Company** details in the sidebar (optional defaults provided).
2. Enter **Customer** details.
3. Add one or more **Products** (name, qty, unit price) → click **Add item**.
4. Set tax rate if needed.
5. View the **Invoice preview**.
6. Download `.txt` or `.html`.

## License

MIT
