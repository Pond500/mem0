"""
Test local embedding model
"""
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

def test_local_embedding():
    """Test local embedding model"""
    model_name = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
    
    print("🔍 Testing Local Embedding Model")
    print(f"   Model: {model_name}")
    print()
    
    try:
        print("📥 Loading model (first time will download)...")
        model = SentenceTransformer(model_name)
        
        print("✅ Model loaded successfully!")
        print()
        
        # Test embedding
        print("🧪 Testing embedding generation...")
        texts = [
            "สวัสดีครับ",
            "Hello, how are you?",
            "Python programming is fun",
            "การเขียนโปรแกรมสนุกมาก"
        ]
        
        embeddings = model.encode(texts)
        
        print(f"✅ Generated embeddings for {len(texts)} texts")
        print(f"   Embedding dimension: {embeddings.shape[1]}")
        print(f"   Embedding shape: {embeddings.shape}")
        print()
        
        # Test similarity
        print("🔍 Testing similarity search...")
        from sklearn.metrics.pairwise import cosine_similarity
        
        similarities = cosine_similarity([embeddings[0]], embeddings[1:])[0]
        
        print("   Similarities with 'สวัสดีครับ':")
        for i, (text, sim) in enumerate(zip(texts[1:], similarities), 1):
            print(f"     {i}. {text}: {sim:.4f}")
        print()
        
        print("=" * 60)
        print("✅ Local embedding model is working perfectly!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        print()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Local Embedding Model Test")
    print("=" * 60)
    print()
    
    test_local_embedding()
