from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.utils.search_tools import SearchTools
from src.agents.base_agent import get_llm  # Add this
from typing import List, Dict
import os
from dotenv import load_dotenv
import json

load_dotenv()


class ResearchAgent:
    """
    Comprehensive research agent that gathers information from multiple sources
    """
    
    def __init__(self):
        # Use local Ollama - no rate limits!
        self.llm = get_llm(temperature=0.2, use_local=True)
        
        self.search_tools = SearchTools()
        
        # Prompt for synthesizing research
        self.synthesis_prompt = PromptTemplate(
            input_variables=["topic", "brand_info", "target_audience", "search_results"],
            template="""
            You are an expert research analyst. Synthesize the following search results into a comprehensive research report.
            
            CONTEXT:
            Brand: {brand_info}
            Topic: {topic}
            Target Audience: {target_audience}
            
            SEARCH RESULTS:
            {search_results}
            
            Create a research report with:
            1. Key Insights: 5-7 main findings about this topic
            2. Recent Statistics: Important numbers and data points (with sources)
            3. Trending Angles: What's currently popular or discussed about this topic
            4. Audience Pain Points: What questions/problems does the target audience have?
            5. Content Opportunities: Unique angles or gaps in existing content
            6. Key Quotes/Facts: Compelling statements that can be used in content
            7. Competitor Insights: What are others saying about this topic?
            
            Be specific, cite sources when possible, and focus on actionable insights.
            """
        )
        
        self.chain = self.synthesis_prompt | self.llm | StrOutputParser()
    
    def generate_search_queries(self, topic: str, brand_info: str, target_audience: str) -> List[str]:
        """
        Generate multiple targeted search queries for comprehensive research
        """
        queries = [
            f"{topic} latest trends 2025",
            f"{topic} statistics and data",
            f"{topic} for {target_audience}",
            f"{brand_info} {topic}",
            f"{topic} best practices",
            f"{topic} common questions",
        ]
        return queries
    
    def conduct_research(self, 
                        topic: str, 
                        brand_info: str, 
                        target_audience: str,
                        industry: str = "") -> dict:
        """
        Main research method - orchestrates the entire research process
        """
        print(f"\n🔍 Starting comprehensive research on: {topic}")
        print(f"📊 Brand: {brand_info}")
        print(f"👥 Target Audience: {target_audience}\n")
        
        # Generate search queries
        search_queries = self.generate_search_queries(topic, brand_info, target_audience)
        
        # Conduct searches
        all_results = []
        for i, query in enumerate(search_queries, 1):
            print(f"Searching [{i}/{len(search_queries)}]: {query}")
            results = self.search_tools.smart_search(query, max_results=3)
            all_results.extend(results)
            print(f"  ✓ Found {len(results)} results")
        
        print(f"\n✅ Total results gathered: {len(all_results)}")
        
        # Format results for LLM
        formatted_results = self._format_search_results(all_results)
        
        # Synthesize research
        print("\n🧠 Synthesizing research insights...")
        research_report = self.chain.invoke({
            "topic": topic,
            "brand_info": brand_info,
            "target_audience": target_audience,
            "search_results": formatted_results
        })
        
        return {
            "success": True,
            "topic": topic,
            "brand_info": brand_info,
            "target_audience": target_audience,
            "research_report": research_report,
            "raw_results": all_results,
            "total_sources": len(all_results)
        }
    
    def _format_search_results(self, results: List[dict]) -> str:
        """
        Format search results for LLM consumption
        """
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(f"""
Source {i}:
Title: {result.get('title', 'N/A')}
URL: {result.get('url', 'N/A')}
Content: {result.get('content', 'N/A')[:500]}...
---
            """)
        
        return "\n".join(formatted)
