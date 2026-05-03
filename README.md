# 🩺 SDAI Calculator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**SDAI (Simplified Disease Activity Index)** is a medical calculator for assessing the activity of rheumatoid arthritis. Implemented in pure Python with no external dependencies.

---

## 📖 What is SDAI?

SDAI is a numerical index that combines clinical and laboratory indicators into a single value to determine the current activity of rheumatoid arthritis. It was developed as a simpler alternative to the DAS28 index and is recommended by ACR/EULAR for monitoring therapy.

### 🧮 Formula

| Component                             | Description                        | Range     |
| ------------------------------------- | ---------------------------------- | --------- |
| **TJC** (Tender Joint Count)          | Number of tender joints out of 28  | 0–28      |
| **SJC** (Swollen Joint Count)         | Number of swollen joints out of 28 | 0–28      |
| **PGA** (Patient Global Assessment)   | Patient global assessment on VAS   | 0–10 cm   |
| **EGA** (Evaluator Global Assessment) | Evaluator global assessment on VAS | 0–10 cm   |
| **CRP** (C-reactive protein)          | C-reactive protein level           | ≥ 0 mg/dL |

### 📊 Interpretation of Results

| SDAI Value        | Activity Category        | Clinical Interpretation                   |
| ----------------- | ------------------------ | ----------------------------------------- |
| ≤ 3.3             | 🟢 **Remission**         | Disease inactive, treatment goal achieved |
| > 3.3 and ≤ 11.0  | 🟡 **Low Activity**      | Minimal activity, acceptable level        |
| > 11.0 and ≤ 26.0 | 🟠 **Moderate Activity** | Therapy adjustment required               |
| > 26.0            | 🔴 **High Activity**     | Severe flare, aggressive therapy needed   |

---

## 🚀 Features

- ✅ Calculation of the SDAI index from five clinical indicators
- ✅ Automatic classification into 4 activity categories
- ✅ Strict input validation with clear error messages
- ✅ Detailed formatted output
- ✅ Enum usage for typo protection
- ✅ Ready-made test examples (4 clinical scenarios)
- ✅ Clean architecture: separation of calculation, validation, and presentation
- ✅ Full English documentation (docstrings, README)
- ✅ Zero external dependencies (standard Python library only)
- ✅ Supports Python 3.8+

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/sdai-calculator.git
cd sdai-calculator
```
