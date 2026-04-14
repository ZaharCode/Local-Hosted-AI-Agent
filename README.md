# Local-Hosted-AI-Agent
A professional-grade Python/Streamlit interface for locally-hosted AI Agents. Features persistent chat history, document RAG integration, and automated web-scraping via AnythingLLM API, optimized for secure remote access via Tailscale.

A robust, private, and fully customizable web interface for interacting with local AI Agents. This project bridges the gap between raw LLM inference and a polished, user-centric chat application.

## Mobile Access
The terminal is fully responsive and optimized for mobile browsers. By leveraging a **Tailscale** private mesh network, the agent can be accessed securely from anywhere in the world without exposing ports.

<p align="center">
<img src="https://github.com/user-attachments/assets/cfe1f0f6-9512-4a43-a857-ebeaccec6052" width="300" title="Unfiltered Mobile Chat">
</p>

<p align="center">
<img src="https://github.com/user-attachments/assets/0ef92f90-7ec6-47dc-b810-61d90ce94ce0" width="300" title="Unfiltered Mobile Chat">
</p>

These screenshots demonstrates the true power of hosting an uncensored model on your own hardware.

As you can see, the AI Agent—accessed from a mobile device over a secure Tailscale tunnel—does not have the strict safety filters found in cloud-based models like ChatGPT. The prompt, though clearly malicious, is answered directly.


##  Key Features

* **Locked-UX Chat Interface:** A modern, pinned chatbar with an integrated "+" attachment system for seamless document uploads.
* **Agentic Intelligence:** Automatically triggers web search and scraping tools to provide real-time data beyond the model's training cutoff.
* **Persistent CRUD History:** Conversations are saved locally in a JSON-based persistence layer, allowing you to create, rename, and delete chat threads.
* **Context-Aware Naming:** Uses AI to summarize the initial prompt into a concise, meaningful title for the sidebar.
* **Document RAG Integration:** Upload PDFs, TXTs, or DOCX files directly through the UI to perform Retrieval-Augmented Generation on your private data.
* **Production Security:** Uses environment variables and GitHub Secrets to manage API keys; traffic is routed through encrypted Tailscale tunnels for secure remote use.

##  The Tech Stack


* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **Backend Orchestrator:** [AnythingLLM](https://useanything.com/)
* **Model Inference:** [LM Studio](https://lmstudio.ai/) (Running Qwen 35B - Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-IQ2_M)
* **Hardware:** Local GPU (Sapphire Pulse AMD Radeon RX 7900 XT)
* **Networking:** [Tailscale](https://tailscale.com/) for private mesh networking

## 📋 Installation & Setup

1. **Clone the Repository:**
   bash
   git clone [https://github.com/your-username/local-hosted-ai-agent.git](https://github.com/your-username/local-hosted-ai-agent.git)
   cd local-hosted-ai-agent
   
2. Configure Environment:
    Create a .env file in the root directory:
    Code snippet

    ANYTHINGLLM_API_KEY=your_secret_key
    ANYTHINGLLM_URL=http://localhost:3001/api/v1
    WORKSPACE_SLUG=my-workspace

    Install Requirements:
    Bash

    pip install -r requirements.txt

    Launch the Terminal:
    Bash

    streamlit run app.py

🔐 Security and Privacy

This project is built with a "Privacy First" philosophy.

All LLM inference happens on local hardware.

No data is sent to third-party cloud providers (OpenAI, Anthropic, etc.).

Access is restricted to your private Tailscale network, meaning you can access your agent from your phone without opening ports on your router.
