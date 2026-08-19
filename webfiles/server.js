// Static AuraOS API Emulator for Netlify
const responses = {
  hello: "Hello. I don't know who you are yet — but I'm here. What would you like to work on?",
  working: "Yes, I'm actively processing your request. What specific task?",
  error: "I encountered an error. Please try rephrasing your request.",
  default: "I'm ready. What would you like to work on?"
};

const getResponse = (message) => {
  const msg = message.toLowerCase().trim();
  if (msg.includes('hello') || msg.includes('hi')) return responses.hello;
  if (msg.includes('work') || msg.includes('working')) return responses.working;
  if (msg.includes('error') || msg.includes('broken')) return responses.error;
  return responses.default;
};

// Serve JSON response for ALL /api/aura requests
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  
  if (url.pathname === '/api/aura') {
    const message = url.searchParams.get('message') || 'hello';
    const response = getResponse(message);
    
    return new Response(JSON.stringify({
      success: true,
      response: response,
      timestamp: new Date().toISOString()
    }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  return new Response('Not Found', { status: 404 });
}