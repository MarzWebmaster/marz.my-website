// Cloudflare Pages Function: GET /api/posts
export async function onRequestGet(context) {
  const posts = [
    {
      "slug": "ai-agents-malaysia-business-2026",
      "title": "How AI Agents Are Transforming Malaysian Businesses in 2026",
      "category": "AI Solutions",
      "author": "Marz Technology",
      "published_at": "2026-06-01T00:00:00Z",
      "excerpt": "Discover how AI-powered chatbots, virtual assistants, and intelligent automation are revolutionising customer service, sales, and operations for Malaysian SMEs and enterprises.",
      "tags": ["AI", "automation", "Malaysia", "business"],
      "url": "blog/ai-agents-malaysia-business-2026.html"
    },
    {
      "slug": "cybersecurity-essentials-malaysia-2026",
      "title": "Cybersecurity Essentials for Malaysian Companies in 2026",
      "category": "Cybersecurity",
      "author": "Marz Technology",
      "published_at": "2026-05-10T00:00:00Z",
      "excerpt": "Key cybersecurity measures every Malaysian company must implement to protect against ransomware, data breaches, and evolving cyber threats.",
      "tags": ["cybersecurity", "ransomware", "data breach", "Malaysia"],
      "url": "blog/cybersecurity-essentials-malaysia-2026.html"
    },
    {
      "slug": "it-infrastructure-malaysia-sme-2026",
      "title": "Essential IT Infrastructure Guide for Malaysian SMEs (2026)",
      "category": "IT Infrastructure",
      "author": "Marz Technology",
      "published_at": "2026-05-20T00:00:00Z",
      "excerpt": "A comprehensive guide to building reliable, scalable, and secure IT infrastructure for Malaysian small and medium enterprises.",
      "tags": ["IT infrastructure", "SME", "networking", "cloud"],
      "url": "blog/it-infrastructure-malaysia-sme-2026.html"
    }
  ];

  // Filter by status if provided
  const url = new URL(context.request.url);
  const status = url.searchParams.get('status');
  const limit = parseInt(url.searchParams.get('limit') || '50');
  
  let filtered = posts;
  if (status === 'published') {
    filtered = posts.filter(p => p.status !== 'draft');
  }
  
  // Limit results
  filtered = filtered.slice(0, limit);

  return new Response(JSON.stringify(filtered), {
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'public, max-age=300'
    }
  });
}