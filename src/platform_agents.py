from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

class TwitterAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.7,  # Higher for more creative social content
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.prompt = PromptTemplate(
            input_variables=["analysis", "original_content"],
            template="""
            You are an expert Twitter/X content strategist. Based on the content analysis below, 
            create an engaging Twitter thread (8-12 tweets).

            CONTENT ANALYSIS:
            {analysis}

            ORIGINAL CONTENT:
            {original_content}

            TWITTER THREAD RULES:
            - Tweet 1: Strong hook that stops scrolling (question, bold statement, or shocking stat)
            - Tweets 2-10: Break down key points, one idea per tweet
            - Use short sentences and line breaks for readability
            - Include 1-2 relevant emojis per tweet (don't overdo it)
            - Last tweet: Clear call-to-action
            - Each tweet must be under 280 characters
            - Number each tweet (1/12, 2/12, etc.)
            - Make it conversational and engaging

            Generate the complete thread now:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate(self, analysis: str, original_content: str) -> dict:
        try:
            thread = self.chain.invoke({
                "analysis": analysis,
                "original_content": original_content
            })
            
            return {
                "success": True,
                "platform": "Twitter",
                "content": thread
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class LinkedInAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.6,
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.prompt = PromptTemplate(
            input_variables=["analysis", "original_content"],
            template="""
            You are a LinkedIn content expert. Transform the analyzed content into a professional 
            LinkedIn post that drives engagement.

            CONTENT ANALYSIS:
            {analysis}

            ORIGINAL CONTENT:
            {original_content}

            LINKEDIN POST RULES:
            - Start with a compelling hook (first 2 lines are crucial)
            - 150-300 words optimal length
            - Professional yet conversational tone
            - Use line breaks for readability (not walls of text)
            - Include 3-5 relevant hashtags at the end
            - End with a question or discussion prompt to encourage comments
            - Focus on insights, lessons, or actionable takeaways
            - Avoid excessive emojis (1-2 max)

            Generate the LinkedIn post now:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate(self, analysis: str, original_content: str) -> dict:
        try:
            post = self.chain.invoke({
                "analysis": analysis,
                "original_content": original_content
            })
            
            return {
                "success": True,
                "platform": "LinkedIn",
                "content": post
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class InstagramAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.7,
            model_name="llama-3.1-8b-instant",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.prompt = PromptTemplate(
            input_variables=["analysis", "original_content"],
            template="""
            You are an Instagram content creator. Create an engaging Instagram caption based on 
            the content analysis.

            CONTENT ANALYSIS:
            {analysis}

            ORIGINAL CONTENT:
            {original_content}

            INSTAGRAM CAPTION RULES:
            - First line must be attention-grabbing (shows in feed preview)
            - 125-150 words optimal
            - Use emojis strategically (3-5 total)
            - Add line breaks for visual appeal
            - Include a call-to-action (save, share, comment)
            - Add 10-15 relevant hashtags at the end (mix of popular and niche)
            - Conversational, friendly, and authentic tone
            - Can include a question to boost engagement

            Generate the Instagram caption now:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate(self, analysis: str, original_content: str) -> dict:
        try:
            caption = self.chain.invoke({
                "analysis": analysis,
                "original_content": original_content
            })
            
            return {
                "success": True,
                "platform": "Instagram",
                "content": caption
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
