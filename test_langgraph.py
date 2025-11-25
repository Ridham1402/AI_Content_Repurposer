from src.orchestrator import ContentCreationOrchestrator

# User inputs - GrowthOS AI Visibility Startup
brand_info = "GrowthOS - A cutting-edge startup specializing in AEO (Answer Engine Optimization), GEO (Generative Engine Optimization), and AI-powered visibility solutions"
industry = "AI Visibility & Digital Marketing"
target_audience = "Brands and startups penetrating new markets who need to maximize their visibility across AI-powered search platforms and answer engines"
topic = "Why AI-powered visibility strategies are crucial for brand discovery in 2025"
brand_tone = "Professional, innovative, product-focused with subtle advertising that positions GrowthOS as the solution"

# Create orchestrator and run
orchestrator = ContentCreationOrchestrator()
result = orchestrator.run(
    brand_info=brand_info,
    industry=industry,
    target_audience=target_audience,
    topic=topic,
    brand_tone=brand_tone
)

# Display final results
print("\n" + "="*80)
print("📱 FINAL APPROVED CONTENT - GROWTHOS")
print("="*80)

print("\n🐦 TWITTER THREAD:")
print("-"*80)
print(result["twitter_content"])
print(f"\nQuality Score: {result['twitter_quality']['overall_score']:.1f}/10")

print("\n\n💼 LINKEDIN POST:")
print("-"*80)
print(result["linkedin_content"])
print(f"\nQuality Score: {result['linkedin_quality']['overall_score']:.1f}/10")

print("\n\n📸 INSTAGRAM CAPTION:")
print("-"*80)
print(result["instagram_content"])
print(f"\nQuality Score: {result['instagram_quality']['overall_score']:.1f}/10")

print("\n\n📧 EMAIL NEWSLETTER:")
print("-"*80)
print(result["newsletter_content"])
print(f"\nQuality Score: {result['newsletter_quality']['overall_score']:.1f}/10")

print("\n" + "="*80)
print("✅ GROWTHOS CONTENT CREATION COMPLETE")
print("="*80)
print(f"\n📊 Campaign Summary:")
print(f"  • Brand: GrowthOS")
print(f"  • Focus: AI Visibility (AEO/GEO)")
print(f"  • Research sources: {result['research_sources']}")
print(f"  • All content optimized for market penetration messaging")
print("="*80)
