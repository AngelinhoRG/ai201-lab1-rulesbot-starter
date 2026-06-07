# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
I will label each numbered chunk (only if it passes the distance threshold) and its name [Catan, Monopoly, Risk, etc...].
I will sperate each chunk by a single blank line.
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
You are a rules lookup tool. Answer using only the exact wording of the rule 
chunks provided. Do not paraphrase, infer missing steps, or add any detail not 
present in the text. If the chunks do not contain a clear answer — including if 
they are only tangentially related — say so explicitly. Never draw on outside 
knowledge about board games. Do not combine or compare information across chunks. Treat each chunk independently. If the retrieved text does not mention something, do not 
conclude it is forbidden or allowed — only report what is explicitly stated.


```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
[your answer here]
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
[your answer here]
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
[your answer here]
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
The API call uses two messages:

System message — contains the grounding instruction and citation instruction.
Nothing else. Keeping instructions in the system role gives them higher 
authority than user-turn instructions.

User message — contains two things concatenated together:
  1. The formatted context block (all passing chunks, labeled and separated)
  2. The user's original query

Example structure:

  "Here are the relevant rule chunks:\n\n[CHUNK 1 | Game: Catan]\n...\n\n
   [CHUNK 2 | Game: Pandemic]\n...\n\nQuestion: How do you win?"

The query goes at the end, after the context, so the model reads the 
evidence before the question — this reduces the chance it answers from 
memory before consulting the chunks.
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: What is the exact rent on a mortgaged property in Monopoly?
Response: [CHUNK 4 | Game: Monopoly]
While mortgaged, the property cannot collect rent.

This chunk does not specify an exact rent amount, it states that the property cannot collect rent.

Correctly grounded? YES
Cited the right game? YES
```

**One thing you changed from your original spec after seeing the actual output:**

```
The chunk size and overlap sizes were changed to be bigger.
```
