from typesafe_sdk import TypeSafeClient, Choice
from domain import IntentResult, Turn, INTENTS


class IntentClassifier:
    def __init__(self, client: TypeSafeClient):
        self.client = client

    def classify(self, message: str, history: list[Turn] | None = None) -> IntentResult:
        response = self.client.system_one(
            state={
                "message": message,
                "history": [turn.model_dump() for turn in history or []]        
            },
            questions={
                "intent": Choice(
                    instructions=(
                        "Identify the customer's primary intent in the latest message. "
                        "Use the prior conversation history only to disambiguate it."
                    ),
                    criteria=INTENTS
                )
            }
        )

        result = response.choices["intent"]
        requires_clarification = result.confidence < 0.8

        return IntentResult(
            intent=result.choice,
            confidence=result.confidence,
            probabilities=result.probabilities,
            requires_clarification=requires_clarification
        )
