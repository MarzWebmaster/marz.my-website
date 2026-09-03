// Cloudflare Pages Function: POST /api/posts/add
// This function adds new posts to the KV store
export async function onRequestPost(context) {
  try {
    const body = await context.request.json();
    
    // Validate required fields
    if (!body.slug || !body.title) {
      return new Response(JSON.stringify({ error: 'slug and title are required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // Store in KV (you'll need to create a KV namespace called BLOG_POSTS)
    const key = `post:${body.slug}`;
    await context.env.BLOG_POSTS.put(key, JSON.stringify(body));

    return new Response(JSON.stringify({ success: true, slug: body.slug }), {
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}