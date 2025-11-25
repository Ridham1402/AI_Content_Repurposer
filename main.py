from src.content_analyzer import analyze_content
from src.platform_agents import TwitterAgent, LinkedInAgent, InstagramAgent

# Test with sample content
sample_content = """
The future of AI in content creation is transforming how we work. 
Content creators spend 80% of their time repurposing content across platforms. 
This is inefficient and drains creativity. AI agents can automate this process, 
analyzing your long-form content and intelligently adapting it for Twitter, 
LinkedIn, Instagram, and more. The key is maintaining your unique voice while 
optimizing for each platform's best practices. This isn't about replacing 
creators—it's about giving them superpowers to focus on what matters: 
creating great original content. The tools exist today. The question is: 
are you ready to 10x your content output?
"""

print("=" * 80)
print("🚀 AI CONTENT REPURPOSER - DEMO")
print("=" * 80)

# Step 1: Analyze content
print("\n🔍 Step 1: Analyzing content...\n")
analysis_result = analyze_content(sample_content)

if not analysis_result["success"]:
    print(f"❌ Analysis failed: {analysis_result['error']}")
    exit()

analysis = analysis_result["analysis"]
print("✅ Analysis complete!\n")

# Step 2: Generate platform-specific content
print("=" * 80)
print("📱 Step 2: Generating platform-specific content...")
print("=" * 80)

# Twitter Thread
print("\n🐦 TWITTER THREAD:\n")
print("-" * 80)
twitter_agent = TwitterAgent()
twitter_result = twitter_agent.generate(analysis, sample_content)
if twitter_result["success"]:
    print(twitter_result["content"])
else:
    print(f"❌ Error: {twitter_result['error']}")

# LinkedIn Post
print("\n\n💼 LINKEDIN POST:\n")
print("-" * 80)
linkedin_agent = LinkedInAgent()
linkedin_result = linkedin_agent.generate(analysis, sample_content)
if linkedin_result["success"]:
    print(linkedin_result["content"])
else:
    print(f"❌ Error: {linkedin_result['error']}")

# Instagram Caption
print("\n\n📸 INSTAGRAM CAPTION:\n")
print("-" * 80)
instagram_agent = InstagramAgent()
instagram_result = instagram_agent.generate(analysis, sample_content)
if instagram_result["success"]:
    print(instagram_result["content"])
else:
    print(f"❌ Error: {instagram_result['error']}")

print("\n" + "=" * 80)
print("✨ Content repurposing complete!")
print("=" * 80)
