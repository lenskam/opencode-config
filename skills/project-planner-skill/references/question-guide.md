# Question Guide — Feature & User Journey Elicitation

This reference provides detailed question templates for each project type. Use these to adapt the standard 7-question sequence from SKILL.md to the specific domain.

## Question Adaptation by Project Type

### SaaS Application

| Question | Adaptation |
|----------|------------|
| Primary goal | "What recurring problem does this SaaS solve? Who's the ideal customer?" |
| Personas | "Will you have free users vs. paid subscribers? Admin roles?" |
| MVP features | "What's the minimum set of features that delivers value and justifies a subscription?" |
| User journeys | "Walk through a user's first 5 minutes with the app. What do they see? What do they click?" |
| Performance | "How many concurrent SaaS users at launch? Multi-tenant? Any SLAs?" |

### Mobile App

| Question | Adaptation |
|----------|------------|
| Primary goal | "What's the core action a user performs on their phone? Offline? Push notifications?" |
| Personas | "One type of user or different roles? Guest browsing vs. registered?" |
| MVP features | "What's the must-have feature that makes someone download this app?" |
| User journeys | "Describe the first-launch experience: onboarding, permissions, main screen." |
| Performance | "Offline support? Background sync? Storage limits on device?" |

### Landing Page

| Question | Adaptation |
|----------|------------|
| Primary goal | "What's the single conversion goal? Signup? Purchase? Waitlist?" |
| Personas | "Visitor vs. customer. Any referral or affiliate program?" |
| MVP features | "Hero section, value proposition, CTA, testimonials, contact form. Anything more?" |
| User journeys | "Walk through a visitor landing on the page for the first time. Where do they click? What happens next?" |
| Performance | "Page load speed target? SEO requirements? Analytics?" |

### API Service

| Question | Adaptation |
|----------|------------|
| Primary goal | "What data or action does this API expose? Who are the API consumers?" |
| Personas | "Developer (consumer) vs. API admin (key management, rate limits)." |
| MVP features | "What endpoints are essential? Authentication method? Rate limiting?" |
| User journeys | "Walk through a developer getting their first API key, making their first call, handling errors." |
| Performance | "Rate limits per tier? Latency targets? Uptime SLA?" |

### E-commerce

| Question | Adaptation |
|----------|------------|
| Primary goal | "What's being sold? Physical goods, digital, subscriptions?" |
| Personas | "Shopper, customer (post-purchase), admin (inventory, orders), vendor (if marketplace)." |
| MVP features | "Product listing, cart, checkout, payment, order history. Any more?" |
| User journeys | "Walk through a shopper finding a product, adding to cart, checking out, receiving confirmation." |
| Performance | "Checkout reliability? Payment gateway? Inventory accuracy?" |

### Full-Stack Web App

| Question | Adaptation |
|----------|------------|
| Primary goal | "What's the core interaction? Is this a tool, a game, a social platform?" |
| Personas | "Standard user roles plus any moderation or admin roles." |
| MVP features | "CRUD on the main entity plus authentication. What's the primary data model?" |
| User journeys | "Walk through a user creating/editing/deleting the main entity." |
| Performance | "Real-time features? WebSockets? File uploads? Search?" |

---

## Follow-up Question Patterns

When answers are vague, use these follow-ups:

### For vague features
- "Can you give me a specific example of a user doing that?"
- "What's the simplest version of this feature where someone still finds it useful?"
- "What happens if this feature isn't in the MVP?"

### For missing edge cases
- "What happens when a user enters invalid data?"
- "What should happen if the network fails during this operation?"
- "What about concurrent users editing the same resource?"

### For unclear priorities
- "If you had to launch with only 3 features, which ones?"
- "Which feature is most important for getting your first 10 users?"
- "Which feature is most technically risky or uncertain?"

### For technical gaps
- "Do you already have a database chosen? Hosting provider?"
- "Any existing code, APIs, or services you need to integrate with?"
- "Any third-party services you plan to use? (Stripe, Auth0, SendGrid, etc.)"

---

## Phase Style Clarification

If the user is unsure about the phase style, use these explanations:

### Use Incremental if:
- You want to show progress to stakeholders every week
- You're building a product-market fit MVP
- You're unsure about requirements and need flexibility
- Your team is small and cross-functional

### Use Chronological if:
- The database schema is complex and must be right
- You're building an API that multiple services will consume
- Security and compliance requirements are strict
- You have a clear architectural vision

### Use Mixed if:
- You have complex infrastructure + many features
- You're building a platform (foundation) + apps (features)
- You have both architectural and product concerns
