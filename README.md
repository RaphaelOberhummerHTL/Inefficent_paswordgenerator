# Inefficient Password Generator

A totally necessary, venture-capital-baiting, and buzzword-packed password generator slapped on top of a local Large Language Model (or "Chatbot", if we are being honest) to maximize corporate synergy and linguistic disruption. 

Instead of using traditional, lightweight, and actually secure random number generators that complete the task in microseconds without consuming the electrical grid of a small nation, this project leverages **local AI translation loops (the "Telephone Game")** to burn CPU cycles and extract password entropy from pure AI confusion. 

I built it because I hope that the nonexisting stockprise of my non-existing company jumps into the sky because I say, that I created a passwordgenerator that uses AI, unless I'm too late for that hype.

Are the generated passwords secure? I don't know, I'm not a security researcher, but I can say, that I have a passwordgenerator with AI and the investors will invest in my non-existing company, so I don't care.

---

## Now to the technical part of the story:

### 💡 How It Works (The Chaos Pipeline)

The generation pipeline relies entirely on turning a coherent piece of text into absolute structural nonsense, then feeding that nonsense into a custom mathematical engine to extract high-entropy character strings.

```
[User Seeds] ──> [LLM Generates Story] ──> [Multi-Round Random Translation Chaos]
│
[Secure Password] <── [Custom Entropy Math Engine] <───────┘
```

1. **The Core Story:** The system prompts a local AI model (`gemma4:12b`) to write an original, cohesive story based on a user-selected **Genre** and **5 unique keywords**.
2. **Linguistic Decay (The Telephone Game):** The script loops through a user-defined number of rounds (default: 40). In each round, it picks a completely random global language (from a pool of 60+ structurally unique languages like Zulu, Basque, Japanese, or Icelandic) and forces the AI to translate the previous text.
3. **The Loss of Information:** Because different language families use vastly different grammars, semantic drift sets in rapidly. Text gets dropped, replaced, or heavily distorted.
4. **Mathematical Distillation:** The chaotic, final text mutated string is iterated character-by-character. The system reads the ASCII numerical values (`ord`) of adjacent characters, compounds them with the user's initial genre/word selections, and passes them through volatile polynomial algorithms to continuously re-seed a pseudorandom character picker.

---

### 🛠️ Project Structure

The project is split into four modular python scripts:

| File | Purpose | Key Variables Documented |
| :--- | :--- | :--- |
| **`main.py`** | The orchestration script. Handles the CLI menu loop, gathers user configurations, tracks performance runtimes, and triggers execution. | `output_choice`, `translations_rounds`, `start`, `end` |
| **`story.py`** | Houses the configuration constants (supported languages list, genre dictionary) and the core narrative generation framework. | `MODEL`, `LANGUAGES`, `GENRE`, `prompt` |
| **`translationchaos.py`** | Manages communication with Ollama. Enforces strict JSON/output formatting and provides safeguarding features if the AI returns an empty string. | `text`, `output_language`, `new_text`, `given_language` |
| **`passwordgenerator.py`** | The entropy engine. Contains the validation loop for password size and the multi-layered polynomial math formulas used to distill characters. | `number`, `length_of_password`, `translated_story` |

---

### 🚀 Prerequisites & Installation

#### 1. Install Ollama
Since this project requires local inference, you must have **Ollama** installed on your system.
* Download it from [ollama.com](https://ollama.com)

#### 2. Download the Model
By default, the project uses `gemma4:12b` for its robust multilingual training corpus. Open your terminal and run:
```bash
ollama run gemma4:12b
```

**Hardware Note:** If your machine lacks a dedicated GPU or has less than 8GB of VRAM and less than 16GB of RAM, you can change the MODEL variable inside story.py to a smaller alternative (e.g., llama3:8b or phi3). Avoid models smaller than 7B parameter sizes, as they tend to "forget" the strict translation constraints and output conversational filler.

3. Install Python Dependencies

Install the official Ollama integration wrapper:
```bash
pip install ollama
```

### 🎮 Usage

Run the master script directly from your terminal:
```bash
python main.py
```

#### Execution Steps:

- **Choose Password Length:** Specify the target length (minimum 10, default 20).
- Select Mode:
  * **[1] Story:** Prints out the step-by-step intermediate translation logs so you can visibly watch the story break down across random global languages before seeing a final translation.
  * **[2] Password:** Quietly calculates the algorithms behind the scenes and returns only your final secure string.

- **Input Words & Genre:** Give the AI 5 words and a narrative style to begin the baseline tracking matrix.
- **Set Translation Rounds:** Input how many times the story should jump languages (e.g., 40).

### 📊 Performance Disclaimer

This password generator is intentionally inefficient.

While a standard password generator completes its task in roughly 0.00005 seconds, this generator spins up billions of mathematical matrix multiplications across your computer hardware over dozens of full neural-network inference cycles. Depending on your GPU/CPU capabilities and your translation loop settings, generating a single password may take anywhere from a few seconds to several hours.

It is the ultimate expression of using a sledgehammer to crack a nut—but it ensures a completely unique, unpredictable entropy footprint.

### ⚖️ License

This project is open-source. Use it for educational entertainment, conceptual cryptographic exploration, or heating your room via processor workloads.