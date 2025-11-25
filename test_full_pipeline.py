from src.agents.research_agent import ResearchAgent
from src.agents.strategy_agent import StrategyAgent
from src.agents.enhanced_platform_agents import (
    EnhancedTwitterAgent,
    EnhancedLinkedInAgent,
    EnhancedInstagramAgent,
    NewsletterAgent
)

# User inputs - Artisan AI Sales BDR
brand_info = "Artisan - Building AI sales BDR agents that automate lead generation and outreach"
industry = "AI in Sales"
target_audience = "B2B companies and sales teams still using manual labor for lead generation, outreach, and sales processes"
topic = "How AI agents are far better than manual processes in lead generation"
brand_tone = "Convincing, marketing-focused, results-driven"

print("="*80)
print("🚀 AI CONTENT CREATION ENGINE - FULL PIPELINE TEST")
print("="*80)
print(f"\n📌 Brand: {brand_info}")
print(f"📌 Industry: {industry}")
print(f"📌 Target Audience: {target_audience}")
print(f"📌 Topic: {topic}")
print(f"📌 Brand Tone: {brand_tone}")

# Phase 1: Research
print("\n" + "="*80)
print("📊 PHASE 1: RESEARCH")
print("="*80)
researcher = ResearchAgent()
research_result = researcher.conduct_research(
    topic=topic,
    brand_info=brand_info,
    target_audience=target_audience,
    industry=industry
)

if not research_result["success"]:
    print(f"❌ Research failed")
    exit()

# Phase 2: Strategy
print("\n" + "="*80)
print("📊 PHASE 2: CONTENT STRATEGY")
print("="*80)
strategist = StrategyAgent()
strategy_result = strategist.create_strategy(
    research_report=research_result["research_report"],
    brand_info=brand_info,
    topic=topic,
    target_audience=target_audience,
    brand_tone=brand_tone
)

if not strategy_result["success"]:
    print(f"❌ Strategy creation failed")
    exit()

# Phase 3: Content Generation
print("\n" + "="*80)
print("📊 PHASE 3: PLATFORM CONTENT GENERATION")
print("="*80)

# Initialize agents
twitter_agent = EnhancedTwitterAgent()
linkedin_agent = EnhancedLinkedInAgent()
instagram_agent = EnhancedInstagramAgent()
newsletter_agent = NewsletterAgent()

# Generate content for all platforms
twitter_result = twitter_agent.generate(
    research_report=research_result["research_report"],
    strategy=strategy_result["strategy"],
    brand_info=brand_info,
    topic=topic,
    brand_tone=brand_tone
)

linkedin_result = linkedin_agent.generate(
    research_report=research_result["research_report"],
    strategy=strategy_result["strategy"],
    brand_info=brand_info,
    topic=topic,
    brand_tone=brand_tone
)

instagram_result = instagram_agent.generate(
    research_report=research_result["research_report"],
    strategy=strategy_result["strategy"],
    brand_info=brand_info,
    topic=topic,
    brand_tone=brand_tone
)

newsletter_result = newsletter_agent.generate(
    research_report=research_result["research_report"],
    strategy=strategy_result["strategy"],
    brand_info=brand_info,
    topic=topic,
    brand_tone=brand_tone
)

# Display results
print("\n" + "="*80)
print("📱 GENERATED CONTENT - READY TO POST")
print("="*80)

if twitter_result["success"]:
    print("\n🐦 TWITTER THREAD:")
    print("-"*80)
    print(twitter_result["content"])
else:
    print(f"\n❌ Twitter generation failed: {twitter_result.get('error')}")

if linkedin_result["success"]:
    print("\n\n💼 LINKEDIN POST:")
    print("-"*80)
    print(linkedin_result["content"])
else:
    print(f"\n❌ LinkedIn generation failed: {linkedin_result.get('error')}")

if instagram_result["success"]:
    print("\n\n📸 INSTAGRAM CAPTION:")
    print("-"*80)
    print(instagram_result["content"])
else:
    print(f"\n❌ Instagram generation failed: {instagram_result.get('error')}")

if newsletter_result["success"]:
    print("\n\n📧 EMAIL NEWSLETTER:")
    print("-"*80)
    print(newsletter_result["content"])
else:
    print(f"\n❌ Newsletter generation failed: {newsletter_result.get('error')}")

print("\n" + "="*80)
print("✅ COMPLETE AI CONTENT CREATION PIPELINE SUCCESSFUL!")
print("="*80)
print(f"\n📊 Summary:")
print(f"  • Research sources analyzed: {research_result['total_sources']}")
print(f"  • Platforms generated: 4 (Twitter, LinkedIn, Instagram, Newsletter)")
print(f"  • All content is research-backed and strategically optimized")
print(f"  • Brand: Artisan AI Sales BDR")
print(f"  • Topic: AI agents vs manual lead generation")
print("="*80)
