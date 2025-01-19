from transformers import AutoTokenizer, AutoModel
import torch
from evaluate import load
bertscore = load("bertscore")
from sklearn.metrics.pairwise import cosine_similarity

# Load AlephBERT
tokenizer = AutoTokenizer.from_pretrained("onlplab/alephbert-base")
model = AutoModel.from_pretrained("onlplab/alephbert-base")


def embed_text(text, tokenizer, model):
    """
    Compute embeddings for a given text using AlephBERT.
    :param text: str
    :param tokenizer: Tokenizer object
    :param model: Model object
    :return: torch.Tensor
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Use the mean of the token embeddings as the sentence embedding
    return outputs.last_hidden_state.mean(dim=1)

def pad_to_match_length(predictions, references):
    """
    Pad predictions or references to match lengths.
    :param predictions: List of predictions
    :param references: List of references
    :return: Tuple of padded predictions and references
    """
    max_length = max(len(predictions), len(references))
    if len(predictions) < max_length:
        predictions.extend([""] * (max_length - len(predictions)))
    if len(references) < max_length:
        references.extend([""] * (max_length - len(references)))
    return predictions, references

def compute_similarity(candidate, reference, tokenizer, model):
    """
    Compute similarity between two texts using bert_score/cosine similarity similarity on embeddings.
    :param candidate: User's answer (string)
    :param reference: Correct answer (string)
    :param tokenizer: Tokenizer object
    :param model: Model object
    :return: float (similarity score)
    """
    candidate_embedding = embed_text(candidate, tokenizer, model)
    reference_embedding = embed_text(reference, tokenizer, model)
    # Compute cosine similarity
    similarity = cosine_similarity(candidate_embedding.numpy(), reference_embedding.numpy())
    return similarity[0][0]  # Extract the similarity value
    # candidate_list = [candidate]
    # reference_list = [reference]
    # candidate_list, reference_list = pad_to_match_length(candidate_list, reference_list)
    # results = bertscore.compute(predictions=candidate_list, references=reference_list, lang="he")
    # return results["f1"][0]


def is_answer_correct(user_answer, correct_answer, threshold=0.7):
    """
    Compare user_answer and correct_answer using cosine similarity of embeddings.
    :param user_answer: str
    :param correct_answer: str
    :param threshold: float (similarity threshold)
    :return: bool
    """
    similarity_score = compute_similarity(user_answer.strip(), correct_answer.strip(), tokenizer, model)
    print(f"Similarity Score: {similarity_score}")
    return similarity_score >= threshold