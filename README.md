# ai-voice-cart-recovery-hackathon
AI voice bot for abandoned cart 



flowchart TD
    A[User abandons cart] --> B[Backend detects abandonment]
    B --> C[POST /trigger_cart_abandonment]
    C --> D[Flask app calls Twilio API]
    D --> E[Twilio initiates voice call]
    E --> F[Twilio requests /voice/entry]
    F --> G[AI voice agent greets, offers coupon]
    G --> H[User asks product question]
    H --> I[Flask /voice/handle_query]
    I --> J[RAG fetches product info]
    J --> K[OpenAI generates answer]
    K --> L[AI voice agent responds]
    L --> M{User: Proceed or More Questions?}
