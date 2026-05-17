import pandas as pd
import chromadb

from chromadb.utils import embedding_functions




def clean_text(text):

    if not isinstance(text, str):
        return ""

    text = text.replace("\n", " ")

    text = " ".join(text.split())

    return text.strip()


# BUILD HIGH QUALITY EMBEDDING DOCUMENT

def build_embedding_document(row):

    name = clean_text(
        row.get("name", "")
    )

    description = clean_text(
        row.get("description", "")
    )

    skills = clean_text(
        row.get("skills", "")
    )

    duration = clean_text(
        row.get("duration", "")
    )

    job_levels = clean_text(
        row.get("job_levels", "")
    )

    languages = clean_text(
        row.get("languages", "")
    )

    test_type = clean_text(
        row.get("test_type", "")
    )

    remote_testing = clean_text(
        row.get("remote_testing", "")
    )

    # IMPORTANT:
    # Weighted semantic structure
    # Role + skills emphasized heavily

    document = f"""
    SHL Assessment:
    {name}

    Assessment Type:
    {test_type}

    Assessment Description:
    {description}

    Skills Measured:
    {skills}

    Suitable Job Levels:
    {job_levels}

    Languages:
    {languages}

    Remote Testing:
    {remote_testing}

    Duration:
    {duration}

    This assessment is useful for:
    hiring,
    recruitment,
    talent assessment,
    candidate evaluation,
    role matching,
    skills evaluation,
    personality evaluation,
    technical screening,
    professional hiring,
    leadership hiring.
    """

    return clean_text(document)




def build_index():

    print("Loading CSV...")

    df = pd.read_csv(
        "data/shl_assessments.csv"
    )

    df = df.fillna("")

    print(
        f"Loaded {len(df)} assessments"
    )

    

    client = chromadb.PersistentClient(
        path="./chroma_db",
        settings=chromadb.Settings(
            anonymized_telemetry=False
        )
    )

   

    embedding_function = (
        embedding_functions
        .SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    )

    

    try:
        client.delete_collection(
            "shl_assessments"
        )
    except:
        pass

    collection = client.create_collection(
        name="shl_assessments",
        embedding_function=embedding_function
    )

    documents = []
    metadatas = []
    ids = []

    print("Building embedding documents...")

    for idx, row in df.iterrows():

        document = build_embedding_document(
            row
        )

        documents.append(document)

        metadatas.append({
            "name": row.get("name", ""),
            "url": row.get("url", ""),
            "test_type": row.get(
                "test_type",
                "Unknown"
            ),
            "job_levels": row.get(
                "job_levels",
                ""
            ),
            "remote_testing": row.get(
                "remote_testing",
                ""
            )
        })

        ids.append(str(idx))

    print("Creating embeddings...")

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(
        f"\nSuccessfully indexed {len(documents)} assessments."
    )


if __name__ == "__main__":
    build_index()