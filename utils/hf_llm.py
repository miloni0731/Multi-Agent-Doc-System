from huggingface_hub import InferenceClient
import streamlit as st

# Load secrets from .streamlit/secrets.toml
HF_TOKEN = st.secrets["api"]["hf_token"]
PROVIDER = st.secrets["api"].get("provider", "together")
MODEL_NAME = st.secrets["api"].get("model_name", "mistralai/Mistral-7B-Instruct-v0.3")

# Initialize the HuggingFace Inference Client
client = InferenceClient(
    provider=PROVIDER,
    api_key=HF_TOKEN,
)

def query_llm(prompt: str, max_tokens: int = 300, temperature: float = 0.7) -> str:
    """
    Sends a prompt to the Together-hosted Mistral LLM and returns the response.
    
    Args:
        prompt (str): Input prompt to send to the model.
        max_tokens (int): Maximum number of tokens in the output.
        temperature (float): Sampling temperature for generation.

    Returns:
        str: Generated response or error message.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"[LLM Error] {str(e)}"

# Standalone test
if __name__ == "__main__":
    test_prompt = """
    Classify this document:

    "Dear Team, Please find the invoice for our last shipment attached. Regards, Acme Ltd."

    Output as:
    {
      "format": "Email",
      "intent": "Invoice"
    }
    """
    print(query_llm(test_prompt))
