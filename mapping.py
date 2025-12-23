import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()  


class AdaptiveTaxonomyMapper:
    def __init__(self):
        self.taxonomy = {
            "Romance": ["Slow-burn", "Enemies-to-Lovers", "Second Chance"],
            "Thriller": ["Espionage", "Psychological", "Legal Thriller"],
            "Sci-Fi": ["Hard Sci-Fi", "Space Opera", "Cyberpunk"],
            "Horror": ["Psychological Horror", "Gothic", "Slasher"]
        }

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = None
        self._build_taxonomy_index()

        try:
            self.llm = ChatGroq(model="llama3-70b-8192", temperature=0)
        except Exception:
            self.llm = None

    def _build_taxonomy_index(self):
        documents = []
        for genre, subs in self.taxonomy.items():
            for sub in subs:
                documents.append(f"{genre} -> {sub}")

        splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
        chunks = splitter.split_text("\n".join(documents))

        self.vector_store = FAISS.from_texts(chunks, self.embeddings)

    def map_story(self, user_tags, story_text):
        retrieved_context = self._retrieve_taxonomy_context(story_text)

        if self.llm:
            try:
                return self._llm_infer(user_tags, story_text, retrieved_context)
            except Exception:
                return self._rule_based_fallback(user_tags, story_text)

        return self._rule_based_fallback(user_tags, story_text)

    def _retrieve_taxonomy_context(self, story_text):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 4})
        docs = retriever.invoke(story_text)
        return "\n".join([d.page_content for d in docs])

    def _llm_infer(self, tags, story, taxonomy_context):
        prompt_template = """
You are an inference engine that maps stories to an internal taxonomy.

Rules:
1. Story context overrides user tags.
2. Choose only from the provided taxonomy.
3. If no category fits, return UNMAPPED.
4. Do not invent new categories.

Taxonomy:
{taxonomy}

Retrieved Taxonomy Context:
{taxonomy_context}

User Tags:
{tags}

Story:
{story}

Return output strictly as JSON:
{{
  "genre": "",
  "subgenre": "",
  "reasoning": ""
}}
"""
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["taxonomy", "taxonomy_context", "tags", "story"]
        )

        chain = prompt | self.llm
        response = chain.invoke({
            "taxonomy": self.taxonomy,
            "taxonomy_context": taxonomy_context,
            "tags": tags,
            "story": story
        })

        result = json.loads(response.content)
        return self._validate(result)

    def _rule_based_fallback(self, tags, story):
        text = story.lower()

        if any(w in text for w in ["lawyer", "judge", "court", "trial"]):
            return {
                "genre": "Thriller",
                "subgenre": "Legal Thriller",
                "reasoning": "Legal proceedings dominate the story context."
            }

        if any(w in text for w in ["spy", "agent", "mission", "classified"]):
            return {
                "genre": "Thriller",
                "subgenre": "Espionage",
                "reasoning": "Espionage-related terms indicate spy thriller."
            }

        if any(w in text for w in ["mansion", "ghost", "haunted", "corridor"]):
            return {
                "genre": "Horror",
                "subgenre": "Gothic",
                "reasoning": "Atmospheric horror elements suggest gothic horror."
            }

        if any(w in text for w in ["years later", "again", "after years"]):
            return {
                "genre": "Romance",
                "subgenre": "Second Chance",
                "reasoning": "Reunion after long separation indicates second chance romance."
            }

        return {
            "genre": "UNMAPPED",
            "subgenre": "UNMAPPED",
            "reasoning": "Story does not fit any category in the taxonomy."
        }

    def _validate(self, result):
        genre = result.get("genre")
        sub = result.get("subgenre")

        if genre == "UNMAPPED":
            return result

        if genre not in self.taxonomy:
            return {
                "genre": "UNMAPPED",
                "subgenre": "UNMAPPED",
                "reasoning": "Genre not present in taxonomy."
            }

        if sub not in self.taxonomy[genre]:
            return {
                "genre": "UNMAPPED",
                "subgenre": "UNMAPPED",
                "reasoning": "Subgenre not present in taxonomy."
            }

        return result


if __name__ == "__main__":
    mapper = AdaptiveTaxonomyMapper()

