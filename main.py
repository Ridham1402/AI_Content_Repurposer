from src.orchestrator import ContentCreationOrchestrator

# User inputs - GrowthOS AI Visibility Startup
brand_info = "Centre for Development of Telematics (Working on developing mission critical communication)"
industry = "Mission critical communication technology"
target_audience = "Organisations interest in adopting mission critical communication solutions"
topic = "MCX - Mission Critical Communication for Next-Gen Connectivity"
brand_tone = "Professional, Innovative, Trustworthy"

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
print(f"📱 FINAL APPROVED CONTENT - {brand_info}")
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
print(f"  • Brand: {brand_info}")
print(f"  • Focus: {topic}")
print(f"  • Research sources: {result['research_sources']}")
print(f"  • All content optimized for market penetration messaging")
print("="*80)
