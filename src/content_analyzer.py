from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

class ContentAnalyzer:
    def __init__(self):
        # Initialize Groq LLM with current available models
        self.llm = ChatGroq(
            temperature=0.3,
            model_name="llama-3.1-8b-instant",  # Updated current model
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Define analysis prompt
        self.analysis_prompt = PromptTemplate(
            input_variables=["content"],
            template="""
            You are an expert content analyst. Analyze the following content and extract:
            
            1. Main Topic: What is the core subject?
            2. Key Points: List 5-7 main takeaways (bullet points)
            3. Tone: Describe the writing style (professional, casual, inspirational, etc.)
            4. Target Audience: Who is this content for?
            5. Call-to-Action: What action should readers take?
            6. Hook Elements: What parts would grab attention on social media?
            
            Content:
            {content}
            
            Provide your analysis in a structured format.
            """
        )
        
        # Create chain with output parser
        self.chain = self.analysis_prompt | self.llm | StrOutputParser()
    
    def analyze(self, content: str) -> dict:
        """
        Analyzes content and returns structured insights
        """
        try:
            analysis_text = self.chain.invoke({"content": content})
            
            return {
                "success": True,
                "analysis": analysis_text,
                "original_length": len(content)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Helper function for easy import
def analyze_content(content: str):
    analyzer = ContentAnalyzer()
    return analyzer.analyze(content)
