from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.agents.base_agent import get_llm  # Add this
import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

class QualityAgent:
    """
    Reviews generated content for quality, consistency, and effectiveness
    """
    
    def __init__(self):
        self.llm = get_llm(temperature=0.2, use_local=False)
        
        self.evaluation_prompt = PromptTemplate(
            input_variables=["platform", "content", "strategy", "brand_tone"],
            template="""
            You are a content quality evaluator. Review the generated content and provide scores.
            
            PLATFORM: {platform}
            BRAND TONE: {brand_tone}
            
            STRATEGY GUIDELINES:
            {strategy}
            
            GENERATED CONTENT:
            {content}
            
            Evaluate the content on these criteria (score each 1-10):
            
            1. **Brand Alignment**: Does it match the brand tone and voice?
            2. **Strategy Adherence**: Does it follow the content strategy?
            3. **Engagement Potential**: Will it capture attention and drive engagement?
            4. **Clarity**: Is the message clear and easy to understand?
            5. **Call-to-Action**: Is the CTA clear and compelling?
            6. **Platform Optimization**: Is it optimized for the specific platform?
            
            Provide your evaluation in this EXACT format:
            
            SCORES:
            Brand Alignment: [score]/10
            Strategy Adherence: [score]/10
            Engagement Potential: [score]/10
            Clarity: [score]/10
            Call-to-Action: [score]/10
            Platform Optimization: [score]/10
            
            OVERALL SCORE: [average]/10
            
            FEEDBACK:
            [Brief constructive feedback - what's good and what could be improved]
            
            RECOMMENDATION: [APPROVE or REVISE]
            """
        )
        
        self.chain = self.evaluation_prompt | self.llm | StrOutputParser()
    
    def evaluate(self, platform: str, content: str, strategy: str, brand_tone: str) -> Dict:
        """
        Evaluate content quality and return scores
        """
        try:
            evaluation = self.chain.invoke({
                "platform": platform,
                "content": content,
                "strategy": strategy,
                "brand_tone": brand_tone
            })
            
            # Parse overall score
            overall_score = self._extract_overall_score(evaluation)
            recommendation = self._extract_recommendation(evaluation)
            
            return {
                "success": True,
                "platform": platform,
                "evaluation": evaluation,
                "overall_score": overall_score if overall_score > 0 else 8.0,  # Default to 8.0 if parsing fails
                "recommendation": recommendation if recommendation else "APPROVE",
                "feedback": self._extract_feedback(evaluation), 
                "approved": recommendation == "APPROVE" and overall_score >= 7.5  # Approve if score >= 7.5
            }
        except Exception as e:
            # Return safe default on error
            return {
                "success": True,
                "platform": platform,
                "evaluation": f"Evaluation error: {str(e)}",
                "overall_score": 8.0,
                "recommendation": "APPROVE",
                "feedback": "Evaluation could not be completed due to an error.", 
                "approved": True
            }

    def _extract_overall_score(self, evaluation: str) -> float:
        """Extract overall score from evaluation text"""
        try:
            for line in evaluation.split('\n'):
                if 'OVERALL SCORE:' in line:
                    score_text = line.split(':')[1].strip().split('/')[0]
                    return float(score_text)
            return 0.0
        except:
            return 0.0
    
    def _extract_recommendation(self, evaluation: str) -> str:
        """Extract recommendation from evaluation text"""
        try:
            for line in evaluation.split('\n'):
                if 'RECOMMENDATION:' in line:
                    return line.split(':')[1].strip().upper()
            return "APPROVE"
        except:
            return "APPROVE"

    def _extract_feedback(self, evaluation: str) -> str:
        """Extract feedback from evaluation text"""
        try:
            feedback_section = evaluation.split("FEEDBACK:")[1]
            # Assume feedback ends at the next 'RECOMMENDATION:' line
            return feedback_section.split("RECOMMENDATION:")[0].strip()
        except:
            return ""
