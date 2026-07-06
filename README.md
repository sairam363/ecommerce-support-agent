# E-commerce Support Agent

A small AI support agent built for the AI Engineering Internship take-home assignment.

The main idea of this project was to create a chatbot that can figure out what kind of question the user is asking and then give the answer.

Some questions need to be answered by looking at the company rules, which are written down in the RAG documents. Other questions need to be answered by checking the order information in a CSV file. For questions that need both the company rules and the order information the chatbot combines both. Then gives a final answer. The chatbot is really good, at understanding what kind of question the user is asking and giving the answer.
---

# My Approach

When I first looked at the assignment I figured out that making a chatbot was not the problem. The big problem was figuring out **where the answer should come from**.

For example
* If someone asks "What is your return policy?" the answer should come from the policy documents.
* If someone asks "What is the status of ORD1004?" the answer should come from the orders dataset.
* If someone asks "Can I return ORD1004?" the chatbot needs to look at both the order information and the return policy to give an answer.

So I made the project simple by using a router that decides which way to go before it gives an answer. The router is, like a decision maker that says **where the answer should come from**.
---

# Project Structure

```
ecommerce-agent/

│
├── app.py                 # Streamlit UI
├── rag.py                 # RAG pipeline
├── router.py              # Decides which route to use
├── tools.py               # Order lookup functions
├── utils.py               # Helper functions
├── test.py                # Test script
├── tests.md               # Test cases
├── requirements.txt
├── README.md
│
└── sample_data
    ├── orders.csv
    └── docs
        ├── account_support.md
        ├── payments.md
        ├── returns.md
        └── shipping.md
```

---

# How the System Works

```
                 User Question
                       │
                       ▼
                 Router (Intent Detection)
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
        RAG         CSV Tool      Hybrid
          │            │            │
          └────────────┼────────────┘
                       ▼
                  Gemini LLM
                       ▼
                Final Response
```

---

# Routing Logic

The router checks the user's question and decides which path to use.

### 1. RAG

Used for policy-related questions.

Examples:

* What is your return policy?
* How long does shipping take?
* What payment methods are accepted?

The router sends these questions to the RAG pipeline.

---

### 2. Tool Call

Used when the user asks about a specific order.

Examples:

* What is the status of ORD1004?
* Show details of ORD1002

The router extracts the order ID and looks it up directly in the CSV file.

The LLM never guesses order information.

---

### 3. Hybrid Route

Some questions require both structured data and policy documents.

Examples:

* Can I return ORD1004?
* Can I cancel ORD1002?

For these questions the system:

1. Retrieves the order from the CSV.
2. Retrieves the relevant policy using RAG.
3. Sends both pieces of information to Gemini.
4. Gemini generates the final answer.

---

# Retrieval Strategy

The policy documents are stored as Markdown files.

During startup:

* All documents are loaded.
* They are split into smaller chunks using LangChain's RecursiveCharacterTextSplitter.
* Embeddings are generated using Sentence Transformers.
* The embeddings are stored in a FAISS vector database.

When the user asks a policy question:

* Similar chunks are retrieved from FAISS.
* Only the retrieved context is given to Gemini.
* Gemini answers using that context instead of relying on its own knowledge.

---

# Why I Chose FAISS

The dataset for this assignment is small, so I wanted something simple and fast.

FAISS was a good choice because:

* easy to set up
* fast retrieval
* works locally
* no external database required

For a larger production system I would probably consider a managed vector database, but FAISS is more than enough for this assignment.

---

# Chunking Strategy

I used recursive text splitting because it preserves the document structure better than splitting at fixed lengths.

The chunks have a small overlap so that information near chunk boundaries is not lost during retrieval.

---

# Why Rule-Based Routing?

I considered using the LLM to decide the route.

Instead, I used a rule-based router because:

* faster
* deterministic
* cheaper
* easier to debug

Since the assignment only has three routing categories, a simple rule-based approach is sufficient and avoids unnecessary LLM calls.

---

# Edge Cases Handled

The project handles a few common edge cases.

### Invalid Order ID

Example: What is the status of ORD9999?

Response:  Order ORD9999 was not found.


---

### Missing Policy

If the requested information is not available in the policy documents, the system returns a clear message instead of making something up.

---

### Missing Information

Some policies depend on information that isn't present in the dataset.

For example, the return policy depends on the delivery date, but the provided CSV only contains the order date.

Instead of guessing eligibility, the assistant explains that it cannot determine the answer with the available information.

---

# Technologies Used

* Python
* Streamlit
* LangChain
* FAISS
* Sentence Transformers
* Google Gemini
* Pandas

---

# Running the Project

## 1. Install dependencies

```
pip install -r requirements.txt
```

## 2. Create a `.env` file

```
GOOGLE_API_KEY=your_api_key_here
```

## 3. Start the application

```
streamlit run app.py
```

---

# Example Questions

### Policy Questions

* What is your return policy?
* How long does shipping take?
* What payment methods are accepted?
* What is the GST policy?

### Order Questions

* What is the status of ORD1004?
* Show details of ORD1002

### Hybrid Questions

* Can I return ORD1004?
* Can I cancel ORD1002?

---

# Testing

I created a separate `tests.md` file containing test questions along with expected and actual outputs.

The tests cover:

* RAG questions
* Tool calls
* Hybrid reasoning
* Invalid order IDs
* Edge cases

---

# Limitations

This project is intentionally simple.

Some current limitations are:

* Routing is keyword-based.
* Only one structured data source (orders.csv) is supported.
* There is no user authentication.
* The provided dataset does not contain delivery dates, so return eligibility cannot always be determined exactly.
* The knowledge base is rebuilt if the FAISS index is deleted.

---

# If I Had More Time

A few improvements I would make are:

* Use semantic intent classification instead of keyword matching.
* Add conversation memory for follow-up questions.
* Support multiple business tools (inventory, customers, invoices, etc.).
* Add source highlighting for retrieved policy sections.
* Deploy the application online.
* Improve evaluation with larger automated test sets.

---

# Time Spent

I spent around **5 hours** building this project.

Most of the time went into designing the routing logic, connecting the RAG pipeline with structured data lookup, handling edge cases, and testing different question types.

Overall, I tried to keep the implementation simple, readable, and easy to understand instead of adding unnecessary complexity.

