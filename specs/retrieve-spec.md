# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
[your answer here]
I will call _collection.query() with three arguments:
  - query_texts=[query]: a list containing the single user query string.
    ChromaDB embeds it automatically using the same SentenceTransformer
    model used during ingestion, so the vector spaces match.
  - n_results=n_results: limits how many chunks are returned (default 3
    from config.py), keeping context concise for the generator.
  - include=["documents", "metadatas", "distances"]: requests the chunk
    text, the game metadata, and the cosine distance score — exactly the
    three fields needed to build the return dicts.
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
[your answer here]
[
    {"text": "chunk text", "game": "Catan", "distance": 0.21},
    {"text": "chunk text", "game": "Catan", "distance": 0.52}
]
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
[your answer here]
The index I need to access to get the actual list of results for a single query is index 0.
The nesting exists in case we ever want to do batch queries, but for now we only do one, hence the index 0.
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
[your answer here]
I will filter out results above a certain distance score. The tradeoff there is that maybe no chunks meet the threshold and you end up with nothing as the result. Leaving everything there might create some sort of clutter.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
[your answer here]
(a) Empty collection: the function returns [] immediately via the early
    check `if _collection.count() == 0` before querying. This avoids a
    ChromaDB error that occurs when querying an empty collection.

(b) No good matches: the function returns all n_results chunks regardless
    of how high their distance scores are. There is no threshold filter,
    so the caller (generate_response) receives the best available chunks
    even if none are truly relevant. The generator must handle low-quality
    context gracefully.

(c) Multiple games matched: the function returns them as-is, ranked by
    distance. It does not filter by game — if chunks from Risk and Catan
    both score well, both appear in the results. This is intentional: the
    user's query may span multiple games, and filtering by game would
    require knowing the answer before asking the question.
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: What happens if you land on a property that you do not want to buy or purchase in Monopoly?

Top result game: Monopoly
Distance score: 0.444
Does it make sense? No, it does not make much sense because the header usually is the closest chunk, followed by chunks with medium level of relevence
```

**One thing about the query results that surprised you:**

```
[your answer here]
For Monopoly, the header "[Monopoly] (dist: 0.444) MONOPOLY — OFFICIAL RULES SUMMARY" is usually the chunk with the best distance score.
```
