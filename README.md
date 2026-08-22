# 🎤 NammaKural

### AI-Powered Voice-First Bookkeeping Assistant for Small Businesses

NammaKural is an AI-powered, voice-first bookkeeping assistant designed to make daily business transaction recording simpler for small business owners.

Instead of manually typing every transaction, users can speak their transaction naturally and NammaKural converts the voice input into structured financial data.

---

## 💡 The Problem

Many small business owners still rely on notebooks, memory, or manual spreadsheets to track their daily income and expenses.

This can make bookkeeping:

- Time-consuming
- Difficult to maintain
- Error-prone
- Difficult for users who are not comfortable with traditional accounting software

---

## 🚀 Our Solution

NammaKural uses a voice-first approach to simplify transaction recording.

For example, a user can say:

> "I bought rice for 250 rupees."

NammaKural processes the voice input and converts it into structured transaction information.

---

## 🏗️ System Architecture

NammaKural follows a voice-to-insight pipeline that transforms natural speech into structured business information.

```text
┌─────────────────────┐
│   🎤 Voice Input    │
│  Business Owner     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 🗣️ Speech-to-Text   │
│      Whisper        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 🧠 Transaction      │
│      Parser         │
│   Python / NLP      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 💰 Structured       │
│    Transaction      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 🗄️ MySQL Database   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 📊 Streamlit        │
│     Dashboard       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ 💡 Business         │
│     Insights        │
└─────────────────────┘
## 🎬 Demo

### Voice-to-Transaction

A user speaks a business transaction naturally, and NammaKural converts the voice input into structured transaction data.

> "I bought rice for 250 rupees."

The system extracts information such as:

- Transaction type: Expense
- Item: Rice
- Amount: ₹250

### Dashboard

The processed transaction is stored in MySQL and visualized through an interactive Streamlit dashboard.

📸 Screenshots coming soon.