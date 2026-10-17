
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# Agent ko milne wali information
class AgentState(TypedDict):
    interests: str
    opportunities: list[dict]
    result: str


# Demo opportunities
SAMPLE_OPPORTUNITIES = [
    {
        "name": "Student Innovation Hackathon",
        "type": "Hackathon",
        "skills": "python innovation teamwork",
        "action": "Team idea finalize karo aur prototype banao."
    },
    {
        "name": "Python Developer Internship Prep",
        "type": "Internship",
        "skills": "python programming development",
        "action": "Python projects aur resume prepare karo."
    },
    {
        "name": "Student Scholarship Discovery",
        "type": "Scholarship",
        "skills": "academics scholarship students",
        "action": "Official scholarship source par eligibility aur deadline check karo."
    },
    {
        "name": "Open Source Contribution Sprint",
        "type": "Open Source",
        "skills": "python git github coding",
        "action": "GitHub par beginner-friendly issue choose karo."
    },
]


# Step 1: Opportunities retrieve karna
def retrieve_opportunities(state: AgentState):
    return {"opportunities": SAMPLE_OPPORTUNITIES}


# Step 2: Interests ke basis par match karna
def evaluate_matches(state: AgentState):
    interests = state["interests"].lower()
    words = set(interests.split())

    ranked = []

    for opportunity in state["opportunities"]:
        skills = set(opportunity["skills"].lower().split())
        score = len(words & skills)

        ranked.append({
            **opportunity,
            "match_score": score,
        })

    ranked.sort(key=lambda item: item["match_score"], reverse=True)

    return {"opportunities": ranked}


# Step 3: User ke liye action plan banana
def make_plan(state: AgentState):
    matches = state["opportunities"]

    lines = ["YOUR UP NEXT OPPORTUNITIES\n"]

    for item in matches:
        lines.append(
            f"{item['name']} ({item['type']})\n"
            f"Keyword match: {item['match_score']}\n"
            f"Next step: {item['action']}\n"
        )

    lines.append(
        "\nNote: These are illustrative demo opportunities. "
        "They are not verified live listings."
    )

    return {"result": "\n".join(lines)}


# LangGraph workflow
graph = StateGraph(AgentState)

graph.add_node("retrieve", retrieve_opportunities)
graph.add_node("evaluate", evaluate_matches)
graph.add_node("plan", make_plan)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "evaluate")
graph.add_edge("evaluate", "plan")
graph.add_edge("plan", END)

upnext_agent = graph.compile()


def find_opportunities(interests: str) -> str:
    output = upnext_agent.invoke({
        "interests": interests,
        "opportunities": [],
        "result": "",
    })

    return output["result"]


if __name__ == "__main__":
    print(find_opportunities("python coding hackathon"))