from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator

from src.agents.research_agent import ResearchAgent
from src.agents.strategy_agent import StrategyAgent
from src.agents.enhanced_platform_agents import (
    EnhancedTwitterAgent,
    EnhancedLinkedInAgent,
    EnhancedInstagramAgent,
    NewsletterAgent
)
from src.agents.quality_agent import QualityAgent

# Define the state that flows through the graph
class ContentCreationState(TypedDict):
    # Inputs
    brand_info: str
    industry: str
    target_audience: str
    topic: str
    brand_tone: str
    
    # Research phase
    research_report: str
    research_sources: int
    
    # Strategy phase
    strategy: str
    
    # Content generation phase
    twitter_content: str
    linkedin_content: str
    instagram_content: str
    newsletter_content: str
    
    # Quality evaluation
    twitter_quality: dict
    linkedin_quality: dict
    instagram_quality: dict
    newsletter_quality: dict
    
    # Overall status
    all_approved: bool
    retry_count: int

    twitter_attempts: list
    linkedin_attempts: list
    instagram_attempts: list
    newsletter_attempts: list
    

class ContentCreationOrchestrator:
    """
    LangGraph-based orchestrator for the entire content creation pipeline
    """
    
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.strategy_agent = StrategyAgent()
        self.twitter_agent = EnhancedTwitterAgent()
        self.linkedin_agent = EnhancedLinkedInAgent()
        self.instagram_agent = EnhancedInstagramAgent()
        self.newsletter_agent = NewsletterAgent()
        self.quality_agent = QualityAgent()
        
        # Build the workflow graph
        self.workflow = self._build_workflow()
    
    def _build_workflow(self):
        """
        Build the LangGraph workflow
        """
        workflow = StateGraph(ContentCreationState)
        
        # Add nodes (each agent is a node)
        workflow.add_node("research", self._research_node)
        workflow.add_node("strategy", self._strategy_node)
        workflow.add_node("generate_content", self._generate_content_node)
        workflow.add_node("quality_check", self._quality_check_node)
        workflow.add_node("regenerate_content", self._regenerate_content_node)  # New node for retry
        
        # Define the flow
        workflow.set_entry_point("research")
        workflow.add_edge("research", "strategy")
        workflow.add_edge("strategy", "generate_content")
        workflow.add_edge("generate_content", "quality_check")
        
        # Conditional edge: if quality is good, end; otherwise retry content generation only
        workflow.add_conditional_edges(
            "quality_check",
            self._should_retry,
            {
                "end": END,
                "retry": "regenerate_content"  # Skip research and strategy
            }
        )
        
        # After regeneration, go back to quality check
        workflow.add_edge("regenerate_content", "quality_check")
        
        return workflow.compile()

    def _research_node(self, state: ContentCreationState) -> ContentCreationState:
        """Research agent node"""
        print("\n" + "="*80)
        print("🔍 NODE 1: RESEARCH AGENT")
        print("="*80)
        
        result = self.research_agent.conduct_research(
            topic=state["topic"],
            brand_info=state["brand_info"],
            target_audience=state["target_audience"],
            industry=state["industry"]
        )
        
        state["research_report"] = result["research_report"]
        state["research_sources"] = result["total_sources"]
        
        print(f"✅ Research complete: {result['total_sources']} sources analyzed")
        return state
    
    def _strategy_node(self, state: ContentCreationState) -> ContentCreationState:
        """Strategy agent node"""
        print("\n" + "="*80)
        print("📋 NODE 2: STRATEGY AGENT")
        print("="*80)
        
        result = self.strategy_agent.create_strategy(
            research_report=state["research_report"],
            brand_info=state["brand_info"],
            topic=state["topic"],
            target_audience=state["target_audience"],
            brand_tone=state["brand_tone"]
        )
        
        state["strategy"] = result["strategy"]
        
        print("✅ Strategy created")
        return state
    
    def _generate_content_node(self, state: ContentCreationState) -> ContentCreationState:
        """Content generation node - all platforms"""
        print("\n" + "="*80)
        print("📱 NODE 3: CONTENT GENERATION (All Platforms)")
        print("="*80)
        
        # Generate for all platforms
        twitter_result = self.twitter_agent.generate(
            research_report=state["research_report"],
            strategy=state["strategy"],
            brand_info=state["brand_info"],
            topic=state["topic"],
            brand_tone=state["brand_tone"],
            feedback=""
        )
        state["twitter_content"] = twitter_result["content"]
        
        linkedin_result = self.linkedin_agent.generate(
            research_report=state["research_report"],
            strategy=state["strategy"],
            brand_info=state["brand_info"],
            topic=state["topic"],
            brand_tone=state["brand_tone"],
            feedback=""
        )
        state["linkedin_content"] = linkedin_result["content"]
        
        instagram_result = self.instagram_agent.generate(
            research_report=state["research_report"],
            strategy=state["strategy"],
            brand_info=state["brand_info"],
            topic=state["topic"],
            brand_tone=state["brand_tone"],
            feedback=""
        )
        state["instagram_content"] = instagram_result["content"]
        
        newsletter_result = self.newsletter_agent.generate(
            research_report=state["research_report"],
            strategy=state["strategy"],
            brand_info=state["brand_info"],
            topic=state["topic"],
            brand_tone=state["brand_tone"],
            feedback=""
        )
        state["newsletter_content"] = newsletter_result["content"]
        
        print("✅ All platform content generated")
        return state
    
    def _quality_check_node(self, state: ContentCreationState) -> ContentCreationState:
        """Quality evaluation node"""
        print("\n" + "="*80)
        print("✅ NODE 4: QUALITY EVALUATION")
        print("="*80)
        
        # Evaluate each platform
        state["twitter_quality"] = self.quality_agent.evaluate(
            platform="Twitter",
            content=state["twitter_content"],
            strategy=state["strategy"],
            brand_tone=state["brand_tone"]
        )
        state["twitter_attempts"].append({
            "content": state["twitter_content"],
            "score": state["twitter_quality"]["overall_score"]
        })
        print(f"  Twitter: {state['twitter_quality']['overall_score']:.1f}/10 - {state['twitter_quality']['recommendation']}")
        
        state["linkedin_quality"] = self.quality_agent.evaluate(
            platform="LinkedIn",
            content=state["linkedin_content"],
            strategy=state["strategy"],
            brand_tone=state["brand_tone"]
        )
        state["linkedin_attempts"].append({
            "content": state["linkedin_content"],
            "score": state["linkedin_quality"]["overall_score"]
        })
        print(f"  LinkedIn: {state['linkedin_quality']['overall_score']:.1f}/10 - {state['linkedin_quality']['recommendation']}")
        
        state["instagram_quality"] = self.quality_agent.evaluate(
            platform="Instagram",
            content=state["instagram_content"],
            strategy=state["strategy"],
            brand_tone=state["brand_tone"]
        )
        state["instagram_attempts"].append({
            "content": state["instagram_content"],
            "score": state["instagram_quality"]["overall_score"]
        })
        print(f"  Instagram: {state['instagram_quality']['overall_score']:.1f}/10 - {state['instagram_quality']['recommendation']}")
        
        state["newsletter_quality"] = self.quality_agent.evaluate(
            platform="Newsletter",
            content=state["newsletter_content"],
            strategy=state["strategy"],
            brand_tone=state["brand_tone"]
        )
        state["newsletter_attempts"].append({
            "content": state["newsletter_content"],
            "score": state["newsletter_quality"]["overall_score"]
        })
        print(f"  Newsletter: {state['newsletter_quality']['overall_score']:.1f}/10 - {state['newsletter_quality']['recommendation']}")
        
        # Check if all approved
        state["all_approved"] = all([
            state["twitter_quality"]["approved"],
            state["linkedin_quality"]["approved"],
            state["instagram_quality"]["approved"],
            state["newsletter_quality"]["approved"]
        ])
        
        return state
    
    def _regenerate_content_node(self, state: ContentCreationState) -> ContentCreationState:
        """Regenerate only failed content (skip research and strategy)"""
        
        # Increment retry count
        current_retry = state.get("retry_count", 0)
        state["retry_count"] = current_retry + 1
        
        print("\n" + "="*80)
        print(f"🔄 NODE: CONTENT REGENERATION - Attempt {state['retry_count']}")
        print("="*80)
        
        # Show which platforms failed
        failed_platforms = []
        if not state["twitter_quality"].get("approved", False):
            failed_platforms.append("Twitter")
        if not state["linkedin_quality"].get("approved", False):
            failed_platforms.append("LinkedIn")
        if not state["instagram_quality"].get("approved", False):
            failed_platforms.append("Instagram")
        if not state["newsletter_quality"].get("approved", False):
            failed_platforms.append("Newsletter")
        
        print(f"Failed platforms: {', '.join(failed_platforms)}")
        print(f"Regenerating only failed content...\n")
        
        # Only regenerate platforms that failed
        if not state["twitter_quality"].get("approved", False):
            print("  🐦 Regenerating Twitter...")
            feedback = state["twitter_quality"].get("feedback", "")
            twitter_result = self.twitter_agent.generate(
                research_report=state["research_report"],
                strategy=state["strategy"],
                brand_info=state["brand_info"],
                topic=state["topic"],
                brand_tone=state["brand_tone"],
                feedback=feedback
            )
            state["twitter_content"] = twitter_result["content"]
        
        if not state["linkedin_quality"].get("approved", False):
            print("  💼 Regenerating LinkedIn...")
            feedback = state["linkedin_quality"].get("feedback", "")
            linkedin_result = self.linkedin_agent.generate(
                research_report=state["research_report"],
                strategy=state["strategy"],
                brand_info=state["brand_info"],
                topic=state["topic"],
                brand_tone=state["brand_tone"],
                feedback=feedback
            )
            state["linkedin_content"] = linkedin_result["content"]
        
        if not state["instagram_quality"].get("approved", False):
            print("  📸 Regenerating Instagram...")
            feedback = state["instagram_quality"].get("feedback", "")
            instagram_result = self.instagram_agent.generate(
                research_report=state["research_report"],
                strategy=state["strategy"],
                brand_info=state["brand_info"],
                topic=state["topic"],
                brand_tone=state["brand_tone"],
                feedback=feedback
            )
            state["instagram_content"] = instagram_result["content"]
        
        if not state["newsletter_quality"].get("approved", False):
            print("  📧 Regenerating Newsletter...")
            feedback = state["newsletter_quality"].get("feedback", "")
            newsletter_result = self.newsletter_agent.generate(
                research_report=state["research_report"],
                strategy=state["strategy"],
                brand_info=state["brand_info"],
                topic=state["topic"],
                brand_tone=state["brand_tone"],
                feedback=feedback
            )
            state["newsletter_content"] = newsletter_result["content"]
        
        print("✅ Failed content regenerated")
        return state

    def _should_retry(self, state: ContentCreationState) -> str:
        """Decide if content should be regenerated"""
        retry_count = state.get("retry_count", 0)
        
        if state["all_approved"]:
            print("\n✅ All content approved!")
            return "end"
        elif retry_count >= 2:  # Max 2 retries (0, 1, 2)
            print(f"\n⚠️  Max retries reached ({retry_count}). Proceeding with current content.")
            return "end"
        else:
            print(f"\n🔄 Quality check failed. Retrying... (Attempt {retry_count + 1})")
            return "retry"

    def run(self, brand_info: str, industry: str, target_audience: str, 
            topic: str, brand_tone: str) -> ContentCreationState:
        """
        Execute the complete workflow
        """
        print("\n" + "="*80)
        print("🚀 LANGGRAPH ORCHESTRATED WORKFLOW - STARTING")
        print("="*80)
        
        # Initialize state
        initial_state = ContentCreationState(
            brand_info=brand_info,
            industry=industry,
            target_audience=target_audience,
            topic=topic,
            brand_tone=brand_tone,
            research_report="",
            research_sources=0,
            strategy="",
            twitter_content="",
            linkedin_content="",
            instagram_content="",
            newsletter_content="",
            twitter_quality={},
            linkedin_quality={},
            instagram_quality={},
            newsletter_quality={},
            all_approved=False,
            retry_count=0,
            twitter_attempts=[], linkedin_attempts=[],
            instagram_attempts=[], newsletter_attempts=[],
        )
        
        # Run the workflow
        final_state = self.workflow.invoke(initial_state)
        
        print("\n" + "="*80)
        print("🎉 WORKFLOW COMPLETED")
        print("="*80)
        
        def choose_best(attempts):
            if not attempts:
                return ""
            # Each attempt is {"content": ..., "score": ...}
            best = max(attempts, key=lambda x: x["score"])
            return best["content"]

        final_state["twitter_content"] = choose_best(final_state["twitter_attempts"])
        final_state["linkedin_content"] = choose_best(final_state["linkedin_attempts"])
        final_state["instagram_content"] = choose_best(final_state["instagram_attempts"])
        final_state["newsletter_content"] = choose_best(final_state["newsletter_attempts"])

        return final_state
