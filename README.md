# 🎤 NammaKural

<div align="center">

### 🗣️ Speak your transaction. Let AI handle the bookkeeping.

**An AI-powered, voice-first bookkeeping assistant for small businesses.**

**Voice → AI → Transaction → Database → Insights**

</div>

---

## 🌱 Why NammaKural?

For many small business owners, bookkeeping still means notebooks, memory, calculators, or manually updating spreadsheets.

That creates a simple but important problem:

> **Recording a ₹250 transaction shouldn't require opening a complicated accounting system.**

NammaKural takes a different approach.

Instead of typing `Expense → Rice → ₹250`, the user can simply say:

> 🎤 **"I bought rice for 250 rupees."**

NammaKural transforms that natural voice input into structured business data.

---

## 🚀 What NammaKural Does

| 🎤 Voice | 🧠 AI | 🗄️ Store | 📊 Understand |
| --- | --- | --- | --- |
| Speak naturally | Convert & parse | Save transactions | Analyze business data |

**Less typing. Less friction. Better visibility into daily business finances.**

---

## 🏗️ How It Works

**Voice → Speech-to-Text → Transaction Parsing → MySQL → Analytics → Insights**

---

## ✨ Current Features

### 🎤 Voice-First Input

Record a natural business transaction instead of manually filling multiple fields.

### 🗣️ Speech-to-Text

Uses **Whisper** to convert spoken transactions into text.

### 🧠 Transaction Parsing

Extracts:

- Transaction type
- Item
- Quantity
- Unit
- Amount

### 🗄️ MySQL Storage

Stores structured transactions in a MySQL database.

### 📊 Business Dashboard

Provides:

- 💰 Income
- 💸 Expenses
- 💵 Balance
- 🔢 Transaction count
- 📈 Cash flow
- 🛒 Expense analysis
- 💡 Business insights

---

## 🧪 Real-World Example

### 🎤 User says

> **"I bought 5 kg rice for 250 rupees."**

### 🧠 NammaKural extracts

| Field | Value |
| --- | --- |
| Transaction Type | Expense |
| Item | Rice |
| Quantity | 5 |
| Unit | kg |
| Amount | ₹250 |

---

## 🛠️ Technology Stack

| Layer | Technology |
| --- | --- |
| Programming Language | Python |
| Speech Recognition | Whisper |
| NLP / Parsing | Python |
| Database | MySQL |
| Data Processing | Pandas |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Version Control | Git + GitHub |

---

## 📸 Product Showcase

### 📊 Dashboard Overview

![NammaKural Dashboard](screenshots/dashboard-overview.png)

---

### 🎤 Voice Input

![NammaKural Voice Input](screenshots/voice-input.png)

---

### 💰 Cash Flow

![NammaKural Cash Flow](screenshots/cash-flow.png)

---

### 📈 Business Analytics

![NammaKural Analytics](screenshots/analytics.png)

---

### 💡 AI Insights

![NammaKural AI Insights](screenshots/ai-insights.png)

---

### 🧠 Detailed Analytics

![NammaKural Detailed Analytics](screenshots/Business-analytics.png)

---

### ⚙️ Business Records

![NammaKural Business Records](screenshots/Business-records.png)

---

## 📁 Project Structure

NammaKural contains the following main components:

- `dashboard.py` — Streamlit dashboard
- `speech_to_text.py` — Speech recognition
- `transaction_parser.py` — Transaction extraction
- `save_transaction.py` — Database storage
- `database_schema.sql` — Database structure
- `requirements.txt` — Python dependencies

---

## ⚙️ Getting Started

### Clone the repository

```bash
git clone https://github.com/DharshanaSenthilkumar/NammaKural.git
cd NammaKural
Install dependencies
py -m pip install -r requirements.txt
Configure MySQL

Create a .env file containing your local database credentials.

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_PASSWORD
MYSQL_DATABASE=nammakkural

⚠️ Never upload your .env file to GitHub.

Run the dashboard
streamlit run dashboard.py
🔐 Security

Sensitive local data is excluded from the repository using .gitignore.

Excluded files include:

.env
transactions.csv
Audio recordings
Python cache files
🔮 Future Roadmap
 🇮🇳 Tamil voice support
 💬 Tamil + Tanglish support
 📱 Flutter mobile application
 🌐 Flask / FastAPI backend
 🧠 Advanced AI insights
 📈 Predictive cash-flow analysis
 🔮 Business forecasting
 👥 Multi-user support
 ☁️ Cloud deployment
🎯 Vision

Make bookkeeping as simple as having a conversation.

NammaKural aims to make digital financial management more accessible to small businesses by replacing complicated manual data entry with natural voice interaction.

👩‍💻 NammaKural

AI-powered voice-first bookkeeping assistant for small businesses.

Python • Whisper • NLP • MySQL • Streamlit • Pandas • Plotly

🚀 Voice → Data → Decisions