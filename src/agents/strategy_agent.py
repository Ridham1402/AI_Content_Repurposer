from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agents.base_agent import get_llm  # Add this
import os
from dotenv import load_dotenv

load_dotenv()

class StrategyAgent:
    """
    Creates platform-specific content strategies based on research
    """
    
    def __init__(self):
        self.llm = get_llm(temperature=0.3, use_local=True)
        
        self.strategy_prompt = PromptTemplate(
            input_variables=["research_report", "brand_info", "topic", "target_audience", "brand_tone"],
            template="""
            You are an expert content strategist. Based on the research report, create a detailed content strategy 
            for social media posts across multiple platforms.
            
            CONTEXT:
            Brand: {brand_info}
            Topic: {topic}
            Target Audience: {target_audience}
            Brand Tone: {brand_tone}
            
            RESEARCH REPORT:
            {research_report}
            
            Create a comprehensive content strategy with:
            
            1. CORE MESSAGE:
               - What is the single most important message to communicate?
               - Why should the audience care?
            
            2. NARRATIVE ANGLE:
               - What storytelling approach will we use? (problem-solution, educational, inspirational, data-driven)
               - How do we position the brand as helpful/authoritative?
            
            3. KEY STATISTICS TO HIGHLIGHT:
               - Pick 2-3 most compelling data points from research
               - Explain why these numbers matter to the audience
            
            4. PLATFORM-SPECIFIC HOOKS:
               Twitter Hook: One attention-grabbing opening line for Twitter thread
               LinkedIn Hook: Professional opening that establishes thought leadership
               Instagram Hook: Relatable, visual-friendly opening line
               Newsletter Hook: Subject line + opening paragraph strategy
            
            5. CALL-TO-ACTION STRATEGY:
               - What action should readers take after consuming content?
               - How to phrase it for each platform?
            
            6. CONTENT STRUCTURE:
               - How should the information flow? (opening → body → closing)
               - What emotions should we evoke? (curiosity, urgency, hope, etc.)
            
            7. KEYWORDS & HASHTAGS:
               - 5-7 relevant keywords to naturally incorporate
               - Platform-specific hashtag recommendations
            
            8. DIFFERENTIATION STRATEGY:
               - Based on competitor insights, what unique angle can we take?
               - What content gap can we fill?
            
            Be specific and actionable. This strategy will guide content creators.
            """
        )
        
        self.chain = self.strategy_prompt | self.llm | StrOutputParser()
    
    def create_strategy(self, 
                       research_report: str,
                       brand_info: str,
                       topic: str,
                       target_audience: str,
                       brand_tone: str = "Professional but approachable") -> dict:
        """
        Generate comprehensive content strategy
        """
        print("\n📋 Creating content strategy...")
        
        try:
            strategy = self.chain.invoke({
                "research_report": research_report,
                "brand_info": brand_info,
                "topic": topic,
                "target_audience": target_audience,
                "brand_tone": brand_tone
            })
            
            print("✅ Strategy created successfully!")
            
            return {
                "success": True,
                "strategy": strategy,
                "brand_info": brand_info,
                "topic": topic,
                "target_audience": target_audience,
                "brand_tone": brand_tone
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
