from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    context_parts = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(f"[CHUNK {i} | Game: {chunk['game']}]\n{chunk['text']}")
    context_block = "\n\n".join(context_parts)

    system_message = (
        "You are a rules lookup tool. Answer using only the exact wording of the rule "
        "chunks provided. Do not paraphrase, infer missing steps, or add any detail not "
        "present in the text. If the chunks do not contain a clear answer — including if "
        "they are only tangentially related — say so explicitly. Never draw on outside "
        "knowledge about board games. Do not combine or compare information across chunks. "
        "Treat each chunk independently. If the retrieved text does not mention something, do not "
        "conclude it is forbidden or allowed — only report what is explicitly stated. "
        "Always identify which game your answer comes from by citing the chunk label (e.g. [CHUNK 1 | Game: Catan])."
    )

    user_message = (
        f"Here are the relevant rule chunks:\n\n{context_block}\n\nQuestion: {query}"
    )

    completion = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
    )

    return completion.choices[0].message.content
