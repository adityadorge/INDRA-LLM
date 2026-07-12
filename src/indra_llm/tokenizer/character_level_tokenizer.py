"""
Data Collection & Preparation
--------------------------------------
Download and prepare the TinyShakespeare dataset. This raw text will be used
to build our character-level tokenizer and create the training/validation
tensors for the decoder-only GPT model.
"""
"""
3. Create a character-level tokenizer by identifying the unique characters in the text.
4. Convert the characters to integer indices (stoi) and create a reverse mapping (itos).
5. Convert to tensors list of integers and wrap it into a 1D Tensor.
6. Split into Training and Validation Sets
7. Define the Context Length (Block Size)
Learn how to extract one (x, y) pair
Create a get_batch() function that returns a batch of (x, y) pairs
Understand the shapes of x and y (this is critical before building the model)
8. Structure the Inputs ($X$) and Targets ($Y$)
9. Create a Batching Function (Data Loader)  / Create batches for training
10. Feed the batches into the model for training
"""
import torch
# 1. Download the TinyShakespeare dataset and read the text file.
with open('data/raw/tiny_shakespeare_raw.txt', 'r', encoding='utf-8') as f:
    text = f.read()
  
# 2. Create a character-level tokenizer 
# 3. Convert the characters to integer indices (stoi) and create a reverse mapping (itos).
itos = dict(enumerate(sorted(set(text))))
stoi = {ch: i for i, ch in enumerate(sorted(set(text)))}
print(f'stoi: {stoi}')
print(f'itos: {itos}')

# 4. Define the encode and decode functions
def encode(s: str) -> list[int]:
    """Encodes a string into a list of integers using the stoi mapping."""
    return [stoi[c] for c in s]   

def decode(l: list[int]) -> str:
    """Decodes a list of integers back into a string using the itos mapping."""
    return ''.join([itos[i] for i in l])

# 5. Test the encode and decode functions
test_text = "world"
print(f'encode("{test_text}"): {encode(test_text)}')
print(f'decode: {decode(encode(test_text))}') 

# 6. Encode the entire dataset
encoded_text = encode(text)
print(f"\nNumber of tokens: {len(encoded_text):,}")

# 7. Convert to a PyTorch tensor
data = torch.tensor(encoded_text, dtype=torch.long)

print(f"Tensor shape : {data.shape}")
print(f"Tensor dtype : {data.dtype}")

# Show the first few tokens
print(data[:20])

# 8. Split into training and validation sets
n = int(0.9 * len(data))

train_data = data[:n]
val_data = data[n:]

print(f"\nTraining tokens  : {len(train_data):,}")
print(f"Validation tokens: {len(val_data):,}")