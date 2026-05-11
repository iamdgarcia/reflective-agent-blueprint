# Reflective Agent Blueprint

A deployable template for a Reflective Agent based on the Agentic AI for Beginners course. This agent can critique and improve its own outputs through self-reflection.

## 🚀 Get Started

**Step 1 — Create your Netlify account:** [Register here](https://join.netlify.com/uk2itht31g7b) *(use this referral link to support the course)*

**Step 2 — Deploy:** Once registered, click below:

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/iamdgarcia/reflective-agent-blueprint&affiliate=8mntz9z1uxdi-96ld6)

## What is a Reflective Agent?

A Reflective Agent improves its outputs through self-critique:
1. **Generate Initial Output** - Produce an initial response
2. **Self-Critique** - Analyze the output for issues
3. **Identify Improvements** - Find areas for enhancement
4. **Iterate** - Produce improved versions
5. **Final Output** - Deliver the refined response

This pattern is covered in Module 3.2 of the Agentic AI for Beginners course.

## Features

- 🔄 **Self-Iteration** - Can improve its own outputs
- 👁️ **Self-Critique** - Evaluates its responses
- 📈 **Quality Scoring** - Scores outputs on various metrics
- ⚡ **Netlify Functions** - Serverless backend
- 📚 **Course-Aligned** - Module 3.2
- 🚀 **One-Click Deploy** - Ready for Netlify

## How It Works

1. Generate initial response
2. Reflect on the response (accuracy, completeness, tone)
3. Identify weaknesses
4. Create improved version
5. Repeat until satisfied

## API

```
https://YOUR-SITE-NAME.netlify.app/.netlify/functions/reflective-agent
```

**Request:**
```json
{"message": "Your task", "history": []}
```

## Course Connection

- **Module 3.2: Reflection and Self-Correction**

---

*Built with ❤️ for The Learning Curve community.*