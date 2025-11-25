from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agents.base_agent import get_llm  # Add this
import os
from dotenv import load_dotenv

load_dotenv()

class EnhancedTwitterAgent:
    """
    Research-driven Twitter thread generator
    """
    
    def __init__(self):
        self.llm = get_llm(temperature=0.7, use_local=False)
        
        self.prompt = PromptTemplate(
            input_variables=["research_report", "strategy", "brand_info", "topic", "brand_tone"],
            template="""
            You are an expert Twitter content creator. Create an engaging Twitter thread based on research and strategy.
            
            BRAND: {brand_info}
            TOPIC: {topic}
            TONE: {brand_tone}
            
            RESEARCH INSIGHTS:
            {research_report}
            
            CONTENT STRATEGY:
            {strategy}
            
            Create a Twitter thread (10-12 tweets) that:
            - Starts with the hook from the strategy (make it attention-grabbing!)
            - Incorporates the key statistics naturally
            - Follows the content structure from strategy
            - Uses the recommended keywords organically
            - Each tweet under 280 characters
            - Number tweets (1/12, 2/12, etc.)
            - Uses 1-2 emojis per tweet strategically
            - Ends with the CTA from strategy
            - Maintains brand tone throughout
            
            Make it conversational, engaging, and scroll-stopping. Use research facts to build credibility.
            
            Generate the complete thread now:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate(self, research_report: str, strategy: str, brand_info: str, 
                 topic: str, brand_tone: str) -> dict:
        try:
            print("\n🐦 Generating Twitter thread...")
            thread = self.chain.invoke({
                "research_report": research_report,
                "strategy": strategy,
                "brand_info": brand_info,
                "topic": topic,
                "brand_tone": brand_tone
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


class EnhancedLinkedInAgent:
    """
    Research-driven LinkedIn post generator
    """
    
    def __init__(self):
        self.llm = get_llm(temperature=0.6, use_local=False)
        
        self.prompt = PromptTemplate(
            input_variables=["research_report", "strategy", "brand_info", "topic", "brand_tone"],
            template="""
            You are a LinkedIn content strategist. Create a professional thought leadership post.
            
            BRAND: {brand_info}
            TOPIC: {topic}
            TONE: {brand_tone}
            
            RESEARCH INSIGHTS:
            {research_report}
            
            CONTENT STRATEGY:
            {strategy}
            
            Create a LinkedIn post that:
            - Opens with the hook from strategy (first 2 lines are crucial!)
            - 200-300 words
            - Incorporates key statistics with context
            - Follows the content structure and emotional arc from strategy
            - Uses line breaks for readability
            - Includes 4-5 hashtags from strategy
            - Ends with the CTA as a discussion prompt
            - Professional yet approachable tone
            - Establishes thought leadership
            
            Make it insightful, credible, and conversation-starting.
            
            Generate the LinkedIn post now:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate(self, research_report: str, strategy: str, brand_info: str,
                 topic: str, brand_tone: str) -> dict:
        try:
            print("\n💼 Generating LinkedIn post...")
            post = self.chain.invoke({
                "research_report": research_report,
                "strategy": strategy,
                "brand_info": brand_info,
                "topic": topic,
                "brand_tone": brand_tone
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


class EnhancedInstagramAgent:
    """
    Research-driven Instagram caption generator
    """
    
    def __init__(self):
        self.llm = get_llm(temperature=0.7, use_local=False)
        
        self.prompt = PromptTemplate(
            input_variables=["research_report", "strategy", "brand_info", "topic", "brand_tone"],
            template="""
            You are an Instagram content creator. Create an engaging caption based on research.
            
            BRAND: {brand_info}
            TOPIC: {topic}
            TONE: {brand_tone}
            
            RESEARCH INSIGHTS:
            {research_report}
            
            CONTENT STRATEGY:
            {strategy}
            
            Create an Instagram caption that:
            - Starts with the hook from strategy (shows in feed preview!)
            - 150-200 words
            - Incorporates 1-2 key statistics naturally
            - Uses 3-5 emojis strategically
            - Line breaks for visual appeal
            - Includes CTA from strategy
            - 10-15 hashtags from strategy (mix popular + niche)
            - Conversational, authentic, relatable tone
            - Encourages engagement (comments/shares)
            
            Make it visually appealing and shareable.
            
            Generate the Instagram caption now:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate(self, research_report: str, strategy: str, brand_info: str,
                 topic: str, brand_tone: str) -> dict:
        try:
            print("\n📸 Generating Instagram caption...")
            caption = self.chain.invoke({
                "research_report": research_report,
                "strategy": strategy,
                "brand_info": brand_info,
                "topic": topic,
                "brand_tone": brand_tone
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


class NewsletterAgent:
    """
    Research-driven email newsletter generator
    """
    
    def __init__(self):
        self.llm = get_llm(temperature=0.6, use_local=False)
        
        self.prompt = PromptTemplate(
            input_variables=["research_report", "strategy", "brand_info", "topic", "brand_tone"],
            template="""
            You are an email marketing expert. Create a compelling newsletter based on research.
            
            BRAND: {brand_info}
            TOPIC: {topic}
            TONE: {brand_tone}
            
            RESEARCH INSIGHTS:
            {research_report}
            
            CONTENT STRATEGY:
            {strategy}
            
            Create an email newsletter with:
            
            **SUBJECT LINE:** 
            (3 options - use hook from strategy)
            
            **PREVIEW TEXT:**
            (Short teaser that appears after subject line)
            
            **EMAIL BODY:**
            - Opening paragraph with hook
            - 3-4 short sections with subheadings
            - Incorporate key statistics with context
            - 400-600 words total
            - Scannable formatting (short paragraphs, bullet points)
            - Personal, conversational tone
            - Clear CTA button text and placement
            - P.S. section with secondary CTA or value add
            
            Make it valuable, skimmable, and action-oriented.
            
            Generate the complete newsletter now:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def generate(self, research_report: str, strategy: str, brand_info: str,
                 topic: str, brand_tone: str) -> dict:
        try:
            print("\n📧 Generating email newsletter...")
            newsletter = self.chain.invoke({
                "research_report": research_report,
                "strategy": strategy,
                "brand_info": brand_info,
                "topic": topic,
                "brand_tone": brand_tone
            })
            
            return {
                "success": True,
                "platform": "Newsletter",
                "content": newsletter
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
