# Test Cases

The following test cases were used to verify the routing logic, retrieval quality, tool calls, hybrid reasoning, and edge case handling.

| Test No. | User Question                        | Expected Route | Expected Result                                                                               | Status |
| -------- | ------------------------------------ | -------------- | --------------------------------------------------------------------------------------------- | ------ |
| 1        | What is your return policy?          | RAG            | Returns the return policy from the policy documents.                                          | ✅ Pass |
| 2        | How long does shipping take?         | RAG            | Returns standard and express shipping information.                                            | ✅ Pass |
| 3        | What payment methods are accepted?   | RAG            | Lists UPI, Cards, Net Banking and COD.                                                        | ✅ Pass |
| 4        | What is your GST policy?             | RAG            | Returns GST and invoice information.                                                          | ✅ Pass |
| 5        | What is the status of ORD1004?       | Tool           | Retrieves order details from the CSV file.                                                    | ✅ Pass |
| 6        | Show details of ORD1002              | Tool           | Retrieves complete order information.                                                         | ✅ Pass |
| 7        | Can I return ORD1004?                | Hybrid         | Retrieves order details, finds the relevant return policy, and generates a combined response. | ✅ Pass |
| 8        | Can I cancel ORD1002?                | Hybrid         | Uses the order status and cancellation policy to answer correctly.                            | ✅ Pass |
| 9        | What is the status of ORD9999?       | Tool           | Returns "Order not found."                                                                    | ✅ Pass |
| 10       | Do you ship internationally?         | RAG            | Returns that international shipping is not available.                                         | ✅ Pass |
| 11       | Can I use two coupon codes together? | RAG            | Returns that only one coupon can be applied per order.                                        | ✅ Pass |
| 12       | How do I reset my password?          | RAG            | Returns the account recovery instructions.                                                    | ✅ Pass |
| 13       | What happens if my shipment is lost? | RAG            | Returns the lost shipment policy.                                                             | ✅ Pass |
| 14       | Can I exchange an item?              | RAG            | Returns the exchange policy and conditions.                                                   | ✅ Pass |
| 15       | What is the status of order ABC123?  | Tool           | Gracefully handles an invalid order ID.                                                       | ✅ Pass |

---

# Edge Cases Tested

### 1. Invalid Order ID

**Question**

```
What is the status of ORD9999?
```

**Expected**

```
Order ORD9999 was not found.
```

**Actual**

```
Order ORD9999 was not found.
```

**Result:** ✅ Pass

---

### 2. Missing Information

The provided dataset does not include a delivery date.

**Question**

```
Can I return ORD1001?
```

**Expected**

The assistant should use the Electronics return policy but should not invent a delivery date or calculate eligibility using unavailable information.

**Actual**

The assistant explains that the Electronics return policy applies and avoids making unsupported claims when sufficient information is unavailable.

**Result:** ✅ Pass

---

### 3. Unknown Policy Question

**Question**

```
Do you offer drone delivery?
```

**Expected**

The assistant should indicate that this information is not available in the provided policy documents instead of making up an answer.

**Result:** ✅ Pass

---

# Routing Summary

| Route                        | Tested | Status |
| ---------------------------- | ------ | ------ |
| RAG                          | ✅      | Pass   |
| Tool Call                    | ✅      | Pass   |
| Hybrid (RAG + Tool)          | ✅      | Pass   |
| Invalid Input Handling       | ✅      | Pass   |
| Missing Information Handling | ✅      | Pass   |

---

Overall, the agent correctly routes policy questions, order-related questions, and hybrid queries while handling invalid inputs and unavailable information gracefully.

